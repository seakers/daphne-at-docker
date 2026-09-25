# ECLSS_Bayesian_Network.py
# Author: Joshua Elston
# Last Edited: 09/24/2026

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
"""

import os

# Clear the terminal screen each time the script is run
# def clear_terminal():
#     os.system('cls' if os.name == 'nt' else 'clear')
# clear_terminal()

import json

from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
# NOTE: using VariableElimination instead of BeliefPropagation (can update if found that this is needed)
from pgmpy.inference import VariableElimination

import importlib
# Set the network type being used ('default', 'expanded', or 'reduced')
# Expanded - 46 anomalies
# Default - 36 anomalies
# Reduced - 23 anomalies
NETWORK_TYPE = os.getenv('NETWORK_TYPE', 'reduced')

# Map each network to its filepath
network_path = {
    'default': {
        'filepath': 'AT.diagnosis.bayesian.networks.default',
        'network': 'network_structure',
        'prior_probabilities': 'prior_probabilities',
        'add_cpds': 'add_cpds',
    },
    'expanded': {
        'filepath': 'AT.diagnosis.bayesian.networks.expanded',
        'network': 'ex_network_structure',
        'prior_probabilities': 'ex_prior_probabilities',
        'add_cpds': 'ex_add_cpds'
    },
    'reduced': {
        'filepath': 'AT.diagnosis.bayesian.networks.reduced',
        'network': 're_network_structure',
        'prior_probabilities': 're_prior_probabilities',
        'add_cpds': 're_add_cpds',
    },
}

# Map .json files for each network
network_json = {
    'default': {
        'folder': 'networks/default',
        'split_probability_dict': 'split_probability_dict.json',
        'hidden_probabilities_dict': 'hidden_probabilities_dict.json',
    },
    'expanded': {
        'folder': 'networks/expanded',
        'split_probability_dict': 'ex_split_probability_dict.json',
        'hidden_probabilities_dict': 'ex_hidden_probabilities_dict.json',
    },
    'reduced': {
        'folder': 'networks/reduced',
        'split_probability_dict': 're_split_probability_dict.json',
        'hidden_probabilities_dict': 're_hidden_probabilities_dict.json',
    },    
}

# Import correct filepaths
folder = network_path[NETWORK_TYPE]
files = folder['filepath']

# Import dictionaries from other files
network = importlib.import_module(f"{files}.{folder['network']}").network
prior_probabilities = importlib.import_module(f"{files}.{folder['prior_probabilities']}").prior_probabilities
add_cpds = importlib.import_module(f"{files}.{folder['add_cpds']}").add_cpds

# Load .json files from correct network folder
def load_network_json(current_dir: str, file_key: str) -> dict:
    folder = network_json[NETWORK_TYPE]
    file = os.path.join(current_dir, folder['folder'], folder[file_key])
    
    with open(file, "r") as f:
        return json.load(f)

from AT.diagnosis.bayesian.ranges import measurement_ranges
from AT.diagnosis.bayesian.user_input import query_parameters #, query_additional_evidence
from AT.diagnosis.bayesian.reduce_entropy import calculate_entropy, select_best_evidence
from AT.diagnosis.bayesian.run_logger import log_run, _hits_at_k

# Module-level flags (persist across calls within same script instance)
_initial_inference_done = False
_stored_initial_entropy = None
_stored_initial_runtime = None
_stored_initial_top_anomaly = None
_stored_initial_best_evidence = None
_stored_initial_best_evidence_rt = None
_stored_initial_hits1 = None
_stored_initial_hits3 = None

def get_probabilities(telemetry_values, additional_evidence=None,
                      calculate_best_evidence=True, should_log=True):
    # Define the anomaly scenario being injected
    # NOTE: Make sure this aligns with the scenario in simulation.py
    anomaly_name = 'Biological Filter Saturation'

    global _initial_inference_done, _stored_initial_entropy, _stored_initial_runtime, \
           _stored_initial_top_anomaly, _stored_initial_best_evidence, \
           _stored_initial_best_evidence_rt, _stored_initial_hits1, _stored_initial_hits3
    # Derive is_followup from internal state
    is_followup = _initial_inference_done

    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Import relevant probability dicionaries
    split_probability_dict = load_network_json(current_dir, 'split_probability_dict')
    hidden_probabilities_dict = load_network_json(current_dir, 'hidden_probabilities_dict')

    # Create the Bayesian Network
    model = BayesianNetwork(network)

    # NOTE: Given that the anomalies are no longer the top layer in the network, they
    # do not have prior probabilities defined given their subgroup parents
    prior_cpds_dict = {}
    # Define the cardinality of each anomaly as 2, where 0 represents the anomaly
    # not being present (False) and 1 represents the anomaly being present (True)
    anomaly_cardinality = 2

    # From the prior probabilities, add CPDs for the anomalies
    for anomaly, prior_probability in prior_probabilities.items():
        model.add_cpds(TabularCPD(
                                variable = anomaly, 
                                variable_card = anomaly_cardinality, 
                                values = [[1 - prior_probability], [prior_probability]] # ordered as [False, True]
                                ))
        prior_cpds_dict[anomaly] = {'False': 1 - prior_probability, 'True': prior_probability}

    # Add the CPDs for the parameters conditioned on multiple anomalies
    add_cpds(model, split_probability_dict, hidden_probabilities_dict, anomaly_cardinality)

    infer = VariableElimination(model)
    probabilities, evidence, inference_runtime = query_parameters(infer, telemetry_values, measurement_ranges, split_probability_dict, additional_evidence, hidden_probabilities_dict)

    initial_entropy = None
    best_evidence = None
    best_evidence_runtime = None
    post_evidence_entropy = None

    if probabilities:
        ranked = sorted(probabilities.keys(), key=lambda k: probabilities[k], reverse=True)
        current_top_anomaly = ranked[0] if ranked else None        
        current_hits1 = _hits_at_k(probabilities, anomaly_name, k=1)
        current_hits3 = _hits_at_k(probabilities, anomaly_name, k=3)

        entropy = calculate_entropy(list(probabilities.values()))
        # Assign entropy to correct variable depending on which call it is
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

        # After the first successful inference, flip followup flag
        if not _initial_inference_done and probabilities:
            _initial_inference_done = True
            _stored_initial_runtime = inference_runtime

        if calculate_best_evidence:
            best_evidence, best_evidence_runtime = select_best_evidence(infer, measurement_ranges, split_probability_dict, hidden_probabilities_dict, evidence, entropy, probabilities)
            # Store initial best evidence values on first call
            if not is_followup:
                _stored_initial_best_evidence = best_evidence
                _stored_initial_best_evidence_rt = best_evidence_runtime

    else:
        print('No evidence entered. Exiting script.')
        best_evidence = None

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


def load_hidden_components():
    """
    Load hidden component names from the hidden_probabilities_dict.json file
    
    Returns:
        list: A list of all hidden component names
    """
    try:
        # Get the file path relative to the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        hidden_probabilities = load_network_json(script_dir, 'hidden_probabilities_dict')
        
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

test_model = BayesianNetwork(network)
print("Number of nodes:", test_model.number_of_nodes())
print("Number of edges:", test_model.number_of_edges())