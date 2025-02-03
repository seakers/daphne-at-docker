import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const debug = process.env.NODE_ENV !== 'production';

export default new Vuex.Store({
    state: {
        questionList: [
            {
                'question': 'Show the current value of X measurement.',
                'parameters': 'A measurement, as a name (e. g.: "Pressure").',
                'answer': 'The last numerical value of measurement X is provided.'
            },
            {
                'question': 'Provide the thresholds of measurement X.',
                'parameters': 'A measurement, as a name (e. g.: "Pressure").',
                'answer': 'The caution and warning thresholds/limits of measurement X are provided.'
            },
            {
                'question': 'Check measurement X status.',
                'parameters': 'A measurement, as a name (e. g.: "Pressure").',
                'answer': 'The X measurement status zone (i. e.: Nominal, UWL, LWL, etc.) is provided.'
            },
            {
                'question': 'What are the potential risks of anomaly X?',
                'parameters': 'An anomaly scenario name (e. g.: "N2 Tank Burst, CDRA failure").',
                'answer': 'A list with the potential risks of anomaly X is provided.'
            },
            {
                'question': 'What is the signature of anomaly X?',
                'parameters': 'An anomaly scenario name (e. g.: "N2 Tank Burst, CDRA failure").',
                'answer': 'A list with the names of the measurements affected by anomaly X is provided.'
            },
            {
                'question': 'What subsystems does anomaly X affect?',
                'parameters': 'An anomaly scenario name (e. g.: "N2 Tank Burst, CDRA failure")',
                'answer': 'A list with the names of the subsystems affected by anomaly X is provided.'
            },
            {
                'question': 'What are the procedures for anomaly X?',
                'parameters': 'An anomaly scenario name (e. g.: "N2 Tank Burst").',
                'answer': 'A list with the names of the procedures related to anomaly X is provided.'
            },
            {
                'question': 'Provide procedure X.',
                'parameters': 'A procedure name or number (e. g.: "N2 Ballast Tank Replacement" or "3.117").',
                'answer': 'A link is provided so that the procedure PDF can be opened in a new tab.'
            },
            {
                'question': 'Which components will procedure X impact?',
                'parameters': 'A procedure name or number (e. g.: "N2 Ballast Tank Replacement" or "3.117").',
                'answer': 'A list with the names of the components affected by procedure X is provided.'
            },
            {
                'question': 'How long will it take to solve anomaly X?',
                'parameters': 'An anomaly scenario name (e. g.: "N2 Tank Burst, CDRA failure").',
                'answer': 'A list with the estimated times to complete each procedure related to anomaly X is provided.'
            },
            {
                'question': 'How long is procedure X?',
                'parameters': 'A procedure name or number (e. g.: "N2 Ballast Tank Replacement, 3.117").',
                'answer': 'The estimated time to complete procedure X is provided.'
            },
            {
                'question': 'Show the image of component X.',
                'parameters': 'A component name (e. g.: "Emergency O2 Generation System, Sabatier Panel").',
                'answer': 'The image for component X has been provided.'
            },
            {
                'question': 'Read steps of procedure X.',
                'parameters': 'A procedure name or number (e. g.: "N2 Ballast Tank Replacement" or "3.117").',
                'answer': 'Reads the steps of the procedure starting from the beginning.'
            },
            {
                'question': 'Next',
                'parameters': 'Does not require any parameters. It is, however, required that the command "Read" is provided before using this command.',
                'answer': 'Reads the next step of the procedure.'
            },
            {
                'question': 'Previous',
                'parameters': 'Does not require any parameters. It is, however, required that the command "Read" is provided before using this command.',
                'answer': 'Reads the previous step of the procedure.'
            },
            {
                'question': 'Repeat',
                'parameters': 'Does not require any parameters. It is, however, required that the command "Read" is provided before using this command.',
                'answer': 'Reads the previous step of the procedure.'
            },
            {
                'question': 'Previous',
                'parameters': 'Does not require any parameters. It is, however, required that the command "Read" is provided before using this command.',
                'answer': 'Reads the previous step of the procedure.'
            },
            {
                'question': 'What is step X of procedure Y?',
                'parameters': 'A valid step number (e. g.: 1.3, 6.2) of a procedure name or number (e. g.: "N2 Ballast Tank Replacement" or "3.117") ',
                'answer': 'Reads a step of the procedure.'
            },
        ],
        selectedQuestionsList: [],
    },
    computed: {
    },
    getters: {
        getQuestionList(state) {return state.questionList},
        getSelectedQuestionsList(state) {return state.selectedQuestionsList},
    },
    mutations: {
        mutateSelectedQuestionsList(state, newVal) {state.selectedQuestionsList = newVal},
    },
    actions: {
        async addSelectedQuestion({state, commit}, question) {
            let currentSelectedQuestions = JSON.parse(JSON.stringify(state.selectedQuestionsList));
            currentSelectedQuestions.push(question);
            commit('mutateSelectedQuestionsList', currentSelectedQuestions);
        },
        async removeSelectedQuestion({state, commit}, question) {
            let currentSelectedQuestions = JSON.parse(JSON.stringify(state.selectedQuestionsList));
            let index = currentSelectedQuestions.indexOf(question);
            currentSelectedQuestions.splice(index, 1);
            commit('mutateSelectedQuestionsList', currentSelectedQuestions);
        },
    },
    modules: {
    },
    strict: debug
});
