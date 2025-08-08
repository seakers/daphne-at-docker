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
          <div class="column is-7" style="margin: 0px; padding: 0px">
            <ul>
              <li class="hover" v-on:click="deselectSymptom(symptom)" v-for="symptom in selectedSymptomsList"
                  style="cursor: pointer">
                {{ symptom['detection_text'] }}
              </li>
            </ul>
          </div>
          <div class="column is-5" style="margin: 0px; padding: 0px">
            <div class="button-row" style="display: flex; gap: 10px; margin: 0px; padding: 0px;">
              <button class="button theme-buttons"
                      style="flex: 1; border-color: #0AFEFF; color: #0AFEFF; background: #002E2E"
                      id="request_diagnosis" v-on:click.prevent="requestKGDiagnosis">KG
              </button>
              <button class="button theme-buttons"
                      style="flex: 1; border-color: #0AFEFF; color: #0AFEFF; background: #002E2E"
                      id="request_diagnosis" v-on:click.prevent="requestDiagnosis">Bayesian
              </button>
              <button class="button theme-buttons"
                      style="flex: 1; border-color: #0AFEFF; color: #0AFEFF; background: #002E2E"
                      id="request_diagnosis" v-on:click.prevent="requestPhysicsDiagnosis">Physics
              </button>
              <button class="button theme-buttons"
                      style="flex: 1; border-color: #0AFEFF; color: #0AFEFF; background: #002E2E"
                      id="clear_symptoms" v-on:click.prevent="clearSymptoms">Clear
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="horizontal-divider" style="margin-top: 10px; margin-bottom: 10px"></div>

        <!-- ################### KG Diagnosis report hypothesis list ########################-->
      <div class="is-content">
        <!-- Simple, independent tab UI -->
        <div class="tabs-container" style="margin-bottom: 20px;">
          <div class="tabs is-boxed tab-wrapper">
            <ul class="draggable-tabs">
              <li v-for="(tab, index) in simpleTabs"
                  :key="index"
                  :class="{ 'is-active': activeSimpleTab === index }">
                <a @click="activeSimpleTab = index">
                  <span>{{ tab.label }}</span>
                  <button class="tab-close" @click.stop="closeSimpleTab(index)">×</button>
                </a>
              </li>
            </ul>
          </div>
        </div>
        <div v-if="simpleTabs[activeSimpleTab]">
          <div class="physics-diagnosis-report">
            <!-- Title Section -->
            <div class="physics-title-section">
              <div>
                <span style="color:#0AFEFF;">Most Probable Anomaly:</span>
                <span style="font-weight:bold; color:white; margin-left:10px;">{{ physicsDiagnosisData.mostProbableAnomaly }}</span>
              </div>
              <div style="margin-left:auto; color:#0AFEFF;">
                Probability: <span style="font-weight:bold; color:white;">{{ physicsDiagnosisData.probability }}</span>
              </div>
            </div>
            <!-- Content Section -->
            <div class="physics-content-section">
              <!-- Left: Table -->
              <div class="physics-table-section">
                <div style="color:#0AFEFF; margin-bottom:8px;">Top 5 Component Anomalies:</div>
                <table class="physics-table">
                  <thead>
                    <tr>
                      <th>Component Anomaly</th>
                      <th>Similarity Score</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="anomaly in physicsDiagnosisData.componentAnomalies" 
                        :key="anomaly.name"
                        :style="anomaly.isHighlighted ? 'background:#c0392b; color:white; font-weight:bold;' : ''">
                      <td>{{ anomaly.name }}</td>
                      <td>{{ anomaly.score }}</td>
                    </tr>
                  </tbody>
                </table>
                
                <!-- Explanation Button -->
                <div style="text-align: center; margin-top: 15px;">
                  <button class="button theme-buttons"
                          style="border-color: #0AFEFF; color: #0AFEFF; background: #002E2E; padding: 8px 16px; font-size: 14px;"
                          v-on:click.prevent="togglePhysicsExplanation">
                    {{ showPhysicsExplanation ? 'Hide Explanation' : 'Explanation' }}
                  </button>
                </div>
              </div>
              <!-- Right: System Configuration Image -->
              <div class="physics-image-section">
                <img src="assets/img/CDRA.png" alt="System Configuration" style="max-width:100%; border-radius:6px;"/>
              </div>
            </div>
            
            <!-- Divider -->
            <div v-if="showPhysicsExplanation" class="horizontal-divider" style="margin-top: 20px; margin-bottom: 20px; height: 1px; background: #0AFEFF; opacity: 0.3;"></div>
            
            <!-- Telemetry Comparison Graph -->
            <div v-if="showPhysicsExplanation" class="physics-explanation-section" style="margin-top: 20px; text-align: center;">
              <!-- Error Display -->
              <div v-if="physicsDiagnosisError" style="background: #c0392b; color: white; padding: 15px; border-radius: 6px; margin-bottom: 15px;">
                <strong>Physics Diagnosis Error:</strong> {{ physicsDiagnosisError }}
              </div>
              
              <!-- Graph Display -->
              <div v-if="!physicsDiagnosisError">
                <div style="color:#0AFEFF; margin-bottom:15px; font-size: 16px; font-weight: bold;">
                  Telemetry Trend Comparison
                </div>
                <div class="telemetry-graph-container" style="background: #001e1e; border-radius: 6px; padding: 20px; min-height: 300px; display: inline-block; max-width: 90%;">
                  <canvas ref="telemetryGraph" width="800" height="300"></canvas>
                </div>
              </div>
            </div>
          </div>
        </div>
        <button class="button" @click="addSimpleTab('New Tab', 'This is a new independent tab.')" style="margin-top: 10px;">
          Add Simple Tab
        </button>

        <div v-if="diagnosisReport.length === 0">
          <img v-if="isLoading"
               src="assets/img/loader.svg"
               style="display: block; margin: auto;"
               height="40" width="40"
               alt="Loading spinner">
          <p v-else>No diagnosis reports requested.</p>
        </div>

        <!-- ################### KG Diagnosis report hypothesis list ########################-->
        <div v-else>
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
            <p v-if="showAlert" style="color: red">Please select an anomaly to investigate.</p>
            <button class="button" type="submit" onclick="errorMessage()"
                    style="width: 30%; border-color: #0AFEFF; color: #0AFEFF; background: #002E2E;"
                    v-on:click.prevent="showExplanations">Show explanations
            </button>
          </div>
        </div>

        <!-- ################### Physics-based Diagnosis report ########################-->


        <!-- ################### Bayesian Diagnosis report previous ########################-->

        <!-- <div v-else> -->
          <!-- Most probable anomaly highlighting -->
          <!-- <div v-if="diagnosisReport['diagnosis_list'].length > 0" class="most-probable-anomaly" 
              style="margin-bottom: 20px; padding: 15px; background: #002E2E; border: 1px solid #0AFEFF; border-radius: 4px;">
            <h3 style="color: #0AFEFF; margin-bottom: 10px;">Most Probable Anomaly:</h3>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span style="font-size: 18px; font-weight: bold;">{{ diagnosisReport['diagnosis_list'][0].anomaly }}</span>
              <span style="background: #003f3f; padding: 5px 10px; border-radius: 4px; font-weight: bold;">
                Probability: {{ (diagnosisReport['diagnosis_list'][0].probability * 100 ).toFixed(4) }}%
              </span>
            </div>
          </div> -->

          <!-- Top 5 anomalies table -->
          <!-- <div style="margin-bottom: 20px;">
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
        </div> -->
              
        <!-- ################### Bayesian Diagnosis report interactive ########################-->

        <div v-else>
          <!-- Diagnosis tabs -->
          <div class="tabs-container">
            <button class="tab-scroll-button left" @click="scrollTabs('left')" v-show="showLeftScroll">
              <i class="fas fa-chevron-left"></i>
            </button>
          
            <div class="tabs is-boxed tab-wrapper" ref="tabsContainer">
              <ul class="draggable-tabs">
                <li :class="{'is-active': activeDiagnosticTab === diagnosticHistory.length}">
                  <a @click="activeDiagnosticTab = diagnosticHistory.length">
                    <span>Current Diagnosis</span>
                  </a>
                </li>
                <li v-for="(diag, index) in diagnosticHistory" 
                    :key="index"
                    :class="{'is-active': activeDiagnosticTab === index}"
                    :draggable="true"
                    @dragstart="dragStart($event, index)"
                    @dragover="dragOver($event)"
                    @dragend="dragEnd($event)"
                    @drop="drop($event, index)">
                  <a @click="activeDiagnosticTab = index" :title="getFullEvidenceLabel(diag)">
                    <span class="tab-evidence">
                      <!-- {{ getEvidenceLabel(diag) }} -->
                      <i v-if="diag.is_hypothetical" class="fas fa-question-circle" style="margin-right: 5px;" title="Hypothetical scenario"></i>
                      {{ diag.is_hypothetical ? 'What if: ' + getEvidenceLabel(diag) : getEvidenceLabel(diag) }}
                    </span>
                    <button class="tab-close" @click.stop="closeTab(index)">×</button>
                  </a>
                </li>
              </ul>
            </div>
          
            <button class="tab-scroll-button right" @click="scrollTabs('right')" v-show="showRightScroll">
              <i class="fas fa-chevron-right"></i>
            </button>
          
            <!-- Undo tab close button -->
            <button 
              class="tab-undo-button" 
              @click="undoCloseTab" 
              v-show="closedTabs.length > 0" 
              title="Undo close tab">
              <i class="fas fa-undo"></i>
            </button>
          </div>
          
          <!-- Current diagnosis content -->
          <div v-if="activeDiagnosticTab === diagnosticHistory.length">
            <!-- Display current diagnosis from store -->
            <div v-if="$store.getters.getDiagnosisReport && $store.getters.getDiagnosisReport.diagnosis_list && $store.getters.getDiagnosisReport.diagnosis_list.length > 0">
              <div class="most-probable-anomaly" style="margin-bottom: 20px; padding: 15px; background: #002E2E; border: 1px solid #0AFEFF; border-radius: 4px;">
                <h3 style="color: #0AFEFF; margin-bottom: 10px;">Most Probable Anomaly:</h3>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                  <span style="font-size: 18px; font-weight: bold;">{{ $store.getters.getDiagnosisReport.diagnosis_list[0].anomaly }}</span>
                  <span style="background: #003f3f; padding: 5px 10px; border-radius: 4px; font-weight: bold;">
                    Probability: {{ ($store.getters.getDiagnosisReport.diagnosis_list[0].probability * 100).toFixed(2) }}%
                  </span>
                </div>
                
                <!-- Added evidence display -->
                <div v-if="Object.keys(additionalEvidence).length > 0" 
                    style="margin-top: 10px; padding: 8px; background: rgba(10, 254, 255, 0.1); border-radius: 4px;">
                  <h4 style="color: #0AFEFF; margin-bottom: 5px; font-size: 14px;">Evidence Considered:</h4>
                  <ul style="list-style-type: disc; margin-left: 20px;">
                    <li v-for="(value, key) in additionalEvidence" :key="key" style="margin-bottom: 3px;">
                      {{ key }}: {{ formatEvidenceValue(value) }}
                    </li>
                  </ul>
                </div>
              </div>
              
              <!-- Top 5 anomalies with progress bar - Current diagnosis -->
              <div style="margin-bottom: 20px;">
                <span style="margin-bottom:20px; color: #0AFEFF; background: #002E2E">Top 5 Most Likely Anomalies:</span>
                <div class="table-container" style="margin-top: 10px;">
                  <table class="table is-bordered is-narrow is-hoverable is-fullwidth" 
                        style="background: transparent; color: white;">
                    <thead>
                      <tr style="background: #002E2E;">
                        <th style="color: #0AFEFF; width: 60%;">Anomaly (Select an anomaly to open the corresponding procedure)</th>
                        <th style="color: #0AFEFF; width: 40%;">Probability</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="item in $store.getters.getDiagnosisReport.diagnosis_list.slice(0, 5)" 
                          style="background: rgba(0,46,46,0.7);">
                        <td v-on:click.prevent="selectAnomaly(item.anomaly)" style="padding: 8px; cursor: pointer; vertical-align: middle;">{{ item.anomaly }}</td>
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
            <div v-else class="notification is-warning">
              No diagnosis data available. Select symptoms and request a diagnosis.
            </div>
          </div>
          
          <!-- Historical diagnoses -->
          <div v-else>
            <!-- Display historical diagnosis from history array -->
            <div v-if="diagnosticHistory[activeDiagnosticTab] && diagnosticHistory[activeDiagnosticTab].diagnosis_list && diagnosticHistory[activeDiagnosticTab].diagnosis_list.length > 0">
              <div class="most-probable-anomaly" style="margin-bottom: 20px; padding: 15px; background: #002E2E; border: 1px solid #0AFEFF; border-radius: 4px;">
                <h3 style="color: #0AFEFF; margin-bottom: 10px;">Most Probable Anomaly (Previous #{{activeDiagnosticTab + 1}}):</h3>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                  <span style="font-size: 18px; font-weight: bold;">{{ diagnosticHistory[activeDiagnosticTab].diagnosis_list[0].anomaly }}</span>
                  <span style="background: #003f3f; padding: 5px 10px; border-radius: 4px; font-weight: bold;">
                    Probability: {{ (diagnosticHistory[activeDiagnosticTab].diagnosis_list[0].probability * 100).toFixed(2) }}%
                  </span>
                </div>

                <div v-if="diagnosticHistory[activeDiagnosticTab] && 
                  diagnosticHistory[activeDiagnosticTab].additional_evidence && 
                  Object.keys(diagnosticHistory[activeDiagnosticTab].additional_evidence || {}).length > 0" 
                      style="margin-top: 10px; padding: 8px; background: rgba(10, 254, 255, 0.1); border-radius: 4px;">
                    <h4 style="color: #0AFEFF; margin-bottom: 5px; font-size: 14px;">Evidence Considered:</h4>
                    <ul style="list-style-type: disc; margin-left: 20px;">
                      <li v-for="(value, key) in diagnosticHistory[activeDiagnosticTab].additional_evidence || {}" 
                          :key="key" 
                          style="margin-bottom: 3px;">
                        {{ key }}: {{ formatEvidenceValue(value) }}
                      </li>
                    </ul>
                  </div>
              </div>
              
              <!-- Top 5 anomalies with progress bar - Historical diagnosis -->
              <div style="margin-bottom: 20px;">
                <span style="margin-bottom:20px; color: #0AFEFF; background: #002E2E">Top 5 Most Likely Anomalies (Previous #{{activeDiagnosticTab + 1}}):</span>
                <div class="table-container" style="margin-top: 10px;">
                  <table class="table is-bordered is-narrow is-hoverable is-fullwidth" 
                        style="background: transparent; color: white;">
                    <thead>
                      <tr style="background: #002E2E;">
                        <th style="color: #0AFEFF; width: 60%;">Anomaly (Select an anomaly to open the corresponding procedure)</th>
                        <th style="color: #0AFEFF; width: 40%;">Probability</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="item in diagnosticHistory[activeDiagnosticTab].diagnosis_list.slice(0, 5)" 
                          style="background: rgba(0,46,46,0.7);">
                        <td v-on:click.prevent="selectAnomaly(item.anomaly)" style="padding: 8px; cursor: pointer; vertical-align: middle;">{{ item.anomaly }}</td>
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
          
          <!-- Add a clear button at the bottom if needed -->
          <div style="text-align: center; margin-top: 20px;">
            <button @click="clearSymptoms" class="button is-danger">
              Clear All Symptoms & Diagnoses
            </button>
          </div>
        </div>

      </div>

      <div class="horizontal-divider" style="margin-top: 10px; margin-bottom: 10px"></div>

      <!-- ################### Robot Procedure Report ########################-->
      <div class="is-content">
        <div class="is-mini-title" style="margin-bottom:5px; font-size: 22px">
          Robot Status
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

      <!-- ################### KG Diagnosis report hypothesis comparison table ########################-->

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
    <!---->
   
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
let CDRAImage = require('../images/CDRA.png');

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
      showAlert: false,
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
      diagnosticHistory: [],
      activeDiagnosticTab: 0,
      bestEvidenceListener: null,
      showLeftScroll: false,
      showRightScroll: false,
      draggedTabIndex: null,
      draggedTab: null,
      dragOverIndex: null,
      closedTabs: [], // Array to store recently closed tabs
      showPhysicsTab: false,
      simpleTabs: [],
      activeSimpleTab: 0,
      showPhysicsExplanation: false,
      physicsDiagnosisError: null,
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
      physicsDiagnosisData: 'getPhysicsDiagnosisData',
      telemetryGraphData: 'getTelemetryGraphData',
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

    getEvidenceLabel(diagnosisData) {
      // For debugging
      if (diagnosisData.is_hypothetical && diagnosisData.hypothetical_evidence) {
        let str = "";
        for (const [key, value] of Object.entries(diagnosisData.hypothetical_evidence)) {
          str += `${key}: ${this.formatEvidenceValue(value)}, `;
        }
        // Remove the last comma and space
        return str.slice(0, -2);
      }
  
      // Existing logic for regular evidence
      if (diagnosisData.additional_evidence && Object.keys(diagnosisData.additional_evidence).length > 0) {
        let str = "";
        for (const [key, value] of Object.entries(diagnosisData.additional_evidence)) {
          str += `${key}: ${this.formatEvidenceValue(value)}, `;
        }
        // Remove the last comma and space  
        str = str.slice(0, -2);
        return str;
      } else {
        return `Initial Diagnosis`;
      }
    },

    getFullEvidenceLabel(diagnosisData) {
      if (diagnosisData.additionalEvidence && Object.keys(diagnosisData.additionalEvidence).length > 0) {
        let str = "";
        for (const [key, value] of Object.entries(diagnosisData.additionalEvidence)) {
          str += `${key}: ${this.formatEvidenceValue(value)}, `;
        }
        return str;
      } else {
        return `Initial Diagnosis`;
      }
    },

    scrollTabs(direction) {
      const container = this.$refs.tabsContainer;
      const scrollAmount = 150; // Adjust as needed
      
      if (direction === 'left') {
        container.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
      } else {
        container.scrollBy({ left: scrollAmount, behavior: 'smooth' });
      }
      
      this.updateScrollButtons();
    },
    
    // Format evidence values for display
    formatEvidenceValue(value) {
      if (typeof value === 'boolean') {
        return value ? 'Yes' : 'No';
      } else if (!isNaN(value)) {
        return value.toString();
      } else {
        return value;
      }
    },

    updateScrollButtons() {
      const container = this.$refs.tabsContainer;
      
      if (container) {
        this.showLeftScroll = container.scrollLeft > 0;
        this.showRightScroll = 
          container.scrollLeft < (container.scrollWidth - container.clientWidth - 5);
      }
    },
    
    closeTab(index) {
      // Store the closed tab in the closedTabs array
      const closedTab = this.diagnosticHistory[index];
      this.closedTabs.push({
        tab: JSON.parse(JSON.stringify(closedTab)),
        originalIndex: index
      });
      
      // Remove the tab from history
      this.diagnosticHistory.splice(index, 1);
      
      // If the closed tab was active or before the active one, adjust the active tab
      if (index <= this.activeDiagnosticTab && this.activeDiagnosticTab !== this.diagnosticHistory.length) {
        this.activeDiagnosticTab = Math.max(0, this.activeDiagnosticTab - 1);
      }
      
      // Limit closedTabs history to 10 items
      if (this.closedTabs.length > 10) {
        this.closedTabs.shift();
      }
    },
    
    undoCloseTab() {
      if (this.closedTabs.length === 0) return;
      
      // Get the most recently closed tab
      const lastClosed = this.closedTabs.pop();
      
      // Calculate where to insert the tab
      let insertIndex = Math.min(lastClosed.originalIndex, this.diagnosticHistory.length);
      
      // Add the tab back to the diagnosticHistory array
      this.diagnosticHistory.splice(insertIndex, 0, lastClosed.tab);
      
      // Set it as the active tab
      this.activeDiagnosticTab = insertIndex;
      
      // Show a brief notification
      this.$store.commit('addDialoguePiece', {
        "visual_message_type": ["text"],
        "visual_message": [`Restored previously closed tab.`],
        "writer": "daphne"
      });
    },
    
    dragStart(event, index) {
      this.draggedTabIndex = index;
      this.draggedTab = this.diagnosticHistory[index];
      
      // Create a custom drag image
      const dragImage = event.target.cloneNode(true);
      dragImage.style.opacity = '0.7';
      dragImage.style.position = 'absolute';
      dragImage.style.top = '-1000px';
      document.body.appendChild(dragImage);
      event.dataTransfer.setDragImage(dragImage, 10, 10);
      
      // Set data transfer
      event.dataTransfer.effectAllowed = 'move';
      event.dataTransfer.setData('text/plain', index);
      
      // Add dragging class
      event.target.classList.add('dragging');
      
      // Remove the drag image after a short delay
      setTimeout(() => {
        document.body.removeChild(dragImage);
      }, 0);
    },
    
    dragOver(event) {
      event.preventDefault();
      const target = this.findTabElement(event.target);
      if (!target) return;
      
      const tabIndex = parseInt(target.getAttribute('data-index') || -1);
      if (tabIndex !== -1 && tabIndex !== this.draggedTabIndex) {
        this.dragOverIndex = tabIndex;
      }
    },
  
    dragEnd(event) {
      event.target.classList.remove('dragging');
      this.draggedTabIndex = null;
      this.draggedTab = null;
      this.dragOverIndex = null;
    },
  
    drop(event, index) {
      event.preventDefault();
      if (this.draggedTabIndex === null || this.draggedTabIndex === index) return;
      
      // Remove tab from old position and insert at new position
      this.diagnosticHistory.splice(this.draggedTabIndex, 1);
      this.diagnosticHistory.splice(index, 0, this.draggedTab);
      
      // Update active tab if needed
      if (this.activeDiagnosticTab === this.draggedTabIndex) {
        this.activeDiagnosticTab = index;
      } else if (
        this.activeDiagnosticTab > this.draggedTabIndex && 
        this.activeDiagnosticTab <= index
      ) {
        this.activeDiagnosticTab--;
      } else if (
        this.activeDiagnosticTab < this.draggedTabIndex && 
        this.activeDiagnosticTab >= index
      ) {
        this.activeDiagnosticTab++;
      }
      
      this.draggedTabIndex = null;
      this.draggedTab = null;
      this.dragOverIndex = null;
    },

    findTabElement(element) {
      while (element && !element.classList.contains('draggable-tabs')) {
        if (element.tagName.toLowerCase() === 'li') {
          return element;
        }
        element = element.parentElement;
      }
      return null;
    },

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

      this.diagnosticHistory = [];
      this.activeDiagnosticTab = 0;
      this.additionalEvidence = {};
      this.closedTabs = []; // Clear closed tabs history when clearing all symptoms

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

    async requestKGDiagnosis() {
      this.allSelected = false;
      this.isLoading = true;
      this.explaining = false;
      this.checked = [];
      await this.$store.dispatch('requestKGDiagnosis', this.selectedSymptomsList);
      this.isLoading = false;
    },

    async requestPhysicsDiagnosis() {
      this.allSelected = false;
      this.isLoading = true;
      this.explaining = false;
      this.checked = [];
      this.showPhysicsTab = true;
      this.physicsDiagnosisError = null; // Clear any previous errors

      try {
        // Request physics diagnosis from backend
        await this.$store.dispatch('requestPhysicsDiagnosis', this.selectedSymptomsList);
        
        // Get the diagnosis report from store
        const diagnosisReport = this.$store.getters.getDiagnosisReport;
        
        console.log("Physics Diagnosis - Raw diagnosis report:", diagnosisReport);
        console.log("Physics Diagnosis - Has physics_diagnosis_data:", diagnosisReport && diagnosisReport.physics_diagnosis_data);
        console.log("Physics Diagnosis - Report keys:", diagnosisReport ? Object.keys(diagnosisReport) : 'No report');
        
        if (diagnosisReport && diagnosisReport.physics_diagnosis_data) {
          // Convert backend data to frontend format
          const physicsDiagnosisData = {
            mostProbableAnomaly: diagnosisReport.physics_diagnosis_data.most_probable_anomaly,
            probability: diagnosisReport.physics_diagnosis_data.probability,
            componentAnomalies: diagnosisReport.physics_diagnosis_data.component_anomalies.map(anomaly => ({
              name: anomaly.name,
              score: anomaly.score,
              isHighlighted: anomaly.is_highlighted
            }))
          };
          this.$store.commit('mutatePhysicsDiagnosisData', physicsDiagnosisData);

          // Convert telemetry data from backend
          const telemetryGraphData = {
            actual: diagnosisReport.physics_diagnosis_data.actual_telemetry,
            simulated: {},
            timeLabels: diagnosisReport.physics_diagnosis_data.time_labels,
            telemetry_metadata: diagnosisReport.physics_diagnosis_data.telemetry_metadata || {
              unit: '',
              sensor_info: {},
              target_sensor: ''
            }
          };

          // Convert simulated data to the expected format
          diagnosisReport.physics_diagnosis_data.component_anomalies.forEach((anomaly, index) => {
            telemetryGraphData.simulated[anomaly.name] = {
              data: anomaly.telemetry_data,
              color: this.getAnomalyColor(index),
              score: parseFloat(anomaly.score)
            };
          });
          this.$store.commit('mutateTelemetryGraphData', telemetryGraphData);

          console.log("Physics diagnosis data successfully loaded from backend");
        } else {
          // Show error message if no proper diagnosis report received
          this.showPhysicsDiagnosisError("No physics diagnosis data received from backend. Please check the backend connection and try again.");
          console.error("Invalid or missing physics diagnosis data from backend:", diagnosisReport);
          return;
        }

        // Add a simple tab with physics diagnosis content
        this.simpleTabs.push({
          label: "Physics Diagnosis",
          content: "Physics diagnosis result goes here."
        });
        this.activeSimpleTab = this.simpleTabs.length - 1;
        
      } catch (error) {
        console.error("Error during physics diagnosis request:", error);
        this.showPhysicsDiagnosisError("Failed to request physics diagnosis. Please check your connection and try again.");
      } finally {
        this.isLoading = false;
      }
    },

    togglePhysicsExplanation() {
      this.showPhysicsExplanation = !this.showPhysicsExplanation;
      if (this.showPhysicsExplanation) {
        this.generateTelemetryGraph();
      }
    },

    generateTelemetryDataForAnomalies() {
      // This method is now disabled - data should come from backend
      console.warn("Frontend telemetry data generation is disabled. Data should come from backend.");
      return false;
    },

    generateTelemetryGraph() {
      this.$nextTick(() => {
        const canvas = this.$refs.telemetryGraph;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;

        // Clear canvas
        ctx.clearRect(0, 0, width, height);

        // Check if we have data from backend
        if (!this.telemetryGraphData.actual || this.telemetryGraphData.actual.length === 0) {
          console.error("No telemetry data available from backend. Cannot display graph.");
          this.showPhysicsDiagnosisError("No telemetry data available. Please ensure backend is properly connected.");
          return;
        }

        // Draw grid
        this.drawGrid(ctx, width, height);

        // Draw axes
        this.drawAxes(ctx, width, height);

        // Debug: Log the data ranges
        console.log('Graph Data Ranges:');
        console.log('Actual telemetry:', this.telemetryGraphData.actual);
        console.log('Simulated anomalies:', this.telemetryGraphData.simulated);
        console.log('Y-axis range:', this.graphYRange);

        // Draw actual telemetry line
        this.drawDataLine(ctx, this.telemetryGraphData.actual, width, height, '#0AFEFF', 'Actual');

        // Draw simulated data lines for each anomaly
        Object.entries(this.telemetryGraphData.simulated).forEach(([anomalyName, anomalyData]) => {
          this.drawDataLine(ctx, anomalyData.data, width, height, anomalyData.color, anomalyName);
        });

        // Draw legend
        this.drawLegend(ctx, width, height);
      });
    },

    showPhysicsDiagnosisError(message) {
      // Set error state
      this.physicsDiagnosisError = message;
      
      // Show error message to user
      this.$store.commit('addDialoguePiece', {
        "voice_message": message,
        "visual_message_type": ["text"],
        "visual_message": [message],
        "writer": "daphne"
      });
      
      // Also log to console for debugging
      console.error("Physics Diagnosis Error:", message);
    },

    getAnomalyEffect(anomalyName) {
      // Different anomalies have different effects on telemetry
      if (anomalyName.includes('Valve Leak')) return 15;
      if (anomalyName.includes('Bearing Wear')) return 10;
      if (anomalyName.includes('Bed Saturated')) return 20;
      if (anomalyName.includes('Coil Failure')) return 25;
      if (anomalyName.includes('Sensor Drift')) return 8;
      return 12; // Default effect
    },

    getAnomalyColor(index) {
      // Different colors for each anomaly line
      const colors = [
        '#ff6b6b', // Red
        '#4ecdc4', // Teal
        '#45b7d1', // Blue
        '#96ceb4', // Green
        '#feca57', // Yellow
        '#ff9ff3', // Pink
        '#54a0ff', // Light Blue
        '#5f27cd', // Purple
        '#00d2d3', // Cyan
        '#ff9f43'  // Orange
      ];
      return colors[index % colors.length];
    },

    drawGrid(ctx, width, height) {
      const metadata = this.telemetryGraphData.telemetry_metadata || {};
      const sensorInfo = metadata.sensor_info || {};
      const leftMargin = 70;
      const bottomMargin = 50;
      const graphWidth = width - leftMargin - 20;
      const graphHeight = height - bottomMargin - 30;

      // Draw basic grid
      ctx.strokeStyle = '#333';
      ctx.lineWidth = 1;

      // Vertical grid lines
      for (let x = 0; x <= width; x += width / 10) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
        ctx.stroke();
      }

      // Horizontal grid lines
      for (let y = 0; y <= height; y += height / 6) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
      }

      // Draw limit lines if sensor info is available
      if (sensorInfo) {
        const yRange = this.graphYRange || { min: 0, max: 100 };
        const yMin = yRange.min;
        const yMax = yRange.max;
        const yRangeSize = yMax - yMin;

        // Function to convert value to Y coordinate
        const valueToY = (value) => {
          return height - bottomMargin - ((value - yMin) * graphHeight / yRangeSize);
        };

        // Draw limit lines
        const limits = [
          { value: sensorInfo.nominal_value, color: '#ccc', label: 'Nominal' },
          { value: sensorInfo.upper_warning, color: '#ff6b6b', label: 'Upper Warning' },
          { value: sensorInfo.upper_caution, color: '#ffd93d', label: 'Upper Caution' },
          { value: sensorInfo.lower_caution, color: '#ffd93d', label: 'Lower Caution' },
          { value: sensorInfo.lower_warning, color: '#ff6b6b', label: 'Lower Warning' }
        ];

        limits.forEach(limit => {
          if (limit.value !== undefined && limit.value !== null) {
            const y = valueToY(limit.value);
            
            // Draw dotted line
            ctx.strokeStyle = limit.color;
            ctx.lineWidth = 1;
            ctx.setLineDash([5, 5]); // Create dotted line effect
            
            ctx.beginPath();
            ctx.moveTo(leftMargin, y);
            ctx.lineTo(width - 20, y);
            ctx.stroke();
            
            // Reset line dash
            ctx.setLineDash([]);
            
            // Add small label on the left
            ctx.fillStyle = limit.color;
            ctx.font = '10px Arial';
            ctx.fillText(limit.label, 5, y + 4);
          }
        });
      }
    },

    drawAxes(ctx, width, height) {
      ctx.strokeStyle = '#666';
      ctx.lineWidth = 2;
      ctx.fillStyle = '#ccc';
      ctx.font = '12px Arial';

      // Calculate dynamic Y-axis range based on all data
      const allData = [
        ...(this.telemetryGraphData.actual || []),
        ...Object.values(this.telemetryGraphData.simulated || {}).map(anomaly => anomaly.data || [])
      ].flat();
      
      let minValue = Math.min(...allData);
      let maxValue = Math.max(...allData);
      
      // Add padding to the range
      const range = maxValue - minValue;
      const padding = range * 0.1; // 10% padding
      minValue = Math.max(0, minValue - padding);
      maxValue = maxValue + padding;
      
      // Store the calculated range for use in drawDataLine
      this.graphYRange = { min: minValue, max: maxValue };

      // Y-axis
      ctx.beginPath();
      ctx.moveTo(70, 0);  // Increased left margin for longer labels
      ctx.lineTo(70, height - 50);  // Increased bottom margin for timestamps
      ctx.stroke();

      // X-axis
      ctx.beginPath();
      ctx.moveTo(70, height - 50);
      ctx.lineTo(width - 20, height - 50);
      ctx.stroke();

      // Y-axis labels with dynamic range and unit
      const unit = (this.telemetryGraphData.telemetry_metadata && this.telemetryGraphData.telemetry_metadata.unit) || '';
      for (let i = 0; i <= 6; i++) {
        const y = height - 50 - (i * (height - 50) / 6);
        const value = maxValue - (i * (maxValue - minValue) / 6);
        ctx.fillText(`${value.toFixed(1)}${unit ? ` ${unit}` : ''}`, 10, y + 4);
      }

      // X-axis labels (time points)
      const timeLabels = this.telemetryGraphData.timeLabels || [];
      if (timeLabels.length > 0) {
        ctx.save();
        ctx.translate(70, height - 30);
        ctx.rotate(-Math.PI / 4);  // Rotate labels for better readability
        
        for (let i = 0; i < timeLabels.length; i += 2) {
          const x = (i * (width - 90) / (timeLabels.length - 1));
          ctx.fillText(timeLabels[i], 0, x);
        }
        
        ctx.restore();
      } else {
        // Fallback labels if no time labels from backend
        for (let i = 0; i <= 20; i += 2) {
          const x = 70 + (i * (width - 90) / 20);
          ctx.fillText(`T${i + 1}`, x - 10, height - 30);
        }
      }

      // Add sensor name and unit as title
      const metadata = this.telemetryGraphData.telemetry_metadata || {};
      const sensorName = metadata.target_sensor || '';
      if (sensorName) {
        ctx.font = '14px Arial';
        ctx.fillStyle = '#0AFEFF';
        ctx.fillText(`${sensorName} (${unit})`, width / 2 - 100, 20);
      }
    },

    drawDataLine(ctx, data, width, height, color, label) {
      if (!data || data.length === 0) return;

      ctx.strokeStyle = color;
      ctx.lineWidth = 3;
      ctx.fillStyle = color;

      const leftMargin = 70;  // Match the increased left margin from drawAxes
      const bottomMargin = 50;  // Match the increased bottom margin from drawAxes
      const rightMargin = 20;
      const topMargin = 30;

      const graphWidth = width - leftMargin - rightMargin;
      const graphHeight = height - bottomMargin - topMargin;

      // Use dynamic Y-axis range if available, otherwise fallback to fixed range
      const yRange = this.graphYRange || { min: 0, max: 100 };
      const yMin = yRange.min;
      const yMax = yRange.max;
      const yRangeSize = yMax - yMin;

      ctx.beginPath();
      data.forEach((value, index) => {
        const x = leftMargin + (index * graphWidth / (data.length - 1));
        const y = height - bottomMargin - ((value - yMin) * graphHeight / yRangeSize);
        
        if (index === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      });
      ctx.stroke();

      // Draw data points
      data.forEach((value, index) => {
        const x = leftMargin + (index * graphWidth / (data.length - 1));
        const y = height - bottomMargin - ((value - yMin) * graphHeight / yRangeSize);
        
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, 2 * Math.PI);
        ctx.fill();
      });
    },

    drawLegend(ctx, width, height) {
      ctx.fillStyle = '#ccc';
      ctx.font = '12px Arial';
      
      // Create legend items for telemetry lines only
      const legendItems = [
        { text: 'Actual Telemetry', color: '#0AFEFF' },
        ...Object.entries(this.telemetryGraphData.simulated || {}).map(([anomalyName, anomalyData]) => ({
          text: `${anomalyName} (${anomalyData.score})`,
          color: anomalyData.color
        }))
      ];
      
      const legendHeight = legendItems.length * 20 + 20;
      const legendWidth = 250;
      
      // Legend background
      ctx.fillStyle = 'rgba(0, 30, 30, 0.9)';
      ctx.fillRect(width - legendWidth - 20, 20, legendWidth, legendHeight);
      
      // Draw telemetry line items
      legendItems.forEach((item, index) => {
        // Draw color line sample
        ctx.strokeStyle = item.color;
        ctx.lineWidth = 2;
        const lineY = 34 + (index * 20);
        ctx.beginPath();
        ctx.moveTo(width - legendWidth - 10, lineY);
        ctx.lineTo(width - legendWidth + 20, lineY);
        ctx.stroke();
        
        // Draw text
        ctx.fillStyle = item.color;
        ctx.fillText(item.text, width - legendWidth + 30, 40 + (index * 20));
      });
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
      this.activeDiagnosticTab = this.diagnosticHistory.length;
      
      this.diagnosticHistory.push(diagnosisReport);
      console.log("Set active diagnostic tab to:", this.activeDiagnosticTab);
      // console.log("current diagnostic history 1111111", this.diagnosticHistory);
      // console.log("current diagnostic history 2222222", this.diagnosticHistory[this.activeDiagnosticTab]);
      // After getting diagnosis report, ask if user has additional evidence
      setTimeout(() => {
      if (this.bestEvidence) {
        this.$store.commit('addDialoguePiece', {
          "voice_message": `I could improve my diagnosis confidence if you could assess the condition of ${this.bestEvidence}. Would you like to provide this information?`,
          "visual_message_type": ["text"],
          "visual_message": [`I could improve my diagnosis confidence if you could assess the condition of ${this.bestEvidence}. Would you like to provide this information?`],
          "writer": "daphne",
          "options": ["Yes", "No"],
          "optionsCallbackEvent": "bestEvidenceResponse"
        });
        
        // Set up listener for response
        this.setupBestEvidenceListener();
      }
    }, 1000);

    if(this.bestEvidence == null) {
      this.$store.commit('addDialoguePiece', {
          "voice_message": `No additional evidence can improve my diagnostic confidence. Please proceed with the anomaly resolution.`,
          "visual_message_type": ["text"],
          "visual_message": [`No additional evidence can improve my diagnostic confidence. Please proceed with the anomaly resolution.`],
          "writer": "daphne",
        });
    }

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

    setupBestEvidenceListener() {
      // Add event listener for options response
      if (!this.bestEvidenceListener) {
        this.$root.$on('bestEvidenceResponse', this.handleBestEvidenceResponse);
        this.bestEvidenceListener = true;
      }
    },

    handleBestEvidenceResponse(response) {
      if (response === "Yes") {
        // Show damage assessment slider for best evidence
        this.showDamageAssessmentSlider();
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
      this.$root.$off('bestEvidenceResponse', this.handleBestEvidenceResponse);
      this.bestEvidenceListener = false;
    },

    showDamageAssessmentSlider() {
      this.$store.commit('addDialoguePiece', {
        "voice_message": `On a scale of 1 to 5, how damaged is the ${this.bestEvidence}? (1 = minimal damage, 5 = severe damage)`,
        "visual_message_type": ["slider"],
        "visual_message": [`On a scale of 1 to 5, how damaged is the ${this.bestEvidence}? (1 = minimal damage, 5 = severe damage)`],
        "writer": "daphne",
        "sliderOptions": {
          "min": 1,
          "max": 5,
          "step": 1,
          "defaultValue": 3,
          "callbackEvent": "damageAssessmentResponse"
        }
      });
      
      // Set up listener for slider response
      this.$root.$on('damageAssessmentResponse', this.handleDamageAssessmentResponse);
    },

    handleDamageAssessmentResponse(value) {
      // Add the assessment to additional evidence
      this.additionalEvidence[this.bestEvidence] = value
      
      // // Thank the user and submit the evidence
      // this.$store.commit('addDialoguePiece', {
      //   "voice_message": `Thank you for your assessment of ${this.bestEvidence}.`,
      //   "visual_message_type": ["text"],
      //   "visual_message": [`Thank you for your assessment of ${this.bestEvidence}.`],
      //   "writer": "daphne"
      // });
      
      // Clean up listener
      this.$root.$off('damageAssessmentResponse', this.handleDamageAssessmentResponse);
      
      // Submit the evidence and update diagnosis
      this.submitAdditionalEvidence();
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

    handleAddHypotheticalDiagnosis(eventData) {
      // Get the last message which contains the hypothetical data
      const dialogueHistory = this.$store.state.daphne.dialogueHistory;
      const lastMessage = dialogueHistory[dialogueHistory.length - 2];
      console.log("last message", lastMessage);
      console.log("last message hypothetical data", lastMessage.hypothetical_data);
      
      if (!lastMessage || !lastMessage.hypothetical_data) {
        console.error("No hypothetical data found in the last message");
        return;
      }
      
      // Create a new diagnosis report object from the hypothetical data
      const hypotheticalDiagnosis = {
        diagnosis_list: lastMessage.hypothetical_data.diagnosis_list,
        additional_evidence: lastMessage.hypothetical_data.additional_evidence,
        is_hypothetical: true,
        hypothetical_evidence: lastMessage.hypothetical_data.additional_evidence
      };
      
      // Add to diagnostic history
      this.diagnosticHistory.push(hypotheticalDiagnosis);
      
      // Switch to the new tab
      this.activeDiagnosticTab = this.diagnosticHistory.length - 1;
      
      // Confirm to the user
      this.$store.commit('addDialoguePiece', {
        "voice_message": "I've added this hypothetical scenario to your diagnosis history tabs.",
        "visual_message_type": ["text"],
        "visual_message": ["I've added this hypothetical scenario to your diagnosis history tabs. You can switch between tabs to compare different evidence scenarios."],
        "writer": "daphne"
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

        // const currentDiagnosisReport = this.$store.getters.getDiagnosisReport;
        // if (currentDiagnosisReport && currentDiagnosisReport.diagnosis_list) {
        //   this.diagnosticHistory.push(JSON.parse(JSON.stringify(currentDiagnosisReport)));
        // }
        // const evidenceData = {
        //   additional_evidence: this.additionalEvidence,
        //   current_telemetry_values: this.currentTelemetryValues,
        // };

        console.log("Submitting additional evidence:", this.additionalEvidence);

        const requestPayload = {
        symptoms: this.selectedSymptomsList,
        additional_evidence: this.additionalEvidence,
        current_telemetry_values: this.currentTelemetryValues
      };
        
        // Make API call

        // await this.$store.dispatch('requestDiagnosis', this.selectedSymptomsList);
        await this.$store.dispatch('requestDiagnosisWithEvidence', requestPayload);
        const diagnosisReport = this.$store.getters.getDiagnosisReport;
        
        this.unconfirmedSymptoms = diagnosisReport.hidden_components;
        this.bestEvidence = diagnosisReport.best_evidence;     
        this.currentTelemetryValues = diagnosisReport.current_telemetry_values
        
        this.$store.commit('addDialoguePiece', {
          "voice_message": "Diagnosis has been updated with your additional evidence!",
          "visual_message_type": ["text"],
          "visual_message": ["Diagnosis has been updated with your additional evidence!"],
          "writer": "daphne"
        });

        this.activeDiagnosticTab = this.diagnosticHistory.length;

        this.diagnosticHistory.push(JSON.parse(JSON.stringify(diagnosisReport)));
        console.log("Set active diagnostic tab to:", this.activeDiagnosticTab);
        console.log("current diagnostic history", this.diagnosticHistory);

        setTimeout(() => {
          if (this.bestEvidence) {
            this.$store.commit('addDialoguePiece', {
              "voice_message": `I could further improve my diagnosis confidence if you could assess the condition of ${this.bestEvidence}. Would you like to provide this information?`,
              "visual_message_type": ["text"],
              "visual_message": [`I could further improve my diagnosis confidence if you could assess the condition of ${this.bestEvidence}. Would you like to provide this information?`],
              "writer": "daphne",
              "options": ["Yes", "No"],
              "optionsCallbackEvent": "bestEvidenceResponse"
            });
            
            // Set up listener for response
            this.setupBestEvidenceListener();
          }
        }, 1000);

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
      this.isLoading = true;
      console.log('Checked anomalies:', this.checked); // <-- Add this line
      if (this.checked.length === 0) {
        this.isLoading = false;
        this.showAlert = true;
        this.explaining = false;
        print("Please select anomalies for investigation.");
      } else {
        this.showAlert = false;
        this.isLoading = false;
        this.explaining = true;
        console.log('Showing explanations for anomalies:', this.checked);
      }
    },

    clearExplanations() {
      this.explaining = false;
      this.checked = [];
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

    addSimpleTab(label, content) {
      this.simpleTabs.push({ label, content });
      this.activeSimpleTab = this.simpleTabs.length - 1;
    },
    
    closeSimpleTab(index) {
      this.simpleTabs.splice(index, 1);
      if (this.activeSimpleTab >= this.simpleTabs.length) {
        this.activeSimpleTab = this.simpleTabs.length - 1;
      }
    }
  },

  mounted() {
    //main
    this.startAstrobeeStatusPolling();
    setInterval(this.startAstrobeeStatusPolling, 1200);

    this.$nextTick(() => {
      if (this.$refs.tabsContainer) {
        this.$refs.tabsContainer.addEventListener('scroll', this.updateScrollButtons);
        window.addEventListener('resize', this.updateScrollButtons);
        this.updateScrollButtons();
      }
    });
    this.$root.$on('addHypotheticalDiagnosis', this.handleAddHypotheticalDiagnosis);
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
  if (this.bestEvidenceListener) {
    this.$root.$off('bestEvidenceResponse', this.handleBestEvidenceResponse);
  }
  this.$root.$off('addHypotheticalDiagnosis', this.handleAddHypotheticalDiagnosis);
  this.$root.$off('damageAssessmentResponse', this.handleDamageAssessmentResponse);

  if (this.$refs.tabsContainer) {
      this.$refs.tabsContainer.removeEventListener('scroll', this.updateScrollButtons);
      window.removeEventListener('resize', this.updateScrollButtons);
    }

  },

  watch: {
    diagnosticHistory() {
      this.$nextTick(() => {
        this.updateScrollButtons();
      });
    },
    physicsDiagnosisData: {
      deep: true,
      handler() {
        if (this.showPhysicsExplanation) {
          this.generateTelemetryGraph();
        }
      }
    },
    telemetryGraphData: {
      deep: true,
      handler() {
        if (this.showPhysicsExplanation) {
          this.generateTelemetryGraph();
        }
      }
    }
  }
}
</script>

<style scoped>
.hover:hover {
  font-weight: bold;
}

.hypothetical-tab a {
  background-color: rgba(100, 50, 150, 0.3) !important; /* Purple tint for hypothetical tabs */
  border-style: dashed !important;
}

.hypothetical-tab.is-active a {
  background-color: rgba(100, 50, 150, 0.5) !important; /* Darker purple for active hypothetical tab */
  border-color: #c4a0ff !important;
  color: #d0b0ff !important;
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

.tabs-container {
  display: flex;
  align-items: center;
  position: relative;
  width: 100%;
  margin-bottom: 1rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  padding: 4px;
}


.tab-wrapper {
  flex: 1;
  overflow-x: auto;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
  background: transparent;
}
.tab-wrapper::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}

.draggable-tabs {
  display: flex;
  flex-wrap: nowrap;
  width: max-content;
}

.draggable-tabs li {
  cursor: pointer;
  position: relative;
  margin-right: 2px;
}

.draggable-tabs li.dragging {
  opacity: 0.7;
  z-index: 10;
}

.draggable-tabs li a {
  display: flex;
  align-items: center;
  padding: 0.5rem 0.75rem;
  height: 100%;
  min-width: 120px;
  border-radius: 4px 4px 0 0;
  border: 1px solid #333;
  border-bottom: none;
  transition: background-color 0.2s, color 0.2s;
  color: #ccc;
}

.tab-evidence {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  padding-right: 5px;
}

.tab-close {
  margin-left: auto;
  background: transparent;
  border: none;
  color: #666;
  font-size: 1.2rem;
  line-height: 1;
  padding: 0 0.3rem;
  cursor: pointer;
  border-radius: 50%;
}

.tab-close {
  margin-left: auto;
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.5);
  font-size: 1.2rem;
  line-height: 1;
  padding: 0 0.3rem;
  cursor: pointer;
  border-radius: 50%;
}

.tab-close:hover {
  background-color: rgba(255, 0, 0, 0.2);
  color: #ff4d4d;
}

.tab-scroll-button {
  background: rgba(0, 0, 0, 0.3);
  border: none;
  border-radius: 4px;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  margin: 0 5px;
  color: #0AFEFF;
  flex-shrink: 0;
}

.tab-scroll-button:hover {
  background: rgba(10, 254, 255, 0.2);
}

/* Style active/inactive tabs */
.draggable-tabs li.is-active a {
  background-color: #002E2E !important;
  color: #0AFEFF !important;
  border-color: #0AFEFF !important;
  font-weight: bold;
  box-shadow: 0 0 4px rgba(10, 254, 255, 0.3);
}


.draggable-tabs li:not(.is-active) a {
  background-color: rgba(0, 46, 46, 0.5);
}

.draggable-tabs li:not(.is-active) a:hover {
  background-color: rgba(0, 46, 46, 0.8);
  color: #ccc;
}

/* Add tooltip-like behavior for overflowing tab names */
.draggable-tabs li a:hover .tab-evidence {
  position: relative;
}

.tab-undo-button {
  background: rgba(10, 254, 255, 0.2);
  border: none;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  margin-left: 5px;
  color: #0AFEFF;
  flex-shrink: 0;
  transition: all 0.3s;
}

.tab-undo-button:hover {
  background: rgba(10, 254, 255, 0.4);
  transform: scale(1.1);
}

.tab-undo-button:active {
  transform: scale(0.95);
}

.physics-diagnosis-report {
  background: #001e1e;
  border-radius: 6px;
  padding: 18px;
  margin: 0;
}

.physics-title-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #003f3f;
  padding: 12px 18px;
  border-radius: 4px;
  margin-bottom: 18px;
}

.physics-content-section {
  display: flex;
  gap: 24px;
  margin-top: 0;
}

.physics-table-section {
  flex: 1.2;
}

.physics-table {
  width: 100%;
  border-collapse: collapse;
  background: #111;
  color: #eee;
  border-radius: 4px;
  overflow: hidden;
}

.physics-table th, .physics-table td {
  padding: 10px 14px;
  text-align: left;
}

.physics-table th {
  background: #002E2E;
  color: #0AFEFF;
}

.physics-table tr:not(:first-child):hover {
  background: #003f3f;
}

.physics-image-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 220px;
}
</style>