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

            let reqData = new FormData();
            reqData.append('command', state.command);
            let dataResponse = await fetchPost('/api/at/dialogue/command', reqData);
            console.log("COMMAND" + state.command);

            if (dataResponse.ok) {
                let data = await dataResponse.json();
                commit('addDialoguePiece', data['response']);
                commit('setResponse', data['response']['visual_message']);
                console.log("VOICE MESSAGE" + data['response']['voice_message']);
                console.log("VISUAL MESSAGE" + data['response']['visual_message']);

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
};

export default {
    state,
    getters,
    actions,
    mutations
}
