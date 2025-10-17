import itertools
import json
import os
import re
import numpy
import pandas as pd
import requests
from neo4j import GraphDatabase, basic_auth
from urllib3.exceptions import InsecureRequestWarning
import ssl


def get_database_connection(physics_simulation_mode=None):
    """
    Get database driver and session based on physics_simulation_mode
    Returns tuple of (driver, session)
    """
    if physics_simulation_mode == "biosim":
        # Use Aura database for biosim mode
        driver = GraphDatabase.driver(
            "neo4j+s://4a24f5d6.databases.neo4j.io", 
            auth=basic_auth("neo4j", "KijLrgvMWe-hpXCYyLxb2FAr58r3dCQdlrA2D70kzE8")
        )
    else:
        # Use original database for other modes
        driver = GraphDatabase.driver("bolt://13.58.54.49:7687", auth=basic_auth("neo4j", "goSEAKers!"))
    
    session = driver.session()
    return driver, session


def set_up_connection(physics_simulation_mode=None):
    # setup neo4j database connection
    driver, session = get_database_connection(physics_simulation_mode)
    return session


def get_components_from_anomaly(anomaly_name: str, max_items: int = 5, physics_simulation_mode=None):
    """
    Get components related to a specific anomaly through subsystems.
    
    Query path: Anomaly.Title -[:SUBSYSTEM]-> Subsystem -[:CONTAINS]-> Component
    
    Args:
        anomaly_name: Name/Title of the anomaly to search for
        max_items: Maximum number of components to return
        physics_simulation_mode: Simulation mode to determine database connection
        
    Returns:
        List of component names
    """
    driver, session = get_database_connection(physics_simulation_mode)
    
    try:
        print(f"[NEO4J] Querying components for anomaly: '{anomaly_name}'")
        
        # Query to find the anomaly and get all components from related subsystems
        query = """
        MATCH (anomaly:Anomaly {Title: $anomaly_name})-[:SUBSYSTEM]->(subsystem:Subsystem)-[:CONTAINS]->(component)
        RETURN DISTINCT component.Title AS component_name, subsystem.Title AS subsystem_name
        ORDER BY subsystem_name, component_name
        LIMIT $max_items
        """
        
        result = session.run(query, {
            'anomaly_name': anomaly_name,
            'max_items': max_items
        })
        
        components = []
        subsystems_found = set()
        
        for record in result:
            component_name = record['component_name']
            subsystem_name = record['subsystem_name']
            
            if component_name:
                components.append(component_name)
                subsystems_found.add(subsystem_name)
        
        print(f"[NEO4J] Found {len(components)} components for anomaly '{anomaly_name}': {components}")
        print(f"[NEO4J] Related subsystems: {list(subsystems_found)}")
        
        return components
        
    except Exception as e:
        print(f"[NEO4J] Error querying components for anomaly '{anomaly_name}': {e}")
        return []
        
    finally:
        session.close()
        driver.close()


def get_target_sensor_from_anomaly_subsystem(anomaly_name: str, physics_simulation_mode=None):
    """
    Get the primary sensor for an anomaly by finding its subsystems and their primary sensors.
    
    Args:
        anomaly_name: Name/Title of the anomaly to search for
        physics_simulation_mode: Simulation mode to determine database connection
        
    Returns:
        Formatted sensor name like "ppCO2_IHab (IHab)" or None
    """
    driver, session = get_database_connection(physics_simulation_mode)
    
    try:
        print(f"[NEO4J] Querying primary sensor for anomaly: '{anomaly_name}'")
        
        # Query to find the anomaly's subsystems and their primary sensors
        query = """
        MATCH (anomaly:Anomaly {Title: $anomaly_name})-[:SUBSYSTEM]->(subsystem:Subsystem)-[:PRIMARY_SENSOR]->(sensor:Measurement)
        RETURN DISTINCT sensor.Name AS sensor_name, sensor.ParameterGroup AS parameter_group
        LIMIT 1
        """
        
        result = session.run(query, {'anomaly_name': anomaly_name})
        
        for record in result:
            sensor_name = record['sensor_name']
            parameter_group = record['parameter_group']
            
            if sensor_name:
                # Format as "SensorName (ParameterGroup)"
                if parameter_group:
                    formatted_sensor = f"{sensor_name} ({parameter_group})"
                else:
                    formatted_sensor = f"{sensor_name} (IHab)"  # Default fallback
                
                print(f"[NEO4J] Found primary sensor for anomaly '{anomaly_name}': {formatted_sensor}")
                return formatted_sensor
        
        print(f"[NEO4J] No primary sensor found for anomaly '{anomaly_name}'")
        return None
        
    except Exception as e:
        print(f"[NEO4J] Error querying primary sensor for anomaly '{anomaly_name}': {e}")
        return None
        
    finally:
        session.close()
        driver.close()


def diagnose_symptoms_by_subset_of_anomaly(symptoms, physics_simulation_mode=None):
    # Setup neo4j database connection
    driver, session = get_database_connection(physics_simulation_mode)

    # build the query based on the symptoms list
    query = ''
    for index, symp in enumerate(symptoms):
        query = query + 'MATCH (m' + str(index) + ':Measurement)-[r' + str(index) + ':' + symp[
            'relationship'] + ']->(g:Anomaly) '
    query = query + 'WHERE '
    for index, symp in enumerate(symptoms):
        if (index + 1) < len(symptoms):
            query = query + 'm' + str(index) + '.Name=\'' + symp['measurement'] + '\' AND '
        else:
            query = query + 'm' + str(index) + '.Name=\'' + symp['measurement'] + '\' RETURN DISTINCT g.Title'

    # query the database
    result = session.run(query)
    diagnosis = [node[0] for node in result]
    
    # Close connections
    session.close()
    driver.close()
    
    return diagnosis


def convert_threshold_tag_to_neo4j_relationship(threshold_tag):
    relationship = ''
    if threshold_tag == 'LowerWarningLimit':
        relationship = 'Exceeds_LowerWarningLimit'
    elif threshold_tag == 'LowerCautionLimit':
        relationship = 'Exceeds_LowerCautionLimit'
    elif threshold_tag == 'UpperWarningLimit':
        relationship = 'Exceeds_UpperWarningLimit'
    elif threshold_tag == 'UpperCautionLimit':
        relationship = 'Exceeds_UpperCautionLimit'
    else:
        print('Invalid threshold tag')
        raise

    return relationship


def diagnose_symptoms_by_intersection_with_anomaly(symptoms_list, physics_simulation_mode=None):
    parsed_symptoms_list = []
    for item in symptoms_list:
        threshold_tag = item['threshold_tag']
        relationship = convert_threshold_tag_to_neo4j_relationship(threshold_tag)
        symptom = {'measurement': item['measurement'],
                   'display_name': item['display_name'],
                   'relationship': relationship}
        parsed_symptoms_list.append(symptom)

    # Setup neo4j database connection
    print("Connecting to the neo4j database...")
    driver, session = get_database_connection(physics_simulation_mode)
    print("Connected to the neo4j database.") 

    # Build the query based on the symptoms list
    query = 'MATCH (m:Measurement)-[r]->(a:Anomaly) WHERE '
    for index, symptom in enumerate(parsed_symptoms_list):
        measurement = symptom['measurement']
        clause = '(m.Name = "' + measurement + '")'
        if (index + 1) < len(parsed_symptoms_list):
            clause = clause + ' OR '
        query = query + clause
    query = query + ' RETURN DISTINCT a.Title;'
    print("Querying the neo4j database with the following query:")
    print(query)
    diagnosis = []
    try:
        # Query the database and parse the result (which is a list of the anomalies which symptoms have non empty
        # intersection with the requested symptoms)
        result = session.run(query)
        print("Query successful with the following result:")
        diagnosis = [node[0] for node in result]
        print(diagnosis)
    except Exception as e:
        print("Query failed with the following error:")
        print(e)
    finally:
        # Properly close the session and driver
        session.close()
        driver.close()

    parsed_input_symptoms = []
    for symptom in parsed_symptoms_list:
        parsed_input_symptoms.append({'measurement': symptom['display_name'], 'relationship': symptom['relationship']})

    parsed_symptoms_of_each_anomaly = {}
    for anomaly in diagnosis:
        # Retrieve symptoms of anomaly
        print("Retrieving symptoms of anomaly:")
        print(anomaly)
        anomaly_symptoms = retrieve_symptoms_from_anomaly(anomaly, physics_simulation_mode)
        print("Anomaly symptoms:")
        print(anomaly_symptoms)
        parsed_symptom_of_anomaly = []
        symptom_of_anomaly = []

        # For each symptom of the anomaly, parse the relationship field
        for symptom in anomaly_symptoms:
            relationship = symptom['relationship']
            symptom_of_anomaly.append(symptom)
            if relationship == "Upper Warning Limit":
                relationship = 'Exceeds_UpperWarningLimit'
            elif relationship == "Upper Caution Limit":
                relationship = 'Exceeds_UpperCautionLimit'
            elif relationship == "Lower Warning Limit":
                relationship = 'Exceeds_LowerWarningLimit'
            elif relationship == "Lower Caution Limit":
                relationship = 'Exceeds_LowerCautionLimit'
            symptom['relationship'] = relationship
            parsed_symptom_of_anomaly.append(symptom)

        # Append the resulting object to the dictionary
        parsed_symptoms_of_each_anomaly[anomaly] = parsed_symptom_of_anomaly
    print(parsed_symptoms_of_each_anomaly)

    # Start-Creating pairs of parsed anomalies

    temp_pair_dict = {}
    for key1 in parsed_symptoms_of_each_anomaly.keys():
        for key2 in parsed_symptoms_of_each_anomaly.keys():
            if key1 != key2:
                values = parsed_symptoms_of_each_anomaly[key1] + parsed_symptoms_of_each_anomaly[key2]
                values = [item for index, item in enumerate(values) if item not in values[:index]]
                print("VALUES", values)
                paired_key = (key1, key2)
                temp_pair_dict[paired_key] = values

    print("TEMP_PAIR_DICT: ", temp_pair_dict)


    parsed_symptoms_of_each_anomaly.update(temp_pair_dict)

    print("parsed_symptom_of_each_anomaly", parsed_symptoms_of_each_anomaly)

    # adding pairs of anomalies to diagnosis as they don't exist in knowledge graph
    temp_diagnosis = []
    anomaly_pretty_name = []

    for i in range(len(diagnosis)):
        for j in range(i + 1, len(diagnosis)):
            pair = (diagnosis[i], diagnosis[j])
            anomaly_pretty_name.append({pair, diagnosis[i] + ' & ' + diagnosis[j]})
            # pair.append(diagnosis[i])
            # pair.append(diagnosis[j])
            temp_diagnosis.append(pair)

    diagnosis.extend(temp_diagnosis)
    print("DIAGNOSIS: ", diagnosis)

    # Creating pairs of parsed anomalies-End

    
    def compare_parsed(anomaly_symptom, parsed_input_symptom):
        measurements_are_equal = (anomaly_symptom['measurement'] == parsed_input_symptom['measurement'])
        
        # Check for exact relationship match first
        relationships_are_equal = (anomaly_symptom['relationship'] == parsed_input_symptom['relationship'])
        
        # If not exact match, check for hierarchical relationship match
        if not relationships_are_equal and measurements_are_equal:
            # Check if the input symptom implies the anomaly symptom through hierarchy
            # For example: if anomaly has "UpperCaution" and input has "UpperWarning", they should match
            # because exceeding warning implies exceeding caution
            
            anomaly_rel = anomaly_symptom['relationship']
            input_rel = parsed_input_symptom['relationship']
            
            # Upper threshold hierarchy: Warning > Caution
            if (anomaly_rel == 'Exceeds_UpperCautionLimit' and input_rel == 'Exceeds_UpperWarningLimit'):
                relationships_are_equal = True
            # Lower threshold hierarchy: Warning < Caution (more severe when going lower)
            elif (anomaly_rel == 'Exceeds_LowerCautionLimit' and input_rel == 'Exceeds_LowerWarningLimit'):
                relationships_are_equal = True
        
        if measurements_are_equal and relationships_are_equal:
            return True
        else:
            return False

    # Initialize result storing variables
    cardinality_for_each_anomaly = {}
    size_of_each_anomaly = {}
    signature = {}
    anomalyContainsRequestedSymptoms = {}
    missing_anomaly_symptoms = {}

    # Loop over the anomalies to get comparison with parsed symptoms
    for anomaly in diagnosis:
        # Initialize the cardinal counter
        cardinal = 0
        containsSymptoms = []
        signatureSymptom = []
        missing_symptom = []
        # Loop over A
        for anomaly_symptom in parsed_symptoms_of_each_anomaly[anomaly]:
            readable_symptom = anomaly_symptom['measurement'] + ' ' + re.sub(r"(\w)([A-Z])", r"\1 \2",
                                                                             anomaly_symptom[
                                                                                 'relationship'].replace(
                                                                                 '_', ' '))
            signatureSymptom.append(readable_symptom)
            # Loop over B
            for parsed_input_symptom in parsed_input_symptoms:
                # Compare
                are_equal = compare_parsed(anomaly_symptom, parsed_input_symptom)
                if are_equal:
                    cardinal += 1
                    containsSymptoms.append(readable_symptom)
        # add missing symptoms from the signature
        for symptom in signatureSymptom:
            if symptom in containsSymptoms:
                pass
            else:
                missing_symptom.append(symptom)

        # Store the results
        cardinality_for_each_anomaly[anomaly] = cardinal
        anomalyContainsRequestedSymptoms[anomaly] = containsSymptoms
        size_of_each_anomaly[anomaly] = len(parsed_symptoms_of_each_anomaly[anomaly])
        signature[anomaly] = signatureSymptom
        missing_anomaly_symptoms[anomaly] = missing_symptom

    # Create the result storing variable and parse the size of the requested symptoms set
    scored_diagnosis = {}
    total_requested_symptoms = len(parsed_symptoms_list)

    # Loop over the anomalies, compute each of the partial scores and the total scores (g1, g2 and g)
    for anomaly in diagnosis:
        # Compute the score
        g1 = cardinality_for_each_anomaly[anomaly] / total_requested_symptoms
        g2 = cardinality_for_each_anomaly[anomaly] / size_of_each_anomaly[anomaly]
        g = g1 * g2
        # Round it for the frontend display
        score = round(g, 2)
        # Save it
        scored_diagnosis[anomaly] = score
    print("SCORED DIAGNOSIS: ", scored_diagnosis)

    # Sort the result according to the scores
    ordered_diagnosis = {k: v for k, v in sorted(scored_diagnosis.items(), key=lambda item1: item1[1])}
    print("ORDERED DIAGNOSIS: ", ordered_diagnosis)
    # Convert the dictionary to a list of its keys
    ordered_diagnosis = list(ordered_diagnosis.keys())
    ordered_diagnosis.reverse()

    # Cast list to top 7 items
    top_n_diagnosis = []
    size_limit = min(7, len(ordered_diagnosis))
    # Adding in different arrays based on score to list in ordered fashion
    # very_likely = []
    # likely = []
    # somewhat_likely = []
    for i in range(0, len(ordered_diagnosis)):
        anomaly = ordered_diagnosis[i]
        score = scored_diagnosis[anomaly]

        anomaly_name = ''
        if type(anomaly) is tuple:
            anomaly_name = anomaly[0] + ' & ' + anomaly[1]
        else:
            anomaly_name = anomaly

        text_score = ""
        # level = 0
        if score != 0:
            if score < 0.12:
                text_score = "Extremely Unlikely : 0-0.11"
                # level = 1
                # somewhat_likely.append({'name': anomaly, 'score': score, 'text_score': text_score})
            elif 0.23 > score >= 0.12:
                text_score = "Highly Unlikely : 0.12-0.22"
                # level = 2
                # likely.append({'name': anomaly, 'score': score, 'text_score': text_score})
            elif 0.34 > score >= 0.23:
                text_score = "Unlikely : 0.23-0.33"
                # level = 3
            elif 0.45 > score >= 0.34:
                text_score = "Moderately Unlikely : 0.34-0.44"
                # level = 4
            elif 0.56 > score >= 0.45:
                text_score = "Equally Likely and Unlikely : 0.45-0.55"
                # level = 5
            elif 0.67 > score >= 0.56:
                text_score = "Moderately Likely : 0.56-0.66"
                # level = 6
            elif 0.78 > score >= 0.67:
                text_score = "Likely : 0.67-0.77"
                # level = 7
            elif 0.89 > score >= 0.78:
                text_score = "Highly Likely : 0.78-0.88"
                # level = 8
            else:
                text_score = "Extremely Likely : 0.89-1.0"
                # level = 9

                # very_likely.append({'name': anomaly, 'score': score, 'text_score': text_score})
            if i < size_limit or top_n_diagnosis[-1]['score'] == score:
                top_n_diagnosis.append({'name': anomaly_name, 'score': score, 'text_score': text_score,
                                        'cardinality': cardinality_for_each_anomaly[anomaly],
                                        'containsRequestedSymptoms': anomalyContainsRequestedSymptoms[
                                            anomaly], 'signature': signature[anomaly],
                                        'missing_symptoms': missing_anomaly_symptoms[anomaly], })

    sorted_top_n_diagnosis = sorted(top_n_diagnosis, key=lambda x: (-x['score'], len(x['name'])))


    # Return result
    final_diagnosis = top_n_diagnosis
    # pair of anomaly changes end
    # Return result
    final_diagnosis = sorted_top_n_diagnosis
    print("FINAL DIAGNOSIS: ", final_diagnosis)

    return final_diagnosis


def retrieve_all_anomalies(physics_simulation_mode=None):
    # Setup neo4j database connection
    driver, session = get_database_connection(physics_simulation_mode)

    # Build and send the query
    query = 'MATCH (n:Anomaly) RETURN DISTINCT n.Title'
    result = session.run(query)

    # Parse the result
    anomaly_list = []
    for item in result:
        anomaly_list.append(item[0])

    # Close connections
    session.close()
    driver.close()

    return anomaly_list


def retrieve_all_measurements(physics_simulation_mode=None):
    # Setup neo4j database connection
    driver, session = get_database_connection(physics_simulation_mode)

    # Build and send the query
    query = 'MATCH (m:Measurement) RETURN DISTINCT m.Name'
    result = session.run(query)

    # Parse the result
    measurement_list = []
    for item in result:
        measurement_list.append(item[0])

    # Close connections
    session.close()
    driver.close()

    return measurement_list


def retrieve_all_measurements_parameter_groups(physics_simulation_mode=None):
    # Setup neo4j database connection
    driver, session = get_database_connection(physics_simulation_mode)

    # Build and send the query
    query = 'MATCH (m:Measurement) RETURN DISTINCT m.ParameterGroup'
    result = session.run(query)

    # Parse the result
    measurement_list = []
    for item in result:
        if item[0] is not None and item[0] != '':
            measurement_list.append(item[0])

    # Close connections
    session.close()
    driver.close()

    return measurement_list


def retrieve_all_procedures():
    # Setup neo4j database connection
    driver = GraphDatabase.driver("bolt://13.58.54.49:7687", auth=basic_auth("neo4j", "goSEAKers!"))
    session = driver.session()

    # Build and send the query
    query = 'MATCH (p:Procedure) RETURN DISTINCT p.Title'
    result = session.run(query)

    # Parse the result
    procedure_list = []
    for item in result:
        procedure_list.append(item[0])

    return procedure_list


def retrieve_procedures_fTitle_from_anomaly(anomaly_name):
    # Setup neo4j database connection
    driver = GraphDatabase.driver("bolt://13.58.54.49:7687", auth=basic_auth("neo4j", "goSEAKers!"))
    session = driver.session()

    # Build and send the query
    query = "MATCH (a:Anomaly)-[s:Solution]-(p:Procedure) WHERE a.Title='" + anomaly_name + "' RETURN p.fTitle ORDER BY s.Order"
    result = session.run(query)

    # Parse the result
    procedure_list = []
    for item in result:
        procedure_list.append(item[0])

    return procedure_list


def retrieve_procedures_title_from_anomaly(anomaly_name):
    # Setup neo4j database connection
    driver = GraphDatabase.driver("bolt://13.58.54.49:7687", auth=basic_auth("neo4j", "goSEAKers!"))
    session = driver.session()

    # Build and send the query
    query = "MATCH (a:Anomaly)-[s:Solution]-(p:Procedure) WHERE a.Title='" + anomaly_name + "' RETURN p.Title ORDER BY s.Order"
    result = session.run(query)

    # Parse the result
    procedure_list = []
    for item in result:
        procedure_list.append(item[0])

    return procedure_list


def retrieve_affected_components_from_procedure(procedure):
    # Setup neo4j database connection
    driver = GraphDatabase.driver("bolt://13.58.54.49:7687", auth=basic_auth("neo4j", "goSEAKers!"))
    session = driver.session()

    try:
        float(procedure)
        # Build and send the query because procedure is a number
        query = "MATCH (p:Procedure)-[:Comprises]-(c:Component) WHERE p.pNumber='" + procedure + "' RETURN DISTINCT " \
                                                                                                 "c.Title "
    except ValueError:
        print("Not a number.")

        # check if it is full title by checking if it starts with a number
        try:
            float(procedure[0])
            # Build and send the query because procedure is a full title
            query = "MATCH (p:Procedure)-[:Comprises]-(c:Component) WHERE p.fTitle='" + procedure + "' RETURN " \
                                                                                                    "DISTINCT " \
                                                                                                    "c.Title "

        except ValueError:
            print("Not a full title.")
            # Build and send the query because procedure is just a name
            query = "MATCH (p:Procedure)-[:Comprises]-(c:Component) WHERE p.Title='" + procedure + "' RETURN " \
                                                                                                   "DISTINCT " \
                                                                                                   "c.Title "
    result = session.run(query)

    # Parse the result
    component_list = []
    for item in result:
        component_list.append(item[0])

    return component_list


def retrieve_time_from_procedure(procedure):
    # Setup neo4j database connection
    driver = GraphDatabase.driver("bolt://13.58.54.49:7687", auth=basic_auth("neo4j", "goSEAKers!"))
    session = driver.session()

    try:
        float(procedure)
        # Build and send the query because procedure is a number
        query = "MATCH (p:Procedure) WHERE p.pNumber='" + procedure + "' RETURN DISTINCT p.ETR"

    except ValueError:
        print("Not a number.")

        # check if it is full title by checking if it starts with a number
        try:
            float(procedure[0])
            # Build and send the query because procedure is a full title
            query = "MATCH (p:Procedure) WHERE p.fTitle='" + procedure + "' RETURN DISTINCT p.ETR"

        except ValueError:
            print("Not a full title.")
            # Build and send the query because procedure is just a name
            query = "MATCH (p:Procedure) WHERE p.Title='" + procedure + "' RETURN DISTINCT p.ETR"

    result = session.run(query)

    # Parse the result
    procedure_time_list = []
    for item in result:
        procedure_time_list.append(item[0])

    time = procedure_time_list[0]

    return time


def retrieve_risks_from_anomaly(anomaly_name):
    # Setup neo4j database connection
    driver = GraphDatabase.driver("bolt://13.58.54.49:7687", auth=basic_auth("neo4j", "goSEAKers!"))
    session = driver.session()

    # Build and send the query
    query = "MATCH (a:Anomaly)-[:Can_Cause]-(r:Risk) WHERE a.Title='" + anomaly_name + "' RETURN DISTINCT r.Title"
    result = session.run(query)
    # Parse the result
    risks_list = []

    if result.peek() is None:
        risks_list.append("None")

    for item in result:
        risks_list.append(item[0])

    return risks_list


def retrieve_affected_subsystems_from_anomaly(anomaly_name):
    # Setup neo4j database connection
    driver = GraphDatabase.driver("bolt://13.58.54.49:7687", auth=basic_auth("neo4j", "goSEAKers!"))
    session = driver.session()

    # Build and send the query
    query = "MATCH (a:Anomaly)-[:Affects]-(s:SubSystem) WHERE a.Title='" + anomaly_name + "' RETURN DISTINCT s.Title"
    result = session.run(query)

    # Parse the result
    subsystems_list = []
    for item in result:
        subsystems_list.append(item[0])

    return subsystems_list


def retrieve_symptoms_from_anomaly(anomaly_name, physics_simulation_mode=None):
    # Setup neo4j database connection
    
    print("Connecting to the neo4j database...")
    driver, session = get_database_connection(physics_simulation_mode)
    print("Connected to the neo4j database.")

    # Build and send the query to obtain the affected measurements that exceed the upper caution limit
    query_UpperCautionLimit = "MATCH (a:Anomaly)-[r:Exceeds_UpperCautionLimit]-(m:Measurement) WHERE a.Title='" + anomaly_name + \
                              "' RETURN DISTINCT m.Name, m.ParameterGroup;"
    # print("Querying the neo4j database with the following query:")
    # print(query_UpperCautionLimit)
    result_UpperCautionLimit = session.run(query_UpperCautionLimit)
    print("Query result:")

    # Parse the result
    symptoms_list_UpperCautionLimit = []
    for item in result_UpperCautionLimit:
        measurement_name = item[0] + ' (' + item[1] + ')'
        symptoms_list_UpperCautionLimit.append(measurement_name)
    print(symptoms_list_UpperCautionLimit)


    # Build and send the query to obtain the affected measurements that exceed the lower caution limit
    query_LowerCautionLimit = "MATCH (a:Anomaly)-[r:Exceeds_LowerCautionLimit]-(m:Measurement) WHERE a.Title='" + \
                              anomaly_name + \
                              "' RETURN DISTINCT m.Name, m.ParameterGroup;"
    # print("Querying the neo4j database with the following query:")
    # print(query_LowerCautionLimit)
    result_LowerCautionLimit = session.run(query_LowerCautionLimit)
    print("Query result:")

    # Parse the result
    symptoms_list_LowerCautionLimit = []
    for item in result_LowerCautionLimit:
        measurement_name = item[0] + ' (' + item[1] + ')'
        symptoms_list_LowerCautionLimit.append(measurement_name)
    print(symptoms_list_LowerCautionLimit)


    # Build and send the query to obtain the affected measurements that exceed the upper warning limit
    query_UpperWarningLimit = "MATCH (a:Anomaly)-[r:Exceeds_UpperWarningLimit]-(m:Measurement) WHERE a.Title='" + \
                              anomaly_name + \
                              "' RETURN DISTINCT m.Name, m.ParameterGroup;"
    # print("Querying the neo4j database with the following query:")
    # print(query_UpperWarningLimit)
    result_UpperWarningLimit = session.run(query_UpperWarningLimit)
    print("Query result:")

    # Parse the result
    symptoms_list_UpperWarningLimit = []
    for item in result_UpperWarningLimit:
        measurement_name = item[0] + ' (' + item[1] + ')'
        symptoms_list_UpperWarningLimit.append(measurement_name)
    print(symptoms_list_UpperWarningLimit)


    # Build and send the query to obtain the affected measurements that exceed the lower warning limit
    query_LowerWarningLimit = "MATCH (a:Anomaly)-[r:Exceeds_LowerWarningLimit]-(m:Measurement) WHERE a.Title='" + \
                              anomaly_name + \
                              "' RETURN DISTINCT m.Name, m.ParameterGroup;"
    # print("Querying the neo4j database with the following query:")
    # print(query_LowerWarningLimit)
    result_LowerWarningLimit = session.run(query_LowerWarningLimit)
    print("Query result:")

    # Parse the result
    symptoms_list_LowerWarningLimit = []
    for item in result_LowerWarningLimit:
        measurement_name = item[0] + ' (' + item[1] + ')'
        symptoms_list_LowerWarningLimit.append(measurement_name)
    print(symptoms_list_LowerWarningLimit)
    
    session.close()
    driver.close()


    # Build the output (making the relationship explicit)
    symptoms_list = []
    for measurement in symptoms_list_LowerCautionLimit:
        symptom = {'measurement': measurement, 'relationship': 'Lower Caution Limit'}
        symptoms_list.append(symptom)
    for measurement in symptoms_list_UpperCautionLimit:
        symptom = {'measurement': measurement, 'relationship': 'Upper Caution Limit'}
        symptoms_list.append(symptom)
    for measurement in symptoms_list_LowerWarningLimit:
        symptom = {'measurement': measurement, 'relationship': 'Lower Warning Limit'}
        symptoms_list.append(symptom)
    for measurement in symptoms_list_UpperWarningLimit:
        symptom = {'measurement': measurement, 'relationship': 'Upper Warning Limit'}
        symptoms_list.append(symptom)
    # print(symptoms_list)
    
    return symptoms_list


def retrieve_thresholds_from_measurement(measurement_name, physics_simulation_mode=None):
    # Setup neo4j database connection
    driver, session = get_database_connection(physics_simulation_mode)

    # Build and send the query
    query = "MATCH (m:Measurement) WHERE m.Name='" + measurement_name + \
            "' RETURN m.ParameterGroup, m.LowerWarningLimit, m.LowerCautionLimit, m.UpperCautionLimit, " \
            "m.UpperWarningLimit "
    result = session.run(query)

    # Parse the result
    parsed_result = []
    for items in result:
        parsed_result.append(items)

    result_info = []
    # Check if the parsed result is empty and proceed accordingly
    if parsed_result:
        for item in parsed_result:
            thresholds_dict = {'ParameterGroup': item[0], 'LowerWarningLimit': item[1], 'LowerCautionLimit': item[2],
                               'UpperCautionLimit': item[3], 'UpperWarningLimit': item[4]}
            result_info.append(thresholds_dict)
    else:
        result_info = {'ParameterGroup': 'None', 'LowerWarningLimit': 'None', 'LowerCautionLimit': 'None',
                       'UpperCautionLimit': 'None', 'UpperWarningLimit': 'None'}

    # Close connections
    session.close()
    driver.close()

    return result_info


def retrieve_units_from_measurement(measurement_name, physics_simulation_mode=None):
    # Setup neo4j database connection
    driver, session = get_database_connection(physics_simulation_mode)

    # Build and send the query
    query = "MATCH (m:Measurement) WHERE m.Name='" + measurement_name + \
            "' RETURN DISTINCT m.Unit"
    result = session.run(query)

    # Parse the result
    parsed_result = ''
    for item in result:
        parsed_result = item

    units = parsed_result[0]

    # Close connections
    session.close()
    driver.close()

    return units


def retrieve_ordered_steps_from_procedure(procedure):
    # Setup neo4j database connection
    driver = GraphDatabase.driver("bolt://13.58.54.49:7687", auth=basic_auth("neo4j", "goSEAKers!"))
    session = driver.session()

    try:
        float(procedure)
        # Build and send the query because procedure is a number
        query = "MATCH (p:Procedure)-[:Has]-(st:Step) WHERE p.pNumber='" + \
                procedure + "' RETURN st.Action ORDER BY st.Title"

    except ValueError:
        print("Not a number.")

        # check if it is full title by checking if it starts with a number
        try:
            float(procedure[0])
            # Build and send the query because procedure is a full title
            query = "MATCH (p:Procedure)-[:Has]-(st:Step) WHERE p.fTitle='" + \
                    procedure + "' RETURN st.Action ORDER BY st.Title"

        except ValueError:
            print("Not a full title.")
            # Build and send the query because procedure is just a name
            query = "MATCH (p:Procedure)-[:Has]-(st:Step) WHERE p.Title='" + \
                    procedure + "' RETURN st.Action ORDER BY st.Title"

    result = session.run(query)

    # Parse the result
    steps_list = []
    for item in result:
        steps_list.append(item[0])

    return steps_list


def retrieve_fancy_steps_from_procedure(procedure):
    # Setup neo4j database connection
    driver = GraphDatabase.driver("bolt://13.58.54.49:7687", auth=basic_auth("neo4j", "goSEAKers!"))
    session = driver.session()

    try:
        float(procedure)
        # Build and send the query because procedure is a number
        query_step_labels = 'MATCH(p:Procedure)-[r:Has]->(s) WHERE p.pNumber=\'' + procedure + '\' RETURN s.Title ORDER BY s.Step, s.SubStep, s.SubSubStep, s.Note'
        query_step_actions = 'MATCH(p:Procedure)-[r:Has]->(s) WHERE p.pNumber=\'' + procedure + '\' RETURN s.Action ORDER BY s.Step, s.SubStep, s.SubSubStep, s.Note'
        query_step_figures = 'MATCH(p:Procedure)-[r:Has]->(s) WHERE p.pNumber=\'' + procedure + '\' RETURN s.Link ORDER BY s.Step, s.SubStep, s.SubSubStep, s.Note'
        query_step_fNumbers = 'MATCH(p:Procedure)-[r:Has]->(s) WHERE p.pNumber=\'' + procedure + '\' RETURN s.fNumber ORDER BY s.Step, s.SubStep, s.SubSubStep, s.Note'
        query_step_figures2 = 'MATCH(p:Procedure)-[r:Has]->(s) WHERE p.pNumber=\'' + procedure + '\' RETURN s.Link2 ORDER BY s.Step, s.SubStep, s.SubSubStep, s.Note'
        query_step_fNumbers2 = 'MATCH(p:Procedure)-[r:Has]->(s) WHERE p.pNumber=\'' + procedure + '\' RETURN s.fNumber2 ORDER BY s.Step, s.SubStep, s.SubSubStep, s.Note'

    except ValueError:
        print("Not a number.")

        # check if it is full title by checking if it starts with a number
        try:
            float(procedure[0])
            # Build and send the query because procedure is a full title
            query_step_labels = 'MATCH(p:Procedure)-[r:Has]->(s) WHERE p.fTitle=\'' + procedure + '\' RETURN s.Title ORDER BY s.Step, s.SubStep, s.SubSubStep, s.Note'
            query_step_actions = 'MATCH(p:Procedure)-[r:Has]->(s) WHERE p.fTitle=\'' + procedure + '\' RETURN s.Action ORDER BY s.Step, s.SubStep, s.SubSubStep, s.Note'
            query_step_figures = 'MATCH(p:Procedure)-[r:Has]->(s) WHERE p.fTitle=\'' + procedure + '\' RETURN s.Link ORDER BY s.Step, s.SubStep, s.SubSubStep, s.Note'
            query_step_fNumbers = 'MATCH(p:Procedure)-[r:Has]->(s) WHERE p.fTitle=\'' + procedure + '\' RETURN s.fNumber ORDER BY s.Step, s.SubStep, s.SubSubStep, s.Note'
            query_step_figures2 = 'MATCH(p:Procedure)-[r:Has]->(s) WHERE p.fTitle=\'' + procedure + '\' RETURN s.Link2 ORDER BY s.Step, s.SubStep, s.SubSubStep, s.Note'
            query_step_fNumbers2 = 'MATCH(p:Procedure)-[r:Has]->(s) WHERE p.fTitle=\'' + procedure + '\' RETURN s.fNumber2 ORDER BY s.Step, s.SubStep, s.SubSubStep, s.Note'

        except ValueError:
            print("Not a full title.")
            # Build and send the query because procedure is just a name
            query_step_labels = 'MATCH(p:Procedure)-[r:Has]->(s) WHERE p.Title=\'' + procedure + '\' RETURN s.Title ORDER BY s.Step, s.SubStep, s.SubSubStep, s.Note'
            query_step_actions = 'MATCH(p:Procedure)-[r:Has]->(s) WHERE p.Title=\'' + procedure + '\' RETURN s.Action ORDER BY s.Step, s.SubStep, s.SubSubStep, s.Note'
            query_step_figures = 'MATCH(p:Procedure)-[r:Has]->(s) WHERE p.Title=\'' + procedure + '\' RETURN s.Link ORDER BY s.Step, s.SubStep, s.SubSubStep, s.Note'
            query_step_fNumbers = 'MATCH(p:Procedure)-[r:Has]->(s) WHERE p.Title=\'' + procedure + '\' RETURN s.fNumber ORDER BY s.Step, s.SubStep, s.SubSubStep, s.Note'
            query_step_figures2 = 'MATCH(p:Procedure)-[r:Has]->(s) WHERE p.Title=\'' + procedure + '\' RETURN s.Link2 ORDER BY s.Step, s.SubStep, s.SubSubStep, s.Note'
            query_step_fNumbers2 = 'MATCH(p:Procedure)-[r:Has]->(s) WHERE p.Title=\'' + procedure + '\' RETURN s.fNumber2 ORDER BY s.Step, s.SubStep, s.SubSubStep, s.Note'

    # Run the queries
    result_step_labels = session.run(query_step_labels)
    result_step_actions = session.run(query_step_actions)
    result_step_figures = session.run(query_step_figures)
    result_step_fNumbers = session.run(query_step_fNumbers)
    result_step_figures2 = session.run(query_step_figures2)
    result_step_fNumbers2 = session.run(query_step_fNumbers2)

    step_labels = []
    for item in result_step_labels:
        step_labels.append(item[0])

    step_actions = []
    for item in result_step_actions:
        step_actions.append(item[0])

    step_figures = []
    for item in result_step_figures:
        step_figures.append(item[0])

    step_fNumbers = []
    step_hasFigure = []
    for item in result_step_fNumbers:
        step_fNumbers.append(item[0])
        if (item[0]) is not None:
            step_hasFigure.append(True)
        else:
            step_hasFigure.append(False)

    step_figures2 = []
    for item in result_step_figures2:
        step_figures2.append(item[0])

    step_fNumbers2 = []
    step_hasFigure2 = []
    for item in result_step_fNumbers2:
        step_fNumbers2.append(item[0])
        if (item[0]) is not None:
            step_hasFigure2.append(True)
        else:
            step_hasFigure2.append(False)

    # Parse the result
    steps = []
    label_counter = {
        'steps': 0,
        'substeps': 0,
        'subsubsteps': 0
    }
    for index, step in enumerate(step_labels):
        isStep = True
        # Retrieve the depth from the label points
        label_points = 0
        for char in step_labels[index]:
            if char == '.':
                label_points += 1
        depth = label_points

        # Decide whether the step should be initially enabled or not
        is_enabled = False
        if depth == 0:
            if label_counter['steps'] == 0:
                is_enabled = True
            label_counter['steps'] += 1
        if depth == 1:
            if label_counter['steps'] == 1 and label_counter['substeps'] == 0:
                is_enabled = True
            label_counter['substeps'] += 1
            isStep = False
        if depth == 2:
            if label_counter['steps'] == 1 and label_counter['substeps'] == 1 and label_counter['subsubsteps'] == 0:
                is_enabled = True
            label_counter['subsubsteps'] += 1
            isStep = False

        # Build the parsed item
        step_item = {'depth': depth,
                     'label': step_labels[index],
                     'action': step_actions[index],
                     'figure': step_figures[index],
                     'fNumber': step_fNumbers[index],
                     'hasFigure': step_hasFigure[index],
                     'figure2': step_figures2[index],
                     'fNumber2': step_fNumbers2[index],
                     'hasFigure2': step_hasFigure2[index],
                     'isDone': False,
                     'isStep': isStep}

        steps.append(step_item)

    return steps


def retrieve_objective_from_procedure(procedure):
    # Setup neo4j database connection
    driver = GraphDatabase.driver("bolt://13.58.54.49:7687", auth=basic_auth("neo4j", "goSEAKers!"))
    session = driver.session()

    try:
        float(procedure)
        # Build and send the query because procedure is a number
        query = "MATCH (p:Procedure) WHERE p.pNumber='" + procedure + "' RETURN p.Objective"

    except ValueError:
        print("Not a number.")

        # check if it is full title by checking if it starts with a number
        try:
            float(procedure[0])
            # Build and send the query because procedure is a full title
            query = "MATCH (p:Procedure) WHERE p.fTitle='" + procedure + "' RETURN p.Objective"

        except ValueError:
            print("Not a full title.")
            # Build and send the query because procedure is just a name
            query = "MATCH (p:Procedure) WHERE p.Title='" + procedure + "' RETURN p.Objective"

    result = session.run(query)

    # Parse the result
    objective_list = []
    for item in result:
        objective_list.append(item[0])

    if len(objective_list) == 0:
        objective = 'ERROR: missing objective description.'
    else:
        objective = objective_list[0]

    return objective


def retrieve_equipment_from_procedure(procedure):
    # Setup neo4j database connection
    driver = GraphDatabase.driver("bolt://13.58.54.49:7687", auth=basic_auth("neo4j", "goSEAKers!"))
    session = driver.session()

    try:
        float(procedure)
        # Build and send the query because procedure is a number
        query = "MATCH (p:Procedure)-[Uses]->(e:Equipment) WHERE p.pNumber='" + procedure + "' RETURN e.Title"

    except ValueError:
        print("Not a number.")

        # check if it is full title by checking if it starts with a number
        try:
            float(procedure[0])
            # Build and send the query because procedure is a full title
            query = "MATCH (p:Procedure)-[Uses]->(e:Equipment) WHERE p.fTitle='" + procedure + "' RETURN e.Title"

        except ValueError:
            print("Not a full title.")
            # Build and send the query because procedure is just a name
            query = "MATCH (p:Procedure)-[Uses]->(e:Equipment) WHERE p.Title='" + procedure + "' RETURN e.Title"

    result = session.run(query)

    # Parse the result
    equipment_list = []
    for item in result:
        equipment_list.append(item[0])

    if len(equipment_list) == 0:
        equipment = ['ERROR: missing equipment list.']
    else:
        equipment = equipment_list

    return equipment


def retrieve_references_from_procedure(procedure):
    # Setup neo4j database connection
    driver = GraphDatabase.driver("bolt://13.58.54.49:7687", auth=basic_auth("neo4j", "goSEAKers!"))
    session = driver.session()

    try:
        float(procedure)
        # Build and send the query because procedure is a number
        query = "MATCH (p:Procedure)-[:Uses]->(r:Reference) WHERE p.pNumber='" + procedure + "' RETURN r.Title"

    except ValueError:
        print("Not a number.")

        # check if it is full title by checking if it starts with a number
        try:
            float(procedure[0])
            # Build and send the query because procedure is a full title
            query = "MATCH (p:Procedure)-[:Uses]->(r:Reference) WHERE p.fTitle='" + procedure + "' RETURN r.Title"

        except ValueError:
            print("Not a full title.")
            # Build and send the query because procedure is just a name
            query = "MATCH (p:Procedure)-[:Uses]->(r:Reference) WHERE p.Title='" + procedure + "' RETURN r.Title"

    result = session.run(query)

    # Parse the result
    reference_list = []
    for item in result:
        reference_list.append(item[0])

    return reference_list


def retrieve_reference_links_from_procedure(procedure):
    # Setup neo4j database connection
    driver = GraphDatabase.driver("bolt://13.58.54.49:7687", auth=basic_auth("neo4j", "goSEAKers!"))
    session = driver.session()

    try:
        float(procedure)
        # Build and send the query because procedure is a number
        query = "MATCH (p:Procedure)-[:Uses]->(r:Reference) WHERE p.pNumber='" + procedure + "' RETURN r.Procedure"

    except ValueError:
        print("Not a number.")

        # check if it is full title by checking if it starts with a number
        try:
            float(procedure[0])
            # Build and send the query because procedure is a full title
            query = "MATCH (p:Procedure)-[:Uses]->(r:Reference) WHERE p.fTitle='" + procedure + "' RETURN r.Procedure"

        except ValueError:
            print("Not a full title.")
            # Build and send the query because procedure is just a name
            query = "MATCH (p:Procedure)-[:Uses]->(r:Reference) WHERE p.Title='" + procedure + "' RETURN r.Procedure"

    result = session.run(query)

    # Parse the result
    reference_list = []
    for item in result:
        reference_list.append(item[0])

    return reference_list


def retrieve_figures_from_procedure(procedure):
    # Setup neo4j database connection
    driver = GraphDatabase.driver("bolt://13.58.54.49:7687", auth=basic_auth("neo4j", "goSEAKers!"))
    session = driver.session()

    try:
        float(procedure)
        # Build and send the query because procedure is a number
        query = "MATCH(p:Procedure)-[r:Has]->(f:Figure) WHERE p.pNumber=\'" + procedure + \
                "\'RETURN f.Link ORDER BY f.Number"

    except ValueError:
        print("Not a number.")

        # check if it is full title by checking if it starts with a number
        try:
            float(procedure[0])
            # Build and send the query because procedure is a full title
            query = "MATCH(p:Procedure)-[r:Has]->(f:Figure) WHERE p.fTitle=\'" + procedure + \
                    "\'RETURN f.Link ORDER BY f.Number"

        except ValueError:
            print("Not a full title.")
            # Build and send the query because procedure is just a name
            query = "MATCH(p:Procedure)-[r:Has]->(f:Figure) WHERE p.Title=\'" + procedure + \
                    "\'RETURN f.Link ORDER BY f.Number"

    result = session.run(query)

    # Parse the result
    figure_list = []
    for item in result:
        figure_list.append(item[0])

    return figure_list


def retrieve_all_components():
    # Setup neo4j database connection
    driver = GraphDatabase.driver("bolt://13.58.54.49:7687", auth=basic_auth("neo4j", "goSEAKers!"))
    session = driver.session()

    # Build and send the query
    query1 = 'MATCH (n) WHERE EXISTS(n.Link) RETURN DISTINCT n.Link AS Link UNION ALL MATCH ()-[r]-() WHERE ' \
             'EXISTS(r.Link) RETURN DISTINCT r.Link AS Link '
    query2 = 'MATCH (n) WHERE EXISTS(n.Link2) RETURN DISTINCT n.Link2 AS Link2 UNION ALL MATCH ()-[r]-() WHERE ' \
             'EXISTS(r.Link2) RETURN DISTINCT r.Link2 AS Link2 '
    result1 = session.run(query1)
    result2 = session.run(query2)

    components_list = []
    for items in itertools.chain(result1, result2):
        for item in items:
            stripped = item.replace(".png", "")
            spaced = stripped.replace("_", " ")
            components_list.append(spaced)

    return components_list


def retrieve_all_procedure_numbers():
    # Setup neo4j database connection
    driver = GraphDatabase.driver("bolt://13.58.54.49:7687", auth=basic_auth("neo4j", "goSEAKers!"))
    session = driver.session()

    # Build and send the query
    query = "MATCH (p:Procedure) RETURN DISTINCT p.pNumber"
    result = session.run(query)

    # Parse the result
    procedure_numbers = []
    for item in result:
        procedure_numbers.append(item[0])

    return procedure_numbers


def retrieve_all_step_numbers():
    # Setup neo4j database connection
    driver = GraphDatabase.driver("bolt://13.58.54.49:7687", auth=basic_auth("neo4j", "goSEAKers!"))
    session = driver.session()

    # Build and send the query
    query = 'MATCH (n) WHERE EXISTS(n.SubStep) RETURN DISTINCT n.Title AS Title UNION ALL MATCH (m) WHERE ' \
            'EXISTS(m.SubSubStep) RETURN DISTINCT m.Title AS Title'
    result = session.run(query)

    # Parse the result
    step_numbers = []
    for item in result:
        step = item[0].replace("Step ", "")
        step_numbers.append(step)

    return step_numbers


def retrieve_procedures_from_pNumber(pNumber):
    # Setup neo4j database connection
    driver = GraphDatabase.driver("bolt://13.58.54.49:7687", auth=basic_auth("neo4j", "goSEAKers!"))
    session = driver.session()

    # Build and send the query
    query = "MATCH (p:Procedure) WHERE p.pNumber='" + pNumber + "' RETURN p.Title"
    result = session.run(query)

    procedure = ''
    # Parse the result
    for item in result:
        procedure = item[0]

    return procedure


def retrieve_step_from_procedure(step_number, procedure):
    # Setup neo4j database connection
    driver = GraphDatabase.driver("neo4j://3.15.160.239:7687", auth=basic_auth("neo4j", "goSEAKers!"))
    session = driver.session()

    try:
        float(procedure)
        # Build and send the query because procedure is a number
        query = "MATCH (p:Procedure)-[:Has]->(s) WHERE p.pNumber='" + procedure + \
                "' AND s.Title='Step " + step_number + "' RETURN s.Action"
    except ValueError:
        print("Not a number.")

        # check if it is full title by checking if it starts with a number
        try:
            float(procedure[0])
            # Build and send the query because procedure is a full title
            query = "MATCH (p:Procedure)-[:Has]->(s) WHERE p.fTitle='" + procedure + \
                    "' AND s.Title='Step " + step_number + "' RETURN s.Action"
        except ValueError:
            print("Not a full title.")
            # Build and send the query because procedure is just a name
            query = "MATCH (p:Procedure)-[:Has]->(s) WHERE p.Title='" + procedure + \
                    "' AND s.Title='Step " + step_number + "' RETURN s.Action"

    result = session.run(query)

    # Parse the result
    for item in result:
        step = item[0]

    return step


def get_explanations_from_historical_database(signature):
    historical_binary_signatures = []
    working_directory = os.getcwd()
    filename = working_directory + '/AT/databases/Historical_Database.csv'

    with open(filename, 'r') as csvfile:
        df = pd.read_csv(csvfile, dtype=object)
        anomaly_id = df.iloc[:, 0]
        start_date = df.iloc[:, 1]
        start_time = df.iloc[:, 2]
        anomaly_description = df.iloc[:, 3]
        anomaly_signature = df.iloc[:, range(4, 56)]
        signature_text = df.iloc[:, 56]
        root_cause = df.iloc[:, 57]
        risks = df.iloc[:, 58]
        actions_taken = df.iloc[:, 59]
        end_date = df.iloc[:, 60]
        end_time = df.iloc[:, 61]
        affected_systems = df.iloc[:, 62]

        signature_header = anomaly_signature.columns.values

        for row in anomaly_signature.values:
            values = "".join(row)
            historical_binary_signatures.append(values)

    binary_signature = get_binary_signatures(signature, signature_header)

    # Number of times occurred in the past
    # First convert everything to numpy array
    # Then do transpose because 'where' method returns a tuple of 1 element
    historical_binary_signatures = numpy.array(historical_binary_signatures)
    binary_signature = numpy.array(binary_signature)
    all_occurrences_in_past = numpy.where(historical_binary_signatures == binary_signature)
    transposed_occurrences = numpy.transpose(all_occurrences_in_past)
    numOfOccurrences = len(transposed_occurrences)

    # show all occurrences, resolution, root cause
    time_stamps = []
    for occurrence in transposed_occurrences:
        time_stamps.append({'start_date': start_date.values[occurrence[0]],
                            'start_time': start_time.values[occurrence[0]],
                            'end_date': end_date.values[occurrence[0]],
                            'end_time': end_time.values[occurrence[0]],
                            'actions_taken': actions_taken.values[occurrence[0]],
                            'root_cause': root_cause.values[occurrence[0]]})

    # Build the explanation report and send it to the frontend
    explanation_report = {'num_occurrences': numOfOccurrences, 'time': time_stamps}

    return explanation_report


def get_binary_signatures(signature, header):
    arr = numpy.zeros(len(header), dtype='<U256')
    for symptom in signature:
        measurement = symptom.split(' Exceeds ')[0]
        threshold = symptom.split(' Exceeds ')[1]
        try:
            index = numpy.where(header == measurement)
            if threshold == "Upper Warning Limit":
                arr[index] = "0001"
            elif threshold == "Upper Caution Limit":
                arr[index] = "0010"
            elif threshold == "Lower Caution Limit":
                arr[index] = "0100"
            elif threshold == "Lower Warning Limit":
                arr[index] = "1000"
        except ValueError:
            print("Measurement doesn't exist.")

    arr[numpy.where(arr == '')] = '0000'
    binary_signature = "".join(arr)
    return binary_signature


def get_astrobee_procedure_list_from_pride():
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    url = "https://10.5.0.3:8000/api/procedures/available"
    # For testing, temporarily disable SSL verification at the Python level
    # WARNING: This is not recommended for production code
    old_https_context = ssl._create_default_https_context
    ssl._create_default_https_context = ssl._create_unverified_context
    print("here1------------------------------------------")
    # url = "https://localhost/api/procedures/available"
    payload = {}
    headers = {
        'Authorization': 'Bearer a57a391b-5e00-4872-844e-66d975e73c0a'
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    print("Response status code:", response.status_code)
    # response = json.loads(response.content)
    if response.status_code == 200:
        response_data = json.loads(response.content)
        procedure_name = []
        print("response_data", response_data)
        for item in response_data:
            if '_' in item.get('filename', ''):
                procedure_name.append({
                    'title': item.get('title', 'Unknown Title'), 
                    'staticProcedureID': item.get('staticProcedureID', '')
                })
        print("procedure_name", procedure_name)
        return procedure_name
    else:
        print(f"Error: API returned status code {response.status_code}")
        print("Response content:", response.content)
        return None

    # procedure_name = []
    # for item in response:
    #     print("astrobee item", item)
    #     print("")
    #     if '_' in item['filename']:
    #         print("filename in item")
    #         procedure_name.append({'title': item['title'], 'staticProcedureID': item['staticProcedureID']})
    # print("procedure_name", procedure_name)
    # return procedure_name


def get_subsystems_for_anomaly(anomaly_name: str, physics_simulation_mode=None):
    """
    Query Neo4j to get subsystems connected to a specific anomaly.
    
    Args:
        anomaly_name: Name of the anomaly to query for
        physics_simulation_mode: Simulation mode to determine database connection
        
    Returns:
        List of subsystem names connected to the anomaly
    """
    driver, session = get_database_connection(physics_simulation_mode)
    
    try:
        # Query to get subsystems connected to the anomaly
        query = """
        MATCH (anomaly:Anomaly)-[:SUBSYSTEM]->(subsystem)
        WHERE anomaly.Title = $anomaly_name OR anomaly.Name = $anomaly_name
        RETURN DISTINCT subsystem.Name AS subsystem_name, subsystem.Title AS subsystem_title
        """
        
        result = session.run(query, anomaly_name=anomaly_name)
        subsystems = []
        
        for record in result:
            subsystem_name = record['subsystem_name'] or record['subsystem_title']
            if subsystem_name:
                subsystems.append(subsystem_name)
        
        return subsystems
        
    finally:
        session.close()
        driver.close()


def get_components_for_subsystem(subsystem_name: str, physics_simulation_mode=None):
    """
    Query Neo4j to get components contained in a specific subsystem.
    
    Args:
        subsystem_name: Name of the subsystem to query for
        physics_simulation_mode: Simulation mode to determine database connection
        
    Returns:
        List of component names contained in the subsystem
    """
    driver, session = get_database_connection(physics_simulation_mode)
    
    try:
        # Query to get components for the subsystem
        query = """
        MATCH (subsystem)-[:CONTAINS]->(component)
        WHERE subsystem.Name = $subsystem_name OR subsystem.Title = $subsystem_name
        RETURN DISTINCT component.Name AS component_name, component.Title AS component_title
        """
        
        result = session.run(query, subsystem_name=subsystem_name)
        components = []
        
        for record in result:
            component_name = record['component_name'] or record['component_title']
            if component_name:
                components.append(component_name)
        
        return components
        
    finally:
        session.close()
        driver.close()


def get_primary_sensor(physics_simulation_mode=None):
    """
    Query Neo4j to get the primary/main sensor for physics diagnosis.
    
    Args:
        physics_simulation_mode: Simulation mode to determine database connection
        
    Returns:
        Primary sensor name
    """
    driver, session = get_database_connection(physics_simulation_mode)
    
    try:
        # Query for the main sensor node
        query = """
        MATCH (sensor:Sensor)
        WHERE sensor.Type = 'Primary' OR sensor.Name CONTAINS 'CO2' OR sensor.Name CONTAINS 'ppCO2'
        RETURN sensor.Name AS sensor_name
        LIMIT 1
        """
        
        result = session.run(query)
        
        for record in result:
            return record['sensor_name']
            
        return None
        
    finally:
        session.close()
        driver.close()


def get_components_for_anomaly(anomaly_name: str, physics_simulation_mode=None):
    """
    Query Neo4j to get all components related to a specific anomaly through subsystems.
    
    Args:
        anomaly_name: Name of the anomaly to query for
        physics_simulation_mode: Simulation mode to determine database connection
        
    Returns:
        Dictionary with subsystems and components
    """
    driver, session = get_database_connection(physics_simulation_mode)
    
    try:
        # Query to get components for each subsystem connected to the anomaly
        query = """
        MATCH (anomaly:Anomaly)-[:SUBSYSTEM]->(subsystem)-[:CONTAINS]->(component)
        WHERE anomaly.Title = $anomaly_name OR anomaly.Name = $anomaly_name
        RETURN DISTINCT 
            subsystem.Name AS subsystem_name, 
            subsystem.Title AS subsystem_title,
            component.Name AS component_name, 
            component.Title AS component_title
        """
        
        result = session.run(query, anomaly_name=anomaly_name)
        
        subsystems = set()
        components = []
        
        for record in result:
            subsystem_name = record['subsystem_name'] or record['subsystem_title']
            component_name = record['component_name'] or record['component_title']
            
            if subsystem_name:
                subsystems.add(subsystem_name)
            if component_name:
                components.append(component_name)
        
        return {
            'subsystems': list(subsystems),
            'components': components
        }
        
    finally:
        session.close()
        driver.close()
