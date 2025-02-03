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
    leftToggleFontWeight(index,symptom) {
      console.log(this.selectedSymptomsList);
      console.log(this.selectedLeftSymptoms);
        if (this.isLeftSelected(index)) {
          this.$store.commit('mutateSelectedLeftSymptomsList',this.selectedLeftSymptoms.filter(item => item.index !== index));
          this.$store.dispatch('removeSelectedSymptom', symptom);

        } else {
          this.selectedLeftSymptoms.push({index: index, symptom: symptom});
          this.$store.commit('mutateSelectedLeftSymptomsList',this.selectedLeftSymptoms);
        }


    },
    isLeftSelected(index) {
      console.log(this.selectedLeftSymptoms);
      if(this.selectedLeftSymptoms!==undefined)
      return this.selectedLeftSymptoms.some(item => item.index === index);
      return false;
    },
    rightToggleFontWeight(index,symptom) {
        if (this.isRightSelected(index)) {
          this.$store.commit('mutateSelectedRightSymptomsList',this.selectedRightSymptoms.filter(item => item.index !== index));
          this.$store.dispatch('removeSelectedSymptom', symptom);
        } else {
          this.selectedRightSymptoms.push({index: index, symptom: symptom});
          this.$store.commit('mutateSelectedRightSymptomsList',this.selectedRightSymptoms);
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
      this.selectedLeftSymptoms.splice(0, this.selectedLeftSymptoms.length);
      this.selectedRightSymptoms.splice(0, this.selectedRightSymptoms.length);
      this.$store.commit('mutateSymptomsList', []);
      this.$store.commit('mutateSelectedSymptomsList', []);
      const now = new Date();
      let formattedDate = now.toLocaleString('en-US', {
            year: 'numeric',
            month: 'long',  // e.g., October
            day: 'numeric', // e.g., 15
            hour: 'numeric',
            minute: 'numeric',
            second: 'numeric',
            hour12: true    // Use 12-hour format with AM/PM
          });
      this.$store.commit('mutateLastUpdatedSymptomsTimestamp', formattedDate);
    },
    selectall() {
      let symptomsList = this.symptomsList;
      let even=0;
      let odd =0;
      for (let i = 0; i < symptomsList.length; i = i + 1) {
        this.$store.dispatch('addSelectedSymptom', symptomsList[i]);
        if(i%2===0)
        {
          this.selectedLeftSymptoms.push({index: even, symptom: symptomsList[i]});
          even++;
        }
        else
        {
          this.selectedRightSymptoms.push({index: odd, symptom: symptomsList[i]});
          odd++;
        }
      }
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
