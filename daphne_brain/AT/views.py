import json
import re
import time
from asyncio import sleep
from datetime import datetime
import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

# THREADS + QUEUES
import AT.global_objects as global_obj
from AT.neo4j_queries.query_functions import diagnose_symptoms_by_intersection_with_anomaly, \
    retrieve_figures_from_procedure, retrieve_references_from_procedure, retrieve_reference_links_from_procedure, \
    get_explanations_from_historical_database, get_astrobee_procedure_list_from_pride
from AT.neo4j_queries.query_functions import retrieve_all_anomalies
from AT.neo4j_queries.query_functions import retrieve_equipment_from_procedure
from AT.neo4j_queries.query_functions import retrieve_fancy_steps_from_procedure
from AT.neo4j_queries.query_functions import retrieve_objective_from_procedure
from AT.neo4j_queries.query_functions import retrieve_procedures_fTitle_from_anomaly
from auth_API.helpers import get_or_create_user_information
from daphne_context.models import UserInformation
from AT.diagnosis.bayesian.ECLSS_Bayesian_Network import get_probabilities
from AT.diagnosis.physics.physics_diagnosis import create_physics_diagnosis_report
from AT.diagnosis.physics.telemetry_storage import telemetry_storage
from django.conf import settings


def is_biosim_connected():
    """
    Check if BioSim is currently connected/active by checking the physics simulation mode.
    
    Returns:
        bool: True if BioSim is connected, False otherwise
    """
    return settings.PHYSICS_SIMULATION_MODE == 'biosim'

def get_simulation_mode():
    return settings.PHYSICS_SIMULATION_MODE
    

astrobee_status = 'NA'
response = 'NA'
countdown = 10
procedure_static_id = ""
global_procedure_runtime_ID = ""


def check_threads_status():
    hub_is_alive = global_obj.hub_thread.is_alive()
    sEclss_is_alive = global_obj.sEclss_thread.is_alive()
    sim_is_alive_one = global_obj.simulator_threads[0].is_alive()
    sim_is_alive_two = global_obj.simulator_threads[1].is_alive()
    sim_is_alive_three = global_obj.simulator_threads[2].is_alive()
    sim_is_alive_four = global_obj.simulator_threads[3].is_alive()
    sEclss_at_is_alive = global_obj.sEclss_at_thread.is_alive()
    sim_at_is_alive_one = global_obj.simulator_at_threads[0].is_alive()
    sim_at_is_alive_two = global_obj.simulator_at_threads[1].is_alive()
    sim_at_is_alive_three = global_obj.simulator_at_threads[2].is_alive()
    sim_at_is_alive_four = global_obj.simulator_at_threads[3].is_alive()

    # Check if all the treads are in a healthy status. Display a message according to the result.
    if hub_is_alive and sEclss_is_alive and sim_is_alive_one and sim_is_alive_two and sim_is_alive_three \
            and sim_is_alive_four and sEclss_at_is_alive and sim_at_is_alive_one and sim_at_is_alive_two \
            and sim_at_is_alive_three and sim_at_is_alive_four:
        print('**********\nAll AT threads started successfully.\n**********')
    else:
        print('**********')
        if not hub_is_alive:
            print('Hub thread start failure.')
        if not sEclss_is_alive:
            print('sEclss thread start failure.')
        if not sim_is_alive_one:
            print('Simulator thread 1 start failure.')
        if not sim_is_alive_two:
            print('Simulator thread 2 start failure.')
        if not sim_is_alive_three:
            print('Simulator thread 3 start failure.')
        if not sim_is_alive_four:
            print('Simulator thread 4 start failure.')
        if not sEclss_at_is_alive:
            print('Anomaly treatment thread for sEclss start failure.')
        if not sim_at_is_alive_one:
            print('Anomaly treatment thread 1 for the simulator thread start failure.')
        if not sim_at_is_alive_two:
            print('Anomaly treatment thread 2 for the simulator thread start failure.')
        if not sim_at_is_alive_three:
            print('Anomaly treatment thread 3 for the simulator thread start failure.')
        if not sim_at_is_alive_four:
            print('Anomaly treatment thread 4 for the simulator thread start failure.')
        print('**********')
    return


class SeclssFeed(APIView):
    def post(self, request):
        if 'habitatStatus' in request.data:
            parameters_data = request.data['habitatStatus']
            parsed_sensor_data = json.loads(parameters_data)

            if global_obj.sEclss_thread is not None \
                    and global_obj.sEclss_thread.is_alive() \
                    and global_obj.sEclss_thread.name == "Real Telemetry Thread":
                global_obj.server_to_sEclss_queue.put(
                    {'type': 'sensor_data', 'content': parsed_sensor_data['Parameters']})
            return Response(parsed_sensor_data)
        else:
            print(request.data)
            print(request.headers)
            print('ERROR retrieving the sensor data from the Lab simulator')
            return Response({
                "status": "error",
                "message": "ERROR retrieving the sensor data from the Lab simulator"
            })


class UserResponse(APIView):
    def get(self, request):
        date = datetime.now().astimezone().isoformat()
        global countdown
        countdown = countdown - 1
        if countdown < 0:
            user_response = {'sysrepName': 'daphne_yaml', 'dataReferenceQuality': 'GOOD', 'dataReferenceTime': date,
                             'dataReferenceDetail': 'A telemetry message from Daphne', 'type': 'STRING',
                             'humanValue': "", 'rawValue': ""}
        else:
            global response
            humanValue = response
            user_response = {'sysrepName': 'daphne_yaml', 'dataReferenceQuality': 'GOOD', 'dataReferenceTime': date,
                             'dataReferenceDetail': 'A telemetry message from Daphne', 'type': 'STRING',
                             'humanValue': humanValue, 'rawValue': humanValue}
        return JsonResponse(user_response, status=201, safe=False)


class YesOrNO(APIView):
    def post(self, request):
        global astrobee_status
        # print("yes or no status:", astrobee_status)
        # print("yes or not data:", request.data)
        if 'user_response' in request.data:
            global response
            response = request.data['user_response']
            response = response.replace('"', '')
            response = ''
            astrobee_status = 'Response received.'
            global countdown
            countdown = 15
            status = {'astrobee_status': astrobee_status}
            print("inside if yes or no")
            return Response(astrobee_status)
        else:
            status = {'astrobee_status': astrobee_status}
            return Response(status)


class PrideStatus(APIView):
    def post(self, request):
        date = datetime.now().astimezone().isoformat()
        # print("pride view", request.data)
        if 'initialData' in request.data:
            params = request.data['initialData']
            status = params[0]['argValue']
            global astrobee_status
            astrobee_status = status
        return HttpResponse(status=200)


class AstrobeeStatus(APIView):
    def post(self, request, format=None):
        # print("astrobee_status:", astrobee_status)
        status = {'astrobee_status': astrobee_status}
        return Response(status)
    
class GetCurrentInstruction(APIView):
    def post(self, request, format=None):

        url = "https://10.5.0.3:8000/api/procedures/" + global_procedure_runtime_ID + "/currentInstruction"
        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer a57a391b-5e00-4872-844e-66d975e73c0a'
        }       
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        # print("get pride shared variables response procedure id", global_procedure_runtime_ID)
        if response.status_code == 200:
            try:
                instruction_data = response.json()
                
                # Extract the important information from the response
                current_instruction = {
                    'text': instruction_data.get('text', ''),
                    'instructionType': instruction_data.get('instructionType', ''),
                    'instructionIdentifier': instruction_data.get('instructionIdentifier', ''),
                    'elementID': instruction_data.get('elementID', ''),
                    'userResponseType': instruction_data.get('userResponseType', []),
                    'status': instruction_data.get('status', ''),
                    'instructionNumber': instruction_data.get('instructionNumber', ''),
                    'dataType': instruction_data.get('dataType', ''),  # For record instructions
                    'dataNomenclature': instruction_data.get('dataNomenclature', ''),  # For record instructions
                    'description': instruction_data.get('description', {})
                }
                
                # Handle different instruction types
                if instruction_data.get('instructionType') == 'manualInstruction':
                    current_instruction['requires_user_action'] = True
                    current_instruction['action_type'] = 'manual'
                elif instruction_data.get('instructionType') == 'record':
                    current_instruction['requires_user_action'] = True
                    current_instruction['action_type'] = 'record'
                elif instruction_data.get('instructionType') == 'step':
                    current_instruction['requires_user_action'] = True
                    current_instruction['action_type'] = 'step'
                else:
                    current_instruction['requires_user_action'] = False
                    current_instruction['action_type'] = 'none'
                
                print("Current instruction extracted:", current_instruction)
            
                return Response({
                    "instruction_data": current_instruction,
                    "full_response": instruction_data
                })
            except json.JSONDecodeError:
                # print("Error decoding JSON response")
                return Response({"error": "Invalid response format"}, status=500)
            
        else:
            # print(f"Error fetching current instruction: {response.status_code}")
            return Response({"error": f"API request failed with status code: {response.status_code}"}, 
                           status=response.status_code)


        #-------if there is no pride server running, return a dummy instruction for testing purposes
        # This is a placeholder for testing purposes. In a real scenario, you would fetch the current instruction from the Pride API.
        # Comment out below to use pride server or Uncomment below to use dummy instruction for testing purposes
        
        # global global_procedure_runtime_ID
        # if global_procedure_runtime_ID == "":
        #     global_procedure_runtime_ID = "dummy_procedure_runtime_id"
        # dummy_instruction = {
        #     "text": "This is a dummy instruction for testing.",
        #     "instructionType": "test",
        #     "instructionNumber": 1,
        #     "userResponseType": ["real"],
        #     "status": "active",
        #     "instructionIdentifier": "dummy-001"
        # }

        # return Response({
        #     "instruction_data": dummy_instruction
        # })


class CompleteInstruction(APIView):
    def post(self, request, format=None):
        global global_procedure_runtime_ID
        
        try:
            instruction_data = json.loads(request.data['instruction_data'])
            activity = request.data['activity']
            record_value = request.data.get('record_value', None)
            
            # Get instruction identifier
            instruction_id = (instruction_data.get('instructionIdentifier') or 
                            instruction_data.get('elementID'))
            
            if not instruction_id:
                return Response({
                    "status": "error",
                    "message": "No instruction identifier found"
                }, status=400)
            
            print(f"Completing instruction with ID: {instruction_id}")
            print(f"Instruction type: {instruction_data.get('instructionType')}")
            
            # Prepare request body for PRIDE API
            request_body = {
                "user": "test",
                "loginID": "test",
                "date": datetime.now().isoformat(),
                "elementID": instruction_id,
                "activity": activity
            }
            
            # Add record value if this is a record instruction
            if record_value is not None:
                request_body["record"] = record_value
                print(f"Adding record value: {record_value}")
            
            print(f"Sending request to PRIDE: {request_body}")
            
            # Call PRIDE API to complete the instruction
            url = f"https://10.5.0.3:8000/api/procedures/running/{global_procedure_runtime_ID}"
            headers = {
                'Authorization': 'Bearer a57a391b-5e00-4872-844e-66d975e73c0a',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(url, headers=headers, json=request_body, verify=False)
            
            if response.ok:
                print(f"Instruction {instruction_id} completed successfully")
                return Response({
                    "status": "success",
                    "message": f"Instruction completed successfully",
                    "pride_response": response.text
                })
            else:
                print(f"Failed to complete instruction. Status: {response.status_code}, Response: {response.text}")
                return Response({
                    "status": "error",
                    "message": f"Failed to complete instruction: {response.status_code}",
                    "pride_response": response.text
                }, status=response.status_code)
                
        except Exception as e:
            print(f"Error completing instruction: {e}")
            return Response({
                "status": "error",
                "message": f"Error completing instruction: {str(e)}"
            }, status=500)


    

class GetPrideSharedVariables(APIView):
    def post(self, request, format=None):

        url = "https://10.5.0.3:8000/api/sharedVariables/telemetry/" + global_procedure_runtime_ID + "?fromSystemRepresentation=Gateway_Robots" 
        # url = "https://localhost:8000/api/procedures/" + global_procedure_runtime_ID + "currentInstruction"
        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer a57a391b-5e00-4872-844e-66d975e73c0a'
        }       
        response = requests.request("GET", url, headers=headers, data=payload, verify=False)
        # print("get pride shared variables response procedure id", global_procedure_runtime_ID)
        # print("get pride shared variables response", response) 
            # start automation of the procedure
        
        if response.status_code == 200:
            pass
            # print("shared variables response", response)
            # print("shared variables response text", response.text)

           
        return Response()



class StartAstrobeeProcedure(APIView):
    def post(self, request, format=None):
        global procedure_static_id, global_procedure_runtime_ID
        procedure_staticID = request.data['procedureID'].replace('"', '')
        procedure_static_id = procedure_staticID
        print("procedure static id is set", procedure_staticID)

        # start/open a procedure to send astrobee
        url = "https://10.5.0.3:8000/api/procedures/available/" + procedure_staticID

        payload = json.dumps({
            "user": "test",
            "startWithAutomation": "true",
            "finishWithAutomation": "true"
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer a57a391b-5e00-4872-844e-66d975e73c0a'
        }

        try:
            response = requests.request("POST", url, headers=headers, data=payload, verify=False)
            
            if response.ok:
                procedure_runtime_ID = response.text.replace('"', '')
                global_procedure_runtime_ID = procedure_runtime_ID
                print("started astrobee procedure", response)

                # start automation of the procedure
                automation_url = f'https://10.5.0.3:8000/api/procedures/{procedure_runtime_ID}/startAutomation'
                automation_payload = json.dumps({"user": "test"})
                
                automation_response = requests.request("PUT", automation_url, headers=headers, data=automation_payload, verify=False)
                print("Starting automation for procedure:", procedure_runtime_ID)
                print("Automation response status:", automation_response.status_code)
                
                global astrobee_status
                astrobee_status = f"Astrobee procedure {procedure_runtime_ID} started."

                return Response({
                    "status": astrobee_status,
                    "procedure_runtime_id": procedure_runtime_ID
                })
            else:
                print(f"Failed to start procedure. Status: {response.status_code}, Response: {response.text}")
                return Response({
                    "status": "error",
                    "message": f"ERROR starting the procedure. Status: {response.status_code}"
                }, status=400)
                
        except requests.exceptions.RequestException as e:
            print(f"Request exception when starting procedure: {e}")
            return Response({
                "status": "error",
                "message": f"Network error when starting procedure: {str(e)}"
            }, status=500)
        except Exception as e:
            print(f"Unexpected error when starting procedure: {e}")
            return Response({
                "status": "error",
                "message": f"Unexpected error: {str(e)}"
            }, status=500)


class HeraFeed(APIView):
    def post(self, request):
        # print("in hera feed")
        # habitatStatus
        try:
            content_type = request.headers.get('Content-Type', '')
            # print("content type", request.data)
            if '_content_type' in request.data:
                    # Handle direct JSON POST
                # print("handling direct json data 1")
                if '_content' in request.data:
                    # print("handling direct json data 2")
                    # Parse the content field
                    # print("in content", request.data.get('_content'))
                    content = json.loads(request.data.get('_content'))
                    parsed_sensor_data = content.get('habitatStatus', {})
                    # print("got the sensor data", parsed_sensor_data)
                else:
                    # Direct habitatStatus field
                    # print("in habitat status directly")
                    # print("handling direct json data 3")
                    parsed_sensor_data = request.data.get('habitatStatus', {})
            else:
                if 'habitatStatus' in request.data:
                    # print("not handling direct json data")
                    parameters_data = request.data['habitatStatus']
                    # print("finally", request.data)
                    if isinstance(parameters_data, dict):
                        parsed_sensor_data = parameters_data
                    elif isinstance(parameters_data, (str, bytes, bytearray)):
                        parsed_sensor_data = json.loads(parameters_data)
                    else:
                        # print("no query dict")
                        parsed_sensor_data = parameters_data
                else:
                    return Response({
                        "error": "No habitat status data found"
                    }, status=400)

            # Store telemetry data for physics diagnosis
            if 'Parameters' in parsed_sensor_data:
                try:
                    parameters_list = parsed_sensor_data['Parameters']
                    # print(f"🔄 HeraFeed: Storing telemetry data with {len(parameters_list)} parameters")
                    #print(f"📊 HeraFeed: Raw Parameters data: {json.dumps(parameters_list, indent=2)}")
                    
                    # Convert list of sensor objects to dictionary for easier access
                    telemetry_dict = {}
                    for sensor in parameters_list:
                        if isinstance(sensor, dict) and 'Name' in sensor and 'currentValue' in sensor:
                            # Create key as "Name (ParameterGroup)" for unique identification
                            sensor_key = f"{sensor['Name']} ({sensor.get('ParameterGroup', 'Unknown')})"
                            telemetry_dict[sensor_key] = sensor['currentValue']
                    
                    # Determine if we should use BioSim parameter format
                    use_biosim_format = is_biosim_connected()
                    data_source = 'BioSim' if use_biosim_format else 'Hera'
                    
                    # Convert to BioSim parameter names if BioSim is connected

                    # print(f"�📊 HeraFeed: Telemetry sensors: {list(telemetry_dict.keys())}")
                    
                    # Check for target sensor (adjust based on format)
                    target_sensor = 'ppCO2_IHab (IHab)' if use_biosim_format else 'ppCO2 (L1)'
                    if target_sensor in telemetry_dict:
                        pass
                        # print(f"✅ HeraFeed: Found {target_sensor} = {telemetry_dict[target_sensor]}")
                    else:
                        print(f"❌ HeraFeed: {target_sensor} not found in telemetry data")
                        # Look for any CO2-related sensors
                        co2_sensors = [k for k in telemetry_dict.keys() if 'CO2' in k or 'co2' in k]
                        # print(f"🔍 HeraFeed: Available CO2-related sensors: {co2_sensors}")
                    
                    # Store telemetry data with appropriate source and format
                    telemetry_record = telemetry_storage.store_telemetry(
                        telemetry_data=telemetry_dict,
                        source=data_source,
                        metadata={
                            'api_endpoint': 'HeraFeed',
                            'parameter_format': 'biosim' if use_biosim_format else 'hera',
                            'original_data': {'Parameters': parameters_list}  # Store original data for sensor info
                        }
                    )
                    # print(f"💾 HeraFeed: Successfully stored telemetry record ID: {telemetry_record.id}")
                    
                except Exception as e:
                    print(f"❌ HeraFeed: Error storing telemetry data: {e}")
                    import traceback
                    traceback.print_exc()
            
            if global_obj.hera_thread is not None \
                    and global_obj.hera_thread.is_alive() \
                    and global_obj.hera_thread.name == "Hera Telemetry Thread":
                global_obj.server_to_hera_queue.put(
                    {'type': 'sensor_data', 'content': parsed_sensor_data['Parameters']})
            return Response(parsed_sensor_data)
        # else:
        #     print(request.data)
        #     print(request.headers)
        #     print('ERROR retrieving the sensor data from the Hera simulator')
        #     return Response({
        #         "status": "error",
        #         "message": "ERROR retrieving the sensor data from the Hera simulator"
        #     })
        except json.JSONDecodeError as e:
            return Response({
                "error": f"Invalid JSON format: {str(e)}"
            }, status=400)
        except Exception as e:
            return Response({
                "error": f"Server error: {str(e)}"
            }, status=500)

class RequestKGDiagnosis(APIView):
    def post(self, request):
        try:
            # Retrieve the symptoms list from the request
            symptoms_list = json.loads(request.data['symptomsList'])

            # Query the neo4j graph (do not delete first line until second one is tested)
            # diagnosis_list = diagnose_symptoms_by_subset_of_anomaly(parsed_symptoms_list)

            diagnosis_list = diagnose_symptoms_by_intersection_with_anomaly(symptoms_list, get_simulation_mode())

            # Build the diagnosis report and send it to the frontend
            diagnosis_report = {'symptoms_list': symptoms_list, 'diagnosis_list': diagnosis_list}
            print("diagnosis report", diagnosis_report)

            return Response(diagnosis_report)
            
        except Exception as e:
            print(f"Error in RequestKGDiagnosis: {e}")
            # Return a graceful error response
            return Response({
                'error': 'Unable to perform knowledge graph diagnosis at this time. Please try again later.',
                'details': str(e),
                'symptoms_list': symptoms_list if 'symptoms_list' in locals() else [],
                'diagnosis_list': []
            }, status=500)

class RequestDiagnosis(APIView):
    def post(self, request):
        # Retrieve the symptoms list from the request
        symptoms_list = json.loads(request.data['symptomsList'])
        telemetry_values = json.loads(request.data['telemetryValues'])
        telemetry_values_t1 = json.loads(request.data['telemetryValuest1'])
        addtional_evidence = None
        if 'additionalEvidence' in request.data:
            addtional_evidence = json.loads(request.data['additionalEvidence'])
        print("previous telemetry values", telemetry_values)
        print("got additional evidence", addtional_evidence) 
        updated_telemetry_values = {}
        for i in telemetry_values:
            if ("Cabin Temperature" in i or "Humidity" in i or "ppCO2" in i or "ppH2" in i or 
            "ppO2" in i or "ppN2" in i or "Pressure" in i or "Total Cabin Pressure" in i or "H2O" in i):
                # print("telemetry x", i)
                x = i
                # print("telemetry x" , x, i)
                updated_telemetry_values[i] = float(telemetry_values[i])

            else:
                x = i.split('(')[0].strip()
                updated_telemetry_values[x] = float(telemetry_values[i])
        telemetry_values = updated_telemetry_values
        for i in telemetry_values_t1:
            if ("Cabin Temperature" in i or "Humidity" in i or "ppCO2" in i or "ppH2" in i or 
            "ppO2" in i or "ppN2" in i or "Pressure" in i or "Total Cabin Pressure" in i or "H2O" in i):
                # print("telemetry x", i)
                x = i
                # print("telemetry x" , x, i)
                name = i + " (t-1)"
                telemetry_values[name] = float(telemetry_values_t1[i])

            else:
                x = i.split('(')[0].strip()
                name = x + " (t-1)"
                telemetry_values[name] = float(telemetry_values_t1[i])
    
        print("herrrre----------------------------------")
        print("symptoms list",symptoms_list)
        print("telemetry values",telemetry_values)


        # Query the neo4j graph (do not delete first line until second one is tested)
        # diagnosis_list = diagnose_symptoms_by_subset_of_anomaly(parsed_symptoms_list)
        # diagnosis_list = diagnose_symptoms_by_intersection_with_anomaly(symptoms_list)
        diagnosis_list = []
        
        # Get initial probabilities WITHOUT calculating best evidence (for faster response)
        probabilities, _, hidden_components = get_probabilities(
            telemetry_values, 
            additional_evidence=addtional_evidence,
            calculate_best_evidence=False  # Skip best evidence for now
        )
        
        top_5_probabilities = dict(sorted(probabilities.items(), 
                                     key=lambda item: item[1], 
                                     reverse=True)[:5])
        
        final_report = []
        for anomaly, probability in top_5_probabilities.items():
            # Get the explanations from the historical database
            # Append the anomaly and its explanation to the final report
            final_report.append({
                'anomaly': anomaly,
                'probability': probability,
            })
        
        print("66666666666666666666666")
        print("Initial probabilities: ", probabilities)
        


        print("done1-----------------------------------")

        # Send request to pride to get all the procedures
        # astrobee_procedure_list = get_astrobee_procedure_list_from_pride()
        astrobee_procedure_list = None
        print("astrovee procedure list", astrobee_procedure_list)
        print("done2-----------------------------------")

        # Build the diagnosis report and send it to the frontend
        diagnosis_report = {
            'symptoms_list': symptoms_list, 
            'diagnosis_list': final_report, 
            'best_evidence': None,  # Will be calculated separately
            'hidden_components': hidden_components,
            'astrobee_procedure_list': astrobee_procedure_list,
            'current_telemetry_values': telemetry_values,
            'calculating_best_evidence': True  # Flag to indicate best evidence is being calculated
        }

        return Response(diagnosis_report)


class CalculateBestEvidence(APIView):
    def post(self, request):
        """
        Calculate the best evidence for a given diagnosis.
        This is called after initial probabilities are returned to the user.
        """
        telemetry_values = json.loads(request.data['telemetryValues'])
        additional_evidence = None
        if 'additionalEvidence' in request.data:
            additional_evidence = json.loads(request.data['additionalEvidence'])
        
        print("Calculating best evidence for telemetry values")
        
        # Now calculate with best evidence
        probabilities, best_evidence, hidden_components = get_probabilities(
            telemetry_values, 
            additional_evidence=additional_evidence,
            calculate_best_evidence=True  # Calculate best evidence this time
        )
        
        response = {
            'best_evidence': best_evidence,
            'hidden_components': hidden_components
        }
        
        return Response(response)


class RequestPhysicsDiagnosis(APIView):
    def post(self, request):
        # Retrieve the symptoms list from the request
        symptoms_list = json.loads(request.data['symptomsList'])
        
        # Retrieve target anomaly if provided (from Bayesian diagnosis)
        target_anomaly = request.data.get('target_anomaly', None)
        print("Received target anomaly:", target_anomaly)
        if target_anomaly:
            target_anomaly = re.sub(r'\s*\(.*?\)\s*', '', target_anomaly).strip()
            print("Cleaned target anomaly:", target_anomaly)
        
        
        # target_anomaly = 'CDRA Failure'
        # if target_anomaly == 'No Anomalies Present':
        #     target_anomaly = 'CDRA Failure'
        #     print("No target anomaly provided, defaulting to 'CDRA Failure'")
        print("🔬 RequestPhysicsDiagnosis: Starting physics diagnosis")
        print(f"📋 RequestPhysicsDiagnosis: Symptoms list: {symptoms_list}")
        if target_anomaly:
            print(f"🎯 RequestPhysicsDiagnosis: Target anomaly from Bayesian: {target_anomaly}")
        
        # Define target telemetry sensor for physics diagnosis
        # target_telemetry_sensor = 'ppCO2_IHab (IHab)'
        target_telemetry_sensor = 'ppCO2_IHab (IHab)' if is_biosim_connected() else 'ppCO2 (L1)'
        print(f"🎯 RequestPhysicsDiagnosis: Target telemetry sensor: {target_telemetry_sensor}")
        
        # Optional simulation controls from frontend
        try:
            sim_duration_seconds = int(request.data.get('sim_duration_seconds'))
        except Exception:
            print("Error getting sim duration seconds")
        try:
            sampling_rate_seconds = int(request.data.get('sampling_rate_seconds'))
        except Exception:
            print("Error getting sampling rate seconds")
        print(f"[API] PhysicsDiagnosis controls: duration={sim_duration_seconds}, sampling_rate={sampling_rate_seconds}s")

        # Generate physics-based diagnosis data using the dedicated module
        print(f"⚙️ RequestPhysicsDiagnosis: Calling create_physics_diagnosis_report (duration={sim_duration_seconds}s)")
        if target_anomaly:
            print(f"🎯 RequestPhysicsDiagnosis: Using target anomaly for focused simulation: {target_anomaly}")
        
        diagnosis_report = create_physics_diagnosis_report(
            symptoms_list, 
            target_telemetry_sensor, 
            sim_duration_seconds, 
            sampling_rate_seconds,
            target_anomaly=target_anomaly
        )
        
        print(f"✅ RequestPhysicsDiagnosis: Diagnosis report generated successfully")
        print(f"📊 Report keys: {list(diagnosis_report.keys())}")
        try:
            pdata = diagnosis_report.get('physics_diagnosis_data', {})
            print(f"[API] actual_len={len(pdata.get('actual_telemetry', []))}, comp_anoms={len(pdata.get('component_anomalies', []))}")
        except Exception:
            pass
        
        return Response(diagnosis_report)

class UpdateDiagnosisWithEvidence(APIView):
    def post(self, request):
        # Retrieve the symptoms list from the request
        additional_evidence = json.loads(request.data['additional_evidence'])
        telemetry_values = json.loads(request.data['current_telemetry_values'])

        print("symptoms list",additional_evidence)
        print("new telemetry values",telemetry_values)

        diagnosis_list = []
        # probabilities, best_evidence, hidden_components = get_probabilities(telemetry_values)
        # top_5_probabilities = dict(sorted(probabilities.items(), 
        #                              key=lambda item: item[1], 
        #                              reverse=True)[:5])
        
        # final_report = []
        # for anomaly, probability in top_5_probabilities.items():
        #     # Get the explanations from the historical database
        #     # Append the anomaly and its explanation to the final report
        #     final_report.append({
        #         'anomaly': anomaly,
        #         'probability': probability,
        #     })
        
        # print("66666666666666666666666")
        # print("probabilities: ", probabilities)
        


        # print("done1-----------------------------------")

        # # Send request to pride to get all the procedures
        # astrobee_procedure_list = get_astrobee_procedure_list_from_pride()
        # print("done2-----------------------------------")

        # Build the diagnosis report and send it to the frontend
        # diagnosis_report = {'symptoms_list': symptoms_list, 'diagnosis_list': final_report, "best_evidence": best_evidence,
        #                     'hidden_components': hidden_components,
        #                     'astrobee_procedure_list': astrobee_procedure_list}

        return Response(None)

class LoadAllAnomalies(APIView):
    def post(self, request):
        # Query the neo4j graph
        anomaly_list = retrieve_all_anomalies(get_simulation_mode())

        return Response(anomaly_list)


class RetrieveProcedureFromAnomaly(APIView):
    def post(self, request):
        # Retrieve the anomaly name list from the request
        anomaly_name = json.loads(request.data['anomaly_name'])

        # Obtain all the procedures related to the anomaly
        procedure_names = retrieve_procedures_fTitle_from_anomaly(anomaly_name)

        return Response(procedure_names)


class RetrieveInfoFromProcedure(APIView):
    def post(self, request):
        # Retrieve the procedure name from the request
        procedure_name = json.loads(request.data['procedure_name'])

        # Query the neo4j to retrieve the procedure information
        steps_list = retrieve_fancy_steps_from_procedure(procedure_name)
        objective = retrieve_objective_from_procedure(procedure_name)
        equipment = retrieve_equipment_from_procedure(procedure_name)
        references = retrieve_references_from_procedure(procedure_name)
        referenceLinks = retrieve_reference_links_from_procedure(procedure_name)
        figures = retrieve_figures_from_procedure(procedure_name)
        checkable_steps = 0
        checkable_steps_list = []

        for step in steps_list:
            if step['depth'] > 0:
                checkable_steps += 1
                checkable_steps_list.append(step)

        # Build the output dictionary
        info = {
            'procedureStepsList': steps_list,
            'checkableSteps': checkable_steps,
            'procedureObjective': objective,
            'procedureEquipment': equipment,
            'procedureReferences': references,
            'procedureReferenceLinks': referenceLinks,
            'procedureFigures': figures,
            'checkableStepsList': checkable_steps_list,
        }

        return Response(info)


class GetPhysicsDiagnosisFromSession(APIView):
    """
    Retrieve physics diagnosis results from the session.
    This endpoint is called by the frontend to get the results
    after a physics diagnosis is completed via the chatbot.
    """
    def post(self, request):
        try:
            # Get the session ID from the request
            session_id = request.data.get('session_id')
            
            if not session_id:
                return Response({
                    'error': 'Session ID is required',
                    'status': 'error'
                }, status=400)
            
            # For now, we'll return a message indicating that the results
            # should be available in the Anomaly Diagnosis window
            # In a full implementation, you would retrieve the actual results from the session
            
            return Response({
                'message': 'Physics diagnosis results are available in the Anomaly Diagnosis window',
                'status': 'success',
                'redirect_to': 'anomaly_diagnosis'
            })
            
        except Exception as e:
            print(f"❌ GetPhysicsDiagnosisFromSession: Error: {e}")
            return Response({
                'error': str(e),
                'status': 'error'
            }, status=500)


class TutorialStatus(APIView):
    def post(self, request):
        user_info = get_or_create_user_information(request.session, request.user, 'AT')
        at_context = user_info.atcontext
        seen_tutorial = at_context.seen_tutorial

        return Response({'seen_tutorial': seen_tutorial})


class CompleteTutorial(APIView):
    def post(self, request):
        user_info = get_or_create_user_information(request.session, request.user, 'AT')
        at_context = user_info.atcontext
        seen_tutorial = at_context.seen_tutorial
        seen_tutorial = not seen_tutorial
        user_info.atcontext.seen_tutorial = seen_tutorial
        user_info.atcontext.save()
        return Response()


class GetAvailableProcedures(APIView):
    def get(self, request, format=None):
        """
        Fetch all available procedures from Pride API
        """
        try:
            url = "https://10.5.0.3:8000/api/procedures/available/"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer a57a391b-5e00-4872-844e-66d975e73c0a'
            }
            
            response = requests.request("GET", url, headers=headers, verify=False)
            
            if response.ok:
                procedures_data = response.json()
                print(f"Successfully fetched {len(procedures_data)} procedures from Pride")
                return Response({
                    "status": "success",
                    "procedures": procedures_data
                })
            else:
                print(f"Failed to fetch procedures from Pride. Status: {response.status_code}, Response: {response.text}")
                return Response({
                    "status": "error",
                    "message": f"Failed to fetch procedures from Pride. Status: {response.status_code}"
                }, status=response.status_code)
                
        except requests.exceptions.RequestException as e:
            print(f"Request exception when fetching procedures: {e}")
            return Response({
                "status": "error",
                "message": f"Network error when fetching procedures: {str(e)}"
            }, status=500)
        except Exception as e:
            print(f"Unexpected error when fetching procedures: {e}")
            return Response({
                "status": "error",
                "message": f"Unexpected error: {str(e)}"
            }, status=500)

