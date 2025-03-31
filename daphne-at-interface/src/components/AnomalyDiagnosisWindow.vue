<template>
  <div id="anomaly_diagnosis">
    <div class="is-title">
      Anomaly Diagnosis
      <span class="tutorialLink">
                <u v-on:click.prevent="diagnosisTutorial">?</u>
            </span>
    </div>
    <div class="is-content">
      <div class="is-content">
        <div v-if="(this.selectedSymptomsList.length === 0)">
          No anomalous symptoms selected.
        </div>
        <div v-else class="columns" style="margin: 0px; padding: 0px">
          <div class="column is-10" style="margin: 0px; padding: 0px">
            <ul>
              <li class="hover" v-on:click="deselectSymptom(symptom)" v-for="symptom in selectedSymptomsList"
                  style="cursor: pointer">
                {{ symptom['detection_text'] }}
              </li>
            </ul>
          </div>
          <div class="column is-2" style="margin: 0px; padding: 0px">
            <button class="button theme-buttons"
                    style="width: 52%; border-color: #0AFEFF; color: #0AFEFF; background: #002E2E"
                    id="request_diagnosis" v-on:click.prevent="requestDiagnosis">Diagnose
            </button>
            <button class="button theme-buttons"
                    style="width: 38%; border-color: #0AFEFF; color: #0AFEFF; background: #002E2E"
                    id="clear_symptoms" v-on:click.prevent="clearSymptoms">Clear
            </button>
          </div>
        </div>
      </div>
      <div class="horizontal-divider" style="margin-top: 10px; margin-bottom: 10px"></div>
      <div class="is-content">
        <div v-if="diagnosisReport.length === 0">
          <img v-if="isLoading"
               src="assets/img/loader.svg"
               style="display: block; margin: auto;"
               height="40" width="40"
               alt="Loading spinner">
          <p v-else>No diagnosis reports requested.</p>
        </div>
        <div v-else>
<!--          <div class="columns" style="margin: 0px; padding: 0px">-->
            <div class="column" style="margin: 0px; padding: 0px">
              <span style="margin-bottom:20px; color: #0AFEFF; background: #002E2E">Set of symptoms selected for diagnosis:</span>
              <ul>
                <li class="hover" v-for="symptom in diagnosisReport['symptoms_list']" v-on:click="recoverSymptomsList()"
                    style="cursor: pointer">
                  {{ symptom['detection_text'] }}
                </li>
              </ul>
            </div>
            <div class="column" style="margin-top: 20px; padding: 0px">
              <span style="margin-bottom:20px; color: #0AFEFF; background: #002E2E">Could be caused by anomalies:</span><br />
              <span><input type='checkbox' v-model="allSelected" v-on:click="selectAllAnomalies()"> Select All </span>
              <ul v-for="anomaly in diagnosisReport['diagnosis_list']">
                <li>
                  <input type="checkbox" class='checkall' v-model="checked" :value="anomaly"
                         style="border-color: #0AFEFF; color: #0AFEFF; background: #002E2E;">
                  {{ anomaly['name'] }} <span :style="{'color': 0.66<anomaly['score']<1?(anomaly['score']<0.33 ? 'green' : 'yellow'):'red'}">({{anomaly['text_score']}}) </span>
                </li>
              </ul>
            </div>
          <div style="text-align: center; margin-top: 30px">
            <p id="alert" style="display: none; color: red">Please select an anomaly to investigate.</p>
            <button class="button" type="submit" onclick="errorMessage()"
                    style="width: 30%; border-color: #0AFEFF; color: #0AFEFF; background: #002E2E;"
                    v-on:click.prevent="showExplanations">Show explanations
            </button>
          </div>
        </div>
      </div>
      <div class="horizontal-divider" style="margin-top: 10px; margin-bottom: 10px"></div>
        <div class="is-content">
          <div class="is-mini-title" style="margin-bottom:5px; font-size: 22px">
            Astrobee Status
          </div>
          
          <div class="box is-main" style="margin-top: 20px; padding: 15px;">
            <div v-if="astrobeeStatus">
              <p style="font-size: 18px; margin-bottom: 15px; color: #0AFEFF;">Current Status:</p>
              <p style="font-size: 16px; text-align: center; padding: 10px; background: #002E2E; border: 1px solid #0AFEFF; border-radius: 4px;">
                {{ astrobeeStatus }}
              </p>
            </div>
            <div v-else>
              <p style="text-align: center;">No active Astrobee procedures running.</p>
            </div>
          </div>
        </div>
      <div class="horizontal-divider" style="margin-top: 10px; margin-bottom: 10px"></div>
      <div class="is-content">
        <div v-if="diagnosisReport.length === 0 || this.explaining === false">
          <img v-if="isLoading"
               src="assets/img/loader.svg"
               style="display: block; margin: auto;"
               height="40" width="40"
               alt="Loading spinner">
          <p v-else>No explanations requested.</p>
        </div>
        <div v-else id='explanations' style="display: block">
          <div class="is-mini-title" style="margin-bottom:5px; font-size: 22px">
            Explanations
            <u style="float: right; cursor: pointer" v-on:click.prevent="clearExplanations">Clear</u>
          </div>

          <div class="box is-main" style="margin-top: 20px">
            <p class="is-mini-title" style="margin-bottom: 10px; text-align: center">Symptom Comparison Table</p>
            <p style="text-align: center; margin-bottom: 10px;">Knowledge-driven explanation of the anomalies you have
              selected. Hover over the cells to see their description.</p>
            <p style="color: red; margin-bottom: 10px; text-align: center"
               v-if="symptomsList.length > selectedSymptomsList.length">WARNING! You have selected only
              {{ this.selectedSymptomsList.length }} out of {{ this.symptomsList.length }} anomalous symptoms for
              diagnosis. </p>
            <div class="table-container">
              <table class="table is-bordered is-narrow is-hoverable is-fullwidth">
                <thead>
                <tr style="align-content: center; text-align: center; font-weight: bold;">
                  <td style="color: #0AFEFF; background: #002E2E" rowspan="2"><p
                      title="The names of potential anomaly scenarios from the Knowledge Graph.">Anomaly scenario</p>
                  </td>
                  <td style="color: #0AFEFF; background: #002E2E" rowspan="2"><p
                      title="This column provides the total number of off-nominal measurements, also called symptoms, that usually define the signature of an anomaly scenario.">
                    Total number of symptoms in anomaly</p></td>
                  <td v-bind:colspan="this.diagnosisReport['symptoms_list'].length"
                      style="color: #0AFEFF; background: #002E2E">
                    <p title="These are the symptoms that you have selected above for diagnosis. Note, that these selected symptoms may or may not be present in the signature of an anomaly scenario present in this table.">
                      Symptoms selected for diagnosis</p>
                  </td>
                  <td style="color: #0AFEFF; background: #002E2E" rowspan="2"><p
                      title="These are the number of symptoms that are missing from this table. This can mean either that they are not currently anomalous or that they are anomalous but you have not selected them for diagnosis.">
                    Symptoms missing</p></td>
                  <td style="color: #0AFEFF; background: #002E2E" rowspan="2"><p
                      title="This column provides the likelihood of the respective anomaly being the current anomaly scenario. The closer to 1 the score is, the more likely it is the anomaly scenario.">
                    Likelihood Score</p></td>
                  <td style="color: #0AFEFF; background: #002E2E" rowspan="2"><p
                      title="Click on the button to see the procedure corresponding to the anomaly selected.">
                    Anomaly Procedure</p></td>
                </tr>
                <tr>
                  <td v-for="symptom in diagnosisReport['symptoms_list']">{{ symptom['detection_text'] }}</td>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(anomaly) in this.checked">
                  <td>{{ anomaly['name'] }}</td>
                  <td style="text-align: center; vertical-align: middle"><p class="hover" style="cursor: pointer"
                                                                            v-bind:title="'The signature of this anomaly is: '+ anomaly['signature']"
                                                                            v-on:click="showSignature(anomaly)">
                    {{ anomaly['signature'].length }}</p></td>
                  <td v-for="symptom in diagnosisReport['symptoms_list']"
                      style="text-align: center; vertical-align: middle;">
                  <span v-if="tickOrCross(anomaly['containsRequestedSymptoms'], symptom['detection_text']) === 'tick'"
                        class="checkmark">
                        <div class="checkmark_circle"></div>
                        <div class="checkmark_stem"></div>
                        <div class="checkmark_kick"></div>
                      </span>
                    <span
                        v-if="tickOrCross(anomaly['containsRequestedSymptoms'], symptom['detection_text']) === 'cross'"
                        class="crosssign">
                        <div class="crosssign_circle"></div>
                        <div class="crosssign_stem"></div>
                        <div class="crosssign_stem2"></div>
                      </span>
                  </td>
                  <td style="text-align: center; vertical-align: middle"><p class="hover" style="cursor: pointer"
                                                                            v-bind:title="'The symptoms of this anomaly that are not present in this table are : '+ anomaly['missing_symptoms']"
                                                                            v-on:click="showMissingSymptoms(anomaly)">
                    {{ anomaly['missing_symptoms'].length }}</p></td>
                  <td style="color:black; text-align: center; vertical-align: middle; font-weight: bold"
                      :style="{'background': 0.66<anomaly['score']<1?(anomaly['score']<0.33 ? 'green' : 'yellow'):'red'}">
                    {{ anomaly['score'] }}
                  </td>
                  <td style="color:black; text-align: center; vertical-align: middle; font-weight: bold">
                    <button class="button" style="width: 70%; border-color: #0AFEFF; color: #0AFEFF; background: #002E2E" v-on:click.prevent="selectAnomaly(anomaly['name'])"> Select </button>
                  </td>
                </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import {mapGetters} from 'vuex';
import { fetchPost } from '../scripts/fetch-helpers';

let loaderImage = require('../images/loader.svg');

export default {
  name: "AnomalyDiagnosisWindow",

  data: function () {
    return {
      isLoading: false,
      isAnomalySelected: false,
      checked: [],
      explaining: false,
      allSelected: false,
      astrobeeStatus: null,
      statusInterval: null
    }
  },

  computed: {
    ...mapGetters({
      symptomsList: 'getSymptomsList',
      selectedSymptomsList: 'getSelectedSymptomsList',
      lastSelectedSymptomsList: 'getLastSelectedSymptomsList',
      diagnosisReport: 'getDiagnosisReport',
      selectedAnomaliesList: 'getSelectedAnomaliesList',
      selectedLeftSymptoms: 'getSelectedLeftSymptomsList',
      selectedRightSymptoms: 'getSelectedRightSymptomsList'
    }),
    checkAll: {
      get: function () {
        return this.diagnosisReport['diagnosis_list'] ? this.checked.length === this.diagnosisReport['diagnosis_list'].length : false;
      },
      set: function (value) {
        let checked = [];
        if (value) {
          this.diagnosisReport['diagnosis_list'].forEach(function (anomaly) {
            checked.push(anomaly);
          });
        }
        this.checked = checked;
      }
    }
  },

  methods: {
    startAstrobeeStatusPolling() {
      if (this.statusInterval) {
        clearInterval(this.statusInterval);
      }
      // Set up polling for status updates
      this.statusInterval = setInterval(async () => {
        console.log('Polling Astrobee status...');
        try {
          const response = await fetchPost('/api/at/astrobee_status');
          // const response1 = await fetchPost('/api/at/pride_status');
          // const response2 = await fetchPost('/api/at/yesorno');
          if (response.ok) {
            const data = await response.json();
            console.log('Got Astrobee status:', data);
            this.astrobeeStatus = data.astrobee_status || "No status available";
          }
          // console.log('Polling PRIDE status...', response1);
          // if (response1.ok) {
          //   const data1 = await response1.json();
          //   console.log('Got PRIDE status:', data1);
          //   this.prideStatus = data1.pride_status || "No status available";
          // }
          // console.log('Polling Yes or No status...');
          // if (response2.ok) {
          //   const data2 = await response2.json();
          //   console.log('Got Yes or No status:', data2);
          //   this.yesOrNo = data2.yesorno || "No status available";
          // }
        } catch (error) {
          console.error('Error getting Astrobee status:', error);
        }
      }, 1000); // Poll every 3 seconds
    },
    selectAllAnomalies: function() {
      let checked = [];
      if (!this.allSelected) {
        this.diagnosisReport['diagnosis_list'].forEach(function (anomaly) {
          checked.push(anomaly);
        });
        this.checked = checked;
      }
      else {
        this.allSelected = false;
        this.checked = checked;
        this.clearExplanations();
      }
    },
    showSignature(anomaly) {
      const sign = 'The signature of the anomaly ' + anomaly['name'] + ' is: ';
      let text = sign + '<ul>';
      for (let symptom in anomaly['signature']) {
        text = text + '<li>' + anomaly['signature'][symptom] + '</li>'
      }
      const voice = sign + ' ' + anomaly['signature']
      text = text + '</ul>'
      if (this.command === 'stop') {
        responsiveVoice.cancel();
      } else {
        this.$store.commit('addDialoguePiece', {
          "voice_message": voice,
          "visual_message_type": ["text"],
          "visual_message": [text],
          "writer": "daphne"
        });
      }
    },
    showMissingSymptoms(anomaly) {
      const missing = 'The symptoms of the anomaly ' + anomaly['name'] + ' that are not present in this table are: ';
      let text = missing + '<ul>';
      for (let symptom in anomaly['missing_symptoms']) {
        text = text + '<li>' + anomaly['missing_symptoms'][symptom] + '</li>'
      }
      text = text + '</ul>'
      const voice = missing + ' ' + anomaly['missing_symptoms']
      if (this.command === 'stop') {
        responsiveVoice.cancel();
      } else {
        this.$store.commit('addDialoguePiece', {
          "voice_message": voice,
          "visual_message_type": ["text"],
          "visual_message": [text],
          "writer": "daphne"
        });
      }
    },
    errorMessage() {
      if (isNaN(document.getElementById("number").value)) {
        // Changing content and color of content
        error.textContent = "Please select anomalies for investigation."
        error.style.color = "red"
      } else {
        error.textContent = ""
      }
    },
    deselectSymptom(symptom) {

      for (let i = 0; i < this.selectedLeftSymptoms.length; i++) {
        console.log(typeof this.selectedLeftSymptoms, typeof symptom)
        // Check if the symptom property of the current object is equal to the value you're looking for
        if (this.selectedLeftSymptoms[i].symptom['detection_text'] === symptom['detection_text']) {
          // If the symptom is found, remove it
          this.selectedLeftSymptoms.splice(i, 1);
          // Exit the loop since the symptom is found
          break;
        }
      }

      for (let i = 0; i < this.selectedRightSymptoms.length; i++) {
        // Check if the symptom property of the current object is equal to the value you're looking for
        if (this.selectedRightSymptoms[i].symptom['detection_text'] === symptom['detection_text']) {
          // If the symptom is found, remove it
          this.selectedRightSymptoms.splice(i, 1);
          // Exit the loop since the symptom is found
          break;
        }
      }

      this.$store.dispatch('removeSelectedSymptom', symptom);
    },
    clearSymptoms() {
      this.selectedLeftSymptoms.splice(0, this.selectedLeftSymptoms.length);
      this.selectedRightSymptoms.splice(0, this.selectedRightSymptoms.length);
      this.$store.dispatch('clearSelectedSymptoms');
      this.$store.dispatch('clearDiagnosisReport');
      this.explaining = false;
      this.checked = [];
    },
    clearFullDiagnosisReport() {
      this.$store.dispatch('clearDiagnosisReport');
      this.explaining = false;
      this.checked = [];
    },
    async requestDiagnosis() {
      this.allSelected = false;
      this.isLoading = true;
      this.explaining = false;
      this.checked = [];
      await this.$store.dispatch('requestDiagnosis', this.selectedSymptomsList);
      

      // Display Astrobee procedures in chat after diagnosis
      const diagnosisReport = this.$store.getters.getDiagnosisReport;
      console.log("diagnosos report",diagnosisReport, diagnosisReport.astrobee_procedure_list);
      if (diagnosisReport && diagnosisReport.astrobee_procedure_list && diagnosisReport.astrobee_procedure_list.length > 0) {
        console.log("Adding procedure message to dialogue", diagnosisReport.astrobee_procedure_list);
        const procedureList = diagnosisReport.astrobee_procedure_list.map(proc => 
          `<li>${proc.title}</li>`
        ).join('');
        const procedureMessage = {
          "voice_message": "I found the following Astrobee procedures that might be helpful for the diagnosed anomalies. Would you like me to start any of these procedures?",
          "visual_message_type": ["text"],
          "visual_message": [
            `I found the following Astrobee procedures that might be helpful for the diagnosed anomalies. Would you like me to start any of these procedures?
            <ul>
              ${procedureList}
            </ul>`
          ],
          "writer": "daphne"
        };
        console.log("Adding procedure message to dialogue: ", procedureMessage);
        this.$store.commit('addDialoguePiece', procedureMessage);
        
        // Set flag to display yes/no buttons for procedure selection
        console.log("Setting anomalous procedures detected flag to true");
        this.$store.commit('setAnomalousProceduresDetected', true);
      }
      this.isLoading = false;
    },
    async selectAnomaly(anomalyName) {
      this.isAnomalySelected = true;
        if (anomalyName.includes('&')) {
          let anomaly = anomalyName.split(' & ');
          let firstAnomaly = anomaly[0];
          let secondAnomaly = anomaly[1];
          if (!this.selectedAnomaliesList.includes(firstAnomaly)) {
            await this.$store.dispatch('addSelectedAnomaly', firstAnomaly);
          }
          if (!this.selectedAnomaliesList.includes(secondAnomaly)) {
            await this.$store.dispatch('addSelectedAnomaly', secondAnomaly);
          }
        }
        else {
          if (!this.selectedAnomaliesList.includes(anomalyName)) {
            await this.$store.dispatch('addSelectedAnomaly', anomalyName);
          }
        }
        this.isAnomalySelected = false;
    },
    recoverSymptomsList() {
      this.$store.dispatch('recoverSymptomsList')
    },
    diagnosisTutorial(event) {
      this.$root.$emit('diagnosisTutorialIndividual');
    },
    showExplanations() {
      this.explaining = false;
      this.isLoading = true;
      if (this.checked.length === 0) {
        this.isLoading = false;
        document.getElementById('alert').style.display = "block";
        document.getElementById('explanations').style.display = "none";
      } else {
        document.getElementById('alert').style.display = "none";
      }
      this.isLoading = false;
      this.explaining = true;
      document.getElementById('explanations').style.display = "block";
    },
    clearExplanations() {
      this.explaining = false;
      this.checked = [];
      document.getElementById('explanations').style.display = "none";
    },
    tickOrCross(anomaly, symptom) {
      let ticksOrCross = 'cross'
      for (let i = 0; i < anomaly.length; i++) {
        if (anomaly[i] === symptom) {
          ticksOrCross = 'tick'
        }
      }
      return ticksOrCross;
    },
  },
  mounted() {
    this.startAstrobeeStatusPolling();
    console.log("Astrobee status polling started");
  },
  beforeDestroy() {
    // Clean up interval when component is destroyed
    if (this.statusInterval) {
      clearInterval(this.statusInterval);
    }
  }
}
</script>

<style scoped>
.hover:hover {
  font-weight: bold;
}

.checkmark {
  display: inline-block;
  width: 22px;
  height: 22px;
  -ms-transform: rotate(45deg); /* IE 9 */
  -webkit-transform: rotate(45deg); /* Chrome, Safari, Opera */
  transform: rotate(45deg);
}

.checkmark_circle {
  position: absolute;
  width: 22px;
  height: 22px;
  background-color: green;
  border-radius: 11px;
  left: 0;
  top: 0;
}

.checkmark_stem {
  position: absolute;
  width: 3px;
  height: 12px;
  background-color: #fff;
  left: 11px;
  top: 5px;
}

.checkmark_kick {
  position: absolute;
  width: 3px;
  height: 3px;
  background-color: #fff;
  left: 8px;
  top: 14px;
}

.crosssign {
  display: inline-block;
  width: 22px;
  height: 22px;
  position: relative;
  transform: rotate(45deg);
}

.crosssign_circle {
  position: absolute;
  width: 22px;
  height: 22px;
  background-color: red;
  border-radius: 11px;
  left: 0;
  top: 0;
}

.crosssign_stem,
.crosssign_stem2 {
  position: absolute;
  background-color: #fff;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.crosssign_stem {
  width: 3px;
  height: 12px;
}

.crosssign_stem2 {
  width: 12px;
  height: 3px;
}

</style>
