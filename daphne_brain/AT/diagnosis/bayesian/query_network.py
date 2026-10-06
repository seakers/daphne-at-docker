# query_network.py
# Author: Joshua Elston
# Last Edited: 09/26/2026

# Used to query the Bayesian network to compute posterior probabilities based on user inputs
# for parameter values --> called in ECLSS_Bayesian_Network.py
# Changes on 10/29/2025 remove parameters from list of query variables (i.e., purely retaining them as evidence)
# Minor update on 06/08/2026 to correctly added Unknown Anomaly in the set of variables to query for inference
# Minor update on 09/19/2026 to correct flooring when rounding to 4 decimals
# Updated on 09/26/2026 to correctly extract runtime and consolidate unused functions

import time, math

def query_network(infer, fan_status, parameter_values, measurement_ranges, split_probability_dict, additional_evidence, hidden_probabilities_dict):
    
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

    PARAMETER_KEY_MAP = {
        'ppO2 (L1)': 'ppO2_IHab (IHab)',
        'ppO2 (L2)': 'ppO2_HALO (HALO)',
        'ppCO2 (L1)': 'ppCO2_IHab (IHab)',
        'ppCO2 (L2)': 'ppCO2_HALO (HALO)',
        'Humidity (L1)': 'Humidity_IHab (IHab)',
        'Humidity (L2)': 'Humidity_HALO (HALO)',
        'ppO2 (L1) (t-1)': 'ppO2_IHab (IHab) (t-1)',
        'ppO2 (L2) (t-1)': 'ppO2_HALO (HALO) (t-1)',
        'ppCO2 (L1) (t-1)': 'ppCO2_IHab (IHab) (t-1)',
        'ppCO2 (L2) (t-1)': 'ppCO2_HALO (HALO) (t-1)',
        'Humidity (L1) (t-1)': 'Humidity_IHab (IHab) (t-1)',
        'Humidity (L2) (t-1)': 'Humidity_HALO (HALO) (t-1)',
        'Total Cabin Pressure (L1)': 'Total_Cabin_Pressure_IHab (IHab)',
        'Total Cabin Pressure (L2)': 'Total_Cabin_Pressure_HALO (HALO)',
        'Total Cabin Pressure (L1) (t-1)': 'Total_Cabin_Pressure_IHab (IHab) (t-1)',
        'Total Cabin Pressure (L2) (t-1)': 'Total_Cabin_Pressure_HALO (HALO) (t-1)'
    }
    
    # Create a new dictionary to store the evidence for a given query
    evidence = {}
    
    # The nested function discretize_values is used to classify the threshold range within which
    # an entered parameter value falls to be stored as evidence when querying the network
    def discretize_values(parameter, value, measurement_ranges):
        # Get the thresholds for the specific parameter of interest
        mapped_parameter = PARAMETER_KEY_MAP.get(parameter, parameter)
        thresholds = measurement_ranges[mapped_parameter]

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
            # print("measurement_ranges keys:", measurement_ranges.keys())
            # print("parameter:", parameter)
            threshold = discretize_values(parameter, value, measurement_ranges)
            mapped_parameter = PARAMETER_KEY_MAP.get(parameter, parameter)
            # Set the evidence based on the threshold returned from 'discrete_values'
            if "Upper" in threshold:
                evidence[f'high {mapped_parameter}'] = high_state_mapping[threshold] # use the corresponding index
                # evidence[f'low_{parameter}'] = low_state_mapping['Nominal'] # set the complementary lower range value to 'Nominal'
            elif "Lower" in threshold:
                # evidence[f'high_{parameter}'] = high_state_mapping['Nominal'] # set the complementary higher range value to 'Nominal
                evidence[f'low {mapped_parameter}'] = low_state_mapping[threshold] # use the corresponding index
            else: # entered value is within the 'Nominal' value range
                evidence[f'high {mapped_parameter}'] = high_state_mapping['Nominal']
                evidence[f'low {mapped_parameter}'] = low_state_mapping['Nominal']
        
    # If the user doesn't enter a value for a given parameter, set its evidence to 'Nominal'
    for parameter in measurement_ranges.keys():
        # As high_X and low_X are set simultaneously, comparing to either one would yield the desired result
        if f'high {parameter}' not in evidence and f'low {parameter}' not in evidence:
            evidence[f'high {parameter}'] = high_state_mapping['Nominal']
            evidence[f'low {parameter}'] = low_state_mapping['Nominal']

    # Fan Status is a binary parameter, currently defined manually in ECLSS_Bayesian_Netowrk_Learned.py.
    # In future, this value should be converted and passed in with other telemetry values
    if fan_status is not None:
        evidence['Fan Status'] = int(fan_status)

    # Verify that evidence is correctly added when querying the network
    print('Evidence:', evidence)

    # NEW CODE ON 10/29/2025
    # Create a set of all parameter variable names to ensure correct parameters are removed as variables prior to inference
    all_parameters = set()
    for param in measurement_ranges.keys():
        all_parameters.add(f"high {param}")
        all_parameters.add(f"low {param}")

    # Extract unique anomalies from the probabilities_dict
    unique_anomalies = set() # using a set handles duplicate anomalies

    for _, anomaly_dict in split_probability_dict.items():
        for anomaly_name in anomaly_dict.keys():
            # Skip anomalies that are themselves parameters in the network
            if anomaly_name in all_parameters:
                continue
            else:
                unique_anomalies.add(anomaly_name) # add anomalies

    anomalies_to_query = list(unique_anomalies)
    # Add the Unknown Anomaly node to the set of anomalies to be queried based on the telemetry feed evidence
    anomalies_to_query.append("Unknown Anomaly")
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

    # Start timing the inference speed
    tic = time.perf_counter()

    try:
        for anomaly in anomalies_to_query:
            result = infer.query(variables = [anomaly], evidence = evidence)
            anomaly_probabilities[anomaly] = result.values[1] # [0] --> anomaly absent

    except Exception as e:
        raise RuntimeError(f"Error during inference: {e}")

    toc = time.perf_counter()
    runtime = round(toc - tic, 3)

    # Create a dictionary to store the normalized probabilities of each anomaly
    normalized_probabilities = {}
    # Normalize the anomaly probabilities by summing to one
    total_anomaly_probabilities = sum(anomaly_probabilities.values())

    # Compute raw normalized values and floor to 4 decimal places
    raw = {k: v / total_anomaly_probabilities for k, v in anomaly_probabilities.items()}
    floored = {k: math.floor(v * 10000) / 10000 for k, v in raw.items()}

    # Calculate how many units of 0.0001 need to be redistributed
    deficit = round(1.0 - sum(floored.values()), 4)
    n_to_adjust = round(deficit / 0.0001)

    # Distribute deficit to keys with the largest remainders
    remainders = {k: raw[k] * 10000 % 1 for k in raw}
    sorted_by_remainder = sorted(remainders, key=lambda k: remainders[k], reverse=True)

    normalized_probabilities = dict(floored)
    for k in sorted_by_remainder[:n_to_adjust]:
        normalized_probabilities[k] = round(normalized_probabilities[k] + 0.0001, 4)

    # for anomaly, probability in anomaly_probabilities.items():
    #     normalized_probabilities[anomaly] = round(probability / total_anomaly_probabilities, 4)

    # Return results and evidence
    return normalized_probabilities, evidence, runtime