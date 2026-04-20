# reduced_hidden_probabilities.py
# Author: Joshua Elston
# Last Edited: 03/03/2026

# Reduced dictionary storing the hidden parameters used for parameter learning using Biosim

# UPDATES:
# Updated on 03/03/2026 to match hidden components to (Habitat) anomalies
# NOTE: Probabilities remained the same from (iHab) failures; may want to change in future

import os, json

reduced_hidden_probabilities_dict = {
    "[HIDDEN] BFS Component": {
        "Biological Filter Saturation": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.985,
                    'False': 0.015
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
    "[HIDDEN] CDRA Failure Component": {
        "CDRA Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.9988,
                    'False': 0.0012
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
    "[HIDDEN] Emergency O2 System Maintenance Component": {
        "Emergency O2 System Maintenance (IHab)": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.9762,
                    'False': 0.0238
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
        "Emergency O2 System Maintenance (HALO)": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.9762,
                    'False': 0.0238
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
    "[HIDDEN] Excess CO2 in Cabin Component": {
        "Excess CO2 in Cabin (IHab)": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.973,
                    'False': 0.027
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
        "Excess CO2 in Cabin (HALO)": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.973,
                    'False': 0.027
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
    "[HIDDEN] Loss of Pressure Component": {
        "Loss of Pressure (IHab)": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.998,
                    'False': 0.002
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
        "Loss of Pressure (HALO)": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.998,
                    'False': 0.002
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
}

# Ensure that all of the probabilities added above sum to 1.0
def check_probabilities_sum(probability_dict):
    # Initialize flag
    all_valid = True

    for parameter, anomalies in probability_dict.items():
        for anomaly, data in anomalies.items():
            # Loop over True and False entries
            for presence, states in data['probabilities'].items():
                total_probability = sum(states.values())
            if total_probability != 1.0:
                print(f"Error: Probabilities for hidden parameter '{parameter}' under anomaly '{anomaly}' ({presence}) sum to {total_probability:.2f}, not 1.0.")
                all_valid = False

    if all_valid:
            print("All probabilities for all hidden parameters under all anomalies (both present and absent) sum to 1.0.")
    print()

# Check that the probabilities developed in the above dictionary correctly sum to one for each symptom under each anomaly
check_probabilities_sum(reduced_hidden_probabilities_dict)

current_dir = os.path.dirname(os.path.abspath(__file__))
output_file_path = os.path.join(current_dir, "reduced_hidden_probabilities_dict.json")

# Store hidden probabilities dictionary as a .json file
with open(output_file_path, "w") as file:
    json.dump(reduced_hidden_probabilities_dict, file)