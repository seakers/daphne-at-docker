# hidden_probabilities.py
# Author: Joshua Elston
# Last Edited: 03/02/2025

# Stores probabilities of hidden nodes being in different qualititative states (translated to True or False),
# conditioned on the presence (or absence) of their specific parent anomaly. The hidden nodes serve as
# additional evidence to reduce the uncertainty in an initial diagnosis.
# Mathematically, these probabilities are: Pr(AE=ae|A)

import json

hidden_probabilities_dict = {
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
    "[HIDDEN] CDRA LiOH Canister Saturation Component": {
        "CDRA LiOH Canister Saturation": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.9755,
                    'False': 0.0245
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
    "[HIDDEN] Electrolysis System Failure Component": {
        "Electrolysis System Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.982,
                    'False': 0.018
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
    "[HIDDEN] Emergency O2 System Maintenance Component": {
        "Emergency O2 System Maintenance": {
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
        "Excess CO2 in Cabin": {
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
    "[HIDDEN] Excess Gas Leak Component": {
        "Excess Gas Leak": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.9886,
                    'False': 0.0114
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
    "[HIDDEN] Excess Water Vapor Pressure in Cabin Component": {
        "Excess Water Vapor Pressure in Cabin": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.986,
                    'False': 0.014
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
    "[HIDDEN] Fuel Cell #1 and PDU Failure Component": {
        "Fuel Cell #1 and PDU Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.991,
                    'False': 0.009
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
    "[HIDDEN] Fuel Cell #2 and PDU Failure Component": {
        "Fuel Cell #2 and PDU Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.9818,
                    'False': 0.0182
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
    "[HIDDEN] Fuel Cell Degrade Component": {
        "Fuel Cell Degrade": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.972,
                    'False': 0.028
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
    "[HIDDEN] Fuel Cell Failure Component": {
        "Fuel Cell Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.982,
                    'False': 0.018
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
    "[HIDDEN] Loss of Pressure Component": {
        "Loss of Pressure": {
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
    "[HIDDEN] Main Cabin Fan Failure Component": {
        "Main Cabin Fan Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.961,
                    'False': 0.039
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
    "[HIDDEN] MOXIE Antenna Failure Component": {
        "MOXIE Antenna Failure": {
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
    "[HIDDEN] MOXIE ECM Failure Component": {
        "MOXIE ECM Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.988,
                    'False': 0.012
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
    "[HIDDEN] MOXIE Fan Failure Component": {
        "MOXIE Fan Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.9752,
                    'False': 0.0248
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
    "[HIDDEN] N2 Tank Burst Component": {
        "N2 Tank Burst": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.986,
                    'False': 0.014
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
    "[HIDDEN] PDU 4 Failure Component": {
        "PDU 4 Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.9681,
                    'False': 0.0319
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
    "[HIDDEN] PDU 5 Failure Component": {
        "PDU 5 Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.965,
                    'False': 0.035
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
    "[HIDDEN] Reduced Main Cabin Fan #1 Capacity Component": {
        "Reduced Main Cabin Fan #1 Capacity": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.982,
                    'False': 0.018
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
    "[HIDDEN] RWGSR Malfunction Component": {
        "RWGSR Malfunction": {
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
    "[HIDDEN] SPE System Maintenance Component": {
        "SPE System Maintenance": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.994,
                    'False': 0.006
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
    "[HIDDEN] TCCS Auxiliary Fan #1 Failure Component": {
        "TCCS Auxiliary Fan #1 Failure": {
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
    "[HIDDEN] TCCS Auxiliary Fan #2 Failure Component": {
        "TCCS Auxiliary Fan #2 Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.977,
                    'False': 0.023
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
    "[HIDDEN] TCCS Auxiliary Fan at Reduced Capacity Component": {
        "TCCS Auxiliary Fan at Reduced Capacity": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.981,
                    'False': 0.019
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
    "[HIDDEN] TCCS Filter Clog Component": {
        "TCCS Filter Clog": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.9742,
                    'False': 0.0258
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
    "[HIDDEN] Trace Contaminants Component": {
        "Trace Contaminants": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.9767,
                    'False': 0.0233
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
    "[HIDDEN] WPA Pump Flow Rate": {
        "WRS Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.97,
                    'False': 0.03
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
    "[HIDDEN] Multifiltration Bed Saturation": {
        "WRS Maintenance": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.972,
                    'False': 0.028
                },
                False: { # probabilities when the anomaly is absent
                    'True': 0.08,
                    'False': 0.92
                },
            },
        },
    },
    "[HIDDEN] Ion Exchange Bed Status": {
        "WRS Off-nominal pH Level": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'True': 0.986,
                    'False': 0.014
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
check_probabilities_sum(hidden_probabilities_dict)

# Store hidden probabilities dictionary as a .json file
with open("hidden_probabilities_dict.json", "w") as file:
    json.dump(hidden_probabilities_dict, file)