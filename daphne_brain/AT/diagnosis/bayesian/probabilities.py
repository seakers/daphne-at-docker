# probabilities.py
# Author: Joshua Elston
# Last Edited: 3/31/2025

# Stores the probabilities dictionary --> called in the ECLSS_Baysian_Network.py script
# Updated to include parameters that are measured separately on L1 and L2

from ranges import measurement_ranges
import json

# Create a dictionary to map the symptom probabilities to string states
# All probability blocks below are parameters conditioned on a single anomaly at a time
# NOTE: This probability dictionary is subsequently split into two seperate dictionaries for the high and low
# values for each parameter at the end of the script, which is then returned to the main script
# NOTE: NOTE: The False probabilities are currently all the same for every anomaly, but should be intelligently
# updated once the dictionary structure is finalized
# Mathematically, these probabilities are: Pr(TM=tm|A)

probability_dict = {
    "2-butanone": {
        "Fuel Cell #1 and PDU Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.16,
                    'Exceeds_UpperCautionLimit': 0.82,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["2-butanone"]
        },
        "Fuel Cell #2 and PDU Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.14,
                    'Exceeds_UpperCautionLimit': 0.84,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["2-butanone"]
        },
        "PDU 4 Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.19,
                    'Exceeds_UpperCautionLimit': 0.79,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["2-butanone"]
        },
        "PDU 5 Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.17,
                    'Exceeds_UpperCautionLimit': 0.81,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["2-butanone"]
        },
        "Reduced Main Cabin Fan #1 Capacity": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.20,
                    'Exceeds_UpperCautionLimit': 0.77,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["2-butanone"]
        },
        "TCCS Auxiliary Fan #1 Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.17,
                    'Exceeds_UpperCautionLimit': 0.81,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["2-butanone"]
        },
        "TCCS Auxiliary Fan #2 Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.15,
                    'Exceeds_UpperCautionLimit': 0.84,
                    'Nominal': 0.00989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["2-butanone"]
        },
        "TCCS Filter Clog": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.22,
                    'Exceeds_UpperCautionLimit': 0.76,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["2-butanone"]
        },
        "Trace Contaminants": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.17,
                    'Exceeds_UpperCautionLimit': 0.80,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["2-butanone"]
        },
    },
    "Acetaldehyde": {
        "Fuel Cell #1 and PDU Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.14,
                    'Exceeds_UpperCautionLimit': 0.84,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Acetaldehyde"]
        },
        "Fuel Cell #2 and PDU Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.16,
                    'Exceeds_UpperCautionLimit': 0.81,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Acetaldehyde"]
        },
        "PDU 4 Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.17,
                    'Exceeds_UpperCautionLimit': 0.81,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Acetaldehyde"]
        },
        "PDU 5 Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.18,
                    'Exceeds_UpperCautionLimit': 0.79,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Acetaldehyde"]
        },
        "TCCS Auxiliary Fan #1 Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.19,
                    'Exceeds_UpperCautionLimit': 0.78,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Acetaldehyde"]
        },
        "TCCS Auxiliary Fan #2 Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.18,
                    'Exceeds_UpperCautionLimit': 0.80,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Acetaldehyde"]
        },
        "TCCS Auxiliary Fan at Reduced Capacity": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.15,
                    'Exceeds_UpperCautionLimit': 0.82,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Acetaldehyde"]
        },
        "TCCS Filter Clog": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.20,
                    'Exceeds_UpperCautionLimit': 0.78,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Acetaldehyde"]
        },
    },
    "Aux Cabin Fan #1": {
        "Fuel Cell #2 and PDU Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.22,
                    'Exceeds_LowerWarningLimit': 0.76
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Aux Cabin Fan #1"]
        },
        "TCCS Auxiliary Fan #1 Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.15,
                    'Exceeds_LowerWarningLimit': 0.82
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Aux Cabin Fan #1"]
        },
    },
    "Aux Cabin Fan #2": {
        "Fuel Cell #1 and PDU Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.23,
                    'Exceeds_LowerWarningLimit': 0.75
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Aux Cabin Fan #2"]
        },
        "PDU 4 Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.24,
                    'Exceeds_LowerWarningLimit': 0.73
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Aux Cabin Fan #2"]
        },
        "PDU 5 Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.22,
                    'Exceeds_LowerWarningLimit': 0.76
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Aux Cabin Fan #2"]
        },
        "TCCS Auxiliary Fan #2 Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.17,
                    'Exceeds_LowerWarningLimit': 0.79
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Aux Cabin Fan #2"]
        },
        "TCCS Auxiliary Fan at Reduced Capacity": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.78,
                    'Exceeds_LowerWarningLimit': 0.19
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Aux Cabin Fan #2"]
        },
    },
    "Cabin Temperature (L1)": {
        "Excess Water Vapor Pressure in Cabin": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.20,
                    'Exceeds_UpperCautionLimit': 0.78,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Cabin Temperature (L1)"]
        },
        "Main Cabin Fan Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.21,
                    'Exceeds_UpperCautionLimit': 0.76,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Cabin Temperature (L1)"]
        }, 
        "PDU 4 Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.81,
                    'Exceeds_UpperCautionLimit': 0.16,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Cabin Temperature (L1)"]
        },
        "PDU 5 Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.79,
                    'Exceeds_UpperCautionLimit': 0.19,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Cabin Temperature (L1)"]
        },
    },
    "Cabin Temperature (L2)": {
        "Excess Water Vapor Pressure in Cabin": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.20,
                    'Exceeds_UpperCautionLimit': 0.78,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Cabin Temperature (L2)"]
        },
        "Main Cabin Fan Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.21,
                    'Exceeds_UpperCautionLimit': 0.76,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Cabin Temperature (L2)"]
        }, 
        "PDU 4 Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.81,
                    'Exceeds_UpperCautionLimit': 0.16,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Cabin Temperature (L2)"]
        },
        "PDU 5 Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.79,
                    'Exceeds_UpperCautionLimit': 0.19,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Cabin Temperature (L2)"]
        },
    },
    "Dichloromethane": {
        "TCCS Auxiliary Fan at Reduced Capacity": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.17,
                    'Exceeds_UpperCautionLimit': 0.81,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Dichloromethane"]
        },
        "TCCS Filter Clog": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.18,
                    'Exceeds_UpperCautionLimit': 0.79,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Dichloromethane"]
        },
    },
    "Fuel Cell #1 Current": {
        "Fuel Cell #1 and PDU Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.16,
                    'Exceeds_LowerWarningLimit': 0.82
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Fuel Cell #1 Current"]
        },
    },
    "Fuel Cell #1 PQM": {
        "Fuel Cell #1 and PDU Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.75,
                    'Exceeds_LowerWarningLimit': 0.12
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Fuel Cell #1 PQM"]
        },
    },
    "Fuel Cell #1 Stack Out Temp": {
        "Fuel Cell #1 and PDU Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.81,
                    'Exceeds_UpperCautionLimit': 0.17,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Fuel Cell #1 Stack Out Temp"]
        },
    },
    "Fuel Cell #1 Voltage": {
        "Fuel Cell #1 and PDU Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.19,
                    'Exceeds_LowerWarningLimit': 0.78
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Fuel Cell #1 Voltage"]
        },
    },
    "Fuel Cell #2 Current": {
        "Fuel Cell #2 and PDU Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.17,
                    'Exceeds_LowerWarningLimit': 0.81
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Fuel Cell #2 Current"]
        },
        "Fuel Cell Degrade": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.20,
                    'Exceeds_LowerWarningLimit': 0.77
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Fuel Cell #2 Current"]
        },
        "Fuel Cell Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.78,
                    'Exceeds_LowerWarningLimit': 0.19
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Fuel Cell #2 Current"]
        },
    },
    "Fuel Cell #2 PQM": {
        "Fuel Cell #2 and PDU Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.74,
                    'Exceeds_LowerWarningLimit': 0.14
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Fuel Cell #2 PQM"]
        },
        "Fuel Cell Degrade": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.22,
                    'Exceeds_LowerWarningLimit': 0.76
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Fuel Cell #2 PQM"]
        },
        "Fuel Cell Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.79,
                    'Exceeds_LowerWarningLimit': 0.18
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Fuel Cell #2 PQM"]
        },
    },
    "Fuel Cell #2 Stack Out Temp": {
        "Fuel Cell #2 and PDU Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.81,
                    'Exceeds_UpperCautionLimit': 0.17,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Fuel Cell #2 Stack Out Temp"]
        },
        "Fuel Cell Degrade": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.75,
                    'Exceeds_LowerWarningLimit': 0.22
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Fuel Cell #2 Stack Out Temp"]
        },
        "Fuel Cell Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.21,
                    'Exceeds_UpperCautionLimit': 0.76,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Fuel Cell #2 Stack Out Temp"]
        },
    },
    "Fuel Cell #2 Voltage": {
        "Fuel Cell #2 and PDU Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.15,
                    'Exceeds_LowerWarningLimit': 0.83
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Fuel Cell #2 Voltage"]
        },
        "Fuel Cell Degrade": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.21,
                    'Exceeds_LowerWarningLimit': 0.76
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Fuel Cell #2 Voltage"]
        },
        "Fuel Cell Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.19,
                    'Exceeds_LowerWarningLimit': 0.79
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Fuel Cell #2 Voltage"]
        },
    },
    "H2O (Crew)": {
        "Electrolysis System Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.74,
                    'Exceeds_LowerWarningLimit': 0.23
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["H2O (Crew)"]
        },
        "RWGSR Malfunction": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.77,
                    'Exceeds_LowerWarningLimit': 0.20
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["H2O (Crew)"]
        },
        "SPE System Maintenance": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.15,
                    'Exceeds_UpperCautionLimit': 0.82,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["H2O (Crew)"]
        },
        "WRS Maintenance": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.76,
                    'Exceeds_LowerWarningLimit': 0.21
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["H2O (Crew)"]
        },
    },
    "H2O pH": {
        "WRS Off-nominal pH Level": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.23,
                    'Exceeds_UpperCautionLimit': 0.74,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["H2O pH"]
        },
    },
    "HMCTS": {
        "Reduced Main Cabin Fan #1 Capacity": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.21,
                    'Exceeds_UpperCautionLimit': 0.76,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["HMCTS"]
        },
        "TCCS Filter Clog": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.23,
                    'Exceeds_UpperCautionLimit': 0.75,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["HMCTS"]
        },
    },
    "Humidity (L1)": {
        "CDRA Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.20,
                    'Exceeds_UpperCautionLimit': 0.78,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Humidity (L1)"]
        },
        "Excess Water Vapor Pressure in Cabin": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.17,
                    'Exceeds_UpperCautionLimit': 0.81,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Humidity (L1)"]
        },
        "Main Cabin Fan Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.22,
                    'Exceeds_UpperCautionLimit': 0.75,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Humidity (L1)"]
        },
        "PDU 4 Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.19,
                    'Exceeds_UpperCautionLimit': 0.78,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Humidity (L1)"]
        },
        "PDU 5 Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.21,
                    'Exceeds_UpperCautionLimit': 0.77,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Humidity (L1)"]
        },
    },
    "Humidity (L2)": {
        "CDRA Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.20,
                    'Exceeds_UpperCautionLimit': 0.78,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Humidity (L2)"]
        },
        "Excess Water Vapor Pressure in Cabin": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.17,
                    'Exceeds_UpperCautionLimit': 0.81,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Humidity (L2)"]
        },
        "Main Cabin Fan Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.22,
                    'Exceeds_UpperCautionLimit': 0.75,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Humidity (L2)"]
        },
        "PDU 4 Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.19,
                    'Exceeds_UpperCautionLimit': 0.78,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Humidity (L2)"]
        },
        "PDU 5 Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.21,
                    'Exceeds_UpperCautionLimit': 0.77,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Humidity (L2)"]
        },
    },
    "LiOH CO2 Saturation": {
        "CDRA LiOH Canister Saturation": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.83,
                    'Exceeds_UpperCautionLimit': 0.15,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["LiOH CO2 Saturation"]
        },
    },
    "Main Cabin Fan #1": {
        "Fuel Cell #2 and PDU Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.17,
                    'Exceeds_LowerWarningLimit': 0.81
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Main Cabin Fan #1"]
        },
        "Reduced Main Cabin Fan #1 Capacity": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.75,
                    'Exceeds_LowerWarningLimit': 0.22
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Main Cabin Fan #1"]
        },           
    },
    "Main Cabin Fan #2": {
        "Fuel Cell #1 and PDU Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.18,
                    'Exceeds_LowerWarningLimit': 0.80
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Main Cabin Fan #2"]
        },
        "Main Cabin Fan Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.19,
                    'Exceeds_LowerWarningLimit': 0.78
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Main Cabin Fan #2"]
        },
        "PDU 4 Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.20,
                    'Exceeds_LowerWarningLimit': 0.78
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Main Cabin Fan #2"]
        },
        "PDU 5 Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.17,
                    'Exceeds_LowerWarningLimit': 0.81
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Main Cabin Fan #2"]
        },
    },
    "MOXIE Compressor Temp": {
        "MOXIE Antenna Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.23,
                    'Exceeds_LowerWarningLimit': 0.75
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["MOXIE Compressor Temp"]
        },
        "MOXIE Fan Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.11,
                    'Exceeds_UpperCautionLimit': 0.76,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["MOXIE Compressor Temp"]
        },            
    },
    "MOXIE Telemetry Quality": {
        "MOXIE Antenna Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.21,
                    'Exceeds_LowerWarningLimit': 0.76
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["MOXIE Telemetry Quality"]
        }, 
    },
    "n_Butanol": {
        "Reduced Main Cabin Fan #1 Capacity": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.14,
                    'Exceeds_UpperCautionLimit': 0.83,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["n_Butanol"]
        },
        "TCCS Auxiliary Fan at Reduced Capacity": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.17,
                    'Exceeds_UpperCautionLimit': 0.81,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["n_Butanol"]
        },
    },
    "PDU 4 Bank 1": {
        "Fuel Cell #1 and PDU Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.18,
                    'Exceeds_LowerWarningLimit': 0.80
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["PDU 4 Bank 1"]
        },
        "PDU 4 Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.21,
                    'Exceeds_LowerWarningLimit': 0.77
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["PDU 4 Bank 1"]
        },
    },
    "PDU 5 Bank 1": {
        "Fuel Cell #2 and PDU Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.17,
                    'Exceeds_LowerWarningLimit': 0.81
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["PDU 5 Bank 1"]
        },
        "PDU 5 Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.22,
                    'Exceeds_LowerWarningLimit': 0.76
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["PDU 5 Bank 1"]
        },
    },
    "ppCO2 (L1)": {
        "Biological Filter Saturation": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.18,
                    'Exceeds_UpperCautionLimit': 0.79,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppCO2 (L1)"]
        },
        "CDRA Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.75,
                    'Exceeds_UpperCautionLimit': 0.23,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppCO2 (L1)"]
        },
        "CDRA LiOH Canister Saturation": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.20,
                    'Exceeds_UpperCautionLimit': 0.77,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppCO2 (L1)"]
        },
        "Excess CO2 in Cabin": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.81,
                    'Exceeds_UpperCautionLimit': 0.17,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppCO2 (L1)"]
        },
        "RWGSR Malfunction": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.19,
                    'Exceeds_UpperCautionLimit': 0.78,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppCO2 (L1)"]
        },
    },
    "ppCO2 (L2)": {
        "Biological Filter Saturation": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.18,
                    'Exceeds_UpperCautionLimit': 0.79,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppCO2 (L2)"]
        },
        "CDRA Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.75,
                    'Exceeds_UpperCautionLimit': 0.23,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppCO2 (L2)"]
        },
        "CDRA LiOH Canister Saturation": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.20,
                    'Exceeds_UpperCautionLimit': 0.77,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppCO2 (L2)"]
        },
        "Excess CO2 in Cabin": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.81,
                    'Exceeds_UpperCautionLimit': 0.17,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppCO2 (L2)"]
        },
        "RWGSR Malfunction": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.19,
                    'Exceeds_UpperCautionLimit': 0.78,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppCO2 (L2)"]
        },
    },
    "ppH2 (L1)": {
        "Excess Gas Leak": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.15,
                    'Exceeds_UpperCautionLimit': 0.82,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppH2 (L1)"]
        },
    },
    "ppH2 (L2)": {
        "Excess Gas Leak": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.15,
                    'Exceeds_UpperCautionLimit': 0.82,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppH2 (L2)"]
        },
    },
    "ppN2 (L1)": {
        "Loss of Pressure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.78,
                    'Exceeds_LowerWarningLimit': 0.20
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppN2 (L1)"]
        },
        "N2 Tank Burst": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.19,
                    'Exceeds_UpperCautionLimit': 0.79,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppN2 (L1)"]
        },
    },
    "ppN2 (L2)": {
        "Loss of Pressure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.78,
                    'Exceeds_LowerWarningLimit': 0.20
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppN2 (L2)"]
        },
        "N2 Tank Burst": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.19,
                    'Exceeds_UpperCautionLimit': 0.79,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppN2 (L2)"]
        },
    },
    "ppO2 (L1)": {
        "Biological Filter Saturation": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.81,
                    'Exceeds_LowerWarningLimit': 0.16
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppO2 (L1)"]
        },
        "CDRA Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.78,
                    'Exceeds_LowerWarningLimit': 0.19
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppO2 (L1)"]
        },
        "CDRA LiOH Canister Saturation": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.80,
                    'Exceeds_LowerWarningLimit': 0.18
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppO2 (L1)"]
        },
        "Electrolysis System Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.76,
                    'Exceeds_LowerWarningLimit': 0.22
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppO2 (L1)"]
        },
        "Emergency O2 System Maintenance": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.77,
                    'Exceeds_LowerWarningLimit': 0.21
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppO2 (L1)"]
        },
        "Loss of Pressure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.74,
                    'Exceeds_LowerWarningLimit': 0.24
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppO2 (L1)"]
        },
        "RWGSR Malfunction": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.78,
                    'Exceeds_LowerWarningLimit': 0.19
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppO2 (L1)"]
        },
    },
    "ppO2 (L2)": {
        "Biological Filter Saturation": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.81,
                    'Exceeds_LowerWarningLimit': 0.16
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppO2 (L2)"]
        },
        "CDRA Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.78,
                    'Exceeds_LowerWarningLimit': 0.19
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppO2 (L2)"]
        },
        "CDRA LiOH Canister Saturation": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.80,
                    'Exceeds_LowerWarningLimit': 0.18
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppO2 (L2)"]
        },
        "Electrolysis System Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.76,
                    'Exceeds_LowerWarningLimit': 0.22
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppO2 (L2)"]
        },
        "Emergency O2 System Maintenance": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.77,
                    'Exceeds_LowerWarningLimit': 0.21
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppO2 (L2)"]
        },
        "Loss of Pressure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.74,
                    'Exceeds_LowerWarningLimit': 0.24
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppO2 (L2)"]
        },
        "RWGSR Malfunction": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.78,
                    'Exceeds_LowerWarningLimit': 0.19
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["ppO2 (L2)"]
        },
    },
    "Pressure (L1)": {
        "Loss of Pressure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.81,
                    'Exceeds_LowerWarningLimit': 0.17
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Pressure (L1)"]
        },
        "N2 Tank Burst": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.22,
                    'Exceeds_UpperCautionLimit': 0.76,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Pressure (L1)"]
        },
    },
    "Pressure (L2)": {
        "Loss of Pressure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.81,
                    'Exceeds_LowerWarningLimit': 0.17
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Pressure (L2)"]
        },
        "N2 Tank Burst": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.22,
                    'Exceeds_UpperCautionLimit': 0.76,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Pressure (L2)"]
        },
    },
    "SOXIE Stack Temp": {
        "MOXIE Antenna Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.25,
                    'Exceeds_LowerWarningLimit': 0.73
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["SOXIE Stack Temp"]
        },
        "MOXIE ECM Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.20,
                    'Exceeds_UpperCautionLimit': 0.77,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["SOXIE Stack Temp"]
        },
    },
    "Total Cabin Pressure (L1)": {
        "Loss of Pressure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.82,
                    'Exceeds_LowerWarningLimit': 0.15
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Total Cabin Pressure (L1)"]
        },
        "N2 Tank Burst": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.19,
                    'Exceeds_UpperCautionLimit': 0.79,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Total Cabin Pressure (L1)"]
        },
    },
    "Total Cabin Pressure (L2)": {
        "Loss of Pressure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.82,
                    'Exceeds_LowerWarningLimit': 0.15
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Total Cabin Pressure (L2)"]
        },
        "N2 Tank Burst": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.19,
                    'Exceeds_UpperCautionLimit': 0.79,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.0001,
                    'Exceeds_LowerWarningLimit': 0.00001
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["Total Cabin Pressure (L2)"]
        },
    },
    "WRS Delivery Pump": {
        "WRS Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.81,
                    'Exceeds_LowerWarningLimit': 0.16
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["WRS Delivery Pump"]
        },
    },
    "WRS Valve Flow": {
        "WRS Failure": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.02989,
                    'Exceeds_LowerCautionLimit': 0.79,
                    'Exceeds_LowerWarningLimit': 0.18
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["WRS Valve Flow"]
        },
        "WRS Maintenance": {
            'probabilities': {
                True: { # probabilities when the anomaly is present
                    'Exceeds_UpperWarningLimit': 0.00001,
                    'Exceeds_UpperCautionLimit': 0.0001,
                    'Nominal': 0.01989,
                    'Exceeds_LowerCautionLimit': 0.76,
                    'Exceeds_LowerWarningLimit': 0.22
                },
                False: { # probabilities when the anomaly is absent
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.9978,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
            },
            'value_ranges': measurement_ranges["WRS Valve Flow"]
        },
    }
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
                print(f"Error: Probabilities for parameter '{parameter}' under anomaly '{anomaly}' ({presence}) sum to {total_probability:.2f}, not 1.0.")
                all_valid = False

    if all_valid:
            print("All probabilities for all telemetry parameters under all anomalies (both present and absent) sum to 1.0.")
    print()

# Check that the probabilities developed in the above dictionary correctly sum to one for each symptom under each anomaly
check_probabilities_sum(probability_dict)

# Create a function to redistribute the probabilities defined above when splitting them into high and low variables
def adjusted_probabilities(states, all_states, probabilities):
    # Find the states not included in the current group
    excluded_states = [state for state in all_states if state not in states]

    # Sum the probabilities of 'Nominal' and the excluded states
    adjusted_nominal_probability = sum([probabilities[state] for state in excluded_states + ['Nominal']])

    # Initialize a dictionary for the adjusted probabilities
    adjusted_probabilities = {}

    # Add 'Nominal' as the first state in the dictionary
    adjusted_probabilities['Nominal'] = adjusted_nominal_probability

    # Add the rest of the states (excluding 'Nominal')
    for state in states:
        if state != 'Nominal':
            adjusted_probabilities[state] = probabilities[state]

    return adjusted_probabilities

# Create a function to split each CPT into two, corresponding to 'high X' and 'low X' 
# for each parameter and each associated parent anomaly
def split_CPT(probabilities, value_ranges, parameter):
    # Define all states the parameters can take, to process which grouping is summed with the nominal probabilities
    all_states = ['Exceeds_UpperWarningLimit', 'Exceeds_UpperCautionLimit', 'Nominal', 'Exceeds_LowerCautionLimit', 'Exceeds_LowerWarningLimit']

    # Define the high and low groups, structured to ensure that the 'Nominal' state is
    # the minimum value of the ordinal variable
    high_states = ['Nominal', 'Exceeds_UpperCautionLimit', 'Exceeds_UpperWarningLimit']
    low_states = ['Nominal', 'Exceeds_LowerCautionLimit', 'Exceeds_LowerWarningLimit']

    # Initialize dictionaries for the high and low split probabilities for the cases where
    # anomalies are either present (True) or absent (False)
    # NOTE: These probabilities are ordered False, True to conform with the TabularCPD structure 
    # when adding the CPDs to the network, which has False = 0 and True = 1
    split_probabilities = {False: {}, True: {}}

    # Loop over the True and False anomaly presence states and adjust the probabilities for each
    for presence in [False, True]:
        adjusted_high = adjusted_probabilities(high_states, all_states, probabilities[presence])
        adjusted_low = adjusted_probabilities(low_states, all_states, probabilities[presence])  

        # Split the value ranges for each parameter into high and low groups
        high_value_ranges = {state: value_ranges[state] for state in high_states}
        low_value_ranges = {state: value_ranges[state] for state in low_states}

        # Rename the high and low groupings based on the parameter currently being assessed
        high_key = f'high {parameter}'
        low_key = f'low {parameter}'

        # Store the adjusted high and low probabilities under their respective keys
        split_probabilities[presence] = {
            high_key: {
                'probabilities': adjusted_high,
                'value_ranges': high_value_ranges
            },
            low_key: {
                'probabilities': adjusted_low,
                'value_ranges': low_value_ranges
            }
        }

    return split_probabilities

# Create a function to split the probability dictionary defined above into two distinct states (high_X/low_X)
# for each parameter X relative to each of their parent states
def process_probability_dict(probability_dict):
    # Create an empty dictionary in which to store values once the probability dictionary is split
    split_probability_dict = {}

    for parameter, anomalies in probability_dict.items():
        # Within the empty dictionary, create an empty dictionary for each specific parameter
        split_probability_dict[parameter] = {}

        for anomaly, data in anomalies.items():
            probabilities = data['probabilities']
            value_ranges = data['value_ranges']
            
            # Split the CPTs for each anomaly being present (True) or absent (False)
            split_CPTs = split_CPT(probabilities, value_ranges, parameter)
            
            # Add the split CPTs (both True and False) to the split dictionary
            split_probability_dict[parameter][anomaly] = {
                'False': split_CPTs[False],
                'True': split_CPTs[True]
            }

    return split_probability_dict

de

# Split the original probability dictionary into high and low dictionaries for each parameter
split_probability_dict = process_probability_dict(probability_dict)

# Store probability dictionary as a .json file
with open("split_probability_dict.json", "w") as file:
    json.dump(split_probability_dict, file)