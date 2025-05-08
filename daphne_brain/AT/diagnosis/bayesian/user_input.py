# user_input.py
# Author: Joshua Elston
# Last Edited: 03/28/2025

# Used to process user inputs and display updated Bayesian network beliefs based on provided evidence --> called in ECLSS_Bayesian_Network.py

import time
from AT.diagnosis.bayesian.query_network import query_network

def get_parameter_input(telemetry_values,measurement_ranges):
    # Prompt the user to enter a parameter and its value
    parameter = input("Enter a parameter to update its value (or 'exit' to quit): ")
    # Check the exit criteria
    if parameter.lower() == 'exit':
        return None, None
    elif parameter not in measurement_ranges:
        print("Invalid parameter. Please try again.")
        return get_parameter_input(measurement_ranges) # recursively prompt user until 'exit' entered
    
    value_input = input(f"Enter a value for {parameter} (leave empty to set to 'Nominal'): ")
    if not value_input:
        # Retrieve a value within the 'Nominal' range if no input is provided
        nominal_range = measurement_ranges[parameter]['Nominal']
        # Set unentered parameters equal to the midpoint of the nominal range
        nominal_value = (nominal_range[0] + nominal_range[1]) / 2
        return parameter, nominal_value # set the parameter value to 'Nominal' if no value entered
    
    try:
        value = float(value_input)
    except ValueError:
        print("Invalid input. Please enter a number.")
        return get_parameter_input(measurement_ranges) # recursively prompt user if an incorrect input is detected
    
    return parameter, value

def query_parameters(infer, telemetry_values, measurement_ranges, split_probability_dict, additional_evidence, hidden_probabilities_dict):
    # Collect parameter values from the user, and query the Bayesian network with the updated evidence
    # while True:
    #     parameter_values = {}

    #     # Gather parameter values from the user
    #     while True:
    #         parameter, value = get_parameter_input(telemetry_values, measurement_ranges)
    #         if parameter is None:
    #             return {}, {} # exit if the user types 'exit'

    #         # Store parameter-value pairs in a dictionary (to be passed to the 'query_network' function)
    #         parameter_values[parameter] = value
    #         print(f"Collected: {parameter} with value {value}")
    #         print()

    #         # Ask the user if they want to enter additional parameter values
    #         if input("Add another parameter? (yes/no): ").strip().lower() != 'yes':
    #             break
    parameter_values = telemetry_values
    print("Parameter values: ", parameter_values)
    if parameter_values: # proceed if parameters detected
        try:
            # Query the Bayesian network
            print("i am here")
            normalized_probabilities, evidence, runtime = query_network(infer, parameter_values, measurement_ranges, split_probability_dict, additional_evidence,hidden_probabilities_dict)

            # Sort anomalies based on the probability of their presence
            sorted_anomalies = sorted(normalized_probabilities.items(), key = lambda x: x[1], reverse = True)

            # Print the sorted anomalies with their probabilities of being present
            print()
            print("Anomalies ranked by probability of presence:")
            for anomaly, prob in sorted_anomalies[:5]:
                if anomaly == 'No Anomalies Present':
                    print(f"P({anomaly}): {prob:.6f}")
                else:
                    print(f"P({anomaly} = 1): {prob:.6f}")
            print()
            print(f"Query runtime: {runtime:.2f}s")
            print()
        
            formatted_probabilities = {key: float(value) for key, value in normalized_probabilities.items()}
            print("Formatted probabilities: ", formatted_probabilities)
            # Return the formatted probabilities to calculate the entropy of the probability distribution
            return formatted_probabilities, evidence

        except RuntimeError as e:
            print(f"Error during querying: {e}")

        # # Ask the user if they wish to continue updating parameters
        # # NOTE: WITH NEW CALL TO QUERY ADDITIONAL EVIDENCE, DOESN'T APPEAR THAT THIS
        # # BLOCK IS BEING USED
        # if input("Would you like to continue updating parameter values? (yes/no): ").strip().lower() != 'yes':
        #     print()
        #     print("Exiting parameter updating process.")
        #     break


#################### User inputs for additional evidence ####################
def get_evidence_info(hidden_probabilities_dict):
    # Extract the names of the additional evidence variables (used to verify if variables entered correctly)
    additional_evidence_variables = []

    for evidence_names, _ in hidden_probabilities_dict.items():
        additional_evidence_variables.append(evidence_names)

    # Collect additional evidence from the crew
    hidden_parameter = input(f"Enter the additional evidence being collected: ").strip()
    # Verify that the variable name entered by the crew matches one of the hidden variables
    # defined in the Bayesian network
    if hidden_parameter not in additional_evidence_variables:
        print("Invalid additional evidence. Please try again.")
        return get_evidence_info(hidden_probabilities_dict) # recursively prompt user to correctly enter additional evidence

    # Collect the state (True/False) of the additional evidence being entered by the crew
    hidden_state = input("Enter the state (True/False): ").strip()
    if hidden_state not in ['False', 'True']:
        print(f"Invalid state for additional evidence variable {hidden_parameter}. Please enter either 'True' or 'False'")
        return get_evidence_info(hidden_probabilities_dict) # recursively prompt user to correctly enter additional evidence

    return hidden_parameter, hidden_state

def query_additional_evidence(infer, split_probability_dict, hidden_probabilities_dict, evidence, best_evidence, additional_evidence):
    # Function takes elements from query_network without the need to remap evidence that should have previous been set and stored there

    while True:
        # Create a dictionary to store additional evidence added by the crew
        # additional_evidence = {}

        # Gather additional evidence from the crew
        # # while True:
        # #     # hidden_parameter, hidden_state = get_evidence_info(hidden_probabilities_dict)

        #     # Create state mappings for the additional evidence
        #     additional_evidence_mapping = {
        #         'False': 0,
        #         'True': 1
        #     }

        #     additional_evidence[hidden_parameter] = additional_evidence_mapping[hidden_state]
        #     print(f"Collected: {hidden_parameter} with state {hidden_state}")
        #     print()

            # if hidden_parameter != best_evidence:
            #     if input(f"The additional evidence collected does not provide the most information about the present anomaly. Would you like to add evidence for {best_evidence}? (yes/no): ") != 'yes':
            #         break
            # else:
            #         break

        if additional_evidence: # proceed if additional evidence provided
            evidence.update(additional_evidence) # add the additional evidence to the main evidence dictionary

            print(f'Mapped evidence: {evidence}')

            # Extract unique anomalies from the probabilities_dict
            unique_anomalies = set() # using a set handles duplicate anomalies
            for _, anomaly in split_probability_dict.items():
                unique_anomalies.update(anomaly.keys()) # add anomalies

            anomalies_to_query = list(unique_anomalies)
            # Add the No Anomalies Present node to the set of anomalies to be queried based on the telemetry feed evidence
            anomalies_to_query.append("No Anomalies Present")
            # print('Anomalies to query:', anomalies_to_query)

            # Initialize a dictionary to store the probability of each anomaly being present
            anomaly_probabilities = {}

            # Perform the inference one anomaly at a time
            # NOTE: Because inference is performed one anomaly at a time, the probabilities are not normalized;
            # once the No Anomalies Present probability is calculated, the set of anomaly probabilities are all
            # normalized prior to calculating entropy
            try:
                for anomaly in anomalies_to_query:
                    result = infer.query(variables = [anomaly], evidence = evidence)
                    probability_of_anomaly_present = result.values[1] # [0] --> anomaly absent
                    anomaly_probabilities[anomaly] = probability_of_anomaly_present

            except Exception as e:
                raise RuntimeError(f"Error during inference: {e}")

            # Create a dictionary to store the normalized probabilities of each anomaly
            normalized_probabilities = {}
            # Normalize the anomaly probabilities by summing to one
            total_anomaly_probabilities = sum(anomaly_probabilities.values())
            for anomaly, probability in anomaly_probabilities.items():
                normalized_probabilities[anomaly] = probability / total_anomaly_probabilities

            # Sort normalized anomalies based on the probability of their presence
            sorted_anomalies = sorted(normalized_probabilities.items(), key = lambda x: x[1], reverse = True)

            # Print the sorted anomalies with their probabilities of being present
            # print()
            # print("Anomalies ranked by probability of presence (following inclusion of additional evidence):")
            # for anomaly, prob in sorted_anomalies[:5]:
            #     if anomaly == 'No Anomalies Present':
            #         print(f"P({anomaly}): {prob:.6f}")
            #     else:
            #         print(f"P({anomaly} = 1): {prob:.6f}")
            # print()

            formatted_probabilities = {key: float(value) for key, value in normalized_probabilities.items()}
            # print(f'Formatted probabilities: {formatted_probabilities}')

            return formatted_probabilities