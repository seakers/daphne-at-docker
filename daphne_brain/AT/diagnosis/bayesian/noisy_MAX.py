# noisy_max
# Author: Joshua Elston
# Last Edited: 06/10/2025

# Computes the CPTs for each parameter conditioned on all of its parent anomalies --> called in the add_cpds.py script

from itertools import product
# from probabilities import split_probability_dict

# The noisy_MAX function is used to compute the conditional probability tables (CPTs) for each parameter conditioned
# on all of their parent anomalies. This approach assumes that the effects of each parent anomaly independently
# influence the child parameter with a certain probability. 
def noisy_MAX(split_probability_dict, parameter, anomalies):
    # Just as done within probabilities.py, define the high and low groups, structured to ensure 
    # that the 'Nominal' state is the minimum value of the ordinal variable
    # NOTE: Based on the implementation in calculate_CPTs, this order is flipped such that 'Nominal'
    # is the first value, but this still corresponds to the minimum value
    high_states = ['Nominal', 'Exceeds_UpperCautionLimit', 'Exceeds_UpperWarningLimit']
    low_states = ['Nominal', 'Exceeds_LowerCautionLimit', 'Exceeds_LowerWarningLimit']

    # Initialize dictionaries to store the noisy MAX CPTs
    cpt_high = {}
    cpt_low = {}

    # Calculate the cumulative probabilities
    def cumulative_probabilities(states, group, anomaly_presence):
        # Initialize an empty dictionary to store the cumulative probabilities
        state_C_y_xi = {}
        
        for i, state in enumerate(states): #range(len(states)):
            # Calculate C_y_xi for each state
            C_y_xi = 1 # start multiplication with a value of 1

            # print('Anomaly presence items:')
            # print(anomaly_presence.items())

            # Iterate over each anomaly and its True/False state to calculate the cumulative probabilities
            for anomaly, parent_type in anomaly_presence.items():
                # print(f'Processing anomaly: {anomaly} ({is_true})')

                # Access the group of probabilities for the high or low parameter values for each parent anomaly state (True/False)
                # group_data = split_probability_dict.get(parameter, {}).get(anomaly, {}).get(str(is_true), {}).get(group, {})
                # group_data = split_probability_dict.get(parameter, {}).get(anomaly, {}).get(is_true, {}).get(group, {})


                print('---------------LOOKUP TRACE---------------')
                print(f"Parameter: {parameter}")
                print(f"Parent: {anomaly}")
                print(f"Parent Type: {parent_type}")
                print(f"Group Key: {group}")
                print('------------------------')

                # NEW CODE
                anomaly_block = split_probability_dict.get(parameter, {}).get(anomaly, {})
                print(f"anomaly block: {anomaly_block}")

                # Determine how to access the probabilities based on the type of parent being handled (binary or multivariate)
                if parent_type in ['False', 'True']:
                    # Binary parent
                    entry = anomaly_block.get(parent_type, {})
                    prob_entry = entry.get(group, {})
                    anomaly_probs = prob_entry.get('probabilities', {})
                    # print(f'[BINARY] Probabilities: {anomaly_probs}')
                else:
                    # Multivariate parent
                    group_entry = anomaly_block.get(group, {})
                    probabilities = group_entry.get('probabilities', {})
                    anomaly_probs = probabilities.get(parent_type, {})

                    print(f"[MULTIVARIATE] Group: {group}")
                    print(f"[MULTIVARIATE] Probabilities keys (parent states): {list(probabilities.keys())}")
                    print(f"[MULTIVARIATE] Probabilities: {anomaly_probs}")
                

                # if not anomaly_probs:
                #     print(f"[WARNING] Missing probabilities for {parameter} given {anomaly} = {parent_type}, group = {group}")
                #     continue
                # else:
                #     print(f"Probabilities present for {parameter} given {anomaly} = {group}")



                # Initialize the conditional probability that X_i, when taking the value x_i, raises the value 
                # of Y to y (this will be summed across all states <= current state) 
                c_zi_xi = 0
                # Sum the probabilities of states <= current state
                for z_idx in range(i + 1): # ensure that z_idx ranges over states <= current state
                    z_state = states[z_idx]
                    # print(f'Parameter State: {z_state}')

                    c_zi_xi += anomaly_probs.get(z_state, 0)
                    # print(f'c_zi_xi: {c_zi_xi}')

                # Multiply the cumulative probability
                C_y_xi *= c_zi_xi
                # print(f'C_y_xi: {C_y_xi}')

            state_C_y_xi[state] = C_y_xi
            # print(f"state_C_y_xi: {state_C_y_xi}")
        return state_C_y_xi
    
    # Calculate the CPTs (P(y|x)) using the above cumulative probabilities
    def calculate_CPTs(cumulative_probs, states):
        # Initialize a dictionary for the CPT
        p_y_given_x = {}

        # print('------------------Calculuating CPTs------------------')
        # print('Cumulative Probabilities: ', cumulative_probs)
        # print('States being processed: ', states)

        for i, state in enumerate(states):
            # print(f'Processing state {state} at index {i}:')
            if i == 0: # corresponding to the minimum state of each parameter ('Nominal' for both groups)
                p_y_given_x[state] = cumulative_probs[state]
                # print(f"First state ({state}): Setting p_y_given_x[{state}] = {cumulative_probs[state]}")
            else:
                p_y_given_x[state] = cumulative_probs[state] - cumulative_probs[states[i - 1]]
                # print(f'State {state}: Setting p_y_given_x[{state}] = {cumulative_probs[state]} - {cumulative_probs[states[i - 1]]} = {p_y_given_x[state]}')
        # print('Final CPT:', p_y_given_x)
        # print()

        # for key, val in p_y_given_x.items():
        #     if not isinstance(val, (int, float)):
        #         print(f"[ERROR] Non-numeric value in CPT: key = {key}, val = {val} (type = {type(val)})")
        #         raise TypeError(f"CPT value must be numeric but got {type(val)} for key {key}: {val}")

        # try:
        #     total = sum(p_y_given_x.values())
        #     print(f"Total of CPT values: {total}")
        # except TypeError as e:
        #     print(f"[EXCEPTION] Failed to sum CPT values: {p_y_given_x}")
        #     raise

        # if total == 0:
        #     print("[WARNING] Total CPT probability is zero. cumulative rpobs:", cumulative_probs)

        # print("------------------End CPT caluclations (prior to normalization------------------)")

        # Normalize probabilities to ensure that they all sum to 1 <-- had previous rounding issues that made this normalization necessary
        def normalize_probabilities(probabilities):
            total = sum(probabilities.values())
            if total == 0:
                raise ValueError("Total probability is zero, cannot normalize")
            normalized_probs = {state: prob / total for state, prob in probabilities.items()}

            # print(f"Normalized probailities: {normalized_probs}")

            return normalized_probs
        
        # Return the normalized probabilities
        p_y_given_x = normalize_probabilities(p_y_given_x)

        return p_y_given_x

    # Create an empty list to store the state spaces for all relevant parent nodes
    parent_state_spaces = []
    for anomaly in anomalies:
        anomaly_dict = split_probability_dict.get(parameter, {}).get(anomaly, {})
        
        # Create an iterator to go through anomaly states to identify whether a binary or multivariate parent is being assessed
        iter_key = next(iter(anomaly_dict), None)

        # First, check if the parent node is binary
        if iter_key in ['True', 'False']:
        # if set(anomaly_dict.items()) == {'True', 'False'}:
            states = list(anomaly_dict.keys())
            parent_state_spaces.append(states)
        else:
            multivariate_states = anomaly_dict[iter_key]
            prob_dict = multivariate_states.get('probabilities', {})
            states = list(prob_dict.keys())
            parent_state_spaces.append(states)

    print(f"Parent state spaces: {parent_state_spaces}")

    # Iterate over all combinations of parent states for a given parameter
    for combo in product(*parent_state_spaces):
        anomaly_presence = dict(zip(anomalies, combo))

    # # Iterate over all combinations of True/False states for the parent anomalies
    # for presence_combination in product([False, True], repeat = len(anomalies)):
    #     # Map each parent anomaly to its True/False state in its current combination
    #     anomaly_presence = dict(zip(anomalies, presence_combination))

        # Get cumulative probabilities for the high and low group states for each parameter
        cumulative_high = cumulative_probabilities(high_states, f'high {parameter}', anomaly_presence)
        cumulative_low = cumulative_probabilities(low_states, f'low {parameter}', anomaly_presence)

        # # Determine the CPTs for the high and low groups for the current parameter
        # cpt_high[presence_combination] = calculate_CPTs(cumulative_high, high_states)
        # cpt_low[presence_combination] = calculate_CPTs(cumulative_low, low_states)

        # Determine the CPTs for the high and low groups for the current parameter
        cpt_high[tuple(combo)] = calculate_CPTs(cumulative_high, high_states)
        cpt_low[tuple(combo)] = calculate_CPTs(cumulative_low, low_states)

        # print("High CPT:")
        # print(cpt_high)

    return cpt_high, cpt_low

def check_cumulative_probabilities(cpt_high, cpt_low):
    def validate_cpt(cpt, group):
        # Initialize flag
        all_valid = True
        for combo, probabilities in cpt.items():
            total = sum(probabilities.values())
            if not total == 1:
                all_valid = False
                print(f"Error in {group} CPT for parent states {combo}: Sum = {total} ≠ 1")
        return all_valid
    
    # Validate each high and low CPT for each parameter
    valid_high = validate_cpt(cpt_high, "high")
    valid_low = validate_cpt(cpt_low, "low")

    return valid_high, valid_low

# # Example
# from probabilities import split_probability_dict
# AuxCabinFan2_high_CPT, AuxCabinFan2_low_CPT = noisy_MAX(split_probability_dict, "Aux Cabin Fan #2", ["Fuel Cell #1 and PDU Failure", "PDU 4 Failure", "PDU 5 Failure" , "TCCS Auxiliary Fan #2 Failure", "TCCS Auxiliary Fan at Reduced Capacity"])

# for combo, cpt in AuxCabinFan2_high_CPT.items():
#     print(f"High Aux Cabin Fan #2 CPT for parent states {combo}:")
#     for state, prob in cpt.items():
#         print(f"{state}: {prob}")
#     print()

# for combo, cpt in AuxCabinFan2_low_CPT.items():
#     print(f"Low Aux Cabin Fan #2 CPT for parent states {combo}:")
#     for state, prob in cpt.items():
#         print(f"{state}: {prob}")
#     print()

# if check_cumulative_probabilities(AuxCabinFan2_high_CPT, AuxCabinFan2_low_CPT):
#     print("All CPTs are valid: probabilities sum to 1")
# else:
#     print("Error: not all CPTs sum to 1")