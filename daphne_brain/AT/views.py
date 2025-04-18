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

astrobee_status = 'NA'
response = 'NA'
countdown = 10


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


class StartAstrobeeProcedure(APIView):
    def post(self, request, format=None):

        procedure_staticID = request.data['procedureID'].replace('"', '')

        # start/open a procedure to send astrobee
        # url = "https://0.0.0.0:8000/api/procedures/available/" + procedure_staticID
        url = "https://localhost:8000/api/procedures/available/" + procedure_staticID

        payload = json.dumps({
            "user": "test",
            "startWithAutomation": "true",
            "finishWithAutomation": "true"
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer a57a391b-5e00-4872-844e-66d975e73c0a'
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        procedure_runtime_ID = response.text.replace('"', '')
        print("in start astrobee procedure", response.text)
        print("response", response)

        if response.ok:
            # start automation of the procedure
            # url = 'https://0.0.0.0:8000/api/procedures/' + procedure_runtime_ID + '/startAutomation'
            url = 'https://localhost:8000/api/procedures/' + procedure_runtime_ID + '/startAutomation'
            payload = json.dumps({
                "user": "test",
            })
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer a57a391b-5e00-4872-844e-66d975e73c0a'
            }

            response = requests.request("PUT", url, headers=headers, data=payload, verify=False)
            print("in astrobee procedure")
            print("response", response)
            print("response.text", response.text)

            global astrobee_status
            astrobee_status = "Astrobee procedure " + procedure_runtime_ID + " started."

            return Response({
                "status": astrobee_status
            })
        else:
            return Response({
                "status": "error",
                "message": "ERROR starting the procedure"
            })


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



class RequestDiagnosis(APIView):
    def post(self, request):
        # Retrieve the symptoms list from the request
        symptoms_list = json.loads(request.data['symptomsList'])
        print("herrrre----------------------------------")

        # Query the neo4j graph (do not delete first line until second one is tested)
        # diagnosis_list = diagnose_symptoms_by_subset_of_anomaly(parsed_symptoms_list)
        diagnosis_list = diagnose_symptoms_by_intersection_with_anomaly(symptoms_list)
        print("done1-----------------------------------")

        # Send request to pride to get all the procedures
        astrobee_procedure_list = get_astrobee_procedure_list_from_pride()
        print("done2-----------------------------------")

        # Build the diagnosis report and send it to the frontend
        diagnosis_report = {'symptoms_list': symptoms_list, 'diagnosis_list': diagnosis_list,
                            'astrobee_procedure_list': astrobee_procedure_list}

        return Response(diagnosis_report)


class LoadAllAnomalies(APIView):
    def post(self, request):
        # Query the neo4j graph
        anomaly_list = retrieve_all_anomalies()

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
