# add_cpds.py
# Author: Joshua Elston
# Last Edited: 03/27/2025

# Adds the CPTs computed in noisy_MAX.py as Tabular CPDs to the Bayesian network --> called in the ECLSS_Baysian_Network.py script
# CPTs for hidden evidence nodes also added here, which are only related to a single anomaly

from AT.diagnosis.bayesian.noisy_MAX import noisy_MAX
from pgmpy.factors.discrete import TabularCPD
from itertools import product
from AT.diagnosis.bayesian.dictionaries import subgroup_dict, nap_dict

def add_cpds(model, split_probability_dict, hidden_probabilities_dict, anomaly_cardinality):
    for parameter, anomalies in split_probability_dict.items():
        # Generate a list of parent anomalies for the current parameter
        anomaly_list = list(anomalies.keys())
    
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

        # Create CPDs for each parameter (using TabularCPD)
        high_cpd = TabularCPD(
            variable = f'high {parameter}',
            variable_card = len(high_states),
            values = high_values,
            evidence = anomaly_list,
            evidence_card = [anomaly_cardinality] * len(anomaly_list)
        )

        low_cpd = TabularCPD(
            variable = f'low {parameter}',
            variable_card = len(low_states),
            values = low_values,
            evidence = anomaly_list,
            evidence_card = [anomaly_cardinality] * len(anomaly_list)
        )

        model.add_cpds(high_cpd, low_cpd)

    # Add CPDs for the hidden nodes
    for hidden_parameter, anomalies in hidden_probabilities_dict.items():
        for anomaly, data in anomalies.items():
            # Extract activation probabilities for each hidden node conditioned
            # on the associated parent anomaly
            c_i = data['probabilities']['true']['True']
            q_i = round(1 - c_i, 3)

            # NOTE: These can either be defined within the hidden_probabilities_dict or automatically
            # for all hidden nodes as done here; this just removes the need for the 'False' subdictionary
            # Defined as such to prevent deterministic behavior observed when setting the A = 0 probabilities
            # to 1 and 0 for AE = 'False' or 'True', respectively (which follows the Noisy OR format)
            hidden_probs = [[0.9999, q_i],
                            [0.0001, c_i]]

            # Create CPTs for each individual parent child relationship
            hidden_cpd = TabularCPD(
                variable = hidden_parameter,
                variable_card = len(hidden_probs),
                values = hidden_probs,
                evidence = [anomaly],
                evidence_card = [anomaly_cardinality]
            )

            model.add_cpds(hidden_cpd)

    # Add CPDs for subgroups conditioned on the status of their related anomalies
    for subgroup, anomalies in subgroup_dict.items():
        num_anomalies = len(anomalies)

        # Create all possible True/False state combinations for the anomalies for a given subgroup
        anomaly_states = list(product([False, True], repeat = num_anomalies))

        # Create an empty list to store the CPT values for each combination of anomaly states
        cpt_values = []
        for state_combo in anomaly_states:
            # If any anomaly is True, set the probability of the subgroup being True to ~1
            if any(state_combo):
                cpt_values.append([0.0001, 0.9999])
            # If no anomalies are True, set the probability of the subgroup being False to ~1
            else:
                cpt_values.append([0.9999, 0.0001])

        # Reshape the CPT values to align with TabularCPD formatting
        cpt_values = list(zip(*cpt_values))
       
        # Create CPDs for each subgroup
        subgroup_cpd = TabularCPD(
           variable = subgroup,
           variable_card = 2,
           values = cpt_values,
           evidence = anomalies,
           evidence_card = [2] * num_anomalies
       )

        model.add_cpds(subgroup_cpd)

    # Add CPD for the No Anomalies Present node conditoned on the state of each of the subgroups
    for nap, subgroups in nap_dict.items():
        num_groups = len(subgroups)

        # Create all possible True/False combinations of the subgroup states
        group_states = list(product([False, True], repeat = num_groups))

        # Create an empty list to store the CPT for each combination of group states
        cpt_values = []
        for state_combo in group_states:
            # If any of the subgroups is True, set the probability of NAP being False to ~1
            if any(state_combo):
                cpt_values.append([0.9999, 0.0001])
            # If none of the subgroups are True, set the probability of NAP being True to ~1
            else:
                cpt_values.append([0.0001, 0.9999])

        # Reshape the CPT values to align with TabularCPD formatting
        cpt_values = list(zip(*cpt_values))

        # Create the CPD for No Anomalies Present conditioned on the states of the subgroups
        nap_cpd = TabularCPD(
            variable = nap,
            variable_card = 2,
            values = cpt_values,
            evidence = subgroups,
            evidence_card = [2] * num_groups
        )

        model.add_cpds(nap_cpd)

    # Verify that the model is valid after adding the CPDs
    #   - Checks if sum of probabilities for each state is equal to 1 (tol = 0.01)
    #   - Checks if CPDs associated with nodes are consistent with their parents
    if model.check_model():
        print("Model is valid with added CPDs.")
    else:
        print("Model is invalid. Please check the format of the input CPTs.")
    print()    