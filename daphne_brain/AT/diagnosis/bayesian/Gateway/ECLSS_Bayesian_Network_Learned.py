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

import json
import pickle

# from pgmpy.models import BayesianNetwork
# from pgmpy.factors.discrete import TabularCPD <-- NOTE: with parameter learning, model built in learn_probabilities.py
# (or more efficiently in 'learn_probabilities_threaded.py')
# NOTE: using VariableElimination instead of BeliefPropagation (can update if found that this is needed)
from pgmpy.inference import VariableElimination

# Set which Gateway network variant is being used ('default' or 'updated')
NETWORK_TYPE = os.getenv('NETWORK_TYPE', 'default')

# Map each network variant to its Gateway networks folder, pickled model,
# and probability dictionaries.
network_config = {
    'default': {
        'folder': os.path.join('networks', 'default'),
        'model_pickle': os.path.join('default_learned_model.pkl'),
        'split_probability_dict': 'split_probabilities_dict.json',
        'hidden_probabilities_dict': 'hidden_probabilities_dict.json',
    },
    'updated': {
        'folder': os.path.join('networks', 'updated'),
        'model_pickle': os.path.join('updated_learned_model.pkl'),
        'split_probability_dict': 'updated_split_probabilities_dict.json',
        'hidden_probabilities_dict': 'updated_hidden_probabilities_dict.json',
    },
}

folder = network_config[NETWORK_TYPE]

# Load .json files from the correct Gateway network folder
def load_network_json(current_dir: str, file_key: str) -> dict:
    file = os.path.join(current_dir, folder['folder'], folder[file_key])
    with open(file, "r") as f:
        return json.load(f)

# Load the pickled, parameter-learned model from the correct Gateway network folder
def load_model(current_dir: str):
    model_path = os.path.join(current_dir, folder['folder'], folder['model_pickle'])
    with open(model_path, 'rb') as f:
        return pickle.load(f)

# Import dictionaries from other files
from AT.diagnosis.bayesian.Gateway.ranges import measurement_ranges
from AT.diagnosis.bayesian.user_input import query_parameters, query_additional_evidence
from AT.diagnosis.bayesian.reduce_entropy import calculate_entropy, select_best_evidence
# Record run results for current timestep
from AT.diagnosis.bayesian.Gateway.run_logger import log_run, _hits_at_k

# Module-level flags (persist across calls within same script instance)
_initial_inference_done = False
_stored_initial_entropy = None
_stored_initial_runtime = None
_stored_initial_top_anomaly = None
_stored_initial_best_evidence = None
_stored_initial_best_evidence_rt = None
_stored_initial_hits1 = None
_stored_initial_hits3 = None

def _build_inference_engine(current_dir):
    """Unpickle the current NETWORK_TYPE's learned model and return a VariableElimination engine."""
    model = load_model(current_dir)
    return VariableElimination(model)


def get_probabilities(telemetry_values, fan_status=None, additional_evidence=None,
                      calculate_best_evidence=True, should_log=True):

    # Define the anomaly scenario being injected, along with the fan status
    # NOTE: Make sure anomaly aligns with the scenario in simulation.py
    #       Additionally, Fan Status is currently a manually-set piece of evidence;
    #       this should be updated to be read in from BioSim in evidence
    #       (with any non-zero values denotes as fan_status=1)
    anomaly_name = 'O2 Delivery System Malfunction (HALO)'
    fan_status = False

    global _initial_inference_done, _stored_initial_entropy, _stored_initial_runtime, \
           _stored_initial_top_anomaly, _stored_initial_best_evidence, \
           _stored_initial_best_evidence_rt, _stored_initial_hits1, _stored_initial_hits3
    # is_followup = _initial_inference_done
    is_followup = bool(additional_evidence)
    print(f"get_probabilities called | followup={is_followup} | additional_evidence={additional_evidence} | should_log={should_log}")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    # NOTE: Make sure to run both files to ensure that probabilities are
    # updated for whichever NETWORK_TYPE the script is running
    split_probability_dict = load_network_json(current_dir, 'split_probability_dict')
    hidden_probabilities_dict = load_network_json(current_dir, 'hidden_probabilities_dict')

    infer = _build_inference_engine(current_dir)

    probabilities, evidence, inference_runtime = query_parameters(
        infer, fan_status, telemetry_values, measurement_ranges,
        split_probability_dict, additional_evidence, hidden_probabilities_dict
    )

    initial_entropy = None
    best_evidence = None
    best_evidence_runtime = None
    post_evidence_entropy = None
    updated_inference_runtime = None
    current_top_anomaly = None
    current_hits1 = None
    current_hits3 = None

    if probabilities:
        ranked = sorted(probabilities.keys(), key=lambda k: probabilities[k], reverse=True)
        current_top_anomaly = ranked[0] if ranked else None
        current_hits1 = _hits_at_k(probabilities, anomaly_name, k=1)
        current_hits3 = _hits_at_k(probabilities, anomaly_name, k=3)
 
        entropy = calculate_entropy(list(probabilities.values()))
        if is_followup:
            post_evidence_entropy = entropy
            updated_inference_runtime = inference_runtime
            initial_entropy = _stored_initial_entropy
            print(f'Updated entropy: {post_evidence_entropy}\n')
        else:
            initial_entropy = entropy
            _stored_initial_entropy = entropy
            print(f'Initial entropy: {initial_entropy}\n')
            _stored_initial_runtime = inference_runtime
            _stored_initial_top_anomaly = current_top_anomaly
            _stored_initial_hits1 = current_hits1
            _stored_initial_hits3 = current_hits3
 
        # if not _initial_inference_done:
        #     _initial_inference_done = True
        #     _stored_initial_runtime = inference_runtime
 
        if calculate_best_evidence:
            best_evidence, best_evidence_runtime = select_best_evidence(
                infer, measurement_ranges, split_probability_dict,
                hidden_probabilities_dict, evidence, entropy, probabilities
            )
            if not is_followup:
                _stored_initial_best_evidence = best_evidence
                _stored_initial_best_evidence_rt = best_evidence_runtime
    else:
        print('No evidence entered. Exiting script.')
 
    record = None
    results_filename = f'{NETWORK_TYPE}_results.jsonl'
 
    if should_log:
        record = log_run(
            scenario_id=anomaly_name,
            true_anomaly=anomaly_name,
            probabilities=probabilities,
            initial_entropy=initial_entropy,
            updated_entropy=post_evidence_entropy,
            initial_top_anomaly=_stored_initial_top_anomaly,
            updated_top_anomaly=current_top_anomaly if is_followup else None,
            initial_best_evidence=_stored_initial_best_evidence,
            updated_best_evidence=best_evidence if is_followup else None,
            initial_best_evidence_runtime=_stored_initial_best_evidence_rt,
            updated_best_evidence_runtime=best_evidence_runtime if is_followup else None,
            initial_hits1=_stored_initial_hits1,
            initial_hits3=_stored_initial_hits3,
            updated_hits1=current_hits1 if is_followup else None,
            updated_hits3=current_hits3 if is_followup else None,
            initial_inference_runtime=_stored_initial_runtime,
            updated_inference_runtime=updated_inference_runtime if is_followup else None,
            telemetry_snapshot=telemetry_values,
            is_followup=is_followup,
            filename=results_filename
        )
        print(json.dumps(record, indent=2))
 
    hidden_components = load_hidden_components()
 
    return probabilities, best_evidence, hidden_components


def update_probabilities_additional(telemetry_values, additional_evidence, fan_status=None, calculate_best_evidence=True):
    # NOTE: Fan Status is currently a manually-set piece of evidence; this should be updated to be
    # read in from BioSim in evidence (with any non-zero value denoted as fan_status=1)
    fan_status = True

    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Read .json probability dictionaries for the current NETWORK_TYPE
    split_probability_dict = load_network_json(current_dir, 'split_probability_dict')
    hidden_probabilities_dict = load_network_json(current_dir, 'hidden_probabilities_dict')

    infer = _build_inference_engine(current_dir)

    probabilities, evidence, inference_runtime = query_parameters(
        infer, fan_status, telemetry_values, measurement_ranges,
        split_probability_dict, additional_evidence, hidden_probabilities_dict
    )    

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
        script_dir = os.path.dirname(os.path.abspath(__file__))
        hidden_probabilities = load_network_json(script_dir, 'hidden_probabilities_dict')
        return list(hidden_probabilities.keys())
    except Exception as e:
        print(f"Error loading hidden components: {e}")
        return []

# Extract the hidden component names
HIDDEN_COMPONENTS = load_hidden_components()

# Print or use the components as needed
print("Hidden Components:")
for component in HIDDEN_COMPONENTS:
    print(f" - {component}")

test_model = load_model(os.path.dirname(os.path.abspath(__file__)))
print("Number of nodes:", test_model.number_of_nodes())
print("Number of edges:", test_model.number_of_edges())