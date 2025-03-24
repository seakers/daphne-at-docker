<template>
    <div class="is-main" id="view-container">
        <div class="is-title">
            User: {{userName}}
            <span  style="float:right">Current stage: {{currentStage}}</span>
        </div>
        <div class="is-content">
            <div class="columns">
                <div class="column is-7">
                    <p class="is-mini-title" style="margin-bottom:20px">Daphne-AT display summary:</p>
                    <div class="content">
                        <p style="color: #0AFEFF">Selected symptoms:  Last Updated: {{lastUpdatedSymptomsTimestamp}}</p>
                        <ul>
                            <li style="color: white" v-for="symptom in selectedSymptomsList">{{ symptom["detection_text"]}}</li>
                        </ul>
                        <p style="color: #0AFEFF">Last provided diagnosis:  Last Updated: {{lastUpdatedDiagnosisTimestamp}}</p>
                        <ul>
                            <li style="color: white" v-for="anomaly in lastProvidedDiagnosis">
                                {{anomaly['name']}} (with a score of {{anomaly['score']}})
                            </li>
                        </ul>
                        <p style="color: #0AFEFF">Selected anomalies:  Last Updated: {{lastUpdatedAnomaliesTimestamp}}</p>
                        <ul>
                            <li style="color: white" v-for="anomaly in selectedAnomaliesList">{{ anomaly }}</li>
                        </ul>
                        <p style="color: #0AFEFF">Selected procedures:  Last Updated: {{lastUpdatedProceduresInfoTimestamp}}</p>
                        <ul>
                            <li style="color: white" v-for="(procedureDict, procedureName) in selectedProceduresInfo">
                                <p style="margin-bottom:2px">{{procedureName}}</p>
                                <p style="margin-left:20px">
                                    Current Step -->
                                    {{writeCurrentStep(procedureDict, procedureName)}}
                                </p>
                            </li>
                        </ul>
                    </div>
                </div>
                <div class="column is-5">
                    <p class="is-mini-title" style="margin-bottom:20px">Chat History:</p>
                    <div class="scrollable-mcccontainer">
                        <ChatArea :dialogue-history="dialogueHistory"></ChatArea>
                    </div>
                    <div class="is-content" style="float: right">
                        <div class="control">
                            <a class="button is-info" v-on:click.prevent="switchAlarms">
                                <span class="icon is-small">
                                    <i class="fas" v-bind:class="[ this.playAlarms ? 'fa-volume-up' : 'fa-volume-off' ]"></i>
                                </span>
                            </a>
                        </div>
                      <div class="control" style="margin-top: 10px">
                        <button type="submit" class="button is-primary" v-on:click="withoutDaphneSessionModal" style="background-color: blue">
                          Without Daphne Session
                        </button>
                      </div>
                        <div class="control">
                            <button type="submit" class="button is-primary" v-on:click="finishExperiment" style="background-color: red">
                                Send Survey Link
                            </button>
                        </div>
                        <div class="control">
                            <button type="submit" class="button is-primary" v-on:click="removeUser" style="background-color: red">
                                Remove User
                            </button>
                        </div>
                        <div class="control">
                            <button type="submit" class="button is-primary" v-on:click="forceFinishExperiment" style="background-color: red">
                                Force Logout User
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import App from "../App";
    import {fetchPost} from "../../scripts/fetch-helpers";
    import ChatArea from "../ChatArea";
    import {actions} from "../../store/modules/daphne-at";
    import {mapGetters} from "vuex";

    export default {
      name: "SubjectViewer",
      props: ["userName", "userId"],
      data() {
        return {
          currentStage: [],
          dialogueHistory: [],
          selectedSymptomsList: [],
          selectedAnomaliesList: [],
          selectedProceduresList: [],
          selectedProceduresInfo: {},
          lastProvidedDiagnosis: [],
          lastUpdatedSymptomsTimestamp: '',
          lastUpdatedAnomaliesTimestamp: '',
          lastUpdatedProceduresTimestamp: '',
          lastUpdatedProceduresInfoTimestamp: '',
          lastUpdatedDiagnosisTimestamp: '',
          playAlarms: false,
          isLoggedIn: false
        }
      },
      components: {
        ChatArea,
        App
      },
      methods: {
        async refreshUserInformation() {
          try {
            let reqData = new FormData();
            reqData.append('user_id', this.userId);

            let dataResponse = await fetchPost(API_URL + 'experiment-at/get-state', reqData);
            if (dataResponse.ok) {
              // Add the new functionality
              let state = await dataResponse.json();

              try {
                eval(state["daphneat"]["isLoggedIn"]);
                if (state["daphneat"]["isLoggedIn"] && state !== 'None') {
                  this.currentStage = state["experiment"]["experimentStage"];
                  this.dialogueHistory = state["daphne"]["dialogueHistory"];
                  this.selectedSymptomsList = state["daphneat"]["selectedSymptomsList"];
                  this.selectedAnomaliesList = state["daphneat"]["selectedAnomaliesList"];
                  this.selectedProceduresList = state["daphneat"]["selectedProceduresList"];
                  this.selectedProceduresInfo = state["daphneat"]["selectedProceduresInfo"];
                  this.lastProvidedDiagnosis = state["daphneat"]["diagnosisReport"]["diagnosis_list"];
                  this.lastUpdatedAnomaliesTimestamp = state["daphneat"]["lastUpdatedAnomaliesTimestamp"],
                  this.lastUpdatedSymptomsTimestamp = state["daphneat"]["lastUpdatedSymptomsTimestamp"],
                  this.lastUpdatedProceduresTimestamp = state["daphneat"]["lastUpdatedProceduresTimestamp"],
                  this.lastUpdatedProceduresInfoTimestamp = state["daphneat"]["lastUpdatedProceduresInfoTimestamp"],
                  this.lastUpdatedDiagnosisTimestamp = state["daphneat"]["lastUpdatedDiagnosisTimestamp"]
                  
                  // try{
                  //   let date = new Date(timestamp);
                  //   // Format the date and time in a readable way
                  //   let formattedDate = date.toLocaleString('en-US', {
                  //     year: 'numeric',
                  //     month: 'long',  // e.g., October
                  //     day: 'numeric', // e.g., 15
                  //     hour: 'numeric',
                  //     minute: 'numeric',
                  //     second: 'numeric',
                  //     hour12: true    // Use 12-hour format with AM/PM
                  //   });
                  //   this.lastUpdatedTimestamp = formattedDate;
                  // }
                  // catch (e) {
                  //   this.lastUpdatedTimestamp = timestamp;
                  // }
                } else {
                  this.currentStage = 'UNKNOWN';
                  this.dialogueHistory = [];
                  this.selectedSymptomsList = [];
                  this.selectedAnomaliesList = [];
                  this.selectedProceduresList = [];
                  this.selectedProceduresInfo = [];
                  this.lastUpdatedAnomaliesTimestamp = '';
                  this.lastUpdatedSymptomsTimestamp = '';
                  this.lastUpdatedProceduresTimestamp = '';
                  this.lastUpdatedProceduresInfoTimestamp = '';
                  this.lastUpdatedDiagnosisTimestamp = '';
                  
                }
              } catch (e) {
                this.currentStage = 'UNKNOWN';
                this.dialogueHistory = [];
                this.selectedSymptomsList = [];
                this.selectedAnomaliesList = [];
                this.selectedProceduresList = [];
                this.selectedProceduresInfo = [];
                this.lastUpdatedAnomaliesTimestamp = '';
                this.lastUpdatedSymptomsTimestamp = '';
                this.lastUpdatedProceduresTimestamp = '';
                this.lastUpdatedProceduresInfoTimestamp = '';
                this.lastUpdatedDiagnosisTimestamp = '';
              }
            } else {
              console.error('Error retrieving user state.');
              this.currentStage = 'UNKNOWN';
              this.dialogueHistory = [];
              this.selectedSymptomsList = [];
              this.selectedAnomaliesList = [];
              this.selectedProceduresList = [];
              this.selectedProceduresInfo = [];
              this.lastUpdatedAnomaliesTimestamp = '';
              this.lastUpdatedSymptomsTimestamp = '';
              this.lastUpdatedProceduresTimestamp = '';
              this.lastUpdatedProceduresInfoTimestamp = '';
              this.lastUpdatedDiagnosisTimestamp = '';
            }
          } catch (e) {
            console.error('Networking error:', e);
            this.currentStage = 'UNKNOWN';
            this.dialogueHistory = [];
            this.selectedSymptomsList = [];
            this.selectedAnomaliesList = [];
            this.selectedProceduresList = [];
            this.selectedProceduresInfo = [];
            this.lastUpdatedAnomaliesTimestamp = '';
            this.lastUpdatedSymptomsTimestamp = '';
            this.lastUpdatedProceduresTimestamp = '';
            this.lastUpdatedProceduresInfoTimestamp = '';
            this.lastUpdatedDiagnosisTimestamp = '';
          }
        },
        async withoutDaphneSessionModal() {
          let reqData = new FormData();
          reqData.append('user_id', this.userId);
          await fetchPost(API_URL + 'experiment-at/without-daphne-session', reqData);
        },
        async finishExperiment() {
          console.log('FINISH EXPERIMENT');
          let reqData = new FormData();
          reqData.append('user_id', this.userId);
          await fetchPost(API_URL + 'experiment-at/finish-experiment-from-mcc', reqData);
          this.$emit('remove-shown', this.userId);
        },
        removeUser() {
          console.log('Remove person');
          this.$emit('remove-shown', this.userId);
        },
        async forceFinishExperiment() {
          console.log('FORCE FINISH EXPERIMENT');
          let reqData = new FormData();
          reqData.append('user_id', this.userId);
          await fetchPost(API_URL + 'experiment-at/force-finish-experiment-from-mcc', reqData);
          this.$emit('remove-shown', this.userId);
        },
        async switchAlarms() {
          console.log("Alarm was on " + this.playAlarms);
          this.playAlarms = !this.playAlarms;
          console.log("Alarm is now on " + this.playAlarms)
          let reqData = new FormData();
          reqData.append('user_id', this.userId);
          await fetchPost(API_URL + 'experiment-at/turn-off-alarms', reqData);
        },
        writeCurrentStep(procedureDict, procedureName) {
          let stepsList = procedureDict['checkableStepsList'];
          let currentStepIndex = procedureDict['procedureCurrentStep'];
          let totalSteps = procedureDict['checkableSteps'];

          if (currentStepIndex === totalSteps) {
            let message = 'COMPLETED (' + currentStepIndex + ' out of ' + totalSteps + ')';
            return message
          } else {
            try {
              let action = stepsList[currentStepIndex]['action'];
              let stepNumber = stepsList[currentStepIndex]['label'];
              let message = stepNumber + " - " + action + ' (' + currentStepIndex + ' out of ' + totalSteps + ')';
              return message
            } catch (err) {
              console.log('ERROR retrieving the procedure current step action.');
              return 'ERROR retrieving the procedure current step information.'
            }
          }
        },
      },
        mounted() {
          this.refreshUserInformation();
          setInterval(this.refreshUserInformation, 1200);

        }
      }
</script>

<style scoped>
.red-border {
    border: 5px red;
}
</style>
