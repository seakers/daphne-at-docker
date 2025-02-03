'use strict';

import Vue from 'vue';

import App from './components/App';
import store from './store';
import {wsTools} from "./scripts/websocket-tools";

// Non ES-modularized libraries
let annyang = require('annyang');
let SpeechKITT = window.SpeechKITT;

// Styles
import 'shepherd.js/dist/css/shepherd.css';
import './styles/app.scss';

// Record state and mutations when inside an experiment
let stateTimer = 0;
let mutationBlackList = [
    'setIsLoading', 'resetDaphne', 'clearFeatures',
    'resetFilter', 'setProblem', 'updateExtra', 'updatePlotData', 'restoreFilter',
    'restoreDaphne', 'restoreExperiment', 'setIsRecovering',
    'mutateTelemetryIsOngoing', 'mutateTelemetryPlotData', 'mutateTelemetryValues', 'mutateTelemetryInfo',
    'mutateTelemetryInputVariables', 'mutateSymptomsList', 'mutateLastSelectedSymptomsList', 'mutateAllAnomaliesList',
    'mutateSelectedAnomaliesInfo', 'mutateSelectedProceduresInfo', 'restoreDaphneAT', 'mutateLoadingNewAnomaly'
];
let daphneATStateBlackList = [
    'telemetryPlotData', 'telemetryValues', 'telemetryInfo', 'telemetryInputVariables', 'symptomsList',
    'loadingNewAnomaly'
];
let updatesContextList = [
    'mutateTelemetryValues',
    'mutateSelectedAnomaliesList',
    'mutateSelectedProceduresList',
    'mutateTelemetryPlotSelectedVariables',
];

store.subscribe(async (mutation, state) => {
    // Only update if inside experiment
    if (state.experiment.inExperiment) {
        // Only update mutations if after tutorial (currentStageNum > 0)
        if (state.experiment.currentStageNum > 0 && !mutationBlackList.includes(mutation.type)) {
            // Upload mutation to server
            if (wsTools.experimentWebsocket !== undefined) {
                wsTools.experimentWebsocket.send(JSON.stringify({
                    msg_type: 'add_action',
                    stage: state.experiment.currentStageNum - 1,
                    action: mutation
                }));
            }
        }

        // Upload new state to server
        if (stateTimer === 0) {
            stateTimer = window.setInterval(() => {
                console.log('State update');
                if (wsTools.experimentWebsocket !== undefined) {
                    let partialState = JSON.parse(JSON.stringify(state));
                    for (let key in partialState['daphneat']) {
                        if (daphneATStateBlackList.includes(key)) {
                            delete partialState['daphneat'][key];
                        }
                    }
                    delete partialState['experiment']['stageInformation']['tutorial']['steps'];

                    wsTools.experimentWebsocket.send(JSON.stringify({
                        msg_type: 'update_state',
                        state: partialState
                    }));
                }
            }, 3000);
        }
    } else {
        if (stateTimer !== 0) {
            clearInterval(stateTimer);
            stateTimer = 0;
        }
    }

    // Context updates TODO: Refactor into something more modular
    if (updatesContextList.includes(mutation.type)) {
        // Lazily create the Websocket to ensure the session is already created by this point
        if (mutation.type === 'mutateTelemetryValues') {
            wsTools.websocket.send(JSON.stringify({
                msg_type: 'context_add',
                new_context: {
                    atcontext: {
                        current_telemetry_values: mutation.payload,
                    }
                }
            }));
        }
        else if (mutation.type === 'mutateSelectedAnomaliesList') {
            wsTools.websocket.send(JSON.stringify({
                msg_type: 'context_add',
                new_context: {
                    atcontext: {
                        selected_anomalies: mutation.payload,
                    }
                }
            }));
        }
        else if (mutation.type === 'mutateTelemetryPlotSelectedVariables') {
            wsTools.websocket.send(JSON.stringify({
                msg_type: 'context_add',
                new_context: {
                    atcontext: {
                        selected_measurements: mutation.payload,
                    }
                }
            }));
        }
        else if (mutation.type === 'mutateSelectedProceduresList') {
            wsTools.websocket.send(JSON.stringify({
                msg_type: 'context_add',
                new_context: {
                    atcontext: {
                        selected_procedures: mutation.payload,
                    }
                }
            }));
        }
    }
});

let app = new Vue({
    el: '#app',
    store,
    propsData: {
        isViewer: false
    },
    render: h => h(App)
});

// Voice recognition
if (annyang) {
    const onFulfilled = () => {
        annyang.addCallback(app.$store.commit('setIsSpeaking', false));
        annyang.removeCallback();
    };
    var wakeWord = {
        'Hey Daphne': function() {
            annyang.addCallback(app.$store.commit('setIsSpeaking', true));
            annyang.addCallback('result', phrases => {
                app.$store.commit('setCommand', phrases[0]);
                app.$store.dispatch('executeCommand').then(onFulfilled());
            });
            setTimeout(annyang.addCommands(wakeWord), 500);

        }
    }



    annyang.addCommands(wakeWord);
    annyang.debug();
    annyang.start();

    // Tell KITT to use annyang
    SpeechKITT.annyang();

    // Define a stylesheet for KITT to use
    SpeechKITT.setStylesheet('//cdnjs.cloudflare.com/ajax/libs/SpeechKITT/0.3.0/themes/flat-turquoise.css.map');

    // Render KITT's interface
    SpeechKITT.vroom();
}
