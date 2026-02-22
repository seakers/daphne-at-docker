# reduced_add_cpds.py
# Author: Joshua Elston
# Last Edited: 02/09/2026

# Quicker to create small development copy of add_cpds for reduced network for parameter learning

# from AT.diagnosis.bayesian.noisy_MAX import noisy_MAX
from noisy_MAX import noisy_MAX
from pgmpy.factors.discrete import TabularCPD
from itertools import product
from math import prod
# from AT.diagnosis.bayesian.dictionaries import combined_failure_dict, subgroup_dict, nap_dict
from reduced_dictionaries import combined_failure_dict, subgroup_dict, nap_dict
import time
import numpy as np

tic = time.time()

def safe_make_cpd(parameter, states, values, evidence, evidence_card):
    # Determine the number of columns expected based on the product of parent node cardinalities
    expected_cols = prod(evidence_card) if evidence else 1
    actual_cols = len(values[0]) if values else 0
    if actual_cols != expected_cols:
        print(f'[ERROR]: {parameter}: columns = {actual_cols}')
        print(f'Expected columns: {expected_cols}, evidence: {evidence}, evidence_card: {evidence_card}')
    try:
        return TabularCPD(variable = parameter,
                      variable_card = states,
                      values = values,
                      evidence = evidence,
                      evidence_card = evidence_card)
    except Exception as e:
        print(f"[FAIL] TabularCPD could not be created for {parameter}: {e}")
        raise

def add_cpds(model, split_probability_dict, hidden_probabilities_dict, anomaly_cardinality, print_cpds=False):
    print('Creating parameter CPDs...')
    
    for parameter, anomalies in split_probability_dict.items():
        # Generate a list of parent anomalies for the current parameter
        anomaly_list = list(anomalies.keys())

        high_parents = [a for a in anomaly_list if not a.startswith("low")]
        low_parents = [a for a in anomaly_list if not a.startswith("high")]

        def get_parent_cards(parents):
            parent_cards = []
            for parent in parents:
                parent_dict = split_probability_dict[parameter][parent]
                
                # Similar to in noisy_MAX, create an iterator to check all states of the current parent node
                iter_key = next(iter(parent_dict), None)
                
                # First, check if the parent is binary
                if iter_key in ['False', 'True']:
                    parent_cards.append(len(parent_dict))
                # If parent is multivariate, adjust accordingly
                else:
                    prob_dict = parent_dict[iter_key].get('probabilities', {})
                    parent_cards.append(len(prob_dict))
                    # print(f"Cardinality for parent {parent}: {len(prob_dict)}")
            return parent_cards
        
        high_cards = get_parent_cards(high_parents)
        low_cards = get_parent_cards(low_parents)

        # Generate CPTs for the low and high cases
        high_cpt, low_cpt = noisy_MAX(split_probability_dict, parameter, anomaly_list)

        # Define the states for the high and low CPDs (identical to those used in the noisy_MAX function)
        high_states = ['Nominal', 'Exceeds_UpperCautionLimit', 'Exceeds_UpperWarningLimit']
        low_states = ['Nominal', 'Exceeds_LowerCautionLimit', 'Exceeds_LowerWarningLimit']

        # Extract probabilities for each state in 'high_states' and 'low_states' across all parent anomaly combinations
        high_values = []
        for state in high_states:
            high_state_probs = [cpt.get(state, 0) for _, cpt in high_cpt.items()]
            high_values.append(high_state_probs)

        low_values = []
        for state in low_states:
            low_state_probs = [cpt.get(state, 0) for _, cpt in low_cpt.items()]
            low_values.append(low_state_probs)

        # Create the CPDs for the high and low states of the current parameter
        high_cpd = safe_make_cpd(
            f'high {parameter}', # variable
            len(high_states), # variable_card
            high_values, # values
            high_parents, # evidence
            high_cards) # evidence_card
       
        low_cpd = safe_make_cpd(
            f'low {parameter}', # variable
            len(low_states), # variable_card
            low_values, # values
            low_parents, # evidence
            low_cards) # evidence_card

        model.add_cpds(high_cpd, low_cpd)

    print('Creating [HIDDEN] CPDs...')
    # Add CPDs for the hidden nodes
    for hidden_parameter, anomalies in hidden_probabilities_dict.items():
        parent_anomalies = list(anomalies.keys())
        num_parents = len(parent_anomalies)

        c_values = [anomalies[a]['probabilities']['true']['True'] for a in parent_anomalies]
        
        parent_combos = list(product([False, True], repeat = num_parents))

        # For each combination, compute the probability that the hidden parameter is True
        cpt_true = []
        for combo in parent_combos:
            # If all parents are False, set the probability of an active hidden parameter extremely low
            if not any(combo):
                p_true = 0.0001
            else:
                # Use noisy-OR combination logic
                p_true = 1 - np.prod([1 - c for c, active in zip(c_values, combo) if active])
            cpt_true.append(p_true)

        # Compute complementary probabilities for the hidden parameter being absent
        cpt_false = [1 - p for p in cpt_true]

        # Convert to pgmpy CPT format (rows = [False, True])
        cpt_values = [cpt_false, cpt_true]

        # Build TabularCPD
        hidden_cpd = TabularCPD(
            variable = hidden_parameter,
            variable_card = 2,
            values = cpt_values,
            evidence = parent_anomalies,
            evidence_card = [2] * num_parents
        )
        # TEST PRINT (11/3/2025)
        if print_cpds:
            print(hidden_cpd)
        model.add_cpds(hidden_cpd)

        # for anomaly, data in anomalies.items():
        #     # Extract activation probabilities for each hidden node conditioned
        #     # on the associated parent anomaly
        #     c_i = data['probabilities']['true']['True']
        #     q_i = round(1 - c_i, 3)

        #     # NOTE: These can either be defined within the hidden_probabilities_dict or automatically
        #     # for all hidden nodes as done here; this just removes the need for the 'False' subdictionary
        #     # Defined as such to prevent deterministic behavior observed when setting the A = 0 probabilities
        #     # to 1 and 0 for AE = 'False' or 'True', respectively (which follows the Noisy OR format)
        #     hidden_probs = [[0.9999, q_i],
        #                     [0.0001, c_i]]

        #     # Create CPTs for each individual parent child relationship
        #     hidden_cpd = TabularCPD(
        #         variable = hidden_parameter,
        #         variable_card = len(hidden_probs),
        #         values = hidden_probs,
        #         evidence = [anomaly],
        #         evidence_card = [anomaly_cardinality]
        #     )

        #     model.add_cpds(hidden_cpd)

# COMMENTED OUT ON 02/11/2026 TO SEE IF REDUCED NETWORK CAN BE BUILT W/O NEED FOR SUBGROUPS
    # print("Creating combined failure CPDs...")
    # # NEW CODE ON 10/31/2025
    # for child, parents in combined_failure_dict.items():
    #     num_parents = len(parents)
    #     evidence_card = [2] * num_parents # binary parents

    #     combinations = list(product([0, 1], repeat = num_parents))

    #     child_failure_probs = []
    #     for combo in combinations:
    #         num_failures = sum(combo)
    #         if num_failures == 0:
    #             p_failure = 0.01
    #         elif num_failures == len(parents):
    #             p_failure = 0.99
    #         else:
    #             p_failure = 0.95
    #         child_failure_probs.append(p_failure)

    #     values = [
    #         [round(1 - p, 2) for p in child_failure_probs],
    #         [p for p in child_failure_probs]
    #     ]

    #     cpd = TabularCPD(
    #         variable = child,
    #         variable_card = 2,
    #         values = values,
    #         evidence = parents,
    #         evidence_card = evidence_card
    #     )
    #     model.add_cpds(cpd)

    # print('Creating subgroup CPDs...')
    # # Add CPDs for subgroups conditioned on the status of their related anomalies
    # for subgroup, anomalies in subgroup_dict.items():
    #     num_anomalies = len(anomalies)

    #     # Create all possible True/False state combinations for the anomalies for a given subgroup
    #     anomaly_states = list(product([False, True], repeat = num_anomalies))

    #     # Create an empty list to store the CPT values for each combination of anomaly states
    #     cpt_values = []
    #     for state_combo in anomaly_states:
    #         # If any anomaly is True, set the probability of the subgroup being True to ~1
    #         if any(state_combo):
    #             cpt_values.append([0.0001, 0.9999])
    #         # If no anomalies are True, set the probability of the subgroup being False to ~1
    #         else:
    #             cpt_values.append([0.9999, 0.0001])

    #     # Reshape the CPT values to align with TabularCPD formatting
    #     cpt_values = list(zip(*cpt_values))
       
    #     # Create CPDs for each subgroup
    #     subgroup_cpd = TabularCPD(
    #        variable = subgroup,
    #        variable_card = 2,
    #        values = cpt_values,
    #        evidence = anomalies,
    #        evidence_card = [2] * num_anomalies
    #    )

    #     model.add_cpds(subgroup_cpd)

    # print('Creating NAP CPD...')
    # # Add CPD for the No Anomalies Present node conditoned on the state of each of the subgroups
    # for nap, subgroups in nap_dict.items():
    #     num_groups = len(subgroups)

    #     # Create all possible True/False combinations of the subgroup states
    #     group_states = list(product([False, True], repeat = num_groups))

    #     # Create an empty list to store the CPT for each combination of group states
    #     cpt_values = []
    #     for state_combo in group_states:
    #         # If any of the subgroups is True, set the probability of NAP being False to ~1
    #         if any(state_combo):
    #             cpt_values.append([0.9999, 0.0001])
    #         # If none of the subgroups are True, set the probability of NAP being True to ~1
    #         else:
    #             cpt_values.append([0.0001, 0.9999])

    #     # Reshape the CPT values to align with TabularCPD formatting
    #     cpt_values = list(zip(*cpt_values))

    #     # Create the CPD for No Anomalies Present conditioned on the states of the subgroups
    #     nap_cpd = TabularCPD(
    #         variable = nap,
    #         variable_card = 2,
    #         values = cpt_values,
    #         evidence = subgroups,
    #         evidence_card = [2] * num_groups
    #     )

    #     model.add_cpds(nap_cpd)

    # Verify expected parents
    if print_cpds:
        testparam = 'CDRA Failure'
        print(f"Expected parents for {testparam}: {model.get_parents(testparam)}")
        print(model.get_cpds(testparam))

    # Verify that the model is valid after adding the CPDs
    #   - Checks if sum of probabilities for each state is equal to 1 (tol = 0.01)
    #   - Checks if CPDs associated with nodes are consistent with their parents
    if model.check_model():
        print("\nModel is valid with added CPDs.")
    else:
        print("Model is invalid. Please check the format of the input CPTs.")
    print()

toc = time.time()
query_time = toc - tic
print(f"Add CPDs runtime: {query_time}")