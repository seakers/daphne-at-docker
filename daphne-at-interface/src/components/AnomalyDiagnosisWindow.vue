<template>
  <div id="anomaly_diagnosis" style="width: 100%;">
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
            <!-- Physics Simulation Duration Input -->
            <div style="margin-top: 10px; display: flex; align-items: center; gap: 10px;">
              <label style="color: #0AFEFF; font-size: 12px; white-space: nowrap;">
                <input 
                  type="checkbox" 
                  v-model="useManualDuration"
                  style="margin-right: 5px; vertical-align: middle;"
                >
                Manual Duration:
              </label>
              <input 
                type="number" 
                v-model="durationValue" 
                :disabled="!useManualDuration"
                min="1" 
                max="10000"
                style="width: 80px; padding: 4px 8px; background: #002E2E; border: 1px solid #0AFEFF; color: #0AFEFF; border-radius: 4px; font-size: 12px;"
                :style="{ opacity: useManualDuration ? 1 : 0.5 }"
              >
              <select 
                v-model="durationUnit" 
                :disabled="!useManualDuration"
                @change="updatePhysicsSimDuration"
                style="padding: 4px 8px; background: #002E2E; border: 1px solid #0AFEFF; color: #0AFEFF; border-radius: 4px; font-size: 12px; min-width: 75px;"
                :style="{ opacity: useManualDuration ? 1 : 0.5 }">
                <option value="seconds">sec</option>
                <option value="minutes">min</option>
                <option value="hours">hrs</option>
              </select>
              <span v-if="!useManualDuration" style="color: #0AFEFF; font-size: 12px; margin-left: 5px;">
                (Auto: {{ autoSimDurationDisplay }})
              </span>
            </div>
          </div>
        </div>
      </div>

      <div class="horizontal-divider" style="margin-top: 10px; margin-bottom: 10px"></div>

        <!-- ################### KG Diagnosis report hypothesis list ########################-->
      <div class="is-content">
        <!-- Loading spinner at the top -->
        <div v-if="isLoading" style="text-align: center; padding: 20px;">
          <img src="assets/img/loader.svg"
               style="display: block; margin: auto;"
               height="40" width="40"
               alt="Loading spinner">
          <p style="color: #0AFEFF; margin-top: 10px;">Processing diagnosis...</p>
        </div>
        
        <!-- Simple, independent tab UI -->
        <div v-if="!isLoading" class="tabs-container" style="margin-bottom: 20px;">
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
        <div v-if="simpleTabs[activeSimpleTab] && !isLoading">
          <!-- KG Diagnosis Results -->
          <div v-if="simpleTabs[activeSimpleTab].type === 'kg'" class="kg-diagnosis-report">
            <div v-if="!simpleTabs[activeSimpleTab].diagnosisData || simpleTabs[activeSimpleTab].diagnosisData.length === 0">
              <p>No KG diagnosis reports requested.</p>
            </div>
            <div v-else>
              <div class="column" style="margin: 0px; padding: 0px">
                <span style="margin-bottom:20px; color: #0AFEFF; background: #002E2E">Set of symptoms selected for diagnosis:</span>
                <ul>
                  <li class="hover" v-for="symptom in simpleTabs[activeSimpleTab].diagnosisData['symptoms_list']" v-on:click="recoverSymptomsList()"
                      style="cursor: pointer">
                    {{ symptom['detection_text'] }}
                  </li>
                </ul>
              </div>
              <div class="column" style="margin-top: 20px; padding: 0px">
                <span style="margin-bottom:20px; color: #0AFEFF; background: #002E2E">Could be caused by anomalies:</span><br />
                <span><input type='checkbox' v-model="simpleTabs[activeSimpleTab].allSelected" v-on:click="selectAllAnomaliesForTab(activeSimpleTab)"> Select All </span>
                <ul v-for="anomaly in simpleTabs[activeSimpleTab].diagnosisData['diagnosis_list']">
                  <li>
                    <input type="checkbox" class='checkall' v-model="simpleTabs[activeSimpleTab].checked" :value="anomaly"
                            style="border-color: #0AFEFF; color: #0AFEFF; background: #002E2E;">
                    {{ anomaly['name'] }} <span :style="{'color': 0.66<anomaly['score']<1?(anomaly['score']<0.33 ? 'green' : 'yellow'):'red'}">({{anomaly['text_score']}}) </span>
                  </li>
                </ul>
              </div>
              <div style="text-align: center; margin-top: 30px">
                <p v-if="showAlert" style="color: red">Please select an anomaly to investigate.</p>
                <button class="button" type="submit" onclick="errorMessage()"
                        style="width: 30%; border-color: #0AFEFF; color: #0AFEFF; background: #002E2E;"
                        v-on:click.prevent="showExplanationsForTab(activeSimpleTab)">Show explanations
                </button>
              </div>
              
              <!-- KG Explanations Section -->
              <div v-if="simpleTabs[activeSimpleTab].explaining" class="horizontal-divider" style="margin-top: 20px; margin-bottom: 20px"></div>
              
              <div v-if="simpleTabs[activeSimpleTab].explaining" class="kg-explanations-section">
                <div class="is-mini-title" style="margin-bottom:5px; font-size: 22px">
                  Explanations
                  <u style="float: right; cursor: pointer" v-on:click.prevent="clearExplanationsForTab(activeSimpleTab)">Clear</u>
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
                        <td v-bind:colspan="simpleTabs[activeSimpleTab].diagnosisData['symptoms_list'].length"
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
                        <td v-for="symptom in simpleTabs[activeSimpleTab].diagnosisData['symptoms_list']">{{ symptom['detection_text'] }}</td>
                      </tr>
                      </thead>
                      <tbody>
                      <tr v-for="(anomaly) in simpleTabs[activeSimpleTab].checked">
                        <td>{{ anomaly['name'] }}</td>
                        <td style="text-align: center; vertical-align: middle"><p class="hover" style="cursor: pointer"
                                                                                  v-bind:title="'The signature of this anomaly is: '+ anomaly['signature']"
                                                                                  v-on:click="showSignature(anomaly)">
                          {{ anomaly['signature'].length }}</p></td>
                        <td v-for="symptom in simpleTabs[activeSimpleTab].diagnosisData['symptoms_list']"
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
          
          <!-- Bayesian Diagnosis Results -->
          <div v-else-if="simpleTabs[activeSimpleTab].type === 'bayesian'" class="bayesian-diagnosis-report">
            <div v-if="!simpleTabs[activeSimpleTab].diagnosisData || simpleTabs[activeSimpleTab].diagnosisData.length === 0">
              <p>No Bayesian diagnosis reports requested.</p>
            </div>
            <div v-else>
              <!-- Most probable anomaly highlighting -->
              <div v-if="simpleTabs[activeSimpleTab].diagnosisData['diagnosis_list'].length > 0" class="most-probable-anomaly" 
                  style="margin-bottom: 20px; padding: 15px; background: #002E2E; border: 1px solid #0AFEFF; border-radius: 4px;">
                <h3 style="color: #0AFEFF; margin-bottom: 10px;">Most Probable Anomaly:</h3>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                  <span style="font-size: 18px; font-weight: bold;">{{ simpleTabs[activeSimpleTab].diagnosisData['diagnosis_list'][0].anomaly }}</span>
                  <span style="background: #003f3f; padding: 5px 10px; border-radius: 4px; font-weight: bold;">
                    Probability: {{ (simpleTabs[activeSimpleTab].diagnosisData['diagnosis_list'][0].probability * 100 ).toFixed(4) }}%
                  </span>
                </div>
                <div style="text-align: center;">
                  <button class="button theme-buttons"
                          style="border-color: #0AFEFF; color: #0AFEFF; background: #002E2E; padding: 8px 16px; font-size: 14px;"
                          v-on:click.prevent="runPhysicsDiagnosisForAnomaly(simpleTabs[activeSimpleTab].diagnosisData['diagnosis_list'][0].anomaly, simpleTabs[activeSimpleTab].diagnosisData['diagnosis_list'][0].probability)">
                    Run Physics Diagnosis
                  </button>
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
                        <th style="color: #0AFEFF; width: 40%;">Anomaly</th>
                        <th style="color: #0AFEFF; width: 35%;">Probability</th>
                        <th style="color: #0AFEFF; width: 25%; text-align: center;">Physics Diagnosis</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="item in simpleTabs[activeSimpleTab].diagnosisData['diagnosis_list']" 
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
                        <td style="padding: 8px; text-align: center; vertical-align: middle;">
                          <button class="button theme-buttons"
                                  style="border-color: #0AFEFF; color: #0AFEFF; background: #002E2E; padding: 8px 16px; font-size: 14px;"
                                  v-on:click.prevent="runPhysicsDiagnosisForAnomaly(item.anomaly, item.probability)">
                            Run Physics Diagnosis
                          </button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Chatbot Physics Diagnosis Results - Show full physics diagnosis like manual request -->
          <div v-else-if="simpleTabs[activeSimpleTab].isChatbotResult || simpleTabs[activeSimpleTab].type === 'physics'" class="physics-diagnosis-report">
            <!-- Title Section -->
            <div class="physics-title-section">
              <div>
                <span style="color:#0AFEFF;">Most Likely Component:</span>
                <span style="font-weight:bold; color:white; margin-left:10px;">{{ simpleTabs[activeSimpleTab].physicsDiagnosisData ? simpleTabs[activeSimpleTab].physicsDiagnosisData.mostProbableAnomaly : 'N/A' }}</span>
              </div>
              <div style="margin-left:auto; color:#0AFEFF;">
                Similarity Score: <span style="font-weight:bold; color:white;">{{ formatSimilarityScore(simpleTabs[activeSimpleTab].physicsDiagnosisData ? simpleTabs[activeSimpleTab].physicsDiagnosisData.probability : null) }}</span>
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
                      <th style="text-align:center;">Show</th>
                      <th>Component Anomaly</th>
                      <th>Similarity Score</th>
                      <th style="text-align:center;">Fault Injection Time</th>
                      <th style="text-align:center;">Procedure</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="anomaly in (simpleTabs[activeSimpleTab].physicsDiagnosisData ? simpleTabs[activeSimpleTab].physicsDiagnosisData.componentAnomalies : [])" 
                        :key="anomaly.name"
                        :style="(anomaly.isHighlighted || anomaly.is_highlighted) ? 'background:#c0392b; color:white; font-weight:bold;' : ''"
                        @mouseenter="hoveredPhysicsAnomaly = anomaly.name"
                        @mouseleave="hoveredPhysicsAnomaly = null">
                      <td class="checkbox-cell">
                        <label class="checkbox-full">
                          <input type="checkbox"
                                 :value="anomaly.name"
                                 v-model="selectedPhysicsAnomalies"
                                 @change="onSelectedAnomaliesChange"/>
                          <span class="check-icon">✓</span>
                        </label>
                      </td>
                      <td>{{ anomaly.name }}</td>
                      <td>{{ anomaly.similarity || anomaly.probability || anomaly.score || 'N/A' }}</td>
                      <td style="text-align:center; font-size: 12px;">
                        <span v-if="anomaly.fault_injection_time_absolute" 
                              :title="`Fault injected at ${anomaly.fault_injection_time_absolute} (data point ${anomaly.faultInjectionTime || anomaly.fault_injection_time})`">
                          {{ anomaly.fault_injection_time_absolute }}
                        </span>
                        <span v-else style="color: #666;">N/A</span>
                      </td>
                      <td style="text-align:center;">
                        <button class="button"
                                style="width: 70%; border-color: #0AFEFF; color: #0AFEFF; background: #002E2E"
                                v-on:click.prevent="handlePhysicsProcedure(anomaly.name)">
                          Select
                        </button>
                      </td>
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
                <img :src="physicsComponentImage" alt="System Configuration" style="max-width:100%; border-radius:6px;"/>
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
                <div class="telemetry-graph-container" style="background: #001e1e; border-radius: 6px; padding: 20px; min-height: 300px; width: 100%;">
                  <vue-plotly 
                    style="width: 100%; height: 400px;"
                    :data="physicsPlotData"
                    :layout="physicsPlotLayout"
                    :options="{displayModeBar: false, responsive: true}"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
        <button class="button" @click="addSimpleTab('New Tab', 'This is a new independent tab.')" style="margin-top: 10px;" v-if="false">
          Add Simple Tab
        </button>

        <!-- Show no reports message only when no tabs are active and not loading -->
        <div v-if="simpleTabs.length === 0 && !isLoading">
          <div v-if="diagnosisReport.length === 0">
            <p>No diagnosis reports requested.</p>
          </div>
        </div>

        <!-- KG diagnosis content is now displayed in tabs above -->

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

        <div v-else v-if="false">
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
    
      <div class="is-content" v-if="false">
        <!-- This section is now deprecated - explanations are shown in tabs -->
        <div v-if="diagnosisReport.length === 0 || this.explaining === false">
          <p>No explanations requested.</p>
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
import { fetchPost, fetchGet } from '../scripts/fetch-helpers';
import SymptomSelectionDialog from './SymptomSelectionDialog.vue';
import VuePlotly from '@statnett/vue-plotly';


let loaderImage = require('../images/loader.svg');

// Dynamically require all PNG images from the images directory
const imageContext = require.context('../images/physics_components/', false, /\.png$/);
const componentImages = {};

// Build a map of image names to their required paths
imageContext.keys().forEach(key => {
  const imageName = key.replace('./', '').replace('.png', '');
  componentImages[imageName] = imageContext(key);
});

export default {
  name: "AnomalyDiagnosisWindow",
  components: {
    SymptomSelectionDialog,
    VuePlotly
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
      currentInstruction: null,
      manualInstructionListener: false,
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
      selectedPhysicsAnomalies: [],
      localPhysicsSimDuration: 3000, // Local copy of physics simulation duration (in seconds)
      durationValue: 30, // The numeric value for duration
      durationUnit: 'hours', // The unit: 'seconds', 'minutes', or 'hours'
      useManualDuration: false, // Default to automatic duration based on simulation time
      hoveredPhysicsAnomaly: null, // Track which anomaly row is being hovered

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
      physicsSimDurationSeconds: 'getPhysicsSimDurationSeconds',
      simulationTime: 'getSimulationTime',
    }),

    // Parse simulation time (T+DD:HH:MM or T-DD:HH:MM) and convert to seconds
    autoSimDurationSeconds() {
      const simTime = this.simulationTime;
      if (!simTime || typeof simTime !== 'string') {
        return 3600; // Default to 1 hour if no simulation time available
      }

      // Parse T+DD:HH:MM or T-DD:HH:MM format
      const match = simTime.match(/^T([+-])(\d{2}):(\d{2}):(\d{2})$/);
      if (!match) {
        return 3600; // Default if format doesn't match
      }

      const [, sign, days, hours, minutes] = match;
      const totalSeconds = (parseInt(days) * 86400) + (parseInt(hours) * 3600) + (parseInt(minutes) * 60);
      
      // If simulation is before T+0, use default
      if (sign === '-') {
        return 3600;
      }

      return totalSeconds;
    },

    // Display auto duration in a human-readable format
    autoSimDurationDisplay() {
      const seconds = this.autoSimDurationSeconds;
      const days = Math.floor(seconds / 86400);
      const hours = Math.floor((seconds % 86400) / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);

      const parts = [];
      if (days > 0) parts.push(`${days}d`);
      if (hours > 0) parts.push(`${hours}h`);
      if (minutes > 0) parts.push(`${minutes}m`);

      return parts.length > 0 ? parts.join(' ') : '0m';
    },

    // Actual duration to use for physics diagnosis
    effectiveSimDurationSeconds() {
      if (this.useManualDuration) {
        // Use manual input
        let durationInSeconds;
        switch (this.durationUnit) {
          case 'seconds':
            durationInSeconds = this.durationValue;
            break;
          case 'minutes':
            durationInSeconds = this.durationValue * 60;
            break;
          case 'hours':
            durationInSeconds = this.durationValue * 3600;
            break;
          default:
            durationInSeconds = this.durationValue;
        }
        return durationInSeconds;
      } else {
        // Use automatic duration based on simulation time
        return this.autoSimDurationSeconds;
      }
    },

    // Vue Plotly data for physics diagnosis graph
    physicsPlotData() {
      console.log("🔍 physicsPlotData computed property called");
      console.log("🔍 telemetryGraphData:", this.telemetryGraphData);
      
      if (!this.telemetryGraphData || !this.telemetryGraphData.actual) {
        console.log("⚠️ No telemetry graph data available");
        return [];
      }

      const plotData = [];

      // Use absolute simulation time labels directly from backend (T+DD:HH:MM format)
      const timeLabels = this.telemetryGraphData.timeLabels || [];
      console.log("🔍 Using absolute simulation time labels:", timeLabels);

      // Add actual telemetry data
      if (this.telemetryGraphData.actual && this.telemetryGraphData.actual.length > 0) {
        plotData.push({
          x: timeLabels.length > 0 ? timeLabels : Array.from({length: this.telemetryGraphData.actual.length}, (_, i) => `T+00:00:${i.toString().padStart(2, '0')}`),
          y: this.telemetryGraphData.actual,
          type: 'scatter',
          mode: 'lines+markers',
          name: 'Actual Telemetry',
          line: { color: '#0AFEFF', width: 3 },
          marker: { size: 6, color: '#0AFEFF' },
          hovertemplate: '<b>%{fullData.name}</b><br>' +
                        'Value: %{y:.2f} mmHg<br>' +
                        'Sim Time: %{x}<br>' +
                        '<extra></extra>'
        });
      }

      // Add simulated anomaly data for selected anomalies
      if (this.telemetryGraphData.simulated) {
        Object.entries(this.telemetryGraphData.simulated)
          .filter(([name]) => this.selectedPhysicsAnomalies.indexOf(name) !== -1)
          .forEach(([anomalyName, anomalyData]) => {
            if (anomalyData.data && anomalyData.data.length > 0) {
              // Create data with proper fault injection time positioning
              const faultInjectionTime = anomalyData.faultInjectionTime || 0;
              const totalLength = this.telemetryGraphData.actual.length;
              
              // Get the absolute simulation time for the fault injection
              const faultTimeLabel = timeLabels.length > 0 && faultInjectionTime < timeLabels.length 
                ? timeLabels[faultInjectionTime] 
                : `T+00:00:${faultInjectionTime.toString().padStart(2, '0')}`;
              
              // Create x-axis labels that account for fault injection time
              const xLabels = [];
              const yValues = [];
              
              for (let i = 0; i < totalLength; i++) {
                if (i < faultInjectionTime) {
                  // Before fault injection: transparent data (no visible points)
                  xLabels.push(timeLabels.length > 0 ? timeLabels[i] : `T+00:00:${i.toString().padStart(2, '0')}`);
                  yValues.push(null); // null values won't be plotted
                } else {
                  // After fault injection: actual simulation data
                  const simIndex = i - faultInjectionTime;
                  if (simIndex < anomalyData.data.length) {
                    xLabels.push(timeLabels.length > 0 ? timeLabels[i] : `T+00:00:${i.toString().padStart(2, '0')}`);
                    yValues.push(anomalyData.data[simIndex]);
                  } else {
                    // Beyond simulation data
                    xLabels.push(timeLabels.length > 0 ? timeLabels[i] : `T+00:00:${i.toString().padStart(2, '0')}`);
                    yValues.push(null);
                  }
                }
              }
              
              plotData.push({
                x: xLabels,
                y: yValues,
                type: 'scatter',
                mode: 'lines+markers',
                name: `${anomalyName} (Fault at ${faultTimeLabel})`,
                line: { 
                  width: 3,
                  color: anomalyData.color  // Use solid color for line
                },
                marker: { 
                  size: 6, 
                  color: anomalyData.color  // Use solid color for markers
                },
                hovertemplate: '<b>%{fullData.name}</b><br>' +
                              'Value: %{y:.2f} mmHg<br>' +
                              'Sim Time: %{x}<br>' +
                              '<extra></extra>'
              });
              
              // Add a vertical line to mark fault injection point
              if (faultInjectionTime > 0 && faultInjectionTime < totalLength) {
                plotData.push({
                  x: [faultTimeLabel, faultTimeLabel],
                  y: [0, 8], // Full y-axis range
                  type: 'scatter',
                  mode: 'lines',
                  name: `${anomalyName} Fault Injection`,
                  line: { 
                    color: anomalyData.color, 
                    width: 2, 
                    dash: 'dash',
                    opacity: 0.6
                  },
                  showlegend: false,
                  hoverinfo: 'skip'
                });
              }
            }
          });
      }

      return plotData;
    },

    // Vue Plotly layout for physics diagnosis graph
    physicsPlotLayout() {
      // Get diagnosis run time from telemetry graph data
      const diagnosisRunTime = this.telemetryGraphData.diagnosis_run_time || '';
      const titleSuffix = diagnosisRunTime ? ` (Diagnosis Run: ${diagnosisRunTime})` : '';
      
      // Get sensor name and unit from telemetry metadata
      const telemetryMetadata = this.telemetryGraphData.telemetry_metadata || {};
      const targetSensor = telemetryMetadata.target_sensor || 'Sensor';
      const unit = telemetryMetadata.unit || 'units';
      const yAxisTitle = `${targetSensor} (${unit})`;
      
      return {
        title: {
          text: `Telemetry Trend Comparison (with Fault Injection Times)${titleSuffix}`,
          font: { color: '#0AFEFF', size: 16 },
          x: 0.5
        },
        plot_bgcolor: '#001e1e',
        paper_bgcolor: '#001e1e',
        font: { color: '#ccc' },
        xaxis: {
          title: 'Absolute Simulation Time (T+DD:HH:MM)',
          gridcolor: '#333',
          zerolinecolor: '#666',
          showline: true,
          linecolor: '#666',
          tickangle: -45,
          tickfont: { size: 10 },
          // Let plotly automatically determine tick spacing for absolute time
          tickmode: 'auto',
          nticks: 10
        },
        yaxis: {
          title: yAxisTitle,
          gridcolor: '#333',
          zerolinecolor: '#666',
          showline: true,
          linecolor: '#666',
          autorange: true,  // Let Plotly automatically determine the range based on data
          tickfont: { size: 10 }
        },
        margin: { l: 60, r: 150, t: 80, b: 80 }, // Increased top margin for longer title
        showlegend: true,
        legend: {
          x: 1.08, // Moved further to the right (was 1.02)
          y: 1,
          xanchor: 'left',
          yanchor: 'top',
          bgcolor: 'rgba(0, 30, 30, 0.9)',
          bordercolor: '#0AFEFF',
          borderwidth: 1,
          font: { color: '#ccc', size: 11 }
        },
        hovermode: 'closest',
        hoverlabel: {
          bgcolor: 'rgba(0, 30, 30, 0.95)',
          bordercolor: '#0AFEFF',
          font: { color: '#fff' }
        },
        // Ensure the plot can expand to full width
        width: null,
        height: null,
        // Add annotations for fault injection points
        annotations: this.getFaultInjectionAnnotations()
      };
    },
    
    // Computed property to determine which physics image to display
    physicsComponentImage() {
      // Get the most probable anomaly from the active tab
      const activeTab = this.simpleTabs[this.activeSimpleTab];
      if (!activeTab || !activeTab.physicsDiagnosisData) {
        return null; // Default fallback
      }
      
      // Use hovered anomaly if available, otherwise use the first (most probable) anomaly
      const componentAnomalies = activeTab.physicsDiagnosisData.componentAnomalies || [];
      let anomalyToDisplay;
      
      if (this.hoveredPhysicsAnomaly) {
        // Use the hovered anomaly
        anomalyToDisplay = this.hoveredPhysicsAnomaly;
      } else if (componentAnomalies.length > 0) {
        // Default to first anomaly in the list
        anomalyToDisplay = componentAnomalies[0].name;
      } else {
        // No anomalies available
        return null;
      }
      
      // Extract component names from the anomaly name
      // Examples: "VCCR Failure" -> ["VCCR"], "VCCR + Dehumidifier" -> ["VCCR", "Dehumidifier"]
      const componentNames = anomalyToDisplay
        .split('+')
        .map(part => {
          // Extract first word (component name) and capitalize properly
          const words = part.trim().split(/\s+/);
          return words[0]; // e.g., "VCCR", "Dehumidifier"
        });
      
      console.log('Component names extracted:', componentNames);
      console.log('Available images:', Object.keys(componentImages));
      
      // Try to find exact match for combination (e.g., "Dehumidifier_VCCR" or "VCCR_Dehumidifier")
      if (componentNames.length > 1) {
        // Try all permutations of component order
        const permutations = [
          componentNames.join('_'),           // e.g., "VCCR_Dehumidifier"
          componentNames.reverse().join('_')  // e.g., "Dehumidifier_VCCR"
        ];
        
        for (const permutation of permutations) {
          // Case-insensitive search
          const matchingKey = Object.keys(componentImages).find(
            key => key.toLowerCase() === permutation.toLowerCase()
          );
          
          if (matchingKey) {
            console.log('Found combination image:', matchingKey);
            return componentImages[matchingKey].default || null;
          }
        }
      }
      
      // Try to find single component match (e.g., "VCCR" -> "VCCR.png")
      if (componentNames.length === 1) {
        const componentName = componentNames[0];
        const matchingKey = Object.keys(componentImages).find(
          key => key.toLowerCase() === componentName.toLowerCase()
        );
        
        if (matchingKey) {
          console.log('Found single component image:', matchingKey);
          return componentImages[matchingKey].default || null;
        }
      }
      
      // Fallback to CDRA if no match found
      console.log('No matching image found, using CDRA fallback');
      return null;
    },
    
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

    formatSimilarityScore(scoreStr) {
      if (!scoreStr || scoreStr === 'N/A') {
        return 'N/A';
      }
      
      // Remove % sign if present and convert to number
      const score = parseFloat(scoreStr.toString().replace('%', ''));
      
      if (isNaN(score)) {
        return 'N/A';
      }
      
      // If it's already in decimal form (< 1), use it directly
      // Otherwise convert from percentage to decimal
      const decimalScore = score > 1 ? score / 100 : score;
      
      return `${decimalScore.toFixed(3)}/1.0`;
    },

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
    
    handlePhysicsDiagnosisFromChatbot(event) {
      /**
       * Handle physics diagnosis completion from chatbot.
       * This method is called when the chatbot completes a physics diagnosis
       * and emits the 'physicsDiagnosisCompleted' event.
       */
      try {
        console.log("🎯 Physics Diagnosis from Chatbot - Event received:", event);
        
        const { diagnosisReport, physicsDiagnosisData } = event.detail;
        
        if (diagnosisReport && physicsDiagnosisData) {
          console.log("📊 Processing physics diagnosis data from chatbot...");
          console.log("📊 physicsDiagnosisData received:", physicsDiagnosisData);
          console.log("📊 componentAnomalies:", physicsDiagnosisData.componentAnomalies);
          if (physicsDiagnosisData.componentAnomalies && physicsDiagnosisData.componentAnomalies.length > 0) {
            console.log("📊 First anomaly:", physicsDiagnosisData.componentAnomalies[0]);
          }
          
          // Check if a physics diagnosis tab already exists
          const existingPhysicsTabIndex = this.simpleTabs.findIndex(tab => 
            tab.label === "Physics Diagnosis (Chatbot)"
          );
          
          if (existingPhysicsTabIndex !== -1) {
            // Update existing tab
            console.log("🔄 Updating existing physics diagnosis tab");
            this.simpleTabs[existingPhysicsTabIndex] = {
              label: "Physics Diagnosis (Chatbot)",
              content: "Physics diagnosis completed via chatbot. Results are displayed below.",
              isChatbotResult: true,
              diagnosisReport: diagnosisReport,
              physicsDiagnosisData: physicsDiagnosisData
            };
            this.activeSimpleTab = existingPhysicsTabIndex;
          } else {
            // Create new tab
            console.log("🆕 Creating new physics diagnosis tab for chatbot results");
            this.simpleTabs.push({
              label: "Physics Diagnosis (Chatbot)",
              content: "Physics diagnosis completed via chatbot. Results are displayed below.",
              isChatbotResult: true,
              diagnosisReport: diagnosisReport,
              physicsDiagnosisData: physicsDiagnosisData
            });
            this.activeSimpleTab = this.simpleTabs.length - 1;
          }
          
          console.log("✅ Physics diagnosis tab created/updated successfully");
          
          // Show success message
          this.$store.commit('addDialoguePiece', {
            "voice_message": "Physics diagnosis results are now displayed in a new tab.",
            "visual_message_type": ["text"],
            "visual_message": ["Physics diagnosis results are now displayed in a new tab."],
            "writer": "daphne"
          });
          
        } else {
          console.error("❌ Invalid event data received from chatbot");
        }
        
               } catch (error) {
           console.error("❌ Error handling physics diagnosis from chatbot:", error);
           
           // Show error message
           this.$store.commit('addDialoguePiece', {
             "voice_message": "Error processing physics diagnosis results from chatbot.",
             "visual_message_type": ["text"],
             "visual_message": ["Error processing physics diagnosis results from chatbot."],
             "writer": "daphne"
           });
         }
       },
       
       viewFullPhysicsResults() {
         /**
          * Navigate to the full physics diagnosis results.
          * This method is called when the user clicks the "View Full Physics Diagnosis Results" button
          * in the chatbot results tab.
          */
         try {
           console.log("🔍 User requested to view full physics diagnosis results");
           
           // Find the physics diagnosis tab (if it exists)
           const physicsTabIndex = this.simpleTabs.findIndex(tab => 
             tab.label === "Physics Diagnosis" && !tab.isChatbotResult
           );
           
           if (physicsTabIndex !== -1) {
             // Switch to the existing physics diagnosis tab
             console.log("🔄 Switching to existing physics diagnosis tab");
             this.activeSimpleTab = physicsTabIndex;
           } else {
             // Create a new physics diagnosis tab with the data from the chatbot
             console.log("🆕 Creating new physics diagnosis tab with chatbot data");
             
             // Get the chatbot results data
             const chatbotTab = this.simpleTabs.find(tab => tab.isChatbotResult);
             if (chatbotTab && chatbotTab.diagnosisReport) {
               // Create a new tab with the full physics diagnosis content
               this.simpleTabs.push({
                 label: "Physics Diagnosis",
                 content: "Full physics diagnosis results from chatbot command.",
                 isChatbotResult: false,
                 diagnosisReport: chatbotTab.diagnosisReport
               });
               this.activeSimpleTab = this.simpleTabs.length - 1;
               
               // Show success message
               this.$store.commit('addDialoguePiece', {
                 "voice_message": "Switched to full physics diagnosis results view.",
                 "visual_message_type": ["text"],
                 "visual_message": ["Switched to full physics diagnosis results view."],
                 "writer": "daphne"
               });
             } else {
               console.error("❌ No chatbot diagnosis report found");
             }
           }
           
         } catch (error) {
           console.error("❌ Error viewing full physics diagnosis results:", error);
           
           // Show error message
           this.$store.commit('addDialoguePiece', {
             "voice_message": "Error viewing full physics diagnosis results.",
             "visual_message_type": ["text"],
             "visual_message": ["Error viewing full physics diagnosis results."],
             "writer": "daphne"
           });
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
            console.log("Instruction type:", instructionData.instructionType);
            
            // Check if this is a new instruction
            const isNewInstruction = this.instructionIdentifier != instructionData.instructionIdentifier;
            const needsProcessing = isNewInstruction || !this.lastInstructionProcessed;
            
            if (needsProcessing) {
              // Update tracking variables
              this.instructionIdentifier = instructionData.instructionIdentifier;
              console.log("Current instruction identifier is set:", this.instructionIdentifier, instructionData.instructionIdentifier);
              this.lastInstructionProcessed = false;
              
              // Handle different instruction types based on actual JSON structure
              if (instructionData.instructionType === "manualInstruction") {
                // Handle manual instructions
                if (isNewInstruction) {
                  this.handleManualInstruction(instructionData);
                }
              } else if (instructionData.instructionType === "record") {
                // Handle record instructions  
                if (isNewInstruction) {
                  this.handleRecordInstruction(instructionData);
                  
                  // Set up listener for user response
                  if (!this.userResponseListener) {
                    this.setupUserResponseListener();
                  }
                }
              } else if (instructionData.userResponseType && 
                        instructionData.userResponseType.length > 0 && 
                        instructionData.userResponseType[0] === "real") {
                // Legacy handling for "real" userResponseType
                if (isNewInstruction) {
                  this.$store.commit('addDialoguePiece', {
                    "voice_message": `${instructionData.text} Please provide a numerical value.`,
                    "visual_message_type": ["text"],
                    "visual_message": [`${instructionData.text} Please provide a numerical value.`],
                    "writer": "daphne"
                  });
                  
                  // Set up listener for user response
                  if (!this.userResponseListener) {
                    this.setupUserResponseListener();
                  }
                }
              } else {
                // Unknown instruction type - log for debugging
                console.log("Unknown instruction type or format:", instructionData);
              }
            }
          }
        }
      } catch (error) {
        console.error('Error getting Astrobee status:', error);
      }
    },

    updatePhysicsSimDuration() {
      // Use the effective duration (either manual or automatic)
      this.localPhysicsSimDuration = this.effectiveSimDurationSeconds;
      
      console.log(`Physics simulation duration updated: ${this.effectiveSimDurationSeconds} seconds (manual mode: ${this.useManualDuration})`);
    },
    
    setupUserResponseListener() {
      // Set up store subscription to listen for user messages
      this.userResponseListener = this.$store.subscribe((mutation, state) => {
        if (mutation.type === 'addDialoguePiece') {
          const newMessage = mutation.payload;
          
          // Process only if we're waiting for a response and this is a user message
          // BUT exclude manual instruction completion responses ("Completed")
          if (!this.lastInstructionProcessed && 
              this.instructionIdentifier !== null &&
              newMessage.writer === 'user' &&
              newMessage.visual_message[0] !== 'Completed') {
            
            this.processUserResponse(newMessage.visual_message[0]);
          }
        }
      });
    },

    /*
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
    */

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

    // New instruction handling methods for PRIDE API integration
    handleManualInstruction(instructionData) {
      console.log("Handling manual instruction:", instructionData);
      
      // Store the current instruction
      this.currentInstruction = instructionData;
      
      // Show manual instruction prompt to user via chat with completion button
      this.$store.commit('addDialoguePiece', {
        "voice_message": `${instructionData.text}. Please click the completed button after finishing.`,
        "visual_message_type": ["text"],
        "visual_message": [`${instructionData.text}. Please click the completed button after finishing.`],
        "writer": "daphne",
        "options": ["Completed"],
        "optionsCallbackEvent": "manualInstructionCompleted"
      });
      
      // Set up listener for completion button click
      if (!this.manualInstructionListener) {
        this.$root.$on('manualInstructionCompleted', this.handleManualInstructionCompletion);
        this.manualInstructionListener = true;
      }
    },

    handleRecordInstruction(instructionData) {
      console.log("Handling record instruction:", instructionData);
      
      // Store the current instruction
      this.currentInstruction = instructionData;
      
      // For record instructions, always expect numerical input
      this.$store.commit('addDialoguePiece', {
        "voice_message": `${instructionData.text}. Please provide a numerical value.`,
        "visual_message_type": ["text"],
        "visual_message": [`${instructionData.text}. Please provide a numerical value.`],
        "writer": "daphne"
      });
    },

    async completeManualInstruction() {
      try {
        console.log("Completing manual instruction");
        
        const reqData = new FormData();
        reqData.append('instruction_data', JSON.stringify(this.currentInstruction));
        reqData.append('activity', 'complete');
        
        const response = await fetchPost('/api/at/complete_instruction', reqData);
        
        if (response.ok) {
          console.log("Manual instruction completed successfully");
          
          // Mark as processed
          this.lastInstructionProcessed = true;
          
          // Show confirmation to user
          this.$store.commit('addDialoguePiece', {
            "voice_message": "Instruction completed successfully.",
            "visual_message_type": ["text"],
            "visual_message": ["Instruction completed successfully."],
            "writer": "daphne"
          });
        } else {
          console.error("Failed to complete manual instruction");
          this.$store.commit('addDialoguePiece', {
            "voice_message": "Failed to complete instruction. Please try again.",
            "visual_message_type": ["text"],
            "visual_message": ["Failed to complete instruction. Please try again."],
            "writer": "daphne"
          });
        }
      } catch (error) {
        console.error('Error completing manual instruction:', error);
      }
    },

    handleManualInstructionCompletion(response) {
      if (response === "Completed") {
        // User clicked the "Completed" button
        this.completeManualInstruction();
        
        // Clean up event listener
        this.$root.$off('manualInstructionCompleted', this.handleManualInstructionCompletion);
        this.manualInstructionListener = false;
      }
    },

    async processUserResponse(message) {
      try {
        // Check if we have a record instruction waiting for user input
        if (this.currentInstruction && 
            this.currentInstruction.instructionType === "record" && 
            !this.lastInstructionProcessed) {
          
          // For record instructions, always expect numerical input
          const numValue = parseFloat(message);
          if (!isNaN(numValue)) {
            const userValue = numValue;
            
            console.log("Processing user response for record instruction:", userValue);
            
            // Mark as processed to avoid duplicate handling
            this.lastInstructionProcessed = true;
            
            // Send completion with record value
            const reqData = new FormData();
            reqData.append('instruction_data', JSON.stringify(this.currentInstruction));
            reqData.append('activity', 'complete');
            reqData.append('record_value', userValue.toString());
            
            const response = await fetchPost('/api/at/complete_instruction', reqData);
            
            if (response.ok) {
              console.log("Record instruction completed successfully");
              
              // Confirm receipt to user
              this.$store.commit('addDialoguePiece', {
                "voice_message": `Thank you, I've recorded your value: ${userValue}.`,
                "visual_message_type": ["text"],
                "visual_message": [`Thank you, I've recorded your value: ${userValue}.`],
                "writer": "daphne"
              });
            } else {
              console.error("Failed to complete record instruction");
              this.$store.commit('addDialoguePiece', {
                "voice_message": "Failed to record your response. Please try again.",
                "visual_message_type": ["text"],
                "visual_message": ["Failed to record your response. Please try again."],
                "writer": "daphne"
              });
            }
          } else {
            // Not a valid number
            this.$store.commit('addDialoguePiece', {
              "voice_message": "I need a numerical value. Please try again.",
              "visual_message_type": ["text"],
              "visual_message": ["I need a numerical value. Please try again."],
              "writer": "daphne"
            });
            // Keep instruction as unprocessed so we'll try again
            this.lastInstructionProcessed = false;
          }
          
          return;
        }

        // Original logic for legacy "real" userResponseType handling
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
      
      // Get the diagnosis report from store
      const diagnosisReport = this.$store.getters.getDiagnosisReport;
      
      // Add a simple tab with KG diagnosis content and store the data
      this.simpleTabs.push({
        label: "KG Diagnosis",
        type: "kg",
        content: "KG diagnosis result goes here.",
        diagnosisData: diagnosisReport, // Store the diagnosis data in the tab
        checked: [], // Store the checked anomalies for this tab
        allSelected: false // Store the select all state for this tab
      });
      this.activeSimpleTab = this.simpleTabs.length - 1;
      
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
        // Update store with effective duration (either manual or auto based on simulation time)
        const durationToUse = this.effectiveSimDurationSeconds;
        console.log(`🔍 Using simulation duration: ${durationToUse} seconds (manual mode: ${this.useManualDuration})`);
        this.$store.commit('mutatePhysicsSimDurationSeconds', durationToUse);
        
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
              isHighlighted: anomaly.is_highlighted,
              faultInjectionTime: anomaly.fault_injection_time,
              faultInjectionTimeSeconds: anomaly.fault_injection_time_seconds,
              fault_injection_time_absolute: anomaly.fault_injection_time_absolute
            }))
          };
          this.$store.commit('mutatePhysicsDiagnosisData', physicsDiagnosisData);

          // Convert telemetry data from backend
          const telemetryGraphData = {
            actual: diagnosisReport.physics_diagnosis_data.actual_telemetry,
            simulated: {},
            diagnosis_run_time: diagnosisReport.physics_diagnosis_data.diagnosis_run_time,
            t_zero: diagnosisReport.physics_diagnosis_data.t_zero,
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
              score: parseFloat(anomaly.score),
              faultInjectionTime: anomaly.fault_injection_time,
              faultInjectionTimeSeconds: anomaly.fault_injection_time_seconds,
              fault_injection_time_absolute: anomaly.fault_injection_time_absolute
            };
          });
          this.$store.commit('mutateTelemetryGraphData', telemetryGraphData);

          // Initialize selection to all anomalies on first load
          this.selectedPhysicsAnomalies = physicsDiagnosisData.componentAnomalies.map(a => a.name);

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
          type: "physics",
          content: "Physics diagnosis result goes here.",
          diagnosisData: diagnosisReport, // Store the diagnosis data in the tab
          physicsDiagnosisData: this.$store.getters.getPhysicsDiagnosisData, // Store physics-specific data
          telemetryGraphData: this.$store.getters.getTelemetryGraphData // Store telemetry data
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
      
      // Debug logging
      if (this.showPhysicsExplanation) {
        console.log("📊 Showing physics explanation...");
        console.log("📊 telemetryGraphData:", this.telemetryGraphData);
        console.log("📊 selectedPhysicsAnomalies:", this.selectedPhysicsAnomalies);
        console.log("📊 physicsPlotData:", this.physicsPlotData);
      }
    },

    generateTelemetryDataForAnomalies() {
      // This method is now disabled - data should come from backend
      console.warn("Frontend telemetry data generation is disabled. Data should come from backend.");
      return false;
    },

    generateBetterXAxisTicks() {
      // Generate better-spaced X-axis ticks to reduce clutter
      if (!this.telemetryGraphData || !this.telemetryGraphData.actual) {
        return { tickvals: [], ticktext: [] };
      }
      
      const totalPoints = this.telemetryGraphData.actual.length;
      
      // For better spacing, use fewer ticks with more strategic placement
      let tickvals = [];
      let ticktext = [];
      
      if (totalPoints <= 5) {
        // For very short data, show all points
        for (let i = 0; i < totalPoints; i++) {
          tickvals.push(i);
          ticktext.push(this.formatTimeLabel(i, totalPoints));
        }
      } else {
        // For longer data, use strategic spacing
        const targetTicks = 6; // Optimal number of ticks for good spacing
        
        // Always include first and last
        tickvals.push(0);
        ticktext.push(this.formatTimeLabel(0, totalPoints));
        
        // Calculate optimal spacing for intermediate ticks
        const step = Math.max(1, Math.floor(totalPoints / (targetTicks - 1)));
        
        // Add intermediate ticks with better distribution
        for (let i = step; i < totalPoints - 1; i += step) {
          tickvals.push(i);
          ticktext.push(this.formatTimeLabel(i, totalPoints));
        }
        
        // Always include the last point
        if (totalPoints > 1) {
          tickvals.push(totalPoints - 1);
          ticktext.push(this.formatTimeLabel(totalPoints - 1, totalPoints));
        }
        
        // Ensure we don't have too many ticks close together at the end
        if (tickvals.length > 2) {
          const lastTick = tickvals[tickvals.length - 1];
          const secondLastTick = tickvals[tickvals.length - 2];
          
          // If last two ticks are too close, remove the second-to-last
          if (lastTick - secondLastTick < Math.floor(totalPoints / 8)) {
            tickvals.splice(tickvals.length - 2, 1);
            ticktext.splice(ticktext.length - 2, 1);
          }
        }
      }
      
      return { tickvals, ticktext };
    },
    
    formatTimeLabel(index, totalLength) {
      // Format time label as "-MM:SS" for better readability
      const timeGap = totalLength - index - 1;
      const minutes = Math.floor(timeGap / 60);
      const seconds = timeGap % 60;
      return `-${minutes}:${seconds.toString().padStart(2, '0')}`;
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


    async requestDiagnosis() {
      this.allSelected = false;
      this.isLoading = true;
      this.explaining = false;
      this.checked = [];
      await this.$store.dispatch('requestDiagnosis', this.selectedSymptomsList);

      const diagnosisReport = this.$store.getters.getDiagnosisReport;
      
      // Set initial values (best evidence may be null initially)
      this.unconfirmedSymptoms = diagnosisReport.hidden_components || [];
      this.bestEvidence = diagnosisReport.best_evidence;     
      this.currentTelemetryValues = diagnosisReport.current_telemetry_values;
      this.activeDiagnosticTab = this.diagnosticHistory.length;
      
      this.diagnosticHistory.push(diagnosisReport);
      console.log("Set active diagnostic tab to:", this.activeDiagnosticTab);
      
      // Add a simple tab with Bayesian diagnosis content
      this.simpleTabs.push({
        label: "Bayesian Diagnosis",
        type: "bayesian",
        content: "Bayesian diagnosis result goes here.",
        diagnosisData: diagnosisReport,
        checked: [],
        allSelected: false
      });
      this.activeSimpleTab = this.simpleTabs.length - 1;
      
      this.isLoading = false;
      
      // Get the most probable anomaly from the diagnosis report
      const topAnomaly = diagnosisReport.diagnosis_list && diagnosisReport.diagnosis_list.length > 0 
        ? diagnosisReport.diagnosis_list[0] 
        : null;
      
      // Special handling for "Loss of Pressure" anomaly
      if (topAnomaly && topAnomaly.anomaly.includes("Loss of Pressure")) {
        // For Loss of Pressure, ask about leak detection directly
        this.$store.commit('addDialoguePiece', {
          "voice_message": `${topAnomaly.anomaly} is the most probable scenario with ${(topAnomaly.probability * 100).toFixed(1)}% probability. There is no additional sub-component to improve diagnosis confidence. Do you want me to check if there is any leak?`,
          "visual_message_type": ["text"],
          "visual_message": [`${topAnomaly.anomaly} is the most probable scenario with ${(topAnomaly.probability * 100).toFixed(1)}% probability. There is no additional sub-component to improve diagnosis confidence. Do you want me to check if there is any leak?`],
          "writer": "daphne",
          "options": ["Yes", "No"],
          "optionsCallbackEvent": "lossOfPressureResponse"
        });
        
        // Set up listener for loss of pressure response
        this.setupLossOfPressureListener(topAnomaly);
      } 
      // For other anomalies with significant probability, suggest physics-based analysis
      else if (topAnomaly && topAnomaly.probability > 0.4 && topAnomaly.anomaly !== "No Anomalies Present") {
        // Set up listener for physics analysis response and get unique event name
        const uniqueEventName = this.setupPhysicsAnalysisListener(topAnomaly);
        
        this.$store.commit('addDialoguePiece', {
          "voice_message": `${topAnomaly.anomaly} is the most probable scenario with ${(topAnomaly.probability * 100).toFixed(1)}% probability. Do you want to run physics-based analysis to determine which subcomponent is likely to have failed?`,
          "visual_message_type": ["text"],
          "visual_message": [`${topAnomaly.anomaly} is the most probable scenario with ${(topAnomaly.probability * 100).toFixed(1)}% probability. Do you want to run physics-based analysis to determine which subcomponent is likely to have failed?`],
          "writer": "daphne",
          "options": ["Yes", "No"],
          "optionsCallbackEvent": uniqueEventName
        });
      } else {
        // No significant anomaly detected or "No Anomalies Present"
        this.$store.commit('addDialoguePiece', {
          "voice_message": `The diagnosis is complete. No significant anomaly requiring further analysis was detected.`,
          "visual_message_type": ["text"],
          "visual_message": [`The diagnosis is complete. No significant anomaly requiring further analysis was detected.`],
          "writer": "daphne",
        });
      }
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

    setupPhysicsAnalysisListener(topAnomaly) {
      // Create a unique event name for this specific diagnosis to prevent multiple listeners from firing
      const uniqueEventName = `physicsAnalysisResponse_${Date.now()}_${Math.random()}`;
      
      // Set up listener for physics analysis response
      this.$root.$once(uniqueEventName, async (response) => {
        if (response === 'Yes') {
          this.$store.commit('addDialoguePiece', {
            "voice_message": "Running physics-based analysis...",
            "visual_message_type": ["text"],
            "visual_message": ["Running physics-based analysis..."],
            "writer": "daphne"
          });

          // Run physics diagnosis using the existing function
          // Note: runPhysicsDiagnosisForAnomaly now handles the robot inspection prompt
          try {
            await this.runPhysicsDiagnosisForAnomaly(topAnomaly.anomaly, topAnomaly.probability);
          } catch (error) {
            console.error("Error running physics diagnosis:", error);
            this.$store.commit('addDialoguePiece', {
              "voice_message": "I encountered an error while running the physics-based analysis.",
              "visual_message_type": ["text"],
              "visual_message": ["I encountered an error while running the physics-based analysis."],
              "writer": "daphne"
            });
          }
        } else {
          this.$store.commit('addDialoguePiece', {
            "voice_message": "Understood. Let me know if you need anything else.",
            "visual_message_type": ["text"],
            "visual_message": ["Understood. Let me know if you need anything else."],
            "writer": "daphne"
          });
        }
      });
      
      // Return the unique event name so the dialog can use it
      return uniqueEventName;
    },

    setupRobotInspectionListener(component) {
      // Extract bayesianAnomaly if provided in component object
      const bayesianAnomaly = component.bayesianAnomaly;
      
      // Set up listener for robot inspection response
      this.$root.$once('robotInspectionResponse', async (response) => {
        if (response === 'Yes') {
          this.$store.commit('addDialoguePiece', {
            "voice_message": "Searching for inspection procedures...",
            "visual_message_type": ["text"],
            "visual_message": ["Searching for inspection procedures..."],
            "writer": "daphne"
          });

          try {
            // Get all available procedures from PRIDE
            const proceduresResponse = await fetchGet('/api/at/get_available_procedures');
            
            if (proceduresResponse.ok) {
              const data = await proceduresResponse.json();
              const allProcedures = data.procedures || [];
              console.log(`Total available procedures: ${allProcedures}`);
              
              // Split component name by '+' to handle multiple components
              const componentNames = component.anomaly.split('+').map(name => name.trim());
              console.log(`Searching for inspection procedures for components: ${componentNames.join(', ')}`);
              
              // Find inspection procedures for each component
              const allInspectionProcedures = [];
              
              for (const componentName of componentNames) {
                const componentNameLower = componentName.toLowerCase();
                const matchingProcedures = allProcedures.filter(proc => {
                  const titleLower = proc.title.toLowerCase();
                  console.log(`Checking procedure title: ${proc.title}`);
                  return titleLower.includes('inspection') && 
                         (titleLower.includes(componentNameLower) || 
                          titleLower.includes(componentNameLower.replace(' ', '')));
                });
                
                if (matchingProcedures.length > 0) {
                  allInspectionProcedures.push(...matchingProcedures);
                }
              }
              
              // Remove duplicates based on staticProcedureID
              const uniqueProcedures = Array.from(
                new Map(allInspectionProcedures.map(proc => [proc.staticProcedureID, proc])).values()
              );

              if (uniqueProcedures.length === 1) {
                // Only one procedure found - start it automatically
                const procedure = uniqueProcedures[0];
                
                this.$store.commit('addDialoguePiece', {
                  "voice_message": `I found the inspection procedure: ${procedure.title}. Starting it now...`,
                  "visual_message_type": ["text"],
                  "visual_message": [`I found the inspection procedure: ${procedure.title}. Starting it now...`],
                  "writer": "daphne"
                });

                // Start the procedure
                let reqData = new FormData();
                reqData.append('procedureID', procedure.staticProcedureID);
                const startResponse = await fetchPost('/api/at/start_astrobee_procedure', reqData);
                
                if (startResponse.ok) {
                  const startData = await startResponse.json();
                  console.log("Procedure start response data:", startData);
                  const runtimeID = startData.procedure_runtime_id; // Get the runtime ID from the response
                  
                  this.$store.commit('addDialoguePiece', {
                    "voice_message": `Procedure started successfully. I'll monitor its progress and check the results when it's complete.`,
                    "visual_message_type": ["text"],
                    "visual_message": [`Procedure started successfully. I'll monitor its progress and check the results when it's complete.`],
                    "writer": "daphne"
                  });

                  // Start polling for procedure completion and shared variables with runtimeID
                  this.monitorProcedureCompletion(component, runtimeID, null, bayesianAnomaly);
                } else {
                  this.$store.commit('addDialoguePiece', {
                    "voice_message": "I encountered an error while starting the procedure.",
                    "visual_message_type": ["text"],
                    "visual_message": ["I encountered an error while starting the procedure."],
                    "writer": "daphne"
                  });
                }
              } else if (uniqueProcedures.length > 1) {
                // Multiple procedures found - let user select which one(s) to run
                const procedureList = uniqueProcedures.map(proc => proc.title).join(', ');
                
                this.$store.commit('addDialoguePiece', {
                  "voice_message": `I found ${uniqueProcedures.length} inspection procedures: ${procedureList}. Please select which procedure(s) you'd like to run.`,
                  "visual_message_type": ["text"],
                  "visual_message": [`I found ${uniqueProcedures.length} inspection procedures for the identified components. Please select which procedure(s) you'd like to run.`],
                  "writer": "daphne"
                });
                
                // Show procedure selection dialog (you may need to implement this)
                // For now, just show the procedures in chat
                this.showProcedureSelection(uniqueProcedures, component);
              } else {
                // No procedures found
                this.$store.commit('addDialoguePiece', {
                  "voice_message": `No inspection procedure found for ${component.anomaly}.`,
                  "visual_message_type": ["text"],
                  "visual_message": [`No inspection procedure found for ${component.anomaly}.`],
                  "writer": "daphne"
                });
              }
            }
          } catch (error) {
            console.error("Error finding/starting inspection procedure:", error);
            this.$store.commit('addDialoguePiece', {
              "voice_message": "I encountered an error while searching for inspection procedures.",
              "visual_message_type": ["text"],
              "visual_message": ["I encountered an error while searching for inspection procedures."],
              "writer": "daphne"
            });
          }
        } else {
          this.$store.commit('addDialoguePiece', {
            "voice_message": "Understood. Let me know if you need anything else.",
            "visual_message_type": ["text"],
            "visual_message": ["Understood. Let me know if you need anything else."],
            "writer": "daphne"
          });
        }
      });
    },

    setupLossOfPressureListener(topAnomaly) {
      // Set up listener for loss of pressure leak check response
      this.$root.$once('lossOfPressureResponse', async (response) => {
        if (response === 'Yes') {
          this.$store.commit('addDialoguePiece', {
            "voice_message": "Starting the Pressure Leak External Inspection procedure...",
            "visual_message_type": ["text"],
            "visual_message": ["Starting the Pressure Leak External Inspection procedure..."],
            "writer": "daphne"
          });

          try {
            // Get all available procedures from PRIDE
            const proceduresResponse = await fetchGet('/api/at/get_available_procedures');
            
            if (proceduresResponse.ok) {
              const data = await proceduresResponse.json();
              const allProcedures = data.procedures || [];
              
              // Find the Pressure Leak External Inspection procedure (02.102)
              const leakProcedure = allProcedures.find(proc => 
                proc.title.includes('Pressure Leak External Inspection') || 
                proc.title.includes('02.102')
              );

              if (leakProcedure) {
                // Start the procedure
                let reqData = new FormData();
                reqData.append('procedureID', leakProcedure.staticProcedureID);
                const startResponse = await fetchPost('/api/at/start_astrobee_procedure', reqData);
                
                if (startResponse.ok) {
                  const startData = await startResponse.json();
                  const runtimeID = startData.procedure_runtime_id; // Get the runtime ID from the response
                  
                  this.$store.commit('addDialoguePiece', {
                    "voice_message": "Pressure leak inspection procedure started. I'll check the results when it's complete.",
                    "visual_message_type": ["text"],
                    "visual_message": ["Pressure leak inspection procedure started. I'll check the results when it's complete."],
                    "writer": "daphne"
                  });

                  // Start polling for procedure completion and leak detection with runtimeID
                  this.monitorLeakDetection(runtimeID);
                }
              } else {
                this.$store.commit('addDialoguePiece', {
                  "voice_message": "Could not find the Pressure Leak External Inspection procedure.",
                  "visual_message_type": ["text"],
                  "visual_message": ["Could not find the Pressure Leak External Inspection procedure."],
                  "writer": "daphne"
                });
              }
            }
          } catch (error) {
            console.error("Error starting leak detection procedure:", error);
            this.$store.commit('addDialoguePiece', {
              "voice_message": "I encountered an error while starting the leak detection procedure.",
              "visual_message_type": ["text"],
              "visual_message": ["I encountered an error while starting the leak detection procedure."],
              "writer": "daphne"
            });
          }
        } else {
          this.$store.commit('addDialoguePiece', {
            "voice_message": "Understood. Let me know if you need anything else.",
            "visual_message_type": ["text"],
            "visual_message": ["Understood. Let me know if you need anything else."],
            "writer": "daphne"
          });
        }
      });
    },

    /**
     * Unified procedure monitoring with Bayesian diagnosis update
     * 
     * This method provides a scalable framework for monitoring inspection procedures,
     * updating Bayesian diagnosis with results, and offering follow-up actions.
     * 
     * USAGE EXAMPLE - Adding a new inspection type:
     * 
     * async monitorTemperatureSensorCheck(runtimeID) {
     *   await this.monitorInspectionProcedure({
     *     runtimeID,
     *     sharedVariableName: 'sensorIsFaulty',
     *     bayesianAnomaly: 'Temperature Control Failure',
     *     tabLabel: 'Sensor Check',
     *     messages: {
     *       positiveVoice: `The sensor check detected a faulty sensor. I've updated the Bayesian diagnosis. Do you want to replace the sensor?`,
     *       negativeVoice: `The sensor check completed. The sensor is functioning normally.`,
     *       notFound: `The sensor check completed, but I couldn't retrieve the sensor status.`
     *     },
     *     followUp: {
     *       eventName: 'sensorReplacementResponse',
     *       setupListener: () => this.setupSensorReplacementListener()
     *     }
     *   });
     * }
     * 
     * @param {Object} config - Configuration object for the procedure
     * @param {string} config.runtimeID - The runtime ID of the procedure
     * @param {string} config.sharedVariableName - Name of the shared variable to check (e.g., 'filterisBad', 'leakDetected')
     * @param {string} config.bayesianAnomaly - Bayesian anomaly name for evidence key (e.g., 'CDRA Failure', 'Loss of Pressure')
     * @param {string} config.tabLabel - Label for the diagnosis tab (e.g., 'Inspection', 'Leak Check')
     * @param {Object} config.messages - Messages to display based on detection result
     * @param {string} config.messages.positiveVoice - Message when issue is detected
     * @param {string} config.messages.negativeVoice - Message when no issue is detected
     * @param {string} config.messages.notFound - Message when variable is not found
     * @param {Object} config.followUp - Optional follow-up configuration
     * @param {string} config.followUp.eventName - Event name for follow-up response
     * @param {Function} config.followUp.setupListener - Function to set up follow-up listener
     * @param {Function} config.completionCallback - Optional custom completion callback
     */
    async monitorInspectionProcedure(config) {
      const {
        runtimeID,
        sharedVariableName,
        bayesianAnomaly,
        tabLabel,
        messages,
        followUp,
        completionCallback
      } = config;

      const pollInterval = setInterval(async () => {
        try {
          // Check if procedure is still running
          const reqData = new FormData();
          reqData.append('runtimeID', runtimeID);
          
          const statusResponse = await fetchPost('/api/at/get_procedure_status', reqData);
          
          if (statusResponse.ok) {
            const statusData = await statusResponse.json();
            console.log(`Procedure status for ${runtimeID}:`, statusData.procedureStatus);
            
            // Only process when procedure is finished
            if (statusData.procedureStatus === 'finish') {
              clearInterval(pollInterval);
              console.log(`${tabLabel} procedure completed, checking shared variables...`);
              
              // If custom callback is provided, use it instead of default behavior
              if (completionCallback) {
                await completionCallback();
                return;
              }
              
              // Default behavior: check shared variables and update Bayesian diagnosis
              const response = await fetchPost('/api/at/get_shared_variables');
          
              if (response.ok) {
                const data = await response.json();
                const sharedVariables = data.shared_variables || [];
                
                // Look for the specified shared variable
                const variable = sharedVariables.find(v => v.label === sharedVariableName);
                
                if (variable) {
                  const issueDetected = variable.raw === 'true' || variable.raw === true;
                  
                  // Remove component suffix like "(IHab)" or "(HALO)" from bayesian anomaly name
                  const cleanedBayesianAnomaly = bayesianAnomaly.replace(/\s*\([^)]+\)\s*$/, '').trim();
                  
                  // Prepare hidden evidence key for Bayesian update
                  const hiddenEvidenceKey = `[HIDDEN] ${cleanedBayesianAnomaly} Component`;
                  
                  // Build additional evidence (4-5 for issue detected, 1-2 for no issue)
                  const additionalEvidence = {
                    [hiddenEvidenceKey]: issueDetected 
                      ? (Math.random() < 0.5 ? 4 : 5)
                      : (Math.random() < 0.5 ? 1 : 2)
                  };
                  
                  // Update Bayesian diagnosis with evidence
                  console.log(`Updating Bayesian diagnosis with ${tabLabel} evidence:`, additionalEvidence);
                  await this.$store.dispatch('requestDiagnosisWithEvidence', {
                    symptoms: this.lastSelectedSymptomsList,
                    additional_evidence: additionalEvidence
                  });
                  
                  // Get updated diagnosis report and add to tabs
                  const diagnosisReport = this.$store.getters.getDiagnosisReport;
                  this.unconfirmedSymptoms = diagnosisReport.hidden_components;
                  this.bestEvidence = diagnosisReport.best_evidence;
                  this.currentTelemetryValues = diagnosisReport.current_telemetry_values;
                  this.activeDiagnosticTab = this.diagnosticHistory.length;
                  this.diagnosticHistory.push(JSON.parse(JSON.stringify(diagnosisReport)));
                  
                  // Add a simple tab with updated Bayesian diagnosis content
                  const evidenceText = Object.keys(additionalEvidence).length > 0 
                    ? `Additional Evidence: ${Object.entries(additionalEvidence).map(([key, value]) => `${key}: ${this.formatEvidenceValue(value)}`).join(', ')}`
                    : '';
                  
                  this.simpleTabs.push({
                    label: `Bayesian Diagnosis (${tabLabel})`,
                    type: "bayesian",
                    content: `Updated Bayesian diagnosis after ${tabLabel.toLowerCase()}. ${evidenceText}`,
                    diagnosisData: diagnosisReport,
                    checked: [],
                    allSelected: false,
                    additionalEvidence: JSON.parse(JSON.stringify(additionalEvidence))
                  });
                  this.activeSimpleTab = this.simpleTabs.length - 1;
                  
                  // Display appropriate message based on detection result
                  const message = issueDetected ? messages.positiveVoice : messages.negativeVoice;
                  this.$store.commit('addDialoguePiece', {
                    "voice_message": message,
                    "visual_message_type": ["text"],
                    "visual_message": [message],
                    "writer": "daphne",
                    ...(issueDetected && followUp ? {
                      "options": ["Yes", "No"],
                      "optionsCallbackEvent": followUp.eventName
                    } : {})
                  });

                  // Set up follow-up listener if issue detected and follow-up is configured
                  if (issueDetected && followUp && followUp.setupListener) {
                    followUp.setupListener();
                  }
                } else {
                  console.warn(`${sharedVariableName} variable not found in shared variables`);
                  this.$store.commit('addDialoguePiece', {
                    "voice_message": messages.notFound,
                    "visual_message_type": ["text"],
                    "visual_message": [messages.notFound],
                    "writer": "daphne"
                  });
                }
              }
            }
          }
        } catch (error) {
          console.error(`Error monitoring ${tabLabel} procedure:`, error);
        }
      }, 5000); // Poll every 5 seconds
      
      // Stop polling after 10 minutes to prevent infinite loops
      setTimeout(() => clearInterval(pollInterval), 600000);
    },

    // Legacy wrapper methods for backward compatibility
    async monitorProcedureCompletion(component, runtimeID, completionCallback = null, bayesianAnomaly = null) {
      // Extract anomaly name from component or use provided bayesianAnomaly
      let anomalyName = bayesianAnomaly || '';
      
      // Handle multi-component anomalies
      if (anomalyName.includes('+')) {
        anomalyName = anomalyName.split('+')[0].trim();
      }

      await this.monitorInspectionProcedure({
        runtimeID,
        sharedVariableName: 'filterisBad',
        bayesianAnomaly: anomalyName,
        tabLabel: 'Inspection',
        messages: {
          positiveVoice: `The inspection procedure detected that the filter is bad. I've updated the Bayesian diagnosis with this information. Do you want to start the procedure for replacing the filter?`,
          negativeVoice: `The inspection procedure completed. The filter appears to be in good condition. I've updated the Bayesian diagnosis with this information.`,
          notFound: `The inspection procedure completed, but I couldn't retrieve the filter status.`
        },
        followUp: {
          eventName: 'filterReplacementResponse',
          setupListener: () => this.setupFilterReplacementListener()
        },
        completionCallback
      });
    },

    async monitorLeakDetection(runtimeID) {
      await this.monitorInspectionProcedure({
        runtimeID,
        sharedVariableName: 'leakDetected',
        bayesianAnomaly: 'Loss of Pressure',
        tabLabel: 'Leak Check',
        messages: {
          positiveVoice: `A leak has been detected. I've updated the Bayesian diagnosis with this information. Do you want to start the procedure for stopping the leak?`,
          negativeVoice: `The leak inspection procedure completed. No leak was detected. I've updated the Bayesian diagnosis with this information.`,
          notFound: `The leak inspection procedure completed, but I couldn't retrieve the leak detection status.`
        },
        followUp: {
          eventName: 'leakRepairResponse',
          setupListener: () => this.setupLeakRepairListener()
        }
      });
    },

    setupFilterReplacementListener() {
      this.$root.$once('filterReplacementResponse', async (response) => {
        if (response === 'Yes') {
          // Find and start the filter replacement procedure
          try {
            const proceduresResponse = await fetchGet('/api/at/get_available_procedures');
            
            if (proceduresResponse.ok) {
              const data = await proceduresResponse.json();
              const allProcedures = data.procedures || [];
              
              const replacementProcedure = allProcedures.find(proc => 
                proc.title.includes('Filter Swapout') || proc.title.includes('03.101')
              );

              if (replacementProcedure) {
                let reqData = new FormData();
                reqData.append('procedureID', replacementProcedure.staticProcedureID);
                const startResponse = await fetchPost('/api/at/start_astrobee_procedure', reqData);
                
                if (startResponse.ok) {
                  const startData = await startResponse.json();
                  const runtimeID = startData.procedure_runtime_id; // Get the runtime ID from the response
                  
                  this.$store.commit('addDialoguePiece', {
                    "voice_message": "Filter replacement procedure started. I'll monitor its progress and notify you when it's complete.",
                    "visual_message_type": ["text"],
                    "visual_message": ["Filter replacement procedure started. I'll monitor its progress and notify you when it's complete."],
                    "writer": "daphne"
                  });
                  
                  // Reuse monitorProcedureCompletion with a custom callback for filter replacement
                  this.monitorProcedureCompletion(null, runtimeID, async () => {
                    this.$store.commit('addDialoguePiece', {
                      "voice_message": "Filter replacement procedure has been completed successfully. Would you like to run Bayesian diagnosis to check if the anomaly was resolved?",
                      "visual_message_type": ["text"],
                      "visual_message": ["Filter replacement procedure has been completed successfully. Would you like to run Bayesian diagnosis to check if the anomaly was resolved?"],
                      "writer": "daphne",
                      "options": ["Yes", "No"],
                      "optionsCallbackEvent": "postReplacementDiagnosisResponse"
                    });
                    
                    // Set up listener for post-replacement diagnosis response
                    this.$root.$once('postReplacementDiagnosisResponse', async (diagnosisResponse) => {
                      if (diagnosisResponse === 'Yes') {
                        this.$store.commit('addDialoguePiece', {
                          "voice_message": "Running Bayesian diagnosis to verify the repair...",
                          "visual_message_type": ["text"],
                          "visual_message": ["Running Bayesian diagnosis to verify the repair..."],
                          "writer": "daphne"
                        });
                        
                        try {
                          // Run Bayesian diagnosis with current symptoms
                          this.isLoading = true;
                          await this.$store.dispatch('requestDiagnosis', this.selectedSymptomsList);
                          
                          const diagnosisReport = this.$store.getters.getDiagnosisReport;
                          
                          // Add to diagnostic history
                          this.diagnosticHistory.push(diagnosisReport);
                          
                          // Add a simple tab with the post-replacement diagnosis
                          this.simpleTabs.push({
                            label: "Post-Replacement Diagnosis",
                            type: "bayesian",
                            content: "Bayesian diagnosis after filter replacement.",
                            diagnosisData: diagnosisReport,
                            checked: [],
                            allSelected: false
                          });
                          
                          // Switch to the new tab
                          this.activeDiagnosticTab = this.diagnosticHistory.length - 1;
                          this.activeSimpleTab = this.simpleTabs.length - 1;
                          
                          this.isLoading = false;
                          
                          // Provide feedback on the diagnosis results
                          const topAnomaly = diagnosisReport.diagnosis_list && diagnosisReport.diagnosis_list.length > 0 
                            ? diagnosisReport.diagnosis_list[0] 
                            : null;
                          
                          if (topAnomaly && topAnomaly.anomaly === "No Anomalies Present") {
                            this.$store.commit('addDialoguePiece', {
                              "voice_message": "The diagnosis shows no anomalies present. The filter replacement appears to have resolved the issue.",
                              "visual_message_type": ["text"],
                              "visual_message": ["The diagnosis shows no anomalies present. The filter replacement appears to have resolved the issue."],
                              "writer": "daphne"
                            });
                          } else if (topAnomaly) {
                            this.$store.commit('addDialoguePiece', {
                              "voice_message": `The diagnosis is complete. ${topAnomaly.anomaly} is now the most probable scenario with ${(topAnomaly.probability * 100).toFixed(1)}% probability. You can review the results in the new diagnosis tab.`,
                              "visual_message_type": ["text"],
                              "visual_message": [`The diagnosis is complete. ${topAnomaly.anomaly} is now the most probable scenario with ${(topAnomaly.probability * 100).toFixed(1)}% probability. You can review the results in the new diagnosis tab.`],
                              "writer": "daphne"
                            });
                          }
                        } catch (error) {
                          console.error("Error running post-replacement diagnosis:", error);
                          this.isLoading = false;
                          this.$store.commit('addDialoguePiece', {
                            "voice_message": "I encountered an error running the diagnosis. Please try again.",
                            "visual_message_type": ["text"],
                            "visual_message": ["I encountered an error running the diagnosis. Please try again."],
                            "writer": "daphne"
                          });
                        }
                      } else {
                        this.$store.commit('addDialoguePiece', {
                          "voice_message": "Understood. Let me know if you need anything else.",
                          "visual_message_type": ["text"],
                          "visual_message": ["Understood. Let me know if you need anything else."],
                          "writer": "daphne"
                        });
                      }
                    });
                  });
                }
              }
            }
          } catch (error) {
            console.error("Error starting filter replacement:", error);
          }
        }
      });
    },

    setupLeakRepairListener() {
      this.$root.$once('leakRepairResponse', async (response) => {
        if (response === 'Yes') {
          this.$store.commit('addDialoguePiece', {
            "voice_message": "Starting the leak repair procedure...",
            "visual_message_type": ["text"],
            "visual_message": ["Starting the leak repair procedure..."],
            "writer": "daphne"
          });
          
          // Here you would find and start the leak repair/EVA procedure
          // This is a placeholder as the exact procedure name wasn't specified
        }
      });
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
        hypothetical_evidence: lastMessage.hypothetical_data.additional_evidence,
        symptoms_list: lastMessage.hypothetical_data.symptoms_list || [],
        best_evidence: lastMessage.hypothetical_data.best_evidence || null,
        hidden_components: lastMessage.hypothetical_data.hidden_components || [],
        current_telemetry_values: lastMessage.hypothetical_data.current_telemetry_values || {}
      };
      
      // Add to diagnostic history (old tabs - keep for compatibility)
      this.diagnosticHistory.push(hypotheticalDiagnosis);
      
      // Add a simple tab with the hypothetical diagnosis
      this.simpleTabs.push({
        label: "Hypothetical Diagnosis",
        type: "bayesian",
        content: "Hypothetical Bayesian diagnosis result.",
        diagnosisData: hypotheticalDiagnosis,
        checked: [],
        allSelected: false,
        isHypothetical: true // Flag to style differently if needed
      });
      
      // Switch to the new tab
      this.activeDiagnosticTab = this.diagnosticHistory.length - 1;
      this.activeSimpleTab = this.simpleTabs.length - 1;
      
      // Confirm to the user
      this.$store.commit('addDialoguePiece', {
        "voice_message": "I've added this hypothetical scenario to your diagnosis history tabs.",
        "visual_message_type": ["text"],
        "visual_message": ["I've added this hypothetical scenario to your diagnosis history tabs. You can switch between tabs to compare different evidence scenarios."],
        "writer": "daphne"
      });
    },

    handleAddBayesianDiagnosis(eventData) {
      // Get the last message which contains the Bayesian diagnosis data
      const dialogueHistory = this.$store.state.daphne.dialogueHistory;
      const lastMessage = dialogueHistory[dialogueHistory.length - 2];
      console.log("Adding Bayesian diagnosis from chat - last message", lastMessage);
      console.log("Diagnosis data", lastMessage.diagnosis_data);
      
      if (!lastMessage || !lastMessage.diagnosis_data) {
        console.error("No diagnosis data found in the last message");
        return;
      }
      
      // Create a new diagnosis report object from the chat-based diagnosis
      const bayesianDiagnosis = {
        diagnosis_list: lastMessage.diagnosis_data.diagnosis_list,
        best_evidence: lastMessage.diagnosis_data.best_evidence || null,
        hidden_components: lastMessage.diagnosis_data.hidden_components || [],
        current_telemetry_values: lastMessage.diagnosis_data.telemetry_values || {},
        symptoms_list: [],
        additional_evidence: null,
        is_from_chat: true // Flag to indicate this came from chat
      };
      
      // Add to diagnostic history (old tabs - keep for compatibility)
      this.diagnosticHistory.push(bayesianDiagnosis);
      
      // Add a simple tab with the Bayesian diagnosis
      this.simpleTabs.push({
        label: "Bayesian Diagnosis (Chat)",
        type: "bayesian",
        content: "Bayesian diagnosis result from chat.",
        diagnosisData: bayesianDiagnosis,
        checked: [],
        allSelected: false
      });
      
      // Switch to the new tab
      this.activeDiagnosticTab = this.diagnosticHistory.length - 1;
      this.activeSimpleTab = this.simpleTabs.length - 1;
      
      // Confirm to the user
      this.$store.commit('addDialoguePiece', {
        "voice_message": "I've added this Bayesian diagnosis to your diagnosis history tabs.",
        "visual_message_type": ["text"],
        "visual_message": ["I've added this Bayesian diagnosis to your diagnosis history tabs. You can review the results in the new tab."],
        "writer": "daphne"
      });
    },

    handleShowProcedureListFromChat(eventData) {
      // Get the last message which contains the procedures data
      const dialogueHistory = this.$store.state.daphne.dialogueHistory;
      const lastMessage = dialogueHistory[dialogueHistory.length - 1]; // Current message should have procedures data
      
      console.log("Showing PRIDE procedures from chat - last message", lastMessage);
      console.log("Procedures data", lastMessage.procedures_data);
      
      if (!lastMessage || !lastMessage.procedures_data) {
        console.error("No procedures data found in the last message");
        return;
      }
      
      const procedures = lastMessage.procedures_data;
      const filterApplied = lastMessage.filter_applied;
      
      // Call the existing showProcedureSelection method with the procedures
      this.showProcedureSelection(
        procedures, 
        filterApplied ? `filtered by '${filterApplied}'` : "all PRIDE procedures",
        !filterApplied  // true if showing all, false if filtered
      );
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

        // Add a simple tab with updated Bayesian diagnosis content
        const evidenceText = Object.keys(this.additionalEvidence).length > 0 
          ? `Additional Evidence: ${Object.entries(this.additionalEvidence).map(([key, value]) => `${key}: ${this.formatEvidenceValue(value)}`).join(', ')}`
          : '';
        
        this.simpleTabs.push({
          label: "Bayesian Diagnosis (Updated)",
          type: "bayesian",
          content: `Updated Bayesian diagnosis with additional evidence. ${evidenceText}`,
          diagnosisData: diagnosisReport, // Store the diagnosis data in the tab
          checked: [], // Store the checked anomalies for this tab
          allSelected: false, // Store the select all state for this tab
          additionalEvidence: JSON.parse(JSON.stringify(this.additionalEvidence)) // Store evidence used
        });
        this.activeSimpleTab = this.simpleTabs.length - 1;

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
        if (this.symptomsMatch(anomaly[i], symptom)) {
          ticksOrCross = 'tick'
          break;
        }
      }
      return ticksOrCross;
    },

    symptomsMatch(anomalySymptom, inputSymptom) {
      // Exact match first
      if (anomalySymptom === inputSymptom) {
        return true;
      }

      // Extract measurement name and threshold type from both symptoms
      const anomalyParts = this.parseSymptomString(anomalySymptom);
      const inputParts = this.parseSymptomString(inputSymptom);

      // If measurements don't match, return false
      if (!anomalyParts || !inputParts || anomalyParts.measurement !== inputParts.measurement) {
        return false;
      }

      // Check hierarchical relationships
      // Upper threshold hierarchy: Warning > Caution
      if (anomalyParts.threshold === 'Upper Caution Limit' && inputParts.threshold === 'Upper Warning Limit') {
        return true;
      }
      // Lower threshold hierarchy: Warning < Caution (more severe when going lower)
      if (anomalyParts.threshold === 'Lower Caution Limit' && inputParts.threshold === 'Lower Warning Limit') {
        return true;
      }

      return false;
    },

    parseSymptomString(symptom) {
      // Parse symptom string like "Humidity_IHab (IHab) Exceeds Upper Caution Limit"
      // Returns {measurement: "Humidity_IHab (IHab)", threshold: "Upper Caution Limit"}
      
      const exceedsPattern = /^(.+?)\s+Exceeds\s+(.+)$/;
      const match = symptom.match(exceedsPattern);
      
      if (match) {
        return {
          measurement: match[1].trim(),
          threshold: match[2].trim()
        };
      }
      
      return null;
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
    },
    
    selectAllAnomaliesForTab(tabIndex) {
      const tab = this.simpleTabs[tabIndex];
      if (tab && tab.diagnosisData && tab.diagnosisData.diagnosis_list) {
        if (!tab.allSelected) {
          tab.checked = [...tab.diagnosisData.diagnosis_list];
        } else {
          tab.allSelected = false;
          tab.checked = [];
          // Clear explanations when unchecking all
          this.$set(tab, 'explaining', false);
        }
      }
    },
    
    showExplanationsForTab(tabIndex) {
      const tab = this.simpleTabs[tabIndex];
      if (tab && tab.checked && tab.checked.length > 0) {
        this.showAlert = false;
        // Set explaining state for this specific tab
        this.$set(tab, 'explaining', true);
        console.log('Showing explanations for anomalies in tab:', tabIndex, tab.checked);
      } else {
        this.showAlert = true;
        console.log("Please select anomalies for investigation in tab:", tabIndex);
      }
    },
    
    clearExplanationsForTab(tabIndex) {
      const tab = this.simpleTabs[tabIndex];
      if (tab) {
        this.$set(tab, 'explaining', false);
        tab.checked = [];
        this.showAlert = false;
      }
    },
    
    async runPhysicsDiagnosisForAnomaly(anomalyName, bayesianProbability = null) {
      try {
        this.isLoading = true;
        
        // Format the Bayesian probability if provided
        const formattedBayesianProbability = bayesianProbability ? 
          `${(bayesianProbability * 100).toFixed(2)}%` : null;
        
        // Show loading message
        // this.$store.commit('addDialoguePiece', {
        //   "voice_message": `Running physics diagnosis for ${anomalyName}...`,
        //   "visual_message_type": ["text"],
        //   "visual_message": [`Running physics diagnosis for ${anomalyName}...`],
        //   "writer": "daphne"
        // });
        
        // Update store with effective duration (either manual or auto based on simulation time)
        const durationToUse = this.effectiveSimDurationSeconds;
        console.log(`🔍 Using simulation duration for anomaly analysis: ${durationToUse} seconds (manual mode: ${this.useManualDuration})`);
        this.$store.commit('mutatePhysicsSimDurationSeconds', durationToUse);
        
        // Request physics diagnosis from backend with specific anomaly
        await this.$store.dispatch('requestPhysicsDiagnosis', {
          selectedSymptomsList: this.selectedSymptomsList,
          targetAnomaly: anomalyName
        });
        
        // Get the diagnosis report from store
        const diagnosisReport = this.$store.getters.getDiagnosisReport;
        
        if (diagnosisReport && diagnosisReport.physics_diagnosis_data) {
          // Convert backend data to frontend format
          const physicsDiagnosisData = {
            mostProbableAnomaly: diagnosisReport.physics_diagnosis_data.most_probable_anomaly,
            probability: diagnosisReport.physics_diagnosis_data.probability,
            componentAnomalies: diagnosisReport.physics_diagnosis_data.component_anomalies.map(anomaly => ({
              name: anomaly.name,
              score: anomaly.score,
              isHighlighted: anomaly.is_highlighted,
              faultInjectionTime: anomaly.fault_injection_time,
              faultInjectionTimeSeconds: anomaly.fault_injection_time_seconds,
              fault_injection_time_absolute: anomaly.fault_injection_time_absolute
            }))
          };
          this.$store.commit('mutatePhysicsDiagnosisData', physicsDiagnosisData);

          // Convert telemetry data from backend
          const telemetryGraphData = {
            actual: diagnosisReport.physics_diagnosis_data.actual_telemetry,
            simulated: {},
            timeLabels: diagnosisReport.physics_diagnosis_data.time_labels,
            diagnosis_run_time: diagnosisReport.physics_diagnosis_data.diagnosis_run_time,
            t_zero: diagnosisReport.physics_diagnosis_data.t_zero,
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
              score: parseFloat(anomaly.score),
              faultInjectionTime: anomaly.fault_injection_time,
              faultInjectionTimeSeconds: anomaly.fault_injection_time_seconds,
              fault_injection_time_absolute: anomaly.fault_injection_time_absolute
            };
          });
          this.$store.commit('mutateTelemetryGraphData', telemetryGraphData);

          // Initialize selection to all anomalies
          this.selectedPhysicsAnomalies = physicsDiagnosisData.componentAnomalies.map(a => a.name);

          // Add a simple tab with physics diagnosis content
          this.simpleTabs.push({
            label: `Physics: ${anomalyName}`,
            type: "physics",
            content: "Physics diagnosis result goes here.",
            diagnosisData: diagnosisReport,
            physicsDiagnosisData: this.$store.getters.getPhysicsDiagnosisData,
            telemetryGraphData: this.$store.getters.getTelemetryGraphData,
            sourceAnomaly: anomalyName, // Track which anomaly triggered this physics diagnosis
            bayesianProbability: formattedBayesianProbability // Store the Bayesian probability
          });
          this.activeSimpleTab = this.simpleTabs.length - 1;
          
          // Show success message
          // this.$store.commit('addDialoguePiece', {
          //   "voice_message": `Physics diagnosis for ${anomalyName} completed and displayed in a new tab.`,
          //   "visual_message_type": ["text"],
          //   "visual_message": [`Physics diagnosis for ${anomalyName} completed and displayed in a new tab.`],
          //   "writer": "daphne"
          // });
          
          // Ask user if they want to run robot inspection for the most likely component
          if (physicsDiagnosisData.componentAnomalies && physicsDiagnosisData.componentAnomalies.length > 0) {
            const mostLikelyComponent = physicsDiagnosisData.componentAnomalies[0];
            
            this.$store.commit('addDialoguePiece', {
              "voice_message": `Physics-based analysis complete. The most likely failed subcomponent is ${mostLikelyComponent.name}. Do you want to command the robot to check ${mostLikelyComponent.name} condition?`,
              "visual_message_type": ["text"],
              "visual_message": [`Physics-based analysis complete. The most likely failed subcomponent is ${mostLikelyComponent.name} with ${(mostLikelyComponent.score * 100).toFixed(1)}% score. Do you want to command the robot to check ${mostLikelyComponent.name} condition?`],
              "writer": "daphne",
              "options": ["Yes", "No"],
              "optionsCallbackEvent": "robotInspectionResponse"
            });

            // Set up listener for robot inspection response
            this.setupRobotInspectionListener({
              anomaly: mostLikelyComponent.name,
              probability: mostLikelyComponent.score,
              bayesianAnomaly: anomalyName  // Pass Bayesian anomaly name for evidence formatting
            });
          }
          
        } else {
          throw new Error("No physics diagnosis data received from backend");
        }
        
      } catch (error) {
        console.error("Error during physics diagnosis for anomaly:", error);
        this.$store.commit('addDialoguePiece', {
          "voice_message": `Failed to run physics diagnosis for ${anomalyName}. Please try again.`,
          "visual_message_type": ["text"],
          "visual_message": [`Failed to run physics diagnosis for ${anomalyName}. Please try again.`],
          "writer": "daphne"
        });
      } finally {
        this.isLoading = false;
      }
    },
    onSelectedAnomaliesChange() {
      // Redraw graph when selection changes
      if (this.showPhysicsExplanation) {
        this.generateTelemetryGraph();
      }
    },
    async handlePhysicsProcedure(anomalyName) {
      try {
        // Show loading message
        this.$store.commit('addDialoguePiece', {
          "voice_message": `Looking for procedures related to ${anomalyName}...`,
          "visual_message_type": ["text"],
          "visual_message": [`Looking for procedures related to ${anomalyName}...`],
          "writer": "daphne"
        });

        // Get all available procedures from backend API
        const response = await fetchGet('/api/at/get_available_procedures');

        if (!response.ok) {
          throw new Error(`Failed to fetch procedures: ${response.status}`);
        }

        const responseData = await response.json();
        if (responseData.status !== 'success') {
          throw new Error(`Backend error: ${responseData.message}`);
        }

        const allProcedures = responseData.procedures;

        let anomaly_names = []
        if (anomalyName.includes('+')) {
          anomaly_names = anomalyName.split(' + ').map(name => name.trim());
        } else {
          anomaly_names.push(anomalyName);
        }
        
        // Filter procedures by anomaly name (case-insensitive search in title)
        const filteredProcedures = allProcedures.filter(procedure => 
          anomaly_names.some(name => 
            procedure.title.toLowerCase().includes(name.toLowerCase()) ||
            procedure.filename.toLowerCase().includes(name.toLowerCase())
          )
        );

        if (filteredProcedures.length === 0) {
          // No procedures found
          this.$store.commit('addDialoguePiece', {
            "voice_message": `No procedures found for ${anomalyName}. Would you like me to show all available procedures instead?`,
            "visual_message_type": ["text"],
            "visual_message": [`No procedures found for ${anomalyName}. Would you like me to show all available procedures instead?`],
            "writer": "daphne",
            "options": ["Yes", "No"],
            "optionsCallbackEvent": "showAllProceduresResponse"
          });

          // Set up listener for response
          this.$root.$once('showAllProceduresResponse', (response) => {
            if (response === "Yes") {
              this.showProcedureSelection(allProcedures, anomalyName, true); // true indicates showing all procedures
            } else {
              this.$store.commit('addDialoguePiece', {
                "voice_message": "Alright, let me know if you need help with anything else.",
                "visual_message_type": ["text"],
                "visual_message": ["Alright, let me know if you need help with anything else."],
                "writer": "daphne"
              });
            }
          });
        } else if (filteredProcedures.length === 1) {
          // Only one procedure found, ask for confirmation with option to view all
          const procedure = filteredProcedures[0];
          this.$store.commit('addDialoguePiece', {
            "voice_message": `I found one procedure for ${anomalyName}: "${procedure.title}". Would you like me to start this procedure?`,
            "visual_message_type": ["text"],
            "visual_message": [`I found one procedure for ${anomalyName}: <br>${procedure.title}.<br><br>Would you like me to start this procedure?`],
            "writer": "daphne",
            "options": ["Yes", "No", "Show All Procedures"],
            "optionsCallbackEvent": "confirmSingleProcedure"
          });

          // Set up listener for confirmation
          this.$root.$once('confirmSingleProcedure', (response) => {
            if (response === "Yes") {
              this.startSelectedProcedure(procedure.staticProcedureID, procedure.title);
            } else if (response === "Show All Procedures") {
              this.showProcedureSelection(allProcedures, anomalyName, true); // true indicates showing all procedures
            } else {
              this.$store.commit('addDialoguePiece', {
                "voice_message": "Alright, procedure not started.",
                "visual_message_type": ["text"],
                "visual_message": ["Alright, procedure not started."],
                "writer": "daphne"
              });
            }
          });
        } else {
          // Multiple procedures found, let user choose with option to view all
          this.showProcedureSelection(filteredProcedures, anomalyName, false, allProcedures); // Pass allProcedures as 4th param
        }

      } catch (error) {
        console.error("Error fetching procedures:", error);
        this.$store.commit('addDialoguePiece', {
          "voice_message": `Failed to fetch procedures for ${anomalyName}. Please try again later.`,
          "visual_message_type": ["text"],
          "visual_message": [`Failed to fetch procedures for ${anomalyName}. Please check your connection and try again.`],
          "writer": "daphne"
        });
      }
    },

    showProcedureSelection(procedures, anomalyName, showingAllProcedures = false, allProcedures = null) {
      // Create procedure list for display
      const procedureList = procedures.map((proc, index) => 
        // `${index + 1}. ${proc.title} (${proc.number}) - ${proc.revision}`
        `${index + 1}. ${proc.title}`
      ).join('<br>');

      // Create options for user selection
      const procedureOptions = procedures.map((proc, index) => 
        `${index + 1}. ${proc.title}`
      );

      // Add "Show All Procedures" button if we're showing filtered procedures and have all procedures available
      if (!showingAllProcedures && allProcedures && allProcedures.length > procedures.length) {
        procedureOptions.push("Show All Procedures");
      }

      // Create different messages based on whether we're showing all procedures or filtered ones
      const voiceMessage = showingAllProcedures 
        ? `Here are all ${procedures.length} available procedures. Please select which one you'd like to start:`
        : `I found ${procedures.length} procedures related to ${anomalyName}. Please select which one you'd like to start:`;

      const visualMessage = showingAllProcedures
        ? `Here are all ${procedures.length} available procedures:<br><br>${procedureList}<br><br>Please select which one you'd like to start:`
        : `I found ${procedures.length} procedures related to ${anomalyName}:<br><br>${procedureList}<br><br>Please select which one you'd like to start:`;

      this.$store.commit('addDialoguePiece', {
        "voice_message": voiceMessage,
        "visual_message_type": ["text"],
        "visual_message": [visualMessage],
        "writer": "daphne",
        "options": procedureOptions,
        "optionsCallbackEvent": "selectProcedureFromList"
      });

      // Set up listener for procedure selection
      this.$root.$once('selectProcedureFromList', (selectedOption) => {
        // Check if user wants to see all procedures
        if (selectedOption === "Show All Procedures") {
          this.showProcedureSelection(allProcedures, anomalyName, true);
          return;
        }

        // Extract the index from the selected option
        const selectedIndex = parseInt(selectedOption.split('.')[0]) - 1;
        const selectedProcedure = procedures[selectedIndex];
        
        if (selectedProcedure) {
          this.startSelectedProcedure(selectedProcedure.staticProcedureID, selectedProcedure.title);
        } else {
          this.$store.commit('addDialoguePiece', {
            "voice_message": "Invalid selection. Please try again.",
            "visual_message_type": ["text"],
            "visual_message": ["Invalid selection. Please try again."],
            "writer": "daphne"
          });
        }
      });
    },

    async startSelectedProcedure(procedureID, procedureTitle) {
      try {
        this.$store.commit('addDialoguePiece', {
          "voice_message": `Starting procedure: ${procedureTitle}...`,
          "visual_message_type": ["text"],
          "visual_message": [`Starting procedure: ${procedureTitle}`],
          "writer": "daphne"
        });

        // Call the existing StartAstrobeeProcedure API
        const reqData = new FormData();
        reqData.append('procedureID', procedureID);
        
        const response = await fetchPost('/api/at/start_astrobee_procedure', reqData);
        
        if (response.ok) {
          const data = await response.json();
          console.log("Procedure started successfully:", data);
          
          this.$store.commit('addDialoguePiece', {
            "voice_message": `Procedure "${procedureTitle}" has been started successfully!`,
            "visual_message_type": ["text"],
            "visual_message": [`Procedure "${procedureTitle}" has been started successfully!`],
            "writer": "daphne"
          });
        } else {
          throw new Error(`Failed to start procedure: ${response.statusText}`);
        }
      } catch (error) {
        console.error("Failed to start procedure:", error);
        this.$store.commit('addDialoguePiece', {
          "voice_message": `Failed to start procedure "${procedureTitle}". Please try again.`,
          "visual_message_type": ["text"],
          "visual_message": [`Failed to start procedure "${procedureTitle}". Please try again.`],
          "writer": "daphne"
        });
      }
    },

    formatFaultInjectionTime(dataPoint, seconds) {
      if (dataPoint === undefined || seconds === undefined) {
        return 'N/A';
      }
      // Format as "T+3 (15s)" or similar
      return `T+${dataPoint} (${seconds}s)`;
    },

    getFaultInjectionAnnotations() {
      if (!this.telemetryGraphData.simulated) {
        return [];
      }

      const annotations = [];
      const timeLabels = this.telemetryGraphData.timeLabels || [];

      Object.entries(this.telemetryGraphData.simulated)
        .filter(([name]) => this.selectedPhysicsAnomalies.indexOf(name) !== -1)
        .forEach(([anomalyName, anomalyData]) => {
          if (anomalyData.faultInjectionTime !== undefined && anomalyData.faultInjectionTime >= 0) {
            // Get the absolute simulation time for this fault injection
            const faultTimeLabel = timeLabels.length > 0 && anomalyData.faultInjectionTime < timeLabels.length
              ? timeLabels[anomalyData.faultInjectionTime]
              : `T+00:00:${anomalyData.faultInjectionTime.toString().padStart(2, '0')}`;
            
            annotations.push({
              x: faultTimeLabel,
              y: 7.5, // Position at top of y-axis
              text: `Fault<br>${anomalyName}`,
              showarrow: true,
              arrowhead: 2,
              arrowsize: 1,
              arrowwidth: 2,
              arrowcolor: anomalyData.color,
              ax: 0,
              ay: -30,
              bgcolor: 'rgba(0, 30, 30, 0.9)',
              bordercolor: anomalyData.color,
              borderwidth: 1,
              font: { color: '#fff', size: 10 }
            });
          }
        });

      return annotations;
    },

    // Convert timestamps to relative time gaps (e.g., "20:51:38" -> "-10:10")
    convertToRelativeTime(timeLabels) {
      if (!timeLabels || timeLabels.length === 0) {
        return null;
      }

      // Find the most recent timestamp (assuming they're in chronological order)
      const mostRecentTime = timeLabels[timeLabels.length - 1];
      
      // Parse the most recent time
      const mostRecentDate = this.parseTimeString(mostRecentTime);
      if (!mostRecentDate) {
        return null;
      }

      // Convert each timestamp to relative time gap
      return timeLabels.map(timeStr => {
        const currentDate = this.parseTimeString(timeStr);
        if (!currentDate) {
          return timeStr; // Fallback to original if parsing fails
        }

        // Calculate time difference in seconds
        const diffSeconds = Math.floor((mostRecentDate - currentDate) / 1000);
        
        // Convert to minutes and seconds
        const minutes = Math.floor(diffSeconds / 60);
        const seconds = diffSeconds % 60;
        
        // Format as "-MM:SS" or "-0:SS" for recent data
        if (minutes === 0) {
          return `-0:${seconds.toString().padStart(2, '0')}`;
        } else {
          return `-${minutes}:${seconds.toString().padStart(2, '0')}`;
        }
      });
    },

    // Parse time string in format "HH:MM:SS" or "HH:MM"
    parseTimeString(timeStr) {
      if (!timeStr || typeof timeStr !== 'string') {
        return null;
      }

      // Handle different time formats
      const timeMatch = timeStr.match(/(\d{1,2}):(\d{2})(?::(\d{2}))?/);
      if (!timeMatch) {
        return null;
      }

      const hours = parseInt(timeMatch[1]);
      const minutes = parseInt(timeMatch[2]);
      const seconds = timeMatch[3] ? parseInt(timeMatch[3]) : 0;

      // Create a date object for today with the given time
      const date = new Date();
      date.setHours(hours, minutes, seconds, 0);
      
      return date;
    },


  },

  mounted() {
    //main
    this.startAstrobeeStatusPolling();
    setInterval(this.startAstrobeeStatusPolling, 1200);

    // Initialize local physics simulation duration with store value
    this.localPhysicsSimDuration = this.physicsSimDurationSeconds;

    // Initialize duration components - default to 50 minutes (3000 seconds)
    this.updatePhysicsSimDuration();

    this.$nextTick(() => {
      if (this.$refs.tabsContainer) {
        this.$refs.tabsContainer.addEventListener('scroll', this.updateScrollButtons);
        window.addEventListener('resize', this.updateScrollButtons);
        this.updateScrollButtons();
      }
    });
    this.$root.$on('addHypotheticalDiagnosis', this.handleAddHypotheticalDiagnosis);
    this.$root.$on('addBayesianDiagnosis', this.handleAddBayesianDiagnosis);
    this.$root.$on('showProcedureListFromChat', this.handleShowProcedureListFromChat);
    
    // Add event listener for physics diagnosis completion from chatbot
    window.addEventListener('physicsDiagnosisCompleted', this.handlePhysicsDiagnosisFromChatbot);
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
  
  // Clean up new event listeners
  this.$root.$off('physicsAnalysisResponse');
  this.$root.$off('robotInspectionResponse');
  this.$root.$off('lossOfPressureResponse');
  this.$root.$off('filterReplacementResponse');
  this.$root.$off('leakRepairResponse');
  
  this.$root.$off('addHypotheticalDiagnosis', this.handleAddHypotheticalDiagnosis);
  this.$root.$off('addBayesianDiagnosis', this.handleAddBayesianDiagnosis);
  this.$root.$off('showProcedureListFromChat', this.handleShowProcedureListFromChat);
  this.$root.$off('damageAssessmentResponse', this.handleDamageAssessmentResponse);

  if (this.$refs.tabsContainer) {
      this.$refs.tabsContainer.removeEventListener('scroll', this.updateScrollButtons);
      window.removeEventListener('resize', this.updateScrollButtons);
    }
    
    // Remove event listener for physics diagnosis completion from chatbot
    window.removeEventListener('physicsDiagnosisCompleted', this.handlePhysicsDiagnosisFromChatbot);



  },

  watch: {
    diagnosticHistory() {
      this.$nextTick(() => {
        this.updateScrollButtons();
      });
    },
    
    // Watch for changes in store physics simulation duration and update local value
    physicsSimDurationSeconds(newVal) {
      this.localPhysicsSimDuration = newVal;
    },

    // Watch for changes in duration value and update physics sim duration
    durationValue() {
      this.updatePhysicsSimDuration();
    },

    // Watch for changes in checkbox state to update duration
    useManualDuration() {
      this.updatePhysicsSimDuration();
    },

    // Watch for changes in simulation time to update auto duration (when in automatic mode)
    simulationTime() {
      if (!this.useManualDuration) {
        this.updatePhysicsSimDuration();
      }
    },

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
  width: 100%;
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
  width: 100%;
  min-width: 100%;
}

.physics-table-section {
  flex: 0.8;
  min-width: 400px;
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
  padding: 10px 8px; /* Reduced padding to accommodate new column */
  text-align: left;
  border: 1px solid rgba(10, 254, 255, 0.18); /* grid lines */
}

.physics-table th:nth-child(4), .physics-table td:nth-child(4) {
  text-align: center; /* Center the fault injection time column */
  min-width: 120px; /* Ensure minimum width for the new column */
}

/* Ensure full width expansion for the main container */
#anomaly_diagnosis {
  width: 100%;
  max-width: 100%;
}

/* Ensure the content areas can expand to full width */
.is-content {
  width: 100%;
  max-width: 100%;
}

/* Ensure the telemetry graph container can expand to full width */
.telemetry-graph-container {
  width: 100% !important;
  max-width: 100% !important;
  min-width: 100% !important;
}

/* Ensure the tabs container can expand to full width */
.tabs-container {
  width: 100%;
  max-width: 100%;
}

/* Ensure the tab content can expand to full width */
.tab-wrapper {
  width: 100%;
  max-width: 100%;
}

.physics-table th {
  background: #002E2E;
  color: #0AFEFF;
}

.physics-table tbody tr {
  transition: background-color 0.2s ease;
  cursor: pointer;
}

.physics-table tbody tr:hover {
  background: #003f3f !important;
  box-shadow: 0 0 8px rgba(10, 254, 255, 0.3);
}

.physics-image-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 220px;
}

.physics-image-section img {
  transition: opacity 0.3s ease;
}

.checkbox-cell {
  text-align: center;
  cursor: pointer;
  padding: 0;
  transition: background 0.15s ease;
}

.checkbox-full {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  padding: 6px 0; /* compact to avoid tall rows */
  margin: 0;
}

.checkbox-full input[type="checkbox"] {
  position: absolute;
  opacity: 0; /* hide native, keep accessible */
  pointer-events: none;
}

.checkbox-full:hover { background: rgba(10, 254, 255, 0.08); }
.check-icon {
  display: inline-block;
  color: rgba(10, 254, 255, 0.25); /* faint when unchecked */
  font-size: 18px;
  line-height: 1;
  opacity: 0.6;
  transition: color 0.12s ease, opacity 0.12s ease;
}
.checkbox-full input[type="checkbox"]:checked + .check-icon {
  color: #0AFEFF; /* solid when checked */
  opacity: 1;
}


</style>