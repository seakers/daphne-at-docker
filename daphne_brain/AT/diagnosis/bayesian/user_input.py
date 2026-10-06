# user_input.py
# Author: Joshua Elston
# Last Edited: 09/26/2026

# Used to process telemetry signatures and display updated Bayesian network
# beliefs based on provided evidence --> called in ECLSS_Bayesian_Network.py
# Consolidated to only include relevant function

from AT.diagnosis.bayesian.query_network import query_network

def query_parameters(infer, fan_status, telemetry_values, measurement_ranges, split_probability_dict, additional_evidence, hidden_probabilities_dict):
    # Collect parameter values from telemetry, and query the Bayesian network with the updated evidence
    parameter_values = telemetry_values
    print("Parameter values: ", parameter_values)
    if parameter_values: # proceed if parameters detected
        try:
            # Query the Bayesian network
            print("i am here")
            normalized_probabilities, evidence, runtime = query_network(infer, fan_status, parameter_values, measurement_ranges, split_probability_dict, additional_evidence,hidden_probabilities_dict)

            # Sort anomalies based on the probability of their presence
            sorted_anomalies = sorted(normalized_probabilities.items(), key = lambda x: x[1], reverse = True)

            # Print the sorted anomalies with their probabilities of being present
            print()
            print("Anomalies ranked by probability of presence:")
            for anomaly, prob in sorted_anomalies[:5]:
                if anomaly == 'Unknown Anomaly':
                    print(f"P({anomaly}): {prob:.4f}")
                else:
                    print(f"P({anomaly} = 1): {prob:.4f}")
            print()
            print(f"Query runtime: {runtime:.2f}s")
            print()
        
            formatted_probabilities = {key: float(value) for key, value in normalized_probabilities.items()}
            # Return the formatted probabilities to calculate the entropy of the probability distribution
            return formatted_probabilities, evidence, runtime

        except RuntimeError as e:
            print(f"Error during querying: {e}")


def query_additional_evidence(infer, measurement_ranges, split_probability_dict, hidden_probabilities_dict, evidence, best_evidence, additional_evidence):
    # Function takes elements from query_network without the need to remap evidence that should have previous been set and stored there
    while True:
        if additional_evidence: # proceed if additional evidence provided
            mapped_additional = {}
            for key, val in additional_evidence.items():
                mapped_additional[key] = 0 if val in [1, 2] else 1
            evidence.update(mapped_additional) 

            print(f'Mapped evidence: {evidence}')

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
                        print(f"Skipping anomaly (it's a parameter): {anomaly_name}")
                        continue
                    else:
                        print(f"Adding anomaly: {anomaly_name}")
                        unique_anomalies.add(anomaly_name) # add anomalies

            anomalies_to_query = list(unique_anomalies)

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

            formatted_probabilities = {key: float(value) for key, value in normalized_probabilities.items()}
            # print(f'Formatted probabilities: {formatted_probabilities}')

            return formatted_probabilities