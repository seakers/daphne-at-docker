// initial state
import * as _ from "lodash-es";
import {fetchGet, fetchPost} from "../../scripts/fetch-helpers";
import {wsTools} from "../../scripts/websocket-tools";
import Shepherd from "shepherd.js";

const state = {
    inExperiment: false,
    isRecovering: false,
    experimentStage: '',
    currentStageNum: -1,
    stageInformation: {
        tutorial: {
            nextStage: '',
            steps: {}
        },
        with_daphne: {
            restrictedQuestions: null,
            nextStage: '',
            startTime: 0,
            stageDuration: 30*60
        },
        without_daphne: {
            restrictedQuestions: {
            },
            nextStage: '',
            startTime: 0,
            stageDuration: 30*60
        }
    }
};

// getters
const getters = {
};

// actions
const actions = {
    async startExperiment({ state, commit }) {
        // Call server to start experiment
        try {
            let response = await fetchGet(API_URL + 'experiment-at/start-experiment');
            if (response.ok) {
                let experimentStages = await response.json();
                // Start the experiment: set the order of the conditions after the tutorial
                commit('setNextStage', { experimentStage: 'tutorial', nextStage: experimentStages[0]});

                for (let i = 0; i < experimentStages.length - 1; ++i) {
                    commit('setNextStage', { experimentStage: experimentStages[i], nextStage: experimentStages[i+1] });
                }
            }
            else {
                console.error('Error starting the experiment.');
            }
        }
        catch(e) {
            console.error('Networking error:', e);
        }
    },

    async startStage({ state, commit }, stage) {
        // Call server to start stage
        try {
            let nextStage = state.currentStageNum;
            let response = await fetchGet(API_URL + 'experiment-at/start-stage/' + nextStage);
            if (response.ok) {
                let startDateData = await response.json();
                // Start the stage: get the starting time from the server information
                console.log(startDateData);
                let startTime = startDateData.start_date + '+00:00';
                startTime = Date.parse(startTime);
                commit('setStartTime', { experimentStage: stage, startTime: startTime });
            }
            else {
                console.error('Error starting the stage.');
            }
        }
        catch(e) {
            console.error('Networking error:', e);
        }
    },

    async finishStage({ state, commit }) {
        // Call server to finish stage
        try {
            let currentStage = state.currentStageNum - 1;
            let response = await fetchGet(API_URL + 'experiment-at/finish-stage/' + currentStage);
            if (response.ok) {
                let experimentInformation = await response.json();
                // Stage is finished!
                console.log(experimentInformation);
            }
            else {
                console.error('Error finishing the stage.');
            }
        }
        catch(e) {
            console.error('Networking error:', e);
        }
    },

    async finishExperiment({ state, commit }) {
        // Call server to finish experiment
        try {
            let response = await fetchGet(API_URL + 'experiment-at/finish-experiment');
            if (response.ok) {
                let experimentInformation = await response.json();
                // Finish the experiment: set inExperiment to false
                console.log(experimentInformation);
                commit('setInExperiment', false);
            }
            else {
                console.error('Error finishing the experiment.');
            }
            // set up pop up to link
            const surveyLink = new Shepherd.Tour({
                defaultStepOptions: {
                    classes: 'shadow-md bg-purple-dark',
                    scrollTo: true
                },
                useModalOverlay: true,
                exitOnEsc: false
            });
            // add steps
            surveyLink.addStep({
                text: `The time for the experiment has expired. Please click the "Survey Link" button to
                    fill out the survey. Thank you.`,
                buttons: [
                    {
                        text: 'Survey Link',
                        action: surveyLink.next
                    }
                ]
            });
            // show the closing pop up
            surveyLink.show();
            // once the button is clicked, the tour is over and redirect to survey
            surveyLink.on("complete", () => {
                setTimeout(() => { window.location.replace("https://tamu.qualtrics.com/jfe/form/SV_2440oXZpxBU2lxA"); }, 2000);
            });
        }
        catch(e) {
            console.error('Networking error:', e);
        }
    },

    async recoverExperiment({ state, commit, rootState, dispatch }) {
        // Call server to see if there is an experiment already running
        try {
            //TODO add and remove restores from modules
            let response = await fetchGet(API_URL + 'experiment-at/reload-experiment');
            if (response.ok) {
                let experimentInformation = await response.json();
                if (experimentInformation['is_running']) {
                    // If experiment was already running restore the last known state
                    try {
                        commit('setIsRecovering', true);
                        commit('restoreAuth', experimentInformation.experiment_data.auth);
                        // Functions inside the problem don't survive the recovery, so they need to be reloaded from scratch
                        commit('restoreDaphne', experimentInformation.experiment_data.daphne);
                        commit('restoreExperiment', experimentInformation.experiment_data.experiment);
                        commit('restoreDaphneAT', experimentInformation.experiment_data.daphneat);
                    }
                    catch(err) {
                        console.log(err);
                    }
                    // Start the websockets after completing the request so the session cookie is already set
                    await wsTools.experimentWsConnect();
                    await wsTools.wsConnect(this);

                    // Start the threads just in case
                    console.log("Trying to start hub thread...")
                    wsTools.websocket.send(JSON.stringify({
                        type: 'start_hub_thread',
                        attempt: '1'
                    }));

                    // Check which telemetry to load from and initialize everything again
                    if (rootState.daphneat.telemetryType === 'fake') {
                        // Start fake telemetry
                        console.log('Trying to start fake telemetry...');
                        wsTools.websocket.send(JSON.stringify({
                            'type': 'start_fake_telemetry',
                            'attempt': '1'
                        }));
                        /* Should get parameters from starting
                        wsTools.websocket.send(JSON.stringify({
                            msg_type: 'get_fake_telemetry_params'
                        }));*/
                    }
                    else if (rootState.daphneat.telemetryType === 'real') {
                        console.log('Trying to start real telemetry...');
                        wsTools.websocket.send(JSON.stringify({
                            'type': 'start_real_telemetry',
                            'attempt': '1'
                        }));
                        /* Should get parameters from starting
                        wsTools.websocket.send(JSON.stringify({
                            msg_type: 'get_real_telemetry_params'
                        }));*/
                        dispatch('loadAllAnomalies');
                    }
                }
            }
            else {
                console.error('Error recovering the experiment.');
            }
        }
        catch(e) {
            console.error('Networking error:', e);
        }
    }
};

// mutations
const mutations = {
    setInExperiment(state, inExperiment) {
        state.inExperiment = inExperiment;
    },
    setExperimentStage(state, experimentStage) {
        state.experimentStage = experimentStage;
        state.currentStageNum++;
    },
    setNextStage(state, { experimentStage, nextStage }) {
        state.stageInformation[experimentStage].nextStage = nextStage;
    },
    setStartTime(state, { experimentStage, startTime }) {
        state.stageInformation[experimentStage].startTime = startTime;
    },
    restoreExperiment(state, recoveredState) {
        Object.keys(recoveredState).forEach((key) => {
            if (key !== 'isRecovering') {
                state[key] = recoveredState[key];
            }
        });
    },
    setIsRecovering(state, isRecovering) {
        state.isRecovering = isRecovering;
    },
};

export default {
    state,
    getters,
    actions,
    mutations
}
