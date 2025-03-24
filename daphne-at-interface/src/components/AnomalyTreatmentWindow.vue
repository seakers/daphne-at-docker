<template>
    <div id="anomaly-treatment">
        <div class="title">Anomaly Treatment</div>
        <div class="columns">
            <div class="column">
                Current symptoms:
                <div style="margin-left: 40px">
                    <ul>
                        <li v-on:click="selectSymptom(message)" v-for="message in symptomsList">
                            {{message}}
                        </li>
                    </ul>
                </div>
            </div>
            <div class="vertical-divider"></div>
            <div class="column">
                <div class="columns">
                    <div class="column is-8">
                        Selected symptoms to be diagnosed:
                        <div style="margin-left: 40px">
                            <ul>
                                <li v-on:click="deselectSymptom(message)" v-for="message in selectedSymptomsList">
                                    {{message}}
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div class="column is-4">
                        <a class="button is-custom-button is-blue" v-on:click.prevent="">DIAGNOSE</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex'

    export default {
        name: "AnomalyTreatmentWindow",

        computed: {
            ...mapGetters({
                symptomsList: 'getSymptomsList',
                selectedSymptomsList: 'getSelectedSymptomsList',
            }),
        },

        methods: {
            selectSymptom(message) {
                this.$store.commit('addSelectedSymptom', message);
            },
            deselectSymptom(message) {
                this.$store.commit('clearSelectedSymptom', message);
            },
        }
    }
</script>

<style scoped>

</style>