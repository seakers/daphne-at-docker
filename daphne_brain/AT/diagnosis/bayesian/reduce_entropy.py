# reduce_entropy.py
# Author: Joshua Elston
# Last Edited: 03/28/2025

# Allows VA to intelligently select pieces of additional evidence to obtain to reduce the entropy in the current
# probabilitiy distribution (to maximize information gain)

import time
import math

# Function queries the Bayesian network for each additional piece of evidence
# at each value that the evidence can take (avoids the print statements present
# in query_network/query_parameters)
def hidden_queries(infer, split_probability_dict, evidence, potential_evidence, evidence_state):

    additional_evidence = {}

    # Create mappings for the additional evidence
    additional_evidence_mapping = {
        'False': 0,
        'True': 1
    }

    additional_evidence[potential_evidence] = additional_evidence_mapping[evidence_state]
    # print(f'Analyzing {additional_evidence}')
    # print('---------------------------------------------------------------------------')

    evidence.update(additional_evidence)
    # print(f'Updated evidence: {evidence}')

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
    try:
        for anomaly in anomalies_to_query:
            result = infer.query(variables = [anomaly], evidence = evidence)
            # print(f"Result: {result}")
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

    # Sort anomalies based on the probability of their presence
    sorted_anomalies = sorted(normalized_probabilities.items(), key = lambda x: x[1], reverse = True)

    # Print the sorted anomalies with their probabilities of being present
    # print()
    # print("Anomalies ranked by probability of presence:")
    # for anomaly, prob in sorted_anomalies[:5]:
    #     if anomaly == 'No Anomalies Present':
    #         print(f"P({anomaly}): {prob:.6f}")
    #     else:
    #         print(f"P({anomaly} = 1): {prob:.6f}")
    # print()

    formatted_probabilities = {key: float(value) for key, value in normalized_probabilities.items()}
    # print(f'Formatted probabilities: {formatted_probabilities}')

    return formatted_probabilities

def calculate_entropy(probabilities):
    entropy_distribution = 0 # initialize the entropy of the probability distribution
    for prob in probabilities:
        # print(f'Probabilities: {prob}')
        if prob == 0:
            print(f"Probability equal to zero.")
        entropy_distribution += -1 * prob * math.log(prob)
        entropy_distribution = round(entropy_distribution, 8) # MAY DELETE LATER, MORE FOR READABILITY

    return entropy_distribution

def select_best_evidence(infer, split_probability_dict, hidden_probabilities_dict, current_evidence, initial_entropy, probabilities):
    # Initialize variables for the reduction in entropy and additional evidence being iterated through
    best_entropy_reduction = float('-inf')
    best_evidence = None

    tic = time.time()

    # Iterate over all hidden nodes
    for potential_evidence, associated_anomaly in hidden_probabilities_dict.items():
        # print(f'Potential Evidence: {potential_evidence}')
        hidden_based_on_tm = infer.query(variables = [potential_evidence], evidence = current_evidence)
        hp_equals_1 = hidden_based_on_tm.values[1]
        # print(f"Pr({potential_evidence} = 1|TM) = {round(hp_equals_1, 8)}")

        # # Extract the name of the anomaly associated with the piece of hidden evidence being added
        # anomaly_name = next(iter(associated_anomaly))
        # # print(f'Anomaly: {anomaly_name}')
        # # Extract the initial probability of each anomaly conditioned on the telemetry feed evidence (used to normalize average entropy)
        # initial_prob = probabilities.get(anomaly_name)
        # initial_prob = round(initial_prob, 8) # reduce decimal places for ease of visualization
        # # print(f"Initial probability for {anomaly_name}: {initial_prob}")

        # Store entropy values for both possible states of the additional evidence
        entropies = []

        evidence = current_evidence.copy()

        # Iterate over both possible states of the additional evidence (AE_n = 0 or AE_n = 1)
        for outcome in ['False', 'True']:
            new_probabilities = hidden_queries(infer, split_probability_dict, evidence, potential_evidence, outcome)

            # print(f"New Probabilities: {new_probabilities}")

            # Compute the entropy of the new probability distribution
            entropy = calculate_entropy(new_probabilities.values())
            entropy = round(entropy, 8) # MAY DELETE LATER, MORE FOR READABILITY
            entropies.append(entropy)

        # Calculate the average entropy of the probabilities distributions based on the
        # addition of the new piece of information (whether it is True or False)
        # print('========================================================================================================================================')
        # print(f'For {potential_evidence}, the updated entropies are: {entropies}')
        # print(f'Computing as: {1 - initial_prob} * {entropies[0]} + {initial_prob} * {entropies[1]}')
        average_entropy = ((1 - hp_equals_1) * entropies[0]) + (hp_equals_1 * entropies[1])
        average_entropy = round(average_entropy, 8) # MAY DELETE LATER, MORE FOR READABILITY
        # print(f'The average entropy when observing the {potential_evidence} is: {average_entropy}')
        delta_h = initial_entropy - average_entropy
        delta_h = round(delta_h, 8) # MAY DELETE LATER, MORE FOR READABILITY
        # print(f'The change in entropy of the probability distribution when collecting {potential_evidence} is: {delta_h}')
        # print('========================================================================================================================================')
        # print()

        # Track the piece of additional evidence the provides the greatest reduction in entropy
        if delta_h > best_entropy_reduction:
            best_entropy_reduction = delta_h
            best_evidence = potential_evidence

    # toc = time.time()
    # evidence_outcome_times = toc - tic
    # print(f'Expanded possible additional evidence states in {round(evidence_outcome_times, 2)}s.')
    # print()

    # # Return the best piece of additional evidence
    # print(f'The best piece of additional evidence to collect is: {best_evidence} with an average reduction in entropy of {best_entropy_reduction}')
    # time.sleep(3)
    # print()
    # crew_prompt = input(f'Can you report the status of {best_evidence}? (yes/no): ')
    # crew_prompt = 'no'
    
    return best_evidence