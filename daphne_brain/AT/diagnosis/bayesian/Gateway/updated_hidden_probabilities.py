# updated_hidden_probabilities.py
# Author: Joshua Elston
# Last Edited: 09/20/2026

# Reduced dictionary storing the hidden parameters used for parameter learning using Biosim
# New file created when testing the inclusion of 'learned' anomalies

import os, json

reduced_hidden_probabilities_dict = {
    "[HIDDEN] OGA Status Panel Indicator": {
        "OGA Failure": {
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
    "[HIDDEN] VCCR Particulate Filter": {
        "VCCR Particulate Filter Saturation": {
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
    # Split into two hidden nodes on 08/27/26
    "[HIDDEN] Cabin O2 Valve Position Indicator (IHab)": {
        "O2 Delivery System Malfunction (IHab)": {
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
    "[HIDDEN] Cabin O2 Valve Position Indicator (HALO)": {
        "O2 Delivery System Malfunction (HALO)": {
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
    "[HIDDEN] VCCR Sorbent Bed": {
        "VCCR Sorbent Bed Saturation": {
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
    "[HIDDEN] Module Pressure Leak (IHab)": {
        "Module Decompression (IHab)": {
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
    "[HIDDEN] Module Pressure Leak (HALO)": {
        "Module Decompression (HALO)": {
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
    # NOTE: NEW
    "[HIDDEN] O2 Tank Valve Status": {
        "O2 Tank Leak": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.9662,
                    'False': 0.0338
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.09,
                    'False': 0.91
                },
            },
        },
    },
    "[HIDDEN] Atmosphere Revitalization Fault Isolation": {
        "Unknown Anomaly": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.99,
                    'False': 0.01
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
    "[HIDDEN] Atmosphere Control and Supply Fault Isolation": {
        "Unknown Anomaly": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.979,
                    'False': 0.021
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