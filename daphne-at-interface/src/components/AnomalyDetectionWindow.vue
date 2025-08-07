<template>
  <div id="anomaly-detection">
    <div class="is-title" v-bind:style="{'background': backgroundColor, 'color': fontColor}">
      Anomaly Detection
      <span class="tutorialLink">
            <u v-on:click.prevent="detectionTutorial">?</u>
            </span>
      <span class="tutorialLink">&#8287; &#8287;</span>
      <span class="tutorialLink">
                <u v-on:click.prevent="clear">Clear</u>
            </span>
      <span class="tutorialLink">&#8287; &#8287;</span>
      <span class="tutorialLink">
                <u v-on:click.prevent="selectall">Select All</u>
            </span>
    </div>
    <div v-if="(this.symptomsList.length === 0)" class="is-content" style="min-height: 100px">
      No anomalous symptoms detected.
    </div>
    <div v-else class="is-content" style="min-height: 100px">
      <div class="columns">
        <div class="column is-6">
          <ul>
            <li v-on:click="selectSymptom(symptom); leftToggleFontWeight(index,symptom)" v-for="(symptom,index) in symptomsListLeftColumn"  v-bind:style="{ 'font-weight': isLeftSelected(index) ? 'bold' : 'normal', cursor: 'pointer'}">
              {{ symptom['detection_text'] }}
            </li>
          </ul>
        </div>
        <div class="column is-6">
          <ul>
            <li v-on:click="selectSymptom(symptom); rightToggleFontWeight(index,symptom)" v-for="(symptom,index) in symptomsListRightColumn"  v-bind:style="{ 'font-weight': isRightSelected(index) ? 'bold' : 'normal', cursor: 'pointer', hover: { 'font-weight': 'bold' }}">
              {{ symptom['detection_text'] }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {mapGetters} from 'vuex'
import {detectionColorStyle} from "../scripts/at-display-builders";

export default {
  name: "AnomalyDetectionWindow",

  data: function () {
    return {
      backgroundColor: '--primary-color',
      fontColor: '--secondary-color',
      flash: false,
    }
  },

  computed: {
    ...mapGetters({
      symptomsList: 'getSymptomsList',
      selectedSymptomsList: 'getSelectedSymptomsList',
      selectedLeftSymptoms: 'getSelectedLeftSymptomsList',
      selectedRightSymptoms: 'getSelectedRightSymptomsList'
    }),
    symptomsListLeftColumn() {
      let aux = [];
      let symptomsList = this.symptomsList;
      for (let i = 0; i < symptomsList.length; i = i + 2) {
        aux.push(symptomsList[i]);
      }
      return aux;
    },
    symptomsListRightColumn() {
      let aux = [];
      let symptomsList = this.symptomsList;
      for (let i = 1; i < symptomsList.length; i = i + 2) {
        aux.push(symptomsList[i]);
      }
      return aux;
    }
  },

  methods: {
    leftToggleFontWeight(index, symptom) {
      if (this.isLeftSelected(index)) {
        // Remove symptom
        const filteredSymptoms = this.selectedLeftSymptoms.filter(item => item.index !== index);
        this.$store.commit('mutateSelectedLeftSymptomsList', filteredSymptoms);
        this.$store.dispatch('removeSelectedSymptom', symptom);
      } else {
        // Add symptom
        const updatedSymptoms = [...this.selectedLeftSymptoms, {index: index, symptom: symptom}];
        this.$store.commit('mutateSelectedLeftSymptomsList', updatedSymptoms);
        this.$store.dispatch('addSelectedSymptom', symptom);
      }
    },
    isLeftSelected(index) {
      console.log(this.selectedLeftSymptoms);
      if(this.selectedLeftSymptoms!==undefined)
      return this.selectedLeftSymptoms.some(item => item.index === index);
      return false;
    },
    rightToggleFontWeight(index, symptom) {
      if (this.isRightSelected(index)) {
        // Remove symptom
        const filteredSymptoms = this.selectedRightSymptoms.filter(item => item.index !== index);
        this.$store.commit('mutateSelectedRightSymptomsList', filteredSymptoms);
        this.$store.dispatch('removeSelectedSymptom', symptom);
      } else {
        // Add symptom
        const updatedSymptoms = [...this.selectedRightSymptoms, {index: index, symptom: symptom}];
        this.$store.commit('mutateSelectedRightSymptomsList', updatedSymptoms);
        this.$store.dispatch('addSelectedSymptom', symptom);
      }
    },
    isRightSelected(index) {
      if(this.selectedRightSymptoms!==undefined)
      return this.selectedRightSymptoms.some(item => item.index === index);
      return false;
    },
    selectSymptom(symptom) {
      this.$store.dispatch('addSelectedSymptom', symptom);
    },
    detectionTutorial(event) {
      this.$root.$emit('detectionTutorialIndividual');
    },
    clear() {
      // Clear all symptoms using mutations
      this.$store.commit('mutateSelectedLeftSymptomsList', []);
      this.$store.commit('mutateSelectedRightSymptomsList', []);
      this.$store.commit('mutateSymptomsList', []);
      this.$store.commit('mutateSelectedSymptomsList', []);
      
      // Update timestamp
      const now = new Date();
      const formattedDate = now.toLocaleString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
        hour12: true
      });
      this.$store.commit('mutateLastUpdatedSymptomsTimestamp', formattedDate);
    },
    selectall() {
      let symptomsList = this.symptomsList;
      let leftSymptoms = [];
      let rightSymptoms = [];
      let even = 0;
      let odd = 0;
      
      for (let i = 0; i < symptomsList.length; i++) {
        this.$store.dispatch('addSelectedSymptom', symptomsList[i]);
        if (i % 2 === 0) {
          leftSymptoms.push({index: even, symptom: symptomsList[i]});
          even++;
        } else {
          rightSymptoms.push({index: odd, symptom: symptomsList[i]});
          odd++;
        }
      }
      
      // Use mutations to update state
      this.$store.commit('mutateSelectedLeftSymptomsList', leftSymptoms);
      this.$store.commit('mutateSelectedRightSymptomsList', rightSymptoms);
    }
  },
  watch: {
    symptomsList(newVal, oldVal) {
      let oldValJSON = JSON.stringify(oldVal);
      let newValJSON = JSON.stringify(newVal);
      if (oldValJSON !== newValJSON) {
        let newSymptomsList = JSON.parse(newValJSON);
        let theColors = detectionColorStyle(newSymptomsList);
        let backgroundColor = theColors['background'];
        let fontColor = theColors['font'];
        this.backgroundColor = backgroundColor;
        this.fontColor = fontColor;
      }

    }
  }
}
</script>

<style scoped>
li:hover {
  font-weight: bold;
}

</style>
