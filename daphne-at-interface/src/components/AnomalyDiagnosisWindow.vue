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
        <!-- <div v-else>
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
       -->

  <div v-else>
  <!-- Most probable anomaly highlighting -->
  <div v-if="diagnosisReport['diagnosis_list'].length > 0" class="most-probable-anomaly" 
       style="margin-bottom: 20px; padding: 15px; background: #002E2E; border: 1px solid #0AFEFF; border-radius: 4px;">
    <h3 style="color: #0AFEFF; margin-bottom: 10px;">Most Probable Anomaly:</h3>
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <span style="font-size: 18px; font-weight: bold;">{{ diagnosisReport['diagnosis_list'][0].anomaly }}</span>
      <span style="background: #003f3f; padding: 5px 10px; border-radius: 4px; font-weight: bold;">
        Probability: {{ (diagnosisReport['diagnosis_list'][0].probability * 100 ).toFixed(4) }}%
      </span>
    </div>
  </div>

  <!-- Top 5 anomalies table -->
  <div style="margin-bottom: 20px;">
    <span style="margin-bottom:20px; color: #0AFEFF; background: #002E2E">Top 5 Most Likely Anomalies:</span>
    <div class="table-container" style="margin-top: 10px;">
      <table class="table is-bordered is-narrow is-hoverable is-fullwidth" 
             style="background: transparent; color: white;">
        <thead>
          <tr style="background: #002E2E;">
            <th style="color: #0AFEFF; width: 60%;">Anomaly</th>
            <th style="color: #0AFEFF; width: 40%;">Probability</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in diagnosisReport['diagnosis_list']" 
              style="background: rgba(0,46,46,0.7);">
            <td style="padding: 8px; vertical-align: middle;">{{ item.anomaly }}</td>
            <td style="padding: 8px;">
              <div class="progress" 
                   style="background: #001e1e; height: 24px; width: 100%; border-radius: 4px; overflow: hidden; position: relative;">
                <div :style="{
                  width: `${item.probability * 100}%`,
                  background: getProbabilityColor(item.probability),
                  height: '100%'
                }"></div>
                <div style="position: absolute; left: 0; right: 0; top: 0; bottom: 0; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; text-shadow: 0 0 2px black;">
                  {{ (item.probability * 100).toFixed(4) }}%
                </div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
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
    <SymptomSelectionDialog 
      :is-active="showSymptomDialog" 
      :symptoms="unconfirmedSymptoms"
      @proceed="handleSymptomSelection"
      @cancel="showSymptomDialog = false"
    />
  </div>
</template>

<script>

import {mapGetters} from 'vuex';
import { fetchPost } from '../scripts/fetch-helpers';
import SymptomSelectionDialog from './SymptomSelectionDialog.vue';


let loaderImage = require('../images/loader.svg');

export default {
  name: "AnomalyDiagnosisWindow",
  components: {
    SymptomSelectionDialog
  },

  data: function () {
    return {
      isLoading: false,
      isAnomalySelected: false,
      checked: [],
      explaining: false,
      allSelected: false,
      astrobeeStatus: null,
      statusInterval: null,
      instructionIdentifier: null,
      lastInstructionProcessed: false,
      userResponseListener: null,
      showSymptomDialog: false,
      symptomsToConfirm: [],
      currentSymptomIndex: -1,
      additionalEvidence: {},
      additionalEvidenceListener: null,
      yesNoQuestionListener: null,
      unconfirmedSymptoms: [],
      bestEvidence: null,
      currentTelemetryValues: {},
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
      selectedRightSymptoms: 'getSelectedRightSymptomsList',
      telemetryValues: 'getTelemetryValues',
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
    async startAstrobeeStatusPolling() {
      if (this.statusInterval) {
        clearInterval(this.statusInterval);
      }
      // Set up polling for status updates
      console.log('Polling Astrobee status...');
      try {
        const response = await fetchPost('/api/at/astrobee_status');
        // const response1 = await fetchPost('/api/at/get_pride_shared_variables');
        const instructionResponse = await fetchPost('/api/at/get_current_instruction');
        // const response2 = await fetchPost('/api/at/yesorno');
        if (response.ok) {
          const data = await response.json();
          this.astrobeeStatus = data.astrobee_status || "No status available";
        }
        console.log('Polling current instruction...', instructionResponse);
        // if (instructionResponse.ok) {
        //   const data1 = await instructionResponse.json();
        //   console.log("the current instruction", data1, data1["instruction_data"])
        //   console.log("the current instruction text", data1["instruction_data"]["text"])
        //   if (data1["instruction_data"] && data1["instruction_data"].text) {
        //     this.astrobeeStatus = data1["instruction_data"].text || "No status available";
        //   }
          
        // }

        if (instructionResponse.ok) {
          const data = await instructionResponse.json();
          console.log("Current instruction data:", data["instruction_data"]);
          
          if (data["instruction_data"] && data["instruction_data"].text) {
            const instructionData = data["instruction_data"];
            const oldStatus = this.astrobeeStatus;
            this.astrobeeStatus = instructionData.text || "No status available";
            console.log("Current instruction id:", this.instructionIdentifier, instructionData.instructionIdentifier, this.lastInstructionProcessed);
            if (instructionData.userResponseType && 
                instructionData.userResponseType.length > 0 && 
                instructionData.userResponseType[0] === "real" &&
                (this.instructionIdentifier != instructionData.instructionIdentifier || 
                !this.lastInstructionProcessed)) {

                  if (this.instructionIdentifier != instructionData.instructionIdentifier){
                    this.$store.commit('addDialoguePiece', {
                      "voice_message": `${instructionData.text} Please provide a numerical value.`,
                      "visual_message_type": ["text"],
                      "visual_message": [`${instructionData.text} Please provide a numerical value.`],
                      "writer": "daphne"
                    });
                  }
              
              // Update tracking variables to prevent duplicate prompts
              this.instructionIdentifier = instructionData.instructionIdentifier;
              console.log("Current instruction identifier is set:", this.instructionIdentifier, instructionData.instructionIdentifier);
              this.lastInstructionProcessed = false;
              
              // Send question to chat
              
              
              // Set up listener for next user response (if not already set)
              if (!this.userResponseListener) {
                this.setupUserResponseListener();
              }
            }
          }
        }
      } catch (error) {
        console.error('Error getting Astrobee status:', error);
      }
    },
    setupUserResponseListener() {
    // Set up store subscription to listen for user messages
    this.userResponseListener = this.$store.subscribe((mutation, state) => {
      if (mutation.type === 'addDialoguePiece') {
        const newMessage = mutation.payload;
        
        // Process only if we're waiting for a response and this is a user message
        if (!this.lastInstructionProcessed && 
            this.instructionIdentifier !== null &&
            newMessage.writer === 'user') {
          
          this.processUserResponse(newMessage.visual_message[0]);
        }
      }
    });
  },
  async processUserResponse(message) {
    try {
      // Try to parse the user's message as a number
      const userValue = parseFloat(message);
      
      if (!isNaN(userValue)) {
        // Valid number response
        console.log("Processing user response:", userValue);
        
        // Mark as processed to avoid duplicate handling
        this.lastInstructionProcessed = true;
        
        // Prepare and send user response to backend
        const reqData = new FormData();
        reqData.append('user_response', userValue.toString());
        reqData.append('instruction_id', this.instructionIdentifier);
        
        const response = await fetchPost('/api/at/user_response', reqData);
        
        if (response.ok) {
          console.log("User response sent successfully");
          
          // Confirm receipt to user
          this.$store.commit('addDialoguePiece', {
            "voice_message": `Thank you, I've recorded your value of ${userValue}.`,
            "visual_message_type": ["text"],
            "visual_message": [`Thank you, I've recorded your value of ${userValue}.`],
            "writer": "daphne"
          });
        } else {
          console.error("Failed to send user response");
        }
      } else {
        // Not a valid number
        this.$store.commit('addDialoguePiece', {
          "voice_message": "I need a numerical value. Please try again.",
          "visual_message_type": ["text"],
          "visual_message": ["I need a numerical value. Please try again."],
          "writer": "daphne"
        });
        
        // Keep the instruction as unprocessed so we'll try again
        this.lastInstructionProcessed = false;
      }
    } catch (error) {
      console.error('Error processing user response:', error);
    }
  },
    getProbabilityColor(probability) {
    // Return color based on probability value
    if (probability < 0.1) {
      return '#00cc00'; // green for very low probabilities
    } else if (probability < 0.3) {
      return '#ffcc00'; // yellow for medium probabilities
    } else {
      return '#ff3300'; // red for high probabilities
    }
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
      const diagnosisReport = this.$store.getters.getDiagnosisReport;
      this.unconfirmedSymptoms = diagnosisReport.hidden_components;
      this.bestEvidence = diagnosisReport.best_evidence;     
      this.currentTelemetryValues = diagnosisReport.current_telemetry_values

      // After getting diagnosis report, ask if user has additional evidence
      setTimeout(() => {
        this.$store.commit('addDialoguePiece', {
          "voice_message": "Would you like to provide additional evidence to improve the diagnosis?",
          "visual_message_type": ["text"],
          "visual_message": ["Would you like to provide additional evidence to improve the diagnosis?"],
          "writer": "daphne",
          // "options": ["Yes", "No"]
        });
        
        // Set up listener for user response
        this.setupAdditionalEvidenceListener();
      }, 1000);

      // Display Astrobee procedures in chat after diagnosis
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
        console.log("diagnosis report", diagnosisReport);
        console.log("diagnosis anomaly report", diagnosisReport['diagnosis_list'], diagnosisReport['diagnosis_list'][0]);
        
        // Set flag to display yes/no buttons for procedure selection
        console.log("Setting anomalous procedures detected flag to true");
        this.$store.commit('setAnomalousProceduresDetected', true);
      }
      this.isLoading = false;
    },
    showSymptomSelectionDialog() {
    this.showSymptomDialog = true;
  },
  handleSymptomSelection(selectedSymptoms) {
    this.showSymptomDialog = false;
    this.symptomsToConfirm = selectedSymptoms;
    this.currentSymptomIndex = -1;
    this.additionalEvidence = {}; // Reset evidence
    
    // Start asking about each symptom
    this.askNextSymptom();
  },
  askNextSymptom() {
  this.currentSymptomIndex++;
  
  if (this.currentSymptomIndex < this.symptomsToConfirm.length) {
    const currentSymptom = this.symptomsToConfirm[this.currentSymptomIndex];
    
    // Set up event listener for the response if not already set
    if (!this.yesNoQuestionListener) {
      this.$root.$on('symptomEvidenceResponse', this.handleSymptomEvidenceResponse);
      this.yesNoQuestionListener = true;
    }
    
    // Ask about this symptom with Yes/No buttons
    this.$store.commit('addDialoguePiece', {
      "voice_message": `Can you report the status of ${currentSymptom}?`,
      "visual_message_type": ["text"],
      "visual_message": [`Can you report the status of ${currentSymptom} ?`],
      "writer": "daphne",
      "options": ["Yes", "No"],
      "optionsCallbackEvent": "symptomEvidenceResponse"
    });
  } else {
    // All done, submit the evidence
    this.submitAdditionalEvidence();
  }
},

handleSymptomEvidenceResponse(response) {
  const currentSymptom = this.symptomsToConfirm[this.currentSymptomIndex];
  const isPresent = response === "Yes";
  
  // Record the evidence
  this.additionalEvidence[currentSymptom] = isPresent;
  
  // Ask about next symptom
  this.askNextSymptom();
},

  setupYesNoQuestionListener() {
    // Clean up previous listener if exists
    if (this.yesNoQuestionListener) {
      this.yesNoQuestionListener();
    }
    
    this.yesNoQuestionListener = this.$store.subscribe((mutation, state) => {
      if (mutation.type === 'addDialoguePiece') {
        const newMessage = mutation.payload;
        
        // Check if this is a user response to our yes/no question
        if (newMessage.writer === 'user' && 
            (newMessage.visual_message[0] === 'Yes' || newMessage.visual_message[0] === 'No')) {
          
          // Unsubscribe after processing
          this.yesNoQuestionListener();
          this.yesNoQuestionListener = null;
          
          const currentSymptom = this.symptomsToConfirm[this.currentSymptomIndex];
          const isPresent = newMessage.visual_message[0] === 'Yes';
          
          // Record the evidence
          this.additionalEvidence[currentSymptom] = isPresent;
          
          // Ask about next symptom
          this.askNextSymptom();
        }
      }
    });
  },

  async submitAdditionalEvidence() {
    try {
      this.isLoading = true;
      this.$store.commit('addDialoguePiece', {
        "voice_message": "Thank you for providing additional evidence. I'm updating the diagnosis...",
        "visual_message_type": ["text"],
        "visual_message": ["Thank you for providing additional evidence. I'm updating the diagnosis..."],
        "writer": "daphne"
      });
      
      // Convert evidence to API format
      const evidenceData = {
        additional_evidence: this.additionalEvidence,
        current_telemetry_values: this.currentTelemetryValues,
      };

      console.log("Submitting additional evidence:", this.additionalEvidence);
      
      // Make API call
      const response = await fetchPost('/api/at/update_diagnosis_with_evidence', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(evidenceData)
      });
      
      if (response.ok) {
        const updatedDiagnosis = await response.json();
        
        // Update diagnosis report in store
        this.$store.commit('mutateDiagnosisReport', updatedDiagnosis);
        
        this.$store.commit('addDialoguePiece', {
          "voice_message": "Diagnosis has been updated with your additional evidence!",
          "visual_message_type": ["text"],
          "visual_message": ["Diagnosis has been updated with your additional evidence!"],
          "writer": "daphne"
        });
      } else {
        throw new Error('Failed to update diagnosis');
      }
    } catch (error) {
      console.error('Error updating diagnosis with additional evidence:', error);
      this.$store.commit('addDialoguePiece', {
        "voice_message": "I couldn't update the diagnosis with your additional evidence. Please try again later.",
        "visual_message_type": ["text"],
        "visual_message": ["I couldn't update the diagnosis with your additional evidence. Please try again later."],
        "writer": "daphne"
      });
    } finally {
      this.isLoading = false;
    }
  },

  setupAdditionalEvidenceListener() {
  // Add event listener for options response
  if (!this.additionalEvidenceListener) {
    this.$root.$on('additionalEvidenceResponse', this.handleAdditionalEvidenceResponse);
    this.additionalEvidenceListener = true;
  }
  
  // Show question with Yes/No buttons
  this.$store.commit('addDialoguePiece', {
    "voice_message": "Would you like to provide additional evidence to improve the diagnosis?",
    "visual_message_type": ["text"],
    "visual_message": ["Would you like to provide additional evidence to improve the diagnosis?"],
    "writer": "daphne",
    "options": ["Yes", "No"],
    "optionsCallbackEvent": "additionalEvidenceResponse"
  });
},

handleAdditionalEvidenceResponse(response) {
  if (response === "Yes") {
    // Show symptom selection dialog
    this.showSymptomDialog = true;
  } else {
    // User doesn't want to provide additional evidence
    this.$store.commit('addDialoguePiece', {
      "voice_message": "Alright, I'll work with the current information.",
      "visual_message_type": ["text"],
      "visual_message": ["Alright, I'll work with the current information."],
      "writer": "daphne"
    });
  }
  
  // Clean up event listener
  this.$root.$off('additionalEvidenceResponse', this.handleAdditionalEvidenceResponse);
  this.additionalEvidenceListener = false;
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
    // this.startAstrobeeStatusPolling();
    // console.log("Astrobee status polling started");
    this.startAstrobeeStatusPolling();
    setInterval(this.startAstrobeeStatusPolling, 1200);
  },
  beforeDestroy() {
    // Clean up interval when component is destroyed
    if (this.statusInterval) {
      clearInterval(this.statusInterval);
    }
    if (this.userResponseListener) {
    this.userResponseListener(); // Unsubscribe from store
    }

  if (this.additionalEvidenceListener) {
    this.$root.$off('additionalEvidenceResponse', this.handleAdditionalEvidenceResponse);
  }
  
  if (this.yesNoQuestionListener) {
    this.$root.$off('symptomEvidenceResponse', this.handleSymptomEvidenceResponse);
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
