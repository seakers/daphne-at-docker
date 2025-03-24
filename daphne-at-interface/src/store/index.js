import Vue from 'vue';
import Vuex from 'vuex';
import daphne from './modules/daphne';
import daphneat from './modules/daphne-at';
import experiment from './modules/experiment';
import auth from'./modules/auth';
import modal from './modules/modal';
import {processedPlotData} from "../scripts/at-display-builders";
import {wsTools} from "../scripts/websocket-tools";
import Shepherd from "shepherd.js";

Vue.use(Vuex);

const debug = process.env.NODE_ENV !== 'production';

export default new Vuex.Store({
    state: {
    },
    computed: {
    },
    getters: {
    },
    mutations: {
    },
    actions: {
        async onWebsocketsMessage({ commit, state, getters, dispatch }, message) {
            let received_info = JSON.parse(message.data);

            // Get result of trying to start the hub thread
            if (received_info['type'] === 'hub_thread_response') {
                let responseDict = received_info['content'];
                console.log(responseDict['message'] + " Occurred on attempt " + responseDict['attempt']);
                // Try 5 times if it doesn't work then stop trying
                let attempt = parseInt(responseDict['attempt']);
                if (responseDict['status'] === 'error' && attempt < 5) {
                    attempt += 1;
                    attempt = attempt.toString();
                    wsTools.websocket.send(JSON.stringify({
                        type: 'start_hub_thread',
                        attempt: attempt
                    }));
                }
            }
            // Get result of trying to stop telemetry
            else if (received_info['type'] === 'stop_telemetry_response') {
                let responseDict = received_info['content'];
                console.log(responseDict['message'] + " Occurred on attempt " + responseDict['attempt']);
                // Try 5 times if it doesn't work then stop trying
                let attempt = parseInt(responseDict['attempt']);
                if (responseDict['status'] === 'error' && attempt < 5) {
                    attempt += 1;
                    attempt = attempt.toString();
                    wsTools.websocket.send(JSON.stringify({
                        type: 'stop_telemetry',
                        attempt: attempt
                    }));
                }
                if (responseDict['status'] === 'success') {
                    commit('mutateTelemetryIsOngoing', false);
                    commit('mutateTelemetryType', null);
                    commit('mutateTelemetryPlotData', []);
                    commit('mutateTelemetryInputVariables', []);
                    commit('mutateTelemetryPlotSelectedVariables', []);
                    commit('mutateTelemetryValues', '');
                    commit('mutateTelemetryInfo', '');
                    commit('mutateSymptomsList', []);
                    commit('mutateSelectedSymptomsList', []);
                    const now = new Date();
                    let formattedDate = now.toLocaleString('en-US', {
                        year: 'numeric',
                        month: 'long',  // e.g., October
                        day: 'numeric', // e.g., 15
                        hour: 'numeric',
                        minute: 'numeric',
                        second: 'numeric',
                        hour12: true    // Use 12-hour format with AM/PM
                      });
                    
                    commit('mutateLastUpdatedSymptomsTimestamp', formattedDate);
                    commit('mutateDiagnosisReport', []);
                    commit('mutateSelectedAnomaliesList', []);
                    commit('mutateSelectedAnomaliesInfo', {});
                    commit('mutateSelectedProceduresList', []);
                    commit('mutateSelectedProceduresInfo', {});
                    commit('mutateLastUpdatedAnomaliesTimestamp', formattedDate);
                    commit('mutateLastUpdatedProceduresTimestamp', formattedDate);
                    commit('mutateLastUpdatedProceduresInfoTimestamp', formattedDate);
                    commit('mutateLastUpdatedDiagnosisTimestamp', formattedDate);
                    commit('setIsTelemetryInitialized', false);
                }
            }
            // Get result of trying to start fake telemetry
            else if (received_info['type'] === 'fake_telemetry_response') {
                let responseDict = received_info['content'];
                console.log(responseDict['message'] + " Occurred on attempt " + responseDict['attempt']);
                // Try 5 times if it doesn't work then stop trying
                let attempt = parseInt(responseDict['attempt']);
                if (responseDict['status'] === 'error' && attempt < 5) {
                    attempt += 1;
                    attempt = attempt.toString();
                    wsTools.websocket.send(JSON.stringify({
                        type: 'start_fake_telemetry',
                        attempt: attempt
                    }));
                }
                if (responseDict['status'] === 'success' || responseDict['status'] === 'already_assigned') {
                    commit('mutateTelemetryIsOngoing', true);
                    commit('mutateTelemetryType', 'fake');
                }
            }
            // Get result of trying to start real telemetry
            else if (received_info['type'] === 'real_telemetry_response') {
                let responseDict = received_info['content'];
                console.log(responseDict['message'] + " Occurred on attempt " + responseDict['attempt']);
                // Try 5 times if it doesn't work then stop trying
                let attempt = parseInt(responseDict['attempt']);
                if (responseDict['status'] === 'error' && attempt < 5) {
                    attempt += 1;
                    attempt = attempt.toString();
                    wsTools.websocket.send(JSON.stringify({
                        type: 'start_real_telemetry',
                        attempt: attempt
                    }));
                }
                if (responseDict['status'] === 'success') {
                    commit('mutateTelemetryIsOngoing', true);
                    commit('mutateTelemetryType', 'real');
                }
            }
            // Get result of trying to start real telemetry
            else if (received_info['type'] === 'hera_telemetry_response') {
                let responseDict = received_info['content'];
                console.log(responseDict['message'] + " Occurred on attempt " + responseDict['attempt']);
                // Try 5 times if it doesn't work then stop trying
                let attempt = parseInt(responseDict['attempt']);
                if (responseDict['status'] === 'error' && attempt < 5) {
                    attempt += 1;
                    attempt = attempt.toString();
                    wsTools.websocket.send(JSON.stringify({
                        type: 'start_real_telemetry',
                        attempt: attempt
                    }));
                }
                if (responseDict['status'] === 'success') {
                    commit('mutateTelemetryIsOngoing', true);
                    commit('mutateTelemetryType', 'real');
                }
            }
            // Active message?
            else if (received_info['type'] === 'active.message') {
                commit('addDialoguePiece', received_info['message']);
            }
            // Ping from the backend confirmation
            else if (received_info['type'] === 'ping') {
                console.log("Ping back!");
            }
            // Console text?
            else if (received_info['type'] === 'console_text') {
                console.log(received_info['text']);
            }
            // Get initialized telemetry and set initialized telemetry flag to true
            else if (received_info['type'] === 'initialize_telemetry') {
                console.log("Telemetry initialized.");
                let telemetryDict = received_info['content'];
                if (telemetryDict !== '') {
                    let telemetryVariablesNames = telemetryDict['variables_names'];
                    commit('mutateTelemetryInputVariables', telemetryVariablesNames);
                    commit('mutateTelemetryPlotSelectedVariables', [telemetryVariablesNames[0]]);
                    commit('setIsTelemetryInitialized', true);
                }
            }
            // Receive telemetry update if telemetry has been initialized
            else if (received_info['type'] === 'telemetry_update') {
                // Only update telemetry plot if it is initialized
                if (state.daphneat.isTelemetryInitialized) {
                    console.log('Telemetry Update Received - All good');
                    let telemetryDict = received_info['content'];
                    let selectedVariables = state.daphneat.telemetryPlotSelectedVariables;
                    let plotData = processedPlotData(telemetryDict, selectedVariables);
                    dispatch('updateTelemetryPlotData', plotData);
                    dispatch('updateTelemetryValuesAndInfo', telemetryDict);
                }
                else {
                    console.log('Telemetry Update Received - Not yet initialized');
                    wsTools.websocket.send(JSON.stringify({
                        'type': 'get_parameters'
                    }))
                }
            }
            // Receive symptoms report and check to trigger alarms
            else if (received_info['type'] === 'symptoms_report') {
                let content = received_info['content'];
                let symptoms_report = content['symptoms_report'];
                let alarm = content['alarm'];
                if (state.daphneat.playAlarms) {
                    dispatch('triggerAlarm', alarm);
                }
                dispatch('updateSymptomsList', symptoms_report);
            }
            // Finish the experiment
            else if (received_info['type'] === 'finish_experiment_from_mcc') {
                dispatch('finishStage').then(() => {
                    dispatch('finishExperiment').then(() => {
                        console.log('Trying to stop telemetry...');
                        wsTools.websocket.send(JSON.stringify({
                            'type': 'stop_telemetry',
                            'attempt': '1'
                        }));
                    });
                });
            }
            else if (received_info['type'] === 'turn_off_alarms') {
                commit('mutatePlayAlarms');
            }
            // Situational Awareness Questions
            else if (received_info['type'] === 'situational_awareness') {
                commit('activateModal', 'SituationalAwarenessModal');
            }
            // Without Daphne Sessions
            else if (received_info['type'] === 'without_daphne_session') {
                commit('activateModal', 'WithoutDaphneSessionModal');
            }
            // Confidence Questions
            else if (received_info['type'] === 'confidence') {
                commit('activateModal', 'ConfidenceModal');
            }
            else if (received_info['type'] === 'send_msg_correct') {
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
                    text: `<b>Congratulations!</b> The procedure you selected has resolved the anomaly. Click on the button below to fill out the survey for this scenario.`,
                    buttons: [
                        {
                            text: 'Survey Link',
                            action: surveyLink.next
                        }
                    ]
                });
                // show the closing pop up
                surveyLink.show();
                surveyLink.on("complete", () => {
                    setTimeout(() => { window.open("https://tamu.qualtrics.com/jfe/form/SV_29RmM0hE4YV4Omq"); }, 1000);
                });
            }
            else if (received_info['type'] === 'send_msg_incorrect') {
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
                    text: `<b>Unfortunately</b>, the procedure you selected was wrong and did not resolve the anomaly. Please fill out the survey for this scenario.`,
                    buttons: [
                        {
                            text: 'Survey Link',
                            action: surveyLink.next
                        }
                    ]
                });
                // show the closing pop up
                surveyLink.show();
                surveyLink.on("complete", () => {
                    setTimeout(() => { window.open("https://tamu.qualtrics.com/jfe/form/SV_29RmM0hE4YV4Omq"); }, 1000);
                });
            }
        },
    },
    modules: {
        daphne,
        experiment,
        daphneat,
        auth,
        modal
    },
    strict: debug
});
