// initial state
import * as _ from 'lodash-es';
import {fetchPost} from '../../scripts/fetch-helpers';
import {wsTools} from "../../scripts/websocket-tools";

const state = {
    isLoggedIn: false,
    username: '',
    password:'',
    permissions: [],
    hasLoginError: false,
    isSecondUser: false,
    loginError: '',
    loginAlert: '',
    hasRegistrationError: false,
    registrationError: '',
    resetPasswordSent: false
};

const initialState = _.cloneDeep(state);

// getters
const getters = {
    getUsername(state) {return state.username},
};

// actions
const actions = {
    async loginUser({ state, commit, rootState }, { username, password, daphneVersion, isSecondUser }) {
        try {
            let reqData = new FormData();
            reqData.append("username", username);
            reqData.append("password", password);
            reqData.append("daphneVersion", daphneVersion);
            reqData.append('isSecondUser', isSecondUser)

            let userInfo = {'username': username, 'password': password};
            commit('setFormData', userInfo);

            let dataResponse = await fetchPost(API_URL + 'auth/login', reqData);
            if (dataResponse.ok) {
                let data = await dataResponse.json();
                if (data['status'] === 'logged_in') {
                    commit('logUserIn', data);
                }
                else if (data['status'] === 'login_alert') {
                    commit('setLoginPopup', data);
                }
                else {
                    commit('setLoginError', data);
                }
            }
            else {
                console.error('Error logging in.');
            }
        }
        catch(e) {
            console.error('Networking error:', e);
        }
    },
    async logoutUser({ state, commit, rootState }) {
        try {
            let reqData = new FormData();
            let dataResponse = await fetchPost(API_URL + 'auth/logout', reqData);

            if (dataResponse.ok) {
                let data = await dataResponse.json();
                console.log(data['message']);
                commit('logUserOut');
            }
            else {
                console.error('Error logging out.');
            }
        }
        catch(e) {
            console.error('Networking error:', e);
        }
    },
    async registerUser({ state, commit }, form) {
        try {
            let reqData = new FormData(form);
            let dataResponse = await fetchPost(API_URL + 'auth/register', reqData);

            if (dataResponse.ok) {
                let data = await dataResponse.json();
                if (data['status'] === 'registered') {
                    commit('activateModal', 'LoginModal');
                }
                else {
                    commit('setRegistrationError', data);
                }
            }
            else {
                console.error('Error registering.');
            }
        }
        catch(e) {
            console.error('Networking error:', e);
        }
    },
    async resetPasswordEmail({ state, commit }, form) {
        try {
            let reqData = new FormData(form);
            let dataResponse = await fetchPost(API_URL + 'auth/reset-password', reqData);

            if (dataResponse.ok) {
                let data = await dataResponse.json();
                if (data['status'] === 'email sent') {
                    commit('setResetPasswordSent', true);
                }
                else {
                    commit('setRegistrationError', data);
                }
            }
            else {
                console.error('Error sending the email.');
            }
        }
        catch(e) {
            console.error('Networking error:', e);
        }
    }
};

// mutations
const mutations = {
    mutateUsername(state, newVal) {state.username = newVal},

    setFormData(state, userInfo) {
        state.isLoggedIn = false;
        state.hasLoginError = false;
        state.isSecondUser = false;
        state.username = userInfo['username'];
        state.password = userInfo['password'];
    },
    logUserIn(state, userInfo) {
        state.isLoggedIn = true;
        state.hasLoginError = false;
        state.isSecondUser = false;
        state.username = userInfo['username'];
        state.permissions = userInfo['permissions'];
    },
    logUserOut(state) {
        state.isLoggedIn = false;
        state.hasLoginError = false;
        state.username = '';
        state.permissions = [];
    },
    setLoginError(state, loginInfo) {
        state.isLoggedIn = false;
        state.hasLoginError = true;
        state.loginError = loginInfo['login_error'];
    },
    setLoginPopup(state, loginInfo) {
        state.isLoggedIn = false;
        state.hasLoginError = false;
        state.isSecondUser = true;
        state.loginAlert = loginInfo['login_error'];
    },
    setRegistrationError(state, registrationInfo) {
        state.isLoggedIn = false;
        state.hasRegistrationError = true;
        state.registrationError = registrationInfo['login_error'];
    },
    setResetPasswordSent(state, resetPasswordSent) {
        state.resetPasswordSent = true;
    },
    restoreAuth(state, recoveredState) {
        Object.keys(recoveredState).forEach((key) => {
            state[key] = recoveredState[key];
        });
    }
};

export default {
    state,
    getters,
    actions,
    mutations
}
