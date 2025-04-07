import {fetchPost} from "../../scripts/fetch-helpers";

// Sound files
import startAnomalySound from '../../sounds/woopwoop.mp3';
import endAnomalySound from '../../sounds/endgame.mp3';


const state = {
    // Telemetry group
    heraUser: true,
    username: '',
    // Telemetry related variables
    telemetryInputVariables: [], // A list of all the telemetry variables. Used for the telemetry plot dropdown menu.
    telemetryPlotSelectedVariables: [], // A list of the telemetry variables selected by the user to be displayed. RELEVANT FOR THE CONTEXT.
    telemetryPlotData: [], // Contains formatted telemetry feed values so that they can be properly plotted using vue.plotly.
    telemetryIsOngoing: false, // Self descriptive.
    telemetryType: null,
    playAlarms: false,
    isTelemetryInitialized: false,
    telemetryValues: '', // A string that stores the telemetry values as a jsoned dataframe.
    telemetryInfo: '', // A string that stores the telemetry info as a jsoned dataframe. To be deprecated.

    // Symptoms detection and diagnosis related variables
    symptomsList: [], // A list of all the currently detected symptoms.
    selectedSymptomsList: [], // A list of the symptoms selected by the user to be diagnosed.
    lastSelectedSymptomsList: [], // A list of the symptoms that appear in the  last requested diagnosis report
    diagnosisReport: [], // Contains the information related to a requested diagnosis.
    selectedLeftSymptoms: [],
    selectedRightSymptoms:[],

    lastUpdatedSymptomsTimestamp: '',
    lastUpdatedAnomaliesTimestamp: '',
    lastUpdatedProceduresTimestamp: '',
    lastUpdatedProceduresInfoTimestamp: '',
    lastUpdatedDiagnosisTimestamp: '',
    // Anomaly treatment related variables
    selectedAnomaliesList: [], // A list of the anomalies selected by the user to be displayed. RELEVANT FOR THE CONTEXT.
    selectedAnomaliesInfo: {}, // A dictionary with all the information of each of the selected anomalies.
    allAnomaliesList: [], // A list of all the anomalies that are present in the knowledge graph. Used for the telemetry plot dropdown menu.
    selectedProceduresList: [], // A list of all the procedures that relate to the current selected anomalies. RELEVANT FOR THE CONTEXT.
    selectedProceduresInfo: {}, // A dictionary with the information regarding the current status of the procedures.
    loadingNewAnomaly: false,
    isLoggedIn: false,
    isChatVisible: true,
    symptoms_timestamp: ""
};

const getters = {
    // A getter for each state variable
    getHeraUser(state) {return state.heraUser},
    getPlotData(state) {return state.telemetryPlotData},
    getSelectedVariables(state) {return state.telemetryPlotSelectedVariables},
    getInputVariables(state) {return state.telemetryInputVariables},
    getTelemetryIsOngoing(state) {return state.telemetryIsOngoing},
    getTelemetryValues(state) {return state.telemetryValues},
    getTelemetryInfo(state) {return state.telemetryInfo},
    getSymptomsList(state) {return state.symptomsList},
    getSelectedSymptomsList(state) {return state.selectedSymptomsList},
    getSelectedLeftSymptomsList(state) {return state.selectedLeftSymptoms},
    getSelectedRightSymptomsList(state) {return state.selectedRightSymptoms},
    getLastSelectedSymptomsList(state) {return state.lastSelectedSymptomsList},
    getDiagnosisReport(state) {return state.diagnosisReport},
    getSelectedAnomaliesList(state) {return state.selectedAnomaliesList},
    getSelectedAnomaliesInfo(state) {return state.selectedAnomaliesInfo},
    getAllAnomaliesList(state) {return state.allAnomaliesList},
    getSelectedProceduresList(state) {return state.selectedProceduresList},
    getSelectedProceduresInfo(state) {return state.selectedProceduresInfo},
    getLoadingNewAnomaly(state) {return state.loadingNewAnomaly},
    getPlayAlarms(state) {return state.playAlarms},
    getIsChatVisible(state) {return state.isChatVisible},
    getSymptomsTimestamp(state) { return state.symptoms_timestamp},
    getLastUpdatedSymptomsTimestamp(state) {return state.lastUpdatedSymptomsTimestamp},
    getLastUpdatedAnomaliesTimestamp(state) {return state.lastUpdatedAnomaliesTimestamp},
    getLastUpdatedProceduresTimestamp(state) {return state.lastUpdatedProceduresTimestamp},
    getLastUpdatedProceduresInfoTimestamp(state) {return state.lastUpdatedProceduresInfoTimestamp},
    getLastUpdatedDiagnosisTimestamp(state) {return state.lastUpdatedDiagnosisTimestamp},
};

const actions = {
    async updateTelemetryPlotData({state, commit}, telemetryData) {
        commit('mutateTelemetryPlotData', telemetryData)
    },
    async updateTelemetryValuesAndInfo({state, commit}, telemetryDict) {
        let telemetryValues = JSON.parse(telemetryDict['values']);
        let telemetryInfo = JSON.parse(telemetryDict['info']);
        commit('mutateTelemetryValues', telemetryValues);
        commit('mutateTelemetryInfo', telemetryInfo);
    },
    async updateSelectedVariables({state, commit}, newVariables) {
        commit('mutateTelemetryPlotSelectedVariables', newVariables);
    },
    async updateSymptomsList({state, commit}, symptomsList) {
        commit('mutateSymptomsList', symptomsList);
    },
    async addSelectedSymptom({state, commit}, symptom) {
        let currentSelectedSymptoms = JSON.parse(JSON.stringify(state.selectedSymptomsList));
        let already_in_list = false;
        for (let index in currentSelectedSymptoms) {
            let item = currentSelectedSymptoms[index];
            if (JSON.stringify(item) === JSON.stringify(symptom)) {
                already_in_list = true;
            }
        }
        if (!already_in_list) {
            currentSelectedSymptoms.push(symptom);
            commit('mutateSelectedSymptomsList', currentSelectedSymptoms);
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
            commit('mutateLastUpdatedSymptomsTimestamp', formattedDate);
        }
    },
    async removeSelectedSymptom({state, commit}, symptom) {
        let currentSelectedSymptoms = JSON.parse(JSON.stringify(state.selectedSymptomsList));
        let stringifiedSymptom = JSON.stringify(symptom);
        let index = -1;
        for (let i = 0; i < currentSelectedSymptoms.length; i++) {
            let stringifiedItem = JSON.stringify(state.selectedSymptomsList[i]);
            if (stringifiedItem === stringifiedSymptom) {
                index = i;
            }
        }

        currentSelectedSymptoms.splice(index, 1);
        commit('mutateSelectedSymptomsList', currentSelectedSymptoms);
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
        commit('mutateLastUpdatedSymptomsTimestamp', formattedDate);
      
    },
    async clearSelectedSymptoms({state, commit}) {
        commit('mutateSelectedSymptomsList', []);
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
        commit('mutateLastUpdatedSymptomsTimestamp', formattedDate);
    },
    async clearDiagnosisReport({state, commit}) {
        commit('mutateDiagnosisReport', []);
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
        commit('mutateLastUpdatedDiagnosisTimestamp', formattedDate);
    },
    async retrieveProceduresFromAnomaly(state, anomalyName) {
        let reqData = new FormData();
        reqData.append('anomaly_name',  JSON.stringify(anomalyName));
        let response = await fetchPost('/api/at/retrieveProcedureFromAnomaly', reqData);
        if (response.ok) {
            let procedureName = await response.json();
            return procedureName;
        } else {
            console.log('Error retrieving the procedure name.');
            return 'ERROR'
        }
    },
    async retrieveInfoFromProcedure(state, procedureName) {
        let reqData = new FormData();
        reqData.append('procedure_name',  JSON.stringify(procedureName));
        let response = await fetchPost('/api/at/retrieveInfoFromProcedure', reqData);
        if (response.ok) {
            let info = await response.json();
            return info;
        } else {
            console.log('Error retrieving the procedure objective.');
            return ['ERROR']
        }
    },
    async addSelectedAnomaly({state, commit}, anomalyName) {
        // Update the loading bool
        commit('mutateLoadingNewAnomaly', true);

        // A copy of each state variable to be modified is made. Modifications will be made upon such copy, and the
        // changes will be committed at the end of the action.
        let newSelectedAnomaliesList = JSON.parse(JSON.stringify(state.selectedAnomaliesList));
        let newSelectedAnomaliesInfo = JSON.parse(JSON.stringify(state.selectedAnomaliesInfo));
        let newSelectedProceduresList = JSON.parse(JSON.stringify(state.selectedProceduresList));
        let newSelectedProceduresInfo = JSON.parse(JSON.stringify(state.selectedProceduresInfo));

        // Retrieve a list with the names of all the procedures related to the anomaly
        let procedures = await Promise.resolve(this.dispatch('retrieveProceduresFromAnomaly', anomalyName));
        // Update the copy of the state variables.
        newSelectedAnomaliesList.push(anomalyName);
        newSelectedAnomaliesInfo[anomalyName] = {'anomalyProcedures': procedures};

        // For each procedure in the list, check if it is already selected (because it may be related to an other selected anomaly)
        for (let index in procedures) {
            let procedureName = procedures[index];
            if (!newSelectedProceduresList.includes(procedureName)) {
                // In case it is not already selected, retrieve its list information
                let info = await Promise.resolve(this.dispatch('retrieveInfoFromProcedure', procedureName));
                let procedureInfo = {
                    'procedureStepsList': info['procedureStepsList'],
                    'procedureCurrentStep': 0,
                    'checkableSteps': info['checkableSteps'],
                    'checkableStepsList': info['checkableStepsList'],
                    'procedureObjective': info['procedureObjective'],
                    'procedureEquipment': info['procedureEquipment'],
                    'procedureReferences': info['procedureReferences'],
                    'procedureReferenceLinks': info['procedureReferenceLinks'],
                    'procedureFigures': info['procedureFigures'],
                    'procedureIsOpen': false,
                };

                // Commit the update on the procedure and its information
                newSelectedProceduresList.push(procedureName);
                newSelectedProceduresInfo[procedureName] = procedureInfo;
            }
        }
        // Perform the commits
        commit('mutateSelectedAnomaliesList', newSelectedAnomaliesList);
        commit('mutateSelectedAnomaliesInfo', newSelectedAnomaliesInfo);
        commit('mutateSelectedProceduresList', newSelectedProceduresList);
        commit('mutateSelectedProceduresInfo', newSelectedProceduresInfo);
        const now = new Date();
        let formattedDate = now.toLocaleString('en-US', {
            year: 'numeric',
            month: 'long', 
            day: 'numeric',
            hour: 'numeric',
            minute: 'numeric',
            second: 'numeric',
            hour12: true 
          });
        commit('mutateLastUpdatedAnomaliesTimestamp', formattedDate);
        commit('mutateLastUpdatedProceduresTimestamp', formattedDate);
        commit('mutateLastUpdatedProceduresInfoTimestamp', formattedDate);
        console.log("mutateeeeeeeee333 updateeeeeeeeee", now, "55555555555555", formattedDate);

        // Update the loading bool
        commit('mutateLoadingNewAnomaly', false);
    },
    removeProcedures({state, commit}, anomalyAndProcedure) {
        let anomalyName = anomalyAndProcedure[0];
        let procedureName = anomalyAndProcedure[1];
        // A copy of each state variable to be modified is made. Modifications will be made upon such copy, and the
        // changes will be committed at the end of the action.
        let newSelectedAnomaliesList = JSON.parse(JSON.stringify(state.selectedAnomaliesList));
        let newSelectedAnomaliesInfo = JSON.parse(JSON.stringify(state.selectedAnomaliesInfo));
        let newSelectedProceduresList = JSON.parse(JSON.stringify(state.selectedProceduresList));
        let newSelectedProceduresInfo = JSON.parse(JSON.stringify(state.selectedProceduresInfo));

        // For comfort, retrieve the list that the procedure will be removed from
        let thisAnomalyProcedures = JSON.parse(JSON.stringify(state.selectedAnomaliesInfo[anomalyName]));
        // For each procedure related to be deleted, check if it has to be deleted or not (that is, if there is any of
        // the other selected anomalies that is also related to the procedure)
        for (let index in thisAnomalyProcedures['anomalyProcedures']) {
            let procedure = thisAnomalyProcedures['anomalyProcedures'][index];
            if (procedureName == procedure) {
                newSelectedAnomaliesInfo[anomalyName]['anomalyProcedures'].splice(index, 1);
                if (newSelectedAnomaliesInfo[anomalyName]['anomalyProcedures'].length == 0) {
                    for (let anomalyIndex in newSelectedAnomaliesList) {
                        if (newSelectedAnomaliesList[anomalyIndex] == anomalyName) {
                            newSelectedAnomaliesList.splice(anomalyIndex, 1);
                        }
                    }
                    for (let anomalyIndex in newSelectedAnomaliesInfo) {
                        if (newSelectedAnomaliesInfo[anomalyIndex] == anomalyName) {
                            newSelectedAnomaliesInfo.splice(anomalyIndex, 1);
                        }
                    }
                }
            }
            for (let indexProcedure in newSelectedProceduresList) {
                if (newSelectedProceduresList[indexProcedure] == procedureName) {
                    newSelectedProceduresList.splice(indexProcedure, 1);
                }
            }
            delete newSelectedProceduresInfo[procedureName];
        }
        // Perform the commits
        commit('mutateSelectedAnomaliesList', newSelectedAnomaliesList);
        commit('mutateSelectedAnomaliesInfo', newSelectedAnomaliesInfo);
        commit('mutateSelectedProceduresList', newSelectedProceduresList);
        commit('mutateSelectedProceduresInfo', newSelectedProceduresInfo);
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
        commit('mutateLastUpdatedAnomaliesTimestamp', formattedDate);
        commit('mutateLastUpdatedProceduresTimestamp', formattedDate);
        commit('mutateLastUpdatedProceduresInfoTimestamp', formattedDate);
        console.log("mutateeeeeeeee111 updateeeeeeeeee", now, "55555555555555", formattedDate);

    },
    removeSelectedAnomaly({state, commit}, anomalyName) {
        // A copy of each state variable to be modified is made. Modifications will be made upon such copy, and the
        // changes will be committed at the end of the action.
        let newSelectedAnomaliesList = JSON.parse(JSON.stringify(state.selectedAnomaliesList));
        let newSelectedAnomaliesInfo = JSON.parse(JSON.stringify(state.selectedAnomaliesInfo));
        let newSelectedProceduresList = JSON.parse(JSON.stringify(state.selectedProceduresList));
        let newSelectedProceduresInfo = JSON.parse(JSON.stringify(state.selectedProceduresInfo));

        // For comfort, retrieve the list of procedures related to the anomaly to be removed.
        let thisAnomalyProcedures = JSON.parse(JSON.stringify(state.selectedAnomaliesInfo[anomalyName]));

        // Search the index of the anomaly to be deleted within the anomaly list
        let indexAnomalyToDelete = 0;
        for (let index in newSelectedAnomaliesList) {
            let anomaly = newSelectedAnomaliesList[index];
            if (anomaly === anomalyName) {
                indexAnomalyToDelete = index;
            }
        }

        // Delete the anomaly list item and the anomaly info key
        newSelectedAnomaliesList.splice(indexAnomalyToDelete, 1);
        delete newSelectedAnomaliesInfo[anomalyName];

        // For each procedure related to the anomaly, check if it has to be deleted or not (that is, if there is any of
        // the other selected anomalies that is also related to the procedure)
        let proceduresToDelete = [];
        for (let index in thisAnomalyProcedures['anomalyProcedures']) {
            let procedure = thisAnomalyProcedures['anomalyProcedures'][index];
            let isRelatedToAnotherAnomaly = false;
            for (let otherAnomalyName in newSelectedAnomaliesInfo) {
                // Note that the entry to the anomaly that has to be deleted has already been removed from the dictionary
                let otherAnomalyProcedures = newSelectedAnomaliesInfo[otherAnomalyName]['anomalyProcedures'];
                if (otherAnomalyProcedures.includes(procedure)) {
                    isRelatedToAnotherAnomaly = true;
                }
            }
            if (!isRelatedToAnotherAnomaly) {
                proceduresToDelete.push(procedure);
            }
        }

        // For each procedure to be deleted...
        for (let index in proceduresToDelete) {
            // ... find the index of the procedure to be deleted from the procedure list...
            let procedureToDelete = proceduresToDelete[index];
            let indexProcedureToDelete = 0;
            for (let index in newSelectedProceduresList) {
                let procedure = newSelectedProceduresList[index];
                if (procedure === procedureToDelete) {
                    indexProcedureToDelete = index;
                }
            }

            // Delete the procedure list item and the procedure info key
            newSelectedProceduresList.splice(indexProcedureToDelete, 1);
            delete newSelectedProceduresInfo[procedureToDelete];
        }

        // Perform the commits
        commit('mutateSelectedAnomaliesList', newSelectedAnomaliesList);
        commit('mutateSelectedAnomaliesInfo', newSelectedAnomaliesInfo);
        commit('mutateSelectedProceduresList', newSelectedProceduresList);
        commit('mutateSelectedProceduresInfo', newSelectedProceduresInfo);
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
        commit('mutateLastUpdatedAnomaliesTimestamp', formattedDate);
        commit('mutateLastUpdatedProceduresTimestamp', formattedDate);
        commit('mutateLastUpdatedProceduresInfoTimestamp', formattedDate);
    },
    updateProcedureDict({state, commit}, newProcedureDict) {
        // A copy of the state variable to be modified is made
        let newSelectedProceduresInfo = JSON.parse(JSON.stringify(state.selectedProceduresInfo));

        // The updated procedure information is parsed
        let procedureName = newProcedureDict['procedureName'];
        let procedureStepsList = newProcedureDict['procedureSteps'];
        let procedureCurrentStep = newProcedureDict['procedureCurrentStep'];
        let checkableSteps = newProcedureDict['checkableSteps'];
        let checkableStepsList = newProcedureDict['checkableStepsList'];
        let procedureObjective = newProcedureDict['procedureObjective'];
        let procedureEquipment = newProcedureDict['procedureEquipment'];
        let procedureReferences = newProcedureDict['procedureReferences'];
        let procedureReferenceLinks = newProcedureDict['procedureReferenceLinks'];
        let procedureFigures = newProcedureDict['procedureFigures'];
        let procedureIsOpen = newProcedureDict['procedureIsOpen'];

        // The copy is modified
        newSelectedProceduresInfo[procedureName] = {
            'procedureStepsList': procedureStepsList,
            'procedureCurrentStep': procedureCurrentStep,
            'checkableSteps': checkableSteps,
            'checkableStepsList': checkableStepsList,
            'procedureObjective': procedureObjective,
            'procedureEquipment': procedureEquipment,
            'procedureReferences': procedureReferences,
            'procedureReferenceLinks': procedureReferenceLinks,
            'procedureFigures': procedureFigures,
            'procedureIsOpen': procedureIsOpen,
        };

        // Perform the commit
        commit('mutateSelectedProceduresInfo', newSelectedProceduresInfo);
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
        commit('mutateLastUpdatedProceduresInfoTimestamp', formattedDate);
    },
    async requestDiagnosis({state, commit}, selectedSymptomsList) {
        // Clean the current diagnosis report
        commit('mutateDiagnosisReport', []);

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

          console.log("formatttttttttttt", formattedDate)
        commit('mutateLastUpdatedDiagnosisTimestamp', formattedDate);

        console.log("mutateeeeeeeee updateeeeeeeeee", now, "55555555555555");
    

        // Update the last selected symptoms list
        let lastSelectedSymptomsList = JSON.parse(JSON.stringify(state.selectedSymptomsList));
        commit('mutateLastSelectedSymptomsList', lastSelectedSymptomsList);

        // Clean the selected symptoms list
        //commit('mutateSelectedSymptomsList', []);

        // Make a local copy of the couple of state variables to be used
        let info = JSON.parse(JSON.stringify(state.telemetryInfo));
        let telemetryValues = state.telemetryValues;
        console.log("telemetry values", telemetryValues)
        console.log("selectedSymptomsList", selectedSymptomsList)
        let parsedSelectedSymptomsList = JSON.parse(JSON.stringify(selectedSymptomsList));


        // Parse the selected symptoms list. Such list contains the names of each measurement with the level add-on
        // (for example, "ppN2 (L1)". To query the knowledge graph, such add-on should be removed (amazing).

        for (let index in parsedSelectedSymptomsList) {
            let displayName = parsedSelectedSymptomsList[index]['measurement'];
            let kgName = info[displayName]['kg_name'];
            parsedSelectedSymptomsList[index]['measurement'] = kgName;
            parsedSelectedSymptomsList[index]['display_name'] = displayName;
        }

       

        // Make the diagnosis request to the backend
        let reqData = new FormData();
        let telemetryValuesDict = Object.fromEntries(
            Object.entries(telemetryValues).map(([key, value]) => [key, { ...value }])
        );
        
        let parsedTelemetryValues = {};

        for (let i in telemetryValuesDict) { 
            let value = telemetryValuesDict[i];
            let valueDict = telemetryValuesDict[i];
            const reversedArray = Object.entries(valueDict)
                .reverse()  // Reverse the array
                .map(([key, value]) => [Number(key), value]);  // Convert keys back to numbers if needed

            console.log("telemetry reversed array", reversedArray)

                // Convert the array back into an object
            console.log("telemetry reversed array i", reversedArray[0])
            parsedTelemetryValues[i] = reversedArray[0][1];
            // console.log("telemetry reversed dict value", reversedValueDict)
            // for (let j in value) {
            //     console.log("telemetry dict value j", value[j])
            // if (value[j] != null || value[j] != undefined) {
            //         parsedTelemetryValues[i] = value[j];
            //         break;
            //     }
            // }
            // console.log("telemetry dict value", value)
        }

        console.log("parsed telemetry values", parsedTelemetryValues); 


        // for (let key in telemetryValues) {
        //     const plainObj = JSON.parse(JSON.stringify(telemetryValues[key]));
    
        //     // Find the first numeric value in the object (excluding __ob__ property)
        //     let firstValueIndex = null;
        //     for (let i = 0; i < Object.keys(plainObj).length; i++) {
        //         if (!isNaN(Number(plainObj[i])) && plainObj[i] !== null && plainObj[i] !== undefined) {
        //             firstValueIndex = i;
        //             break;
        //         }
        //     }
            
        //     // Use the found index, or undefined if none found
        //     parsedTelemetryValues[key] = firstValueIndex !== null ? plainObj[firstValueIndex] : undefined;
        //     console.log("telemetry value each", parsedTelemetryValues[key]);
        // }

        console.log("parsedTelemetryValues", parsedTelemetryValues)
        console.log("telemetry values", telemetryValues)
        reqData.append('symptomsList',  JSON.stringify(parsedSelectedSymptomsList));
        reqData.append('telemetryValues',  JSON.stringify(parsedTelemetryValues));
        let response = await fetchPost('/api/at/requestDiagnosis', reqData);
        if (response.ok) {
            let diagnosis_report = await response.json();
            console.log("new diagnosis_report from backend", diagnosis_report)
            commit('mutateDiagnosisReport', diagnosis_report);
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
        commit('mutateLastUpdatedDiagnosisTimestamp', formattedDate);
        } else {
            console.log('Error requesting a diagnosis report.')
            return [];
        }
    },
    async loadAllAnomalies({state, commit}) {
        let reqData = new FormData();
        let response = await fetchPost('/api/at/loadAllAnomalies', reqData);
        if (response.ok) {
            let anomaly_list = await response.json();
            commit('mutateAllAnomaliesList', anomaly_list);
        } else {
            console.log('Error loading the anomalies list.');
        }
    },
    async completeTutorial(state) {
        let reqData = new FormData();
        await fetchPost(API_URL + 'at/completeTutorial', reqData);
    },
    async recoverSymptomsList({state, commit}) {
        let lastSymptomsList = state.lastSelectedSymptomsList;
        commit('mutateSelectedSymptomsList', lastSymptomsList);
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
        commit('mutateLastUpdatedSymptomsTimestamp', formattedDate);
    },
    async triggerAlarm(state, alarm) {
        if (alarm === 'alarmIn') {
            let audio = new Audio(startAnomalySound);
            await audio.play();
        }
        else if (alarm === 'alarmOut') {
            let audio = new Audio(endAnomalySound);
            await audio.play();
        }
    }
};

const mutations = {
    mutateLoginStatus(state, newVal) {state.isLoggedIn = newVal},
    mutateHeraUser(state, newVal) {state.heraUser = newVal; },
    mutateTelemetryIsOngoing(state, telemetryIsOngoing) {state.telemetryIsOngoing = telemetryIsOngoing; },
    mutateTelemetryType(state, telemetryType) {state.telemetryType = telemetryType; },
    mutateTelemetryPlotData(state, newVal) {state.telemetryPlotData = newVal; },
    mutateTelemetryValues(state, newVal) {state.telemetryValues = newVal; },
    mutateTelemetryInfo(state, newVal) {state.telemetryInfo = newVal; },
    mutateTelemetryInputVariables(state, newVal) {state.telemetryInputVariables = newVal; },
    mutateTelemetryPlotSelectedVariables(state, newVal) {state.telemetryPlotSelectedVariables = newVal; },
    mutateSymptomsList(state, newVal) {state.symptomsList = newVal; },
    mutateSelectedSymptomsList(state, newVal) {state.selectedSymptomsList = newVal; },
    mutateSelectedLeftSymptomsList(state, newVal) {state.selectedLeftSymptoms = newVal; },
    mutateSelectedRightSymptomsList(state, newVal) {state.selectedRightSymptoms = newVal; },
    mutateLastSelectedSymptomsList(state, newVal) {state.lastSelectedSymptomsList = newVal; },
    mutateDiagnosisReport(state, newVal) {state.diagnosisReport = newVal; },
    mutateAllAnomaliesList(state, newVal) {state.allAnomaliesList = newVal; },
    mutateSelectedAnomaliesList(state, newVal) {state.selectedAnomaliesList = newVal; },
    mutateSelectedAnomaliesInfo(state, newVal) {state.selectedAnomaliesInfo = newVal; },
    mutateSelectedProceduresList(state, newVal) {state.selectedProceduresList = newVal; },
    mutateSelectedProceduresInfo(state, newVal) {state.selectedProceduresInfo = newVal; },
    mutateLoadingNewAnomaly(state, newVal) {state.loadingNewAnomaly = newVal; },
    setIsTelemetryInitialized(state, isTelemetryInitialized) {state.isTelemetryInitialized = isTelemetryInitialized; },
    mutatePlayAlarms(state) {state.playAlarms = !state.playAlarms; },
    setTelemetryType(state, telemetryType) {state.telemetryType = telemetryType; },
    mutateIsChatVisible(state) {state.isChatVisible = !state.isChatVisible},
    restoreDaphneAT(state, recoveredState) {
        Object.keys(recoveredState).forEach((key) => {
            state[key] = recoveredState[key];
        });
    },
    mutateSymptomsTimestamp(state, newVal) { state.symptoms_timestamp = newVal },
    mutateLastUpdatedSymptomsTimestamp(state, newVal) { state.lastUpdatedSymptomsTimestamp = newVal},
    mutateLastUpdatedAnomaliesTimestamp(state, newVal) { state.lastUpdatedAnomaliesTimestamp = newVal},
    mutateLastUpdatedProceduresTimestamp(state, newVal) { state.lastUpdatedProceduresTimestamp = newVal},
    mutateLastUpdatedProceduresInfoTimestamp(state, newVal) { state.lastUpdatedProceduresInfoTimestamp = newVal},
    mutateLastUpdatedDiagnosisTimestamp(state, newVal) { state.lastUpdatedDiagnosisTimestamp = newVal},
};

export default {
    state,
    getters,
    actions,
    mutations,
}
