<template>
    <div id="telemetry-feed">
        <div class="is-title">
            Sensor Data
            <span class="tutorialLink">
            <u v-on:click.prevent="telemetryTutorial">?</u>
            </span>
            <span class="tutorialLink">&#8287; &#8287;</span>
            <span class="tutorialLink">
                <u v-on:click.prevent="clear">Clear</u>
            </span>
            <span class="tutorialLink">&#8287; &#8287;</span>
            <span class="tutorialLink">
                <u v-on:click.prevent="plotAll">Plot All</u>
            </span>

        </div>
        <div class="is-centered is-content">
            <div class="is-content is-multiselect">
                    <multiselect
                            :value="value"
                            :options="options"
                            :multiple="true"
                            :searchable="true"
                            :close-on-select="true"
                            :clear-on-select="false"
                            :preserve-search="true"
                            :allow-empty="false"
                            placeholder="Search and/or select the measurements to be displayed."
                            label="name"
                            selectLabel="Click to select"
                            deselectLabel="Click to remove"
                            openDirection="below"
                            track-by="name"
                            :preselect-first="true"
                            @input="newSelection">
                    </multiselect>
            </div>
            <div class="box is-stretched is-centered space-marker" style="background: var(--color__bg); overflow: hidden; resize: vertical">
                <vue-plotly style="width: 95%; height: 95%;"
                        :data="plotData"
                        :layout="plotLayout"
                        :options="{displayModeBar: false}"/>
            </div>
        </div>
    </div>
</template>

<script>
    import VuePlotly from '@statnett/vue-plotly'
    import Multiselect from 'vue-multiselect'
    import { mapGetters, mapMutations } from 'vuex';
    import {setLayout} from "../scripts/at-display-builders";


    export default {
        name: "SensorDataWindow",

        computed: {
            ...mapGetters({
                symptomsList: 'getSymptomsList',
                plotData: 'getPlotData',
                selectedVariables: 'getSelectedVariables',
                inputVariables: 'getInputVariables',
                telemetryIsOngoing: 'getTelemetryIsOngoing',
                telemetryInfo: 'getTelemetryInfo',
            }),
            value ()  {
                let variables = this.selectedVariables;
                let aux = [];
                for (let i = 0; i < variables.length; i++) {
                    aux.push({'name': variables[i]});
                }
                return aux;
            },
            options ()  {
                let variables = this.inputVariables;
                let aux = [];
                for (let i = 0; i < variables.length; i++) {
                    aux.push({'name': variables[i]});
                }
              aux.sort((a,b) => (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0))
              return aux;
            },
            plotLayout () {
                try {
                    return setLayout(this.selectedVariables, this.telemetryInfo, this.plotData);
                }
                catch(err) {
                    console.log(err);
                    console.log('ERROR setting the plot layout.')
                }
            }
        },

        methods: {
            newSelection(newElement) {
                let newSelectedVariables = [];
                for (let i = 0; i < newElement.length; i++) {
                    newSelectedVariables[i] = newElement[i]['name'];
                }
                this.$store.dispatch('updateSelectedVariables', newSelectedVariables);
            },
            telemetryTutorial(event) {
                this.$root.$emit('telemetryTutorialIndividual');
            },
            plotAll() {
                let newSelectedVariables = [];
                let symptomsList = this.symptomsList;
                for (let i = 0; i < symptomsList.length; i++) {
                    newSelectedVariables[i] = symptomsList[i]['display_name'];
                }    
                this.$store.dispatch('updateSelectedVariables', newSelectedVariables);
            },
            clear(){
                let variables = this.inputVariables;
                let newSelectedVariables = [variables[0]];
                this.$store.dispatch('updateSelectedVariables', newSelectedVariables);
            },
        },

        components: {
            VuePlotly,
            Multiselect,
        }
    }
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style scoped>

</style>
