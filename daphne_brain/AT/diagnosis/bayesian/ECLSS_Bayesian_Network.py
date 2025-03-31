# ECLSS_Bayesian_Network.py
# Author: Joshua Elston
# Last Edited: 03/28/2025

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
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
clear_terminal()

import time
# Time script run time
start_time = time.time()

import json

from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
# NOTE: using VariableElimination instead of BeliefPropagation (can update if found that this is needed)
from pgmpy.inference import VariableElimination

# Import dictionaries from other files
from network_struture import network
from prior_probabilities import prior_probabilities
from ranges import measurement_ranges
# from probabilities import split_probability_dict # NOTE: Imported as a .json --> make sure probabilities are updated
# from hidden_probabilities import hidden_probabilities_dict # NOTE: Imported as a .json --> make sure probabilities are updated
from add_cpds import add_cpds
# from plot_bayesian_network import plot_bayesian_network # NOTE: This currently does not include hidden nodes
from user_input import query_parameters, query_additional_evidence
from reduce_entropy import calculate_entropy, select_best_evidence

# Read .json files with probability dictionary (such that these do not need to computed each time the script is ran)
with open("split_probability_dict.json", "r") as file:
    split_probability_dict = json.load(file)
with open("hidden_probabilities_dict.json", "r") as file:
    hidden_probabilities_dict = json.load(file)

# Define the cardinality of each measurement as 5, representing the 5 possible states that a parameter measurement can be within:
thresholds = [
    'Exceeds_UpperWarningLimit',
    'Exceeds_UpperCautionLimit',
    'Nominal',
    'Exceeds_LowerCautionLimit',
    'Exceeds_LowerWarningLimit'
]
measurement_cardinality = len(thresholds)

# Define the cardinality of each anomaly as 2, where 0 represents the anomaly not being present (False) and 1 represents the anomaly being present (True)
anomaly_cardinality = 2

# Create the Bayesian Network
model = BayesianNetwork(network)

# NOTE: Given that the anomalies are no longer the top layer in the network, they
# do not have prior probabilities defined given their subgroup parents

prior_cpds_dict = {}

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

# Verify that the CPDs have been added correctly
for cpd in model.get_cpds():
    print(f'CPD for {cpd.variable}:')
    print(cpd)
    print()

# If desired, plot the Bayesian network with CPDs displayed next to the nodes
# plot_bayesian_network(model)

# Create an inference to the model
infer = VariableElimination(model)

# Add user-provided evidence to the Bayesian network and update the beliefs about the presence of anomalies
probabilities, evidence = query_parameters(infer, measurement_ranges, split_probability_dict)
# print(f'Probabilities: {probabilities.values()}')
# print(f'Evidence: {evidence}')

# Execute the remainder of the code if evidence is entered by the user
if probabilities:
    # Calculate the initial entropy of the probability distribution based on only readings from the telemetry feed
    initial_probabilities = list(probabilities.values())
    initial_entropy = calculate_entropy(initial_probabilities)
    print(f'Initial entropy: {initial_entropy}')
    print()

    # Determine which piece of additional evidence the crew member(s) could collect to
    # cause the greatest reduction in the entropy of the probability distribution
    # (corresponding to the largest information gain)
    best_evidence, crew_prompt = select_best_evidence(infer, split_probability_dict, hidden_probabilities_dict, evidence, initial_entropy, probabilities)

    # Prompt the crew to collect the additional piece of evidence
    if crew_prompt == 'yes':
        updated_probabilities = query_additional_evidence(infer, split_probability_dict, hidden_probabilities_dict, evidence, best_evidence)
        updated_probabilities = list(updated_probabilities.values())
        final_entropy = calculate_entropy(updated_probabilities)
        print(f'Final entropy: {final_entropy}')
    else:
        print('Understood. Pausing evidence collection.')
else:
    print('No evidence entered. Exiting script.')

# Stop script run timing
end_time = time.time()
run_time = end_time - start_time
print()
print(f"Script runtime: {run_time:.2f}s")
print()