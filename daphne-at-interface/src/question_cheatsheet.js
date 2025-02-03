'use strict';

import Vue from 'vue';
import MCCApp from './components/QuestionCheatsheet/QuestionCheatsheetApp';
import store from './question_cheatsheet_store';


// Styles
import './styles/app.scss';

let questionCheatsheet = new Vue({
    el: '#question-cheatsheet',
    store,
    render: h => h(MCCApp)
});
