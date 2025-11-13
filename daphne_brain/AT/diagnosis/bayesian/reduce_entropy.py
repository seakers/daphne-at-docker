# reduce_entropy.py
# Author: Joshua Elston
# Last Edited: 10/29/2025

# Allows VA to intelligently select pieces of additional evidence to obtain to reduce the entropy in the current
# probabilitiy distribution (to maximize information gain)
# Changes on 10/29/2025 remove parameters from list of query variables (i.e., purely retaining them as evidence)

import time
import math

# Function queries the Bayesian network for each additional piece of evidence
# at each value that the evidence can take (avoids the print statements present
# in query_network/query_parameters)
def hidden_queries(infer, measurement_ranges, split_probability_dict, evidence, potential_evidence, evidence_state):

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

    # NEW CODE ON 10/29/2025
    # Create a set of all parameter variable names to ensure correct parameters are removed as variables prior to inference
    all_parameters = set()
    for param in measurement_ranges.keys():
        all_parameters.add(f"high {param}")
        all_parameters.add(f"low {param}")

    unique_anomalies = set() # using a set handles duplicate anomalies

    for _, anomaly_dict in split_probability_dict.items():
        for anomaly_name in anomaly_dict.keys():
            # Skip anomalies that are themselves parameters in the network
            if anomaly_name in all_parameters:
                continue
            else:
                unique_anomalies.add(anomaly_name) # add anomalies

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
        entropy_distribution = round(entropy_distribution, 8) # MAY DELETE ROUNDING LATER, MORE FOR READABILITY

    return entropy_distribution

def select_best_evidence(infer, measurement_ranges, split_probability_dict, hidden_probabilities_dict, current_evidence, initial_entropy, probabilities, top_n_anomalies=5):
    # Initialize variables for the reduction in entropy and additional evidence being iterated through
    best_entropy_reduction = float('-inf')
    best_evidence = None

    tic = time.time()
    
    # Get top N most probable anomalies
    top_anomalies = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)[:top_n_anomalies]
    top_anomaly_names = set([name for name, _ in top_anomalies])
    
    print(f"Top {top_n_anomalies} anomalies: {[f'{name} ({prob:.4f})' for name, prob in top_anomalies]}")
    
    # Filter hidden components to only those related to top anomalies
    relevant_hidden_components = []
    for component, related_info in hidden_probabilities_dict.items():
        # Skip if already in evidence
        if component in current_evidence:
            continue
            
        # Get the list of related anomalies for this hidden component
        if isinstance(related_info, dict):
            related_anomalies = set(related_info.keys())
        else:
            # If it's not a dict, assume it's a single anomaly or list
            related_anomalies = {related_info} if isinstance(related_info, str) else set(related_info)
        
        # Check if any of the related anomalies are in the top N
        if related_anomalies.intersection(top_anomaly_names):
            relevant_hidden_components.append(component)
    
    print(f"Filtered to {len(relevant_hidden_components)} hidden components (from {len(hidden_probabilities_dict)} total)")
    print(f"Relevant components: {relevant_hidden_components}")
    
    if not relevant_hidden_components:
        print("No relevant hidden components found for top anomalies")
        return None

    evaluated_count = 0
    # Iterate over relevant hidden components only
    for potential_evidence in relevant_hidden_components:
        evaluated_count += 1
        
        hidden_based_on_tm = infer.query(variables = [potential_evidence], evidence = current_evidence)
        hp_equals_1 = hidden_based_on_tm.values[1]
      
        entropies = []
        evidence = current_evidence.copy()

        for outcome in ['False', 'True']:
            new_probabilities = hidden_queries(infer, measurement_ranges, split_probability_dict, evidence, potential_evidence, outcome)
            entropy = calculate_entropy(new_probabilities.values())
            entropy = round(entropy, 8)
            entropies.append(entropy)

        average_entropy = ((1 - hp_equals_1) * entropies[0]) + (hp_equals_1 * entropies[1])
        average_entropy = round(average_entropy, 8)
        delta_h = initial_entropy - average_entropy
        delta_h = round(delta_h, 8)

        if delta_h > best_entropy_reduction:
            best_entropy_reduction = delta_h
            best_evidence = potential_evidence
            print(f"  New best: {best_evidence} (ΔH = {delta_h:.6f})")
    
    elapsed = time.time() - tic
    print(f"Best evidence selection completed in {elapsed:.2f}s (evaluated {evaluated_count} components)")
    print(f"Selected best evidence: {best_evidence} with entropy reduction: {best_entropy_reduction:.6f}")

    return best_evidence