# query_network.py
# Author: Joshua Elston
# Last Edited: 03/28/2025

# Used to query the Bayesian network to compute posterior probabilities based on user inputs
# for parameter values --> called in ECLSS_Bayesian_Network.py

import time

def query_network(infer, parameter_values, measurement_ranges, split_probability_dict, additional_evidence, hidden_probabilities_dict):
    # Start timing the network query
    tic = time.time()
    
    # Create state mappings for the high and low parameter variables
    high_state_mapping = {
        'Nominal': 0,
        'Exceeds_UpperCautionLimit': 1,
        'Exceeds_UpperWarningLimit': 2
    }
    low_state_mapping = {
        'Nominal': 0,
        'Exceeds_LowerCautionLimit': 1,
        'Exceeds_LowerWarningLimit': 2
    }
    
    # Create a new dictionary to store the evidence for a given query
    evidence = {}
    
    # The nested function discretize_values is used to classify the threshold range within which
    # an entered parameter value falls to be stored as evidence when querying the network
    def discretize_values(parameter, value, measurement_ranges):
        # Get the thresholds for the specific parameter of interest
        thresholds = measurement_ranges[parameter]

        # Check which threshold range the entered value falls into
        matched_threshold = None

        if value is not None:
            for threshold_name, (low, high, include_low, include_high) in thresholds.items():
                if (
                    (low is None or (include_low and value >= low) or (not include_low and value > low)) and
                    (high is None or (include_high and value <= high) or (not include_high and value < high))
                ):
                    matched_threshold = threshold_name
                    break
        # If a matching threshold is found, return it
        if matched_threshold:
            return matched_threshold
        else:
            raise(ValueError(f"The value {value} for {parameter} does not match any defined thresholds."))

    # Prepare evidence based on user input
    for parameter, value in parameter_values.items():
        if value is not None:
            threshold = discretize_values(parameter, value, measurement_ranges)
            # Set the evidence based on the threshold returned from 'discrete_values'
            if "Upper" in threshold:
                evidence[f'high {parameter}'] = high_state_mapping[threshold] # use the corresponding index
                # evidence[f'low_{parameter}'] = low_state_mapping['Nominal'] # set the complementary lower range value to 'Nominal'
            elif "Lower" in threshold:
                # evidence[f'high_{parameter}'] = high_state_mapping['Nominal'] # set the complementary higher range value to 'Nominal
                evidence[f'low {parameter}'] = low_state_mapping[threshold] # use the corresponding index
            else: # entered value is within the 'Nominal' value range
                evidence[f'high {parameter}'] = high_state_mapping['Nominal']
                evidence[f'low {parameter}'] = low_state_mapping['Nominal']
        
    # If the user doesn't enter a value for a given parameter, set its evidence to 'Nominal'
    for parameter in measurement_ranges.keys():
        # As high_X and low_X are set simultaneously, comparing to either one would yield the desired result
        if f'high {parameter}' not in evidence and f'low {parameter}' not in evidence:
            evidence[f'high {parameter}'] = high_state_mapping['Nominal']
            evidence[f'low {parameter}'] = low_state_mapping['Nominal']

    # Verify that evidence is correctly added when querying the network
    print('Evidence:', evidence)

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
    # NOTE: Trying to perform inference on all anomalies at once leads to a runtime error, as it is too big of problem;
    # thus, it seems that the individual query approach is the most feasible currently
    if additional_evidence is not None:
        additional_evidence_dict = {}
        for i in additional_evidence:
            if additional_evidence[i] in [1,2]:
                additional_evidence_dict[i] = 0
            else:
                additional_evidence_dict[i] = 1
        # Add the additional evidence to the existing evidence dictionary
        evidence.update(additional_evidence_dict)
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

    toc = time.time()
    runtime = toc - tic

    # Return results and evidence
    return normalized_probabilities, evidence, runtime


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