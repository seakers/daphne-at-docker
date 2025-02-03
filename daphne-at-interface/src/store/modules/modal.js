// initial state
import * as _ from 'lodash-es';
import {fetchPost} from '../../scripts/fetch-helpers';

const state = {
    isModalActive: false,
    modalContent: ''
};

const initialState = _.cloneDeep(state);

// getters
const getters = {
};

// actions
const actions = {
};

// mutations
const mutations = {
    activateModal(state, modalContent) {
        state.isModalActive = true;
        state.modalContent = modalContent;

    },
    closeModal(state) {
        state.isModalActive = false;
    }
};

export default {
    state,
    getters,
    actions,
    mutations
}
