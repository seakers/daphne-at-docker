// initial state
import * as _ from 'lodash-es';
import {fetchGet, fetchPost} from "../../scripts/fetch-helpers";

const state = {
    command: '',
    dialogueHistory: [],
    response: {},
    prevResponse: {},
    isLoading: false,
    isListening: false,
    isSpeaking: false,
    isUnmute: true,
    timeCounter:0,
    daphneVoice: 'US English Female'
    ,
    // anomalousSymptomsDetected: false,
    anomalousProceduresDetected: false,
    selectedProcedure: null,
};

const initialState = _.cloneDeep(state);

// getters
const getters = {
    getResponse(state) {
        return state.response;
    },
    getPrevResponse(state) {
        return state.prevResponse;
    },
    getIsLoading(state) {
        return state.isLoading;
    },
    getIsListening(state) {
        return state.isListening;
    },
    getIsSpeaking(state) {
        return state.isSpeaking;
    },
    getIsUnmute(state) {
        return state.isUnmute;
    },
    getDaphneVoice(state) {
        return state.daphneVoice;
    }
};

// actions
const actions = {
    async loadDialogue({ state, commit, rootState }) {
        try {
            let dataResponse = await fetchGet(API_URL + 'at/dialogue/history');

            if (dataResponse.ok) {
                let data = await dataResponse.json();
                commit('setDialogueHistory', data['dialogue_pieces']);
            }
            else {
                console.error('Error retrieving past conversation history.');
            }
        }
        catch(e) {
            console.error('Networking error:', e);
        }
    },
    async clearHistory({ state, commit, rootState }) {
        try {
            let reqData = new FormData();
            let dataResponse = await fetchPost(API_URL + 'at/dialogue/clear-history', reqData);

            if (dataResponse.ok) {
                let data = await dataResponse.json();
                commit('setDialogueHistory', []);
            }
            else {
                console.error('Error clearing conversation history.');
            }
        }
        catch(e) {
            console.error('Networking error:', e);
        }
    },
    async executeCommand({ state, commit, rootState }) {
        try {
            commit('setIsLoading', true);
            commit('addDialoguePiece', {
                "voice_message": state.command,
                "visual_message_type": ["text"],
                "visual_message": [state.command],
                "writer": "user"
            });

            let telemetryValues = rootState.daphneat.telemetryValues;
            console.log("telemetry values", telemetryValues)


            let telemetryValuesDict = Object.fromEntries(
                Object.entries(telemetryValues).map(([key, value]) => [key, { ...value }])
            );
            
            let parsedTelemetryValues = {};
            let parsedTelemetryValuest1 = {};

            for (let i in telemetryValuesDict) { 
                let valueDict = telemetryValuesDict[i];
                const reversedArray = Object.entries(valueDict)
                    .reverse() 
                    .map(([key, value]) => [Number(key), value]);  // Convert keys back to numbers if needed

                parsedTelemetryValues[i] = reversedArray[0][1];
                
                // Get t-1 value (30 steps back or last available)
                if (reversedArray.length > 30) {
                    parsedTelemetryValuest1[i] = reversedArray[29][1];
                } else {
                    parsedTelemetryValuest1[i] = reversedArray[reversedArray.length - 1][1];
                }
            }

            console.log("parsedTelemetryValues", parsedTelemetryValues)
            console.log("parsedTelemetryValuest1", parsedTelemetryValuest1)

            let reqData = new FormData();
            reqData.append('telemetry_values', JSON.stringify(parsedTelemetryValues));
            reqData.append('telemetry_values_t1', JSON.stringify(parsedTelemetryValuest1));
            reqData.append('addtional_evidence', JSON.stringify(rootState.daphneat.additionalEvidence));

            reqData.append('command', state.command);
            const formattedHistory = state.dialogueHistory
                .slice(-10) // Get only the last 10 entries
                .map(item => ({
                    writer: item.writer,
                    message: item.visual_message ? 
                    (Array.isArray(item.visual_message) ? item.visual_message[0] : item.visual_message) : 
                    (item.voice_message || '')
                }));
            reqData.append('dialogue_history', JSON.stringify(formattedHistory));
            let dataResponse = await fetchPost('/api/at/dialogue/command', reqData);
            console.log("COMMAND" + state.command);

            if (dataResponse.ok) {
                let data = await dataResponse.json();
                commit('addDialoguePiece', data['response']);
                commit('setResponse', data['response']['visual_message']);
                console.log("VOICE MESSAGE" + data['response']['voice_message']);
                console.log("VISUAL MESSAGE" + data['response']['visual_message']);
                
                // Check if this is a physics diagnosis completion response
                if (data['response'].diagnosis_report) {
                    console.log("Physics diagnosis completed via chatbot, processing results...");
                    console.log("diagnosis_report content:", data['response'].diagnosis_report);
                    await actions.handlePhysicsDiagnosisFromChatbot({ commit, rootState }, data['response'].diagnosis_report);
                }

            }
            else {
                console.error('Error processing the command.');
            }
        }
        catch(e) {
            console.error('Networking error:', e);
        }
        commit('setIsLoading', false);
    },
    async handlePhysicsDiagnosisFromChatbot({ commit, rootState }, diagnosisReport) {
        try {
            console.log("Physics Diagnosis from Chatbot - Received diagnosis report:", diagnosisReport);
            
            // The diagnosis_report has physics_diagnosis_data nested inside
            // Extract the actual physics data (it's nested one level deeper)
            let physicsData = null;
            
            if (diagnosisReport && diagnosisReport.physics_diagnosis_data) {
                // Check if it's double-nested (physics_diagnosis_data.physics_diagnosis_data)
                if (diagnosisReport.physics_diagnosis_data.physics_diagnosis_data) {
                    console.log("Found double-nested physics_diagnosis_data structure");
                    physicsData = diagnosisReport.physics_diagnosis_data.physics_diagnosis_data;
                } else {
                    console.log("Found single-nested physics_diagnosis_data structure");
                    physicsData = diagnosisReport.physics_diagnosis_data;
                }
            }
            
            if (!physicsData || !physicsData.component_anomalies) {
                console.error("component_anomalies not found in physics data");
                console.log("Available keys:", physicsData ? Object.keys(physicsData) : 'physicsData is null');
                return false;
            }
            
            console.log("Successfully extracted physics data with component_anomalies");
            
            // Process the physics diagnosis data similar to the existing requestPhysicsDiagnosis
            const physicsDiagnosisData = {
                mostProbableAnomaly: physicsData.most_probable_anomaly,
                probability: physicsData.probability,
                componentAnomalies: physicsData.component_anomalies.map(anomaly => ({
                    name: anomaly.name,
                    probability: anomaly.score || anomaly.probability,
                    similarity: anomaly.score || anomaly.similarity,
                    score: anomaly.score,  // Keep original score field
                    telemetry: anomaly.telemetry_data || anomaly.telemetry || [],
                    faultInjectionTime: anomaly.fault_injection_time,
                    faultInjectionTimeSeconds: anomaly.fault_injection_time_seconds,
                    isHighlighted: anomaly.is_highlighted,
                    // Keep snake_case versions too for template fallback
                    fault_injection_time: anomaly.fault_injection_time,
                    fault_injection_time_seconds: anomaly.fault_injection_time_seconds,
                    is_highlighted: anomaly.is_highlighted
                }))
            };
            
            // Update the store with the physics diagnosis data
            // Since daphneat module is not namespaced, commit directly without namespace prefix
            commit('mutatePhysicsDiagnosisData', physicsDiagnosisData, { root: true });
            
            // Update the telemetry graph data
            if (physicsData.actual_telemetry) {
                // Build simulated data object from component anomalies
                const simulatedData = {};
                physicsData.component_anomalies.forEach((anomaly, index) => {
                    const telemetryData = anomaly.telemetry_data || anomaly.telemetry || [];
                    if (telemetryData && telemetryData.length > 0) {
                        simulatedData[anomaly.name] = {
                            data: telemetryData,
                            color: `hsl(${index * 137.5 % 360}, 70%, 50%)`
                        };
                    }
                });

                // Update telemetry graph data in one mutation
                commit('mutateTelemetryGraphData', {
                    actual: physicsData.actual_telemetry,
                    simulated: simulatedData,
                    timeLabels: physicsData.time_labels,
                    telemetry_metadata: physicsData.telemetry_metadata || {
                        unit: 'mmHg',
                        sensor_info: {},
                        target_sensor: 'ppCO2 (L1)'
                    }
                }, { root: true });
            }
            
            // Emit a custom event to notify the component that physics diagnosis is complete
            // This will trigger tab creation in the AnomalyDiagnosisWindow component
            if (typeof window !== 'undefined' && window.dispatchEvent) {
                const physicsDiagnosisEvent = new CustomEvent('physicsDiagnosisCompleted', {
                    detail: {
                        diagnosisReport: diagnosisReport,
                        physicsDiagnosisData: physicsDiagnosisData
                    }
                });
                window.dispatchEvent(physicsDiagnosisEvent);
            }
            
            console.log("Physics diagnosis data successfully loaded from chatbot");
            return true;
        } catch (error) {
            console.error("Error handling physics diagnosis from chatbot:", error);
            console.error("Error stack:", error.stack);
            return false;
        }
    },
    // async detectAnomalousSymptoms({ commit }, value) {
    //     commit('setAnomalousSymptomsDetected', value);
    //     if (value) {
    //         commit('addDialoguePiece', {
    //             "voice_message": `I have detected a change in the measurements. Would you like me to plot the measurements?`,
    //             "visual_message_type": ["text"],
    //             "visual_message": ['I have detected a change in the measurements. Would you like me to plot the measurements?'],
    //             "writer": "daphne"
    //         });
    //     }
    // },
};

// mutations
const mutations = {
    setCommand(state, command) {
        state.command = command;
    },
    setIsListening(state, listen) {
        state.isListening = listen;
    },
    setIsSpeaking(state, speak) {
        state.isSpeaking = speak;
    },
    setResponse(state, response) {
        state.prevResponse = state.response;
        state.response = response;
    },
    setIsLoading(state, isLoading) {
        state.isLoading = isLoading;
    },
    resetDaphne(state) {
        state = Object.assign(state, _.cloneDeep(initialState));
    },
    restoreDaphne(state, recoveredState) {
        Object.keys(recoveredState).forEach((key) => {
            state[key] = recoveredState[key];
        });
    },
    setDialogueHistory(state, dialogueHistory) {
        state.dialogueHistory = dialogueHistory;
    },
    // setAnomalousSymptomsDetected(state, value) {
    //     state.anomalousSymptomsDetected = value;
    // },

    setAnomalousProceduresDetected(state, value) {
        state.anomalousProceduresDetected = value;
      },
      setSelectedProcedure(state, procedure) {
        state.selectedProcedure = procedure;
      },
    addDialoguePiece(state, dialoguePiece) {
        console.log("pushed to dialogue history")
        state.dialogueHistory.push(dialoguePiece);
    },
    setIsUnmute(state, newVal) {
        state.isUnmute = newVal
    },
    setDaphneVoice(state, newVal) {
        console.log(newVal)
        state.daphneVoice = newVal
    },
    setTimeCounter(state, newVal) {
        state.timeCounter = newVal
    }
};

export default {
    state,
    getters,
    actions,
    mutations
}