# ECLSS_Bayesian_Network.py
# Author: Joshua Elston
# Last Edited: 08/27/2026

"""
This main script is used to generate a Bayesian network for an ECLSS environment containing anomalies (parent nodes) and parameters (child nodes).
Parameters can take on one of five distinct states, determined by the current value of that parameter, while anomalies are either present (1) or
absent (0). For terminology, any time that a parameter is found to not be in its 'Nominal' state (either above or below bounds), it is said to be 
a symptom. Prior probabilities for the anomalies are paired with conditional probability distributions for the child parameters conditioned on all 
of their parent anomalies. These conditional probability distributions are created using the Noisy MAX method (discussed in Díez and Druzdzel), 
which requires each parameter to be split into two different variables (high_X and low_X) such that the 'Nominal' state is always the minimum value 
for these graded variables. The network then allows users to pass in updated parameter values, which are used to update the network's beliefs about 
the probability of certain anomalies being present. Any parameters for which values are not explicitly entered by the user are assumed to be in 
their 'Nominal' state.
If parameter learning is being used to create the network CPDs, some of the scripts within the 'bayesian/HERA' folder are not used. Other scripts must
be run prior to executing the main script and are thus not directly called here. These include:
- reduced_hidden_probabilities.py
- reduced_probabilities.py
"""

import os

# Clear the terminal screen each time the script is run
# def clear_terminal():
#     os.system('cls' if os.name == 'nt' else 'clear')
# clear_terminal()

# import time
# Time script run time
# start_time = time.time()

import json
import pickle

from pgmpy.models import BayesianNetwork
# from pgmpy.factors.discrete import TabularCPD <-- NOTE: with parameter learning, model built in learn_probabilities.py
# (or more efficiently in 'learn_probabilities_threaded.py')
# NOTE: using VariableElimination instead of BeliefPropagation (can update if found that this is needed)
from pgmpy.inference import VariableElimination

# Record run results for current timestep
from AT.diagnosis.bayesian.Gateway.run_logger import log_run

# Import dictionaries from other files
# ----- GATEWAY NETWORK (PARAMETER LEARNING) -----
from AT.diagnosis.bayesian.Gateway.reduced_network_structure import reduced_network
from AT.diagnosis.bayesian.Gateway.reduced_ranges import measurement_ranges
from AT.diagnosis.bayesian.user_input import query_parameters, query_additional_evidence
from AT.diagnosis.bayesian.reduce_entropy import calculate_entropy, select_best_evidence

current_dir = os.path.dirname(os.path.abspath(__file__))
# NOTE: Make sure to run both files to ensure that probabilities are updated
split_probability_dict = os.path.join(current_dir, "reduced_split_probabilities_dict.json")
hidden_probabilities_dict = os.path.join(current_dir, "reduced_hidden_probabilities_dict.json")

def load_initial_model(fan_status, telemetry_values, additional_evidence):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    split_probability_dict = os.path.join(current_dir, "reduced_split_probabilities_dict.json")
    hidden_probabilities_dict = os.path.join(current_dir, "reduced_hidden_probabilities_dict.json")
    with open(split_probability_dict, "r") as file:
        split_probability_dict = json.load(file)
    with open(hidden_probabilities_dict, "r") as file:
        hidden_probabilities_dict = json.load(file)

    # Renamed model to differentiate from other experimental runs
    model = pickle.load(open(os.path.join(current_dir, "parameter_learning", "model", "final_learned_model.pkl"),'rb'))

    # To perform inference on the Bayesian Network, the Variable Elimination algorithm is used.
    # For more information on VariableElimination within the pgmpy library, refer here:
    # https://pgmpy.org/exact_infer/ve.html 
    infer = VariableElimination(model)

    # NOTE: Fan Status is currently a manually-set piece of evidence; this should be updated to be read in from biosim in evidence
    # (with any non-zero values denotes as fan_status=1)
    fan_status = False

    # Add user-provided evidence to the Bayesian network and update the beliefs about the presence of anomalies
    # print(query_parameters(infer, telemetry_values, measurement_ranges, split_probability_dict))
    probabilities, evidence = query_parameters(infer, fan_status, telemetry_values, measurement_ranges, split_probability_dict, additional_evidence, hidden_probabilities_dict)

    return infer, probabilities, evidence, split_probability_dict, hidden_probabilities_dict

def get_probabilities(telemetry_values, fan_status=None, additional_evidence=None, calculate_best_evidence=True, should_log=True):

    infer, probabilities, evidence, split_probability_dict, hidden_probabilities_dict = load_initial_model(fan_status, telemetry_values, additional_evidence)

    initial_entropy = None
    best_evidence = None

    # Only calculate best evidence if requested
    if calculate_best_evidence and probabilities:
        initial_probabilities = list(probabilities.values())
        initial_entropy = calculate_entropy(initial_probabilities)
        print(f'Initial entropy: {initial_entropy}')
        print()
        best_evidence = select_best_evidence(infer, measurement_ranges, split_probability_dict, hidden_probabilities_dict, evidence, initial_entropy, probabilities)
    
    hidden_components = load_hidden_components()

    # NOTE: UPDATE THE SCENARIO ID AND TRUE ANOMALY FIELDS WHEN STORING RUN RESULTS
    # Store run results for just telemetry feed values (without additional evidence)
    record = None
    if should_log:
        record = log_run(
            scenario_id='oga_ihab.biosim',
            true_anomaly='OGA Failure',
            probabilities=probabilities,
            initial_entropy=initial_entropy,
            best_evidence=best_evidence,
            telemetry_snapshot=telemetry_values
        )
        print(json.dumps(record, indent=2))

    return probabilities, best_evidence, hidden_components

def update_probabilities_additional(telemetry_values, additional_evidence, fan_status=None, calculate_best_evidence=True):
    # Read .json files with probability dictionary (such that these do not need to computed each time the script is ran)
    infer, probabilities, evidence, split_probability_dict, hidden_probabilities_dict = load_initial_model(fan_status, telemetry_values, additional_evidence)

    if probabilities:
        # Calculate the initial entropy of the probability distribution based on only readings from the telemetry feed
        initial_probabilities = list(probabilities.values())
        initial_entropy = calculate_entropy(initial_probabilities)
        print(f'Initial entropy: {initial_entropy}')
        print()

        # Determine which piece of additional evidence the crew member(s) could collect to
        # cause the greatest reduction in the entropy of the probability distribution
        # (corresponding to the largest information gain)
        best_evidence = select_best_evidence(infer, measurement_ranges, split_probability_dict, hidden_probabilities_dict, evidence, initial_entropy, probabilities)

        updated_probabilities = query_additional_evidence(infer, measurement_ranges, split_probability_dict, hidden_probabilities_dict, evidence, best_evidence, additional_evidence)
        updated_probabilities = list(updated_probabilities.values())
        final_entropy = calculate_entropy(updated_probabilities)
        print(f'Final entropy: {final_entropy}')
        
    else:
        print('No evidence entered. Exiting script.')
        best_evidence = None
    
    hidden_components = load_hidden_components()

    return probabilities, best_evidence, hidden_components


def load_hidden_components():
    """
    Load hidden component names from the hidden_probabilities_dict.json file
    
    Returns:
        list: A list of all hidden component names
    """
    try:
        # Get the file path relative to the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, 'hidden_probabilities_dict.json')
        
        # Open and load the JSON file
        with open(file_path, 'r') as file:
            hidden_probabilities = json.load(file)
        
        # Extract all top-level keys (hidden component names)
        hidden_components = list(hidden_probabilities.keys())
        
        return hidden_components
    except Exception as e:
        print(f"Error loading hidden components: {e}")
        return []

# Extract the hidden component names
HIDDEN_COMPONENTS = load_hidden_components()

# Print or use the components as needed
print("Hidden Components:")
for component in HIDDEN_COMPONENTS:
    print(f" - {component}")

test_model = BayesianNetwork(reduced_network)
print("Number of nodes:", test_model.number_of_nodes())
print("Number of edges:", test_model.number_of_edges())