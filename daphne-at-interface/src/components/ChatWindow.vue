<template>
  <div class="chat-container box is-main" style="margin: 5px; width: 24%; height: 92%">
    <div class="is-title " style="text-align: center">
      Chatbot
      <u v-on:click="minimizeChat" class="tutorialLink">Hide</u>
    </div>
    <div style="height: 85%">
      <section class="chat-area" style="height: 85%" ref="chatArea">
        <div v-for="piece in dialogueHistory" class="chat-message content"
             :class="{ 'chat-message-user': piece.writer === 'user', 'chat-message-daphne': piece.writer === 'daphne' }">
          <component v-for="(response, index) in piece['visual_message']"
                     v-bind:is="responseTypes[piece['visual_message_type'][index]]" :response="formatText(response)"
                     :key="index"></component>
        </div>
        <img src="assets/img/loader.svg" style="display: block; margin: auto;" align="center" height="64" width="64"
             v-if="isLoading" alt="Loading spinner">
      </section>
    </div>

    <div>
      <div class="sticky-textbox" style="position: absolute" width="24%">
        <div id="siri-container" style="height: 30px;"></div>
        <!-- <div v-if="anomalousSymptomsDetected" style="text-align: center;">
          <button class="button theme-buttons" @click="handleAnomalyResponse('yes')">Yes</button>
          <button class="button theme-buttons" @click="handleAnomalyResponse('no')">No</button>
        </div>
        <div v-else> -->

        <div v-if="anomalousProceduresDetected" style="text-align: center;">
          <div class="field">
            <div class="control">
              <div class="select" style="width: 100%; margin-bottom: 10px;">
                <select v-model="selectedProcedure" style="width: 100%; background-color: var(--color__bg); border-color: var(--color__shadow); color: var(--color__text);">
                  <option value="" disabled>Select a procedure</option>
                  <option v-for="procedure in diagnosisReport.astrobee_procedure_list" :value="procedure">{{ procedure }}</option>
                </select>
              </div>
            </div>
          </div>
          <button class="button theme-buttons" @click="handleProcedureResponse('yes')" :disabled="!selectedProcedure">Yes</button>
          <button class="button theme-buttons" @click="handleProcedureResponse('no')">No</button>
        </div>
        <div class="field has-addons is-fullwidth">
          <div class="control is-expanded">
            <input class="input" style="background-color: var(--color__bg); border-color: var(--color__shadow); color: var(--color__text); " type="text"
                   name="command" placeholder="Ask me something" v-model="command" v-on:keyup.enter="sendCommand">
          <!-- </div> -->
        </div>
        </div>

        <div style="width: 100%; text-align: center">
          <button class="button theme-buttons" style="width: 10%;"
                  v-on:click.prevent="switchVoice">
            <i class="fas" v-bind:class="[ this.isUnmute ? 'fa-volume-up' : 'fa-volume-off' ]"></i>
          </button>
          <button class="button theme-buttons" style="width: 55%;"
                  id="send_command" v-on:click.prevent="sendCommand">Send
          </button>
          <button class="button theme-buttons" style="width: 20%;"
                  id="clear_history" v-on:click.prevent="clearHistory">Clear
          </button>
          <button class="button theme-buttons" style="width: 10%;"
                  v-on:click.prevent="chatTutorial">?
          </button>
        </div>
        <div style="text-align: center; font-weight: bold">
          <a href="/question_cheatsheet.html" target="_blank">Help</a>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import * as _ from 'lodash-es';
import TextResponse from './TextResponse';
import ListResponse from './ListResponse';
import {mapMutations, mapState} from "vuex";
import {mapGetters} from 'vuex';
import SiriWave from "siriwave";
import daphne_awake from '../sounds/awake.mp3'
import daphne_asleep from '../sounds/asleep.mp3'
import {commit} from "lodash-es";
let loaderImage = require('../images/loader.svg');
let responsiveVoice = window.responsiveVoice;
import {fetchGet, fetchPost} from "../scripts/fetch-helpers";

export default {
  name: "ChatWindow",
  components: {
    // QuestionBar,
    TextResponse,
    ListResponse,
  },
  data() {
    return {
      responseTypes: {
        text: 'TextResponse',
        list: 'ListResponse',
        multilist: 'MultiListResponse',
        timeline_plot: 'TimelineResponse',
        active_message: 'ActiveMessage',
      },
    }
  },
  computed: {
    ...mapState({
      dialogueHistory: state => state.daphne.dialogueHistory,
      isLoading: state => state.daphne.isLoading,
      isSpeaking: state => state.daphne.isSpeaking,
      // anomalousSymptomsDetected: state => state.daphne.anomalousSymptomsDetected,
      anomalousProceduresDetected: state => state.daphne.anomalousProceduresDetected,
    }),
    ...mapGetters([
      'getResponse'
    ]),
    ...mapGetters({
      symptomsList: 'getSymptomsList',
      isListening: 'getIsListening',
      isSpeaking: 'getIsSpeaking',
      isUnmute: 'getIsUnmute',
      daphneVoice: 'getDaphneVoice',
      diagnosisReport: 'getDiagnosisReport',
    }),
    selectedProcedure: {
      get() {
        return this.$store.state.daphne.selectedProcedure;
      },
      set(newValue) {
        this.$store.commit('setSelectedProcedure', newValue);
      }
    },
    command: {
      get() {
        return this.$store.state.daphne.command;
      },
      set(newCommand) {
        this.$store.commit('setCommand', newCommand);
      }
    },
    isUnmute: {
      get() {
        return this.$store.state.daphne.isUnmute;
      },
      set(newValue) {
        this.$store.commit('setIsUnmute', newValue);
      },
    },
    daphneVoice: {
      get() {
        return this.$store.state.daphne.daphneVoice;
      },
      set(newValue) {
        this.$store.commit('setDaphneVoice', newValue);
      },
    }
  },
  methods: {
    scrollToBottom: function () {
      let container = this.$el.querySelector(".chat-area");
      container.scrollTop = container.scrollHeight;
    },
    clearHistory(event) {
      this.$store.dispatch('clearHistory');
    },
    sendCommand(event) {
      if (this.command === 'stop') {
        responsiveVoice.cancel();
      } else {
        this.$store.dispatch('executeCommand');
      }
    },
    switchVoice() {
      this.isUnmute = !this.isUnmute;
      this.$store.commit("setIsUnmute", this.isUnmute);
    },
    chatTutorial(event) {
      this.$root.$emit('chatTutorialIndividual');
    },
    minimizeChat(event) {
      this.$store.commit('mutateIsChatVisible');
    },

    async handleProcedureResponse(response) {
      if (response === 'yes' && this.selectedProcedure) {
        // Make API call to start the procedure
        try {
          let reqData = new FormData();
          reqData.append('procedureID', this.selectedProcedure.staticProcedureID);
          let response = await fetchPost('/api/at/start_astrobee_procedure', reqData);
          
          if (response.ok) {
            const data = await response.json();
            console.log("Procedure started successfully:", data);
            // Add response to chat
            this.$store.commit('addDialoguePiece', {
              "voice_message": `I've started the ${this.selectedProcedure.title} procedure successfully.`,
              "visual_message_type": ["text"],
              "visual_message": [`I've started the ${this.selectedProcedure.title} procedure successfully. ${data.status}`],
              "writer": "daphne"
            });
          } else {
            this.$store.commit('addDialoguePiece', {
              "voice_message": `I encountered an error while trying to start the procedure.`,
              "visual_message_type": ["text"],
              "visual_message": ["I encountered an error while trying to start the procedure."],
              "writer": "daphne"
            });
          }
        } catch (error) {
          console.error('Error starting procedure:', error);
        }
      } else if (response === 'no') {
        this.$store.commit('addDialoguePiece', {
          "voice_message": "Let me know if you change your mind or if you need anything else.",
          "visual_message_type": ["text"],
          "visual_message": ["Let me know if you change your mind or if you need anything else."],
          "writer": "daphne"
        });
      }
      
      // Reset the state
      this.$store.commit('setAnomalousProceduresDetected', false);
      this.$store.commit('setSelectedProcedure', null);
    },
    // handleAnomalyResponse(response) {
    //   // Handle the "Yes" action
    //   if(response==='yes'){
    //     let newSelectedVariables = [];
    //     let symptomsList = this.symptomsList;
    //     for (let i = 0; i < symptomsList.length; i++) {
    //       newSelectedVariables[i] = symptomsList[i]['display_name'];
    //     }
        
    //     this.$store.dispatch('updateSelectedVariables', newSelectedVariables);
    //   }
    //   this.$store.commit('setAnomalousSymptomsDetected', false);
    // },
    formatText(response) {
      // Replace newline characters with <br> tags
      return response.replace(/\n/g, '<br>');
    },
  },
  watch: {
    dialogueHistory: function (val, oldVal) {
      console.log("dialogue history changed");
      this.$nextTick(() => {
        this.scrollToBottom();
      });
      if (this.isUnmute) {
        if (val.length > 0) {
          let lastMessage = val[val.length - 1];
          console.log("lastmessage",lastMessage);
          if (lastMessage['writer'] === "daphne") {
            let voiceAnswer = lastMessage['voice_message'];
            responsiveVoice.speak(voiceAnswer, this.daphneVoice, {rate: 1.05}, {volume: 1});
          }
        }
      }
    },
    isLoading: function (val, oldVal) {
      if (val === true) {
        _.delay(() => {
          this.scrollToBottom();
        }, 500);
      }
    },
    isSpeaking: async function (val, oldVal) {
      if (val) {
        this.siriWave = new SiriWave({
          container: document.getElementById('siri-container'),
          cover: true,
          style: "ios9",
          curveDefinition: [
            {color: "255,255,255", supportLine: true},
            {color: "15, 82, 169"}, // blue
            {color: "173, 57, 76"}, // red
            {color: "48, 220, 155"}, // green
          ]
        });
        this.siriWave.start();
        let audio = new Audio(daphne_awake);
        await audio.play();
        this.siriWave.setAmplitude(5);
      } else {
        let audio = new Audio(daphne_asleep);
        await audio.play();
        this.siriWave.stop();
        this.siriWave.dispose();
      }
    }
  }
}
</script>

<style lang="scss">
@import "../../node_modules/bulma/sass/utilities/initial-variables";

.chat-container {
  position: fixed;
  display: flex;
  flex-direction: column;
  padding-bottom: 1em;
}

.chat-area {
  width: 100%;
  overflow: auto;
  flex-grow: 1;
  margin: 0.5em;
}

.chat-message {
  width: 100%;
  border-radius: 10px;
  padding: .8em;
  margin-bottom: .8em;
  font-size: 15px;
}

.chat-message-daphne {
  float: left;
  background: #303030;
  color: $white;
  width: 80%;
}

.chat-message-user {
  float: right;
  margin-right: 15px;
  color: $white;
  background: $cyan;
  width: 80%;
}

.sticky-textbox {
  bottom: 0;
  padding: 0.5em;
  width: 100%;
}

::placeholder {
  color: gray !important;
}
</style>
