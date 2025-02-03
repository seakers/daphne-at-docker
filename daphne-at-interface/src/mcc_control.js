'use strict';

import Vue from 'vue';
import MCCApp from './components/MCC/MCCApp';
import store from './mcc_store';


// Styles
import './styles/app.scss';

let mccDisplay = new Vue({
    el: '#mcc-control',
    store,
    render: h => h(MCCApp)
});
