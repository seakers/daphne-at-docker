# reduced_probabilities.py
# Author: Joshua Elston
# Last Edited: 03/06/2026

# Reduced set of parameters and probabilities for parameter learning with Biosim

# UPDATES:
# Updated on 03/03/2026 to reflect that parameters measured in IHab are related to both
# (IHab) and (Habitat) failures, while those measured in HALO are only related to
# (Habitat) failures. This pertains to Humidity, ppCO2, and ppO2 (not Cabin Pressure)
# Updated on 03/04/2026 to add Unknown Anomaly probabilities for each parameter
# Updated on 03/06/2026 to remove parent probabilities between "Unknown Anomaly" and each network parameter

from ranges import measurement_ranges
import json
import os

reduced_probability_dict = {
    "Humidity_IHab (IHab)": {
        # Temporal probabilities
        "Humidity_IHab (IHab) (t-1)": {
            'probabilities': {
                'Exceeds_UpperWarningLimit': {
                    'Exceeds_UpperWarningLimit': 0.84,
                    'Exceeds_UpperCautionLimit': 0.14,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Exceeds_UpperCautionLimit': {
                    'Exceeds_UpperWarningLimit': 0.14,
                    'Exceeds_UpperCautionLimit': 0.83,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Nominal': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.02,
                    'Nominal': 0.9598,
                    'Exceeds_LowerCautionLimit': 0.02,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Exceeds_LowerCautionLimit': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.83,
                    'Exceeds_LowerWarningLimit': 0.14
                },
                'Exceeds_LowerWarningLimit': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.14,
                    'Exceeds_LowerWarningLimit': 0.84
                },
            },
            'value_ranges': measurement_ranges["Humidity_IHab (IHab)"]
        },
        # Anomaly probabilities
        "CDRA Failure (IHab)": {
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
            'value_ranges': measurement_ranges["Humidity_IHab (IHab)"]
        },
        "CDRA Failure (Habitat)": {
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
            'value_ranges': measurement_ranges["Humidity_IHab (IHab)"]
        },
        # # Unknown Anomaly <-- equal effect in all direction
        # "Unknown Anomaly": {
        #     'probabilities': {
        #         True: { # probabilities when the anomaly is present
        #             'Exceeds_UpperWarningLimit': 0.20,
        #             'Exceeds_UpperCautionLimit': 0.20,
        #             'Nominal': 0.20,
        #             'Exceeds_LowerCautionLimit': 0.20,
        #             'Exceeds_LowerWarningLimit': 0.20
        #         },
        #         False: { # probabilities when the anomaly is absent
        #             'Exceeds_UpperWarningLimit': 0.0025,
        #             'Exceeds_UpperCautionLimit': 0.015,
        #             'Nominal': 0.965,
        #             'Exceeds_LowerCautionLimit': 0.015,
        #             'Exceeds_LowerWarningLimit': 0.0025
        #         },
        #     },
        #     'value_ranges': measurement_ranges["Humidity_IHab (IHab)"]
        # },
    },
    "Humidity_HALO (HALO)": {
        # Spatial probabilities
        "Humidity_IHab (IHab)": {
            'probabilities': {
                'Exceeds_UpperWarningLimit': {
                    'Exceeds_UpperWarningLimit': 0.86,
                    'Exceeds_UpperCautionLimit': 0.12,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Exceeds_UpperCautionLimit': {
                    'Exceeds_UpperWarningLimit': 0.12,
                    'Exceeds_UpperCautionLimit': 0.85,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Nominal': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.02,
                    'Nominal': 0.9598,
                    'Exceeds_LowerCautionLimit': 0.02,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Exceeds_LowerCautionLimit': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.85,
                    'Exceeds_LowerWarningLimit': 0.12
                },
                'Exceeds_LowerWarningLimit': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.12,
                    'Exceeds_LowerWarningLimit': 0.86
                },
            },
            'value_ranges': measurement_ranges["Humidity_HALO (HALO)"]
        },
        # Temporal probabilities
        "Humidity_HALO (HALO) (t-1)": {
            'probabilities': {
                'Exceeds_UpperWarningLimit': {
                    'Exceeds_UpperWarningLimit': 0.85,
                    'Exceeds_UpperCautionLimit': 0.13,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Exceeds_UpperCautionLimit': {
                    'Exceeds_UpperWarningLimit': 0.13,
                    'Exceeds_UpperCautionLimit': 0.84,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Nominal': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.02,
                    'Nominal': 0.9598,
                    'Exceeds_LowerCautionLimit': 0.02,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Exceeds_LowerCautionLimit': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.84,
                    'Exceeds_LowerWarningLimit': 0.13
                },
                'Exceeds_LowerWarningLimit': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.13,
                    'Exceeds_LowerWarningLimit': 0.85
                },
            },
            'value_ranges': measurement_ranges["Humidity_HALO (HALO)"]
        },
        # Anomaly probabilities
        "CDRA Failure (Habitat)": {
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
            'value_ranges': measurement_ranges["Humidity_HALO (HALO)"]
        },
        # # Unknown Anomaly <-- equal effect in all direction
        # "Unknown Anomaly": {
        #     'probabilities': {
        #         True: { # probabilities when the anomaly is present
        #             'Exceeds_UpperWarningLimit': 0.2,
        #             'Exceeds_UpperCautionLimit': 0.2,
        #             'Nominal': 0.2,
        #             'Exceeds_LowerCautionLimit': 0.2,
        #             'Exceeds_LowerWarningLimit': 0.2
        #         },
        #         False: { # probabilities when the anomaly is absent
        #             'Exceeds_UpperWarningLimit': 0.0025,
        #             'Exceeds_UpperCautionLimit': 0.015,
        #             'Nominal': 0.965,
        #             'Exceeds_LowerCautionLimit': 0.015,
        #             'Exceeds_LowerWarningLimit': 0.0025
        #         },
        #     },
        #     'value_ranges': measurement_ranges["Humidity_HALO (HALO)"]
        # },
    },
    "ppCO2_IHab (IHab)": {
        # Temporal probabilities
        "ppCO2_IHab (IHab) (t-1)": {
            'probabilities': {
                'Exceeds_UpperWarningLimit': {
                    'Exceeds_UpperWarningLimit': 0.86,
                    'Exceeds_UpperCautionLimit': 0.12,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Exceeds_UpperCautionLimit': {
                    'Exceeds_UpperWarningLimit': 0.12,
                    'Exceeds_UpperCautionLimit': 0.85,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Nominal': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.02,
                    'Nominal': 0.9598,
                    'Exceeds_LowerCautionLimit': 0.02,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Exceeds_LowerCautionLimit': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.85,
                    'Exceeds_LowerWarningLimit': 0.12
                },
                'Exceeds_LowerWarningLimit': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.12,
                    'Exceeds_LowerWarningLimit': 0.86
                },
            },
            'value_ranges': measurement_ranges["ppCO2_IHab (IHab)"]
        },
        # Anomaly probabilities
        "Biological Filter Saturation (IHab)": {
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
            'value_ranges': measurement_ranges["ppCO2_IHab (IHab)"]
        },
        "Biological Filter Saturation (Habitat)": {
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
            'value_ranges': measurement_ranges["ppCO2_IHab (IHab)"]
        },
        "CDRA Failure (IHab)": {
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
            'value_ranges': measurement_ranges["ppCO2_IHab (IHab)"]
        },
        "CDRA Failure (Habitat)": {
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
            'value_ranges': measurement_ranges["ppCO2_IHab (IHab)"]
        },
        "Loss of Pressure (IHab)": {
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
            'value_ranges': measurement_ranges["ppCO2_IHab (IHab)"]
        },
        "Excess CO2 in Cabin (IHab)": {
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
            'value_ranges': measurement_ranges["ppCO2_IHab (IHab)"]
        },
        # # Unknown Anomaly <-- equal effect in all direction
        # "Unknown Anomaly": {
        #     'probabilities': {
        #         True: { # probabilities when the anomaly is present
        #             'Exceeds_UpperWarningLimit': 0.2,
        #             'Exceeds_UpperCautionLimit': 0.2,
        #             'Nominal': 0.2,
        #             'Exceeds_LowerCautionLimit': 0.2,
        #             'Exceeds_LowerWarningLimit': 0.2
        #         },
        #         False: { # probabilities when the anomaly is absent
        #             'Exceeds_UpperWarningLimit': 0.0025,
        #             'Exceeds_UpperCautionLimit': 0.015,
        #             'Nominal': 0.965,
        #             'Exceeds_LowerCautionLimit': 0.015,
        #             'Exceeds_LowerWarningLimit': 0.0025
        #         },
        #     },
        #     'value_ranges': measurement_ranges["ppCO2_IHab (IHab)"]
        # },
    },
    "ppCO2_HALO (HALO)": {
        # Spatial probabilities
        "ppCO2_IHab (IHab)": {
            'probabilities': {
                'Exceeds_UpperWarningLimit': {
                    'Exceeds_UpperWarningLimit': 0.85,
                    'Exceeds_UpperCautionLimit': 0.13,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Exceeds_UpperCautionLimit': {
                    'Exceeds_UpperWarningLimit': 0.13,
                    'Exceeds_UpperCautionLimit': 0.84,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Nominal': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.02,
                    'Nominal': 0.9598,
                    'Exceeds_LowerCautionLimit': 0.02,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Exceeds_LowerCautionLimit': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.84,
                    'Exceeds_LowerWarningLimit': 0.13
                },
                'Exceeds_LowerWarningLimit': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.13,
                    'Exceeds_LowerWarningLimit': 0.85
                },
            },
            'value_ranges': measurement_ranges["ppCO2_HALO (HALO)"]
        },
        # Temporal probabilities
        "ppCO2_HALO (HALO) (t-1)": {
            'probabilities': {
                'Exceeds_UpperWarningLimit': {
                    'Exceeds_UpperWarningLimit': 0.87,
                    'Exceeds_UpperCautionLimit': 0.11,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Exceeds_UpperCautionLimit': {
                    'Exceeds_UpperWarningLimit': 0.11,
                    'Exceeds_UpperCautionLimit': 0.86,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Nominal': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.02,
                    'Nominal': 0.9598,
                    'Exceeds_LowerCautionLimit': 0.02,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Exceeds_LowerCautionLimit': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.86,
                    'Exceeds_LowerWarningLimit': 0.11
                },
                'Exceeds_LowerWarningLimit': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.11,
                    'Exceeds_LowerWarningLimit': 0.87
                },
            },
            'value_ranges': measurement_ranges["ppCO2_HALO (HALO)"]
        },
        # Anomaly probabilities
        "Biological Filter Saturation (Habitat)": {
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
            'value_ranges': measurement_ranges["ppCO2_HALO (HALO)"]
        },
        "CDRA Failure (Habitat)": {
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
            'value_ranges': measurement_ranges["ppCO2_HALO (HALO)"]
        },
        "Loss of Pressure (HALO)": {
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
            'value_ranges': measurement_ranges["ppCO2_HALO (HALO)"]
        },
        "Excess CO2 in Cabin (HALO)": {
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
            'value_ranges': measurement_ranges["ppCO2_HALO (HALO)"]
        },
        # # Unknown Anomaly <-- equal effect in all direction
        # "Unknown Anomaly": {
        #     'probabilities': {
        #         True: { # probabilities when the anomaly is present
        #             'Exceeds_UpperWarningLimit': 0.2,
        #             'Exceeds_UpperCautionLimit': 0.2,
        #             'Nominal': 0.2,
        #             'Exceeds_LowerCautionLimit': 0.2,
        #             'Exceeds_LowerWarningLimit': 0.2
        #         },
        #         False: { # probabilities when the anomaly is absent
        #             'Exceeds_UpperWarningLimit': 0.0025,
        #             'Exceeds_UpperCautionLimit': 0.015,
        #             'Nominal': 0.965,
        #             'Exceeds_LowerCautionLimit': 0.015,
        #             'Exceeds_LowerWarningLimit': 0.0025
        #         },
        #     },
        #     'value_ranges': measurement_ranges["ppCO2_HALO (HALO)"]
        # },
    },
    "ppO2_IHab (IHab)": {
        # Temporal probabilities
        "ppO2_IHab (IHab) (t-1)": {
            'probabilities': {
                'Exceeds_UpperWarningLimit': {
                    'Exceeds_UpperWarningLimit': 0.88,
                    'Exceeds_UpperCautionLimit': 0.1,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Exceeds_UpperCautionLimit': {
                    'Exceeds_UpperWarningLimit': 0.1,
                    'Exceeds_UpperCautionLimit': 0.87,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Nominal': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.02,
                    'Nominal': 0.9598,
                    'Exceeds_LowerCautionLimit': 0.02,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Exceeds_LowerCautionLimit': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.87,
                    'Exceeds_LowerWarningLimit': 0.1
                },
                'Exceeds_LowerWarningLimit': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.1,
                    'Exceeds_LowerWarningLimit': 0.88
                },
            },
            'value_ranges': measurement_ranges["ppO2_IHab (IHab)"]
        },
        # Anomaly probabilities <-- updated to reflect level-specific failures
        "Biological Filter Saturation (IHab)": {
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
            'value_ranges': measurement_ranges["ppO2_IHab (IHab)"]
        },
        "Biological Filter Saturation (Habitat)": {
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
            'value_ranges': measurement_ranges["ppO2_IHab (IHab)"]
        },
        "CDRA Failure (IHab)": {
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
            'value_ranges': measurement_ranges["ppO2_IHab (IHab)"]
        },
        "CDRA Failure (Habitat)": {
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
            'value_ranges': measurement_ranges["ppO2_IHab (IHab)"]
        },
        "Emergency O2 System Maintenance (IHab)": {
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
            'value_ranges': measurement_ranges["ppO2_IHab (IHab)"]
        },
        "Loss of Pressure (IHab)": {
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
            'value_ranges': measurement_ranges["ppO2_IHab (IHab)"]
        },
        # # Unknown Anomaly <-- equal effect in all direction
        # "Unknown Anomaly": {
        #     'probabilities': {
        #         True: { # probabilities when the anomaly is present
        #             'Exceeds_UpperWarningLimit': 0.2,
        #             'Exceeds_UpperCautionLimit': 0.2,
        #             'Nominal': 0.2,
        #             'Exceeds_LowerCautionLimit': 0.2,
        #             'Exceeds_LowerWarningLimit': 0.2
        #         },
        #         False: { # probabilities when the anomaly is absent
        #             'Exceeds_UpperWarningLimit': 0.0025,
        #             'Exceeds_UpperCautionLimit': 0.015,
        #             'Nominal': 0.965,
        #             'Exceeds_LowerCautionLimit': 0.015,
        #             'Exceeds_LowerWarningLimit': 0.0025
        #         },
        #     },
        #     'value_ranges': measurement_ranges["ppO2_IHab (IHab)"]
        # },
    },
    "ppO2_HALO (HALO)": {
        # Spatial probabilities
        "ppO2_IHab (IHab)": {
            'probabilities': {
                'Exceeds_UpperWarningLimit': {
                    'Exceeds_UpperWarningLimit': 0.86,
                    'Exceeds_UpperCautionLimit': 0.12,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Exceeds_UpperCautionLimit': {
                    'Exceeds_UpperWarningLimit': 0.12,
                    'Exceeds_UpperCautionLimit': 0.85,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Nominal': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.02,
                    'Nominal': 0.9598,
                    'Exceeds_LowerCautionLimit': 0.02,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Exceeds_LowerCautionLimit': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.85,
                    'Exceeds_LowerWarningLimit': 0.12
                },
                'Exceeds_LowerWarningLimit': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.12,
                    'Exceeds_LowerWarningLimit': 0.86
                },
            },
            'value_ranges': measurement_ranges["ppO2_HALO (HALO)"]
        },
        # Temporal probabilities
        "ppO2_HALO (HALO) (t-1)": {
            'probabilities': {
                'Exceeds_UpperWarningLimit': {
                    'Exceeds_UpperWarningLimit': 0.87,
                    'Exceeds_UpperCautionLimit': 0.11,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Exceeds_UpperCautionLimit': {
                    'Exceeds_UpperWarningLimit': 0.11,
                    'Exceeds_UpperCautionLimit': 0.86,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Nominal': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.02,
                    'Nominal': 0.9598,
                    'Exceeds_LowerCautionLimit': 0.02,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Exceeds_LowerCautionLimit': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.86,
                    'Exceeds_LowerWarningLimit': 0.11
                },
                'Exceeds_LowerWarningLimit': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.11,
                    'Exceeds_LowerWarningLimit': 0.87
                },
            },
            'value_ranges': measurement_ranges["ppO2_HALO (HALO)"]
        },
        # Anomaly probabilities <-- updated to reflect level-specific failures
        "Biological Filter Saturation (Habitat)": {
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
            'value_ranges': measurement_ranges["ppO2_HALO (HALO)"]
        },
        "CDRA Failure (Habitat)": {
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
            'value_ranges': measurement_ranges["ppO2_HALO (HALO)"]
        },
        "Emergency O2 System Maintenance (HALO)": {
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
            'value_ranges': measurement_ranges["ppO2_HALO (HALO)"]
        },
        "Loss of Pressure (HALO)": {
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
            'value_ranges': measurement_ranges["ppO2_HALO (HALO)"]
        },
        # # Unknown Anomaly <-- equal effect in all direction
        # "Unknown Anomaly": {
        #     'probabilities': {
        #         True: { # probabilities when the anomaly is present
        #             'Exceeds_UpperWarningLimit': 0.2,
        #             'Exceeds_UpperCautionLimit': 0.2,
        #             'Nominal': 0.2,
        #             'Exceeds_LowerCautionLimit': 0.2,
        #             'Exceeds_LowerWarningLimit': 0.2
        #         },
        #         False: { # probabilities when the anomaly is absent
        #             'Exceeds_UpperWarningLimit': 0.0025,
        #             'Exceeds_UpperCautionLimit': 0.015,
        #             'Nominal': 0.965,
        #             'Exceeds_LowerCautionLimit': 0.015,
        #             'Exceeds_LowerWarningLimit': 0.0025
        #         },
        #     },
        #     'value_ranges': measurement_ranges["ppO2_HALO (HALO)"]
        # },
    },
    "Total_Cabin_Pressure_IHab (IHab)": {
        # Temporal probabilities
        "Total_Cabin_Pressure_IHab (IHab) (t-1)": {
            'probabilities': {
                'Exceeds_UpperWarningLimit': {
                    'Exceeds_UpperWarningLimit': 0.88,
                    'Exceeds_UpperCautionLimit': 0.1,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Exceeds_UpperCautionLimit': {
                    'Exceeds_UpperWarningLimit': 0.1,
                    'Exceeds_UpperCautionLimit': 0.87,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Nominal': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.02,
                    'Nominal': 0.9598,
                    'Exceeds_LowerCautionLimit': 0.02,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Exceeds_LowerCautionLimit': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.87,
                    'Exceeds_LowerWarningLimit': 0.1
                },
                'Exceeds_LowerWarningLimit': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.1,
                    'Exceeds_LowerWarningLimit': 0.88
                },
            },
            'value_ranges': measurement_ranges["Total_Cabin_Pressure_IHab (IHab)"]
        },
        # Anomaly probabilities
        "Loss of Pressure (IHab)": {
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
            'value_ranges': measurement_ranges["Total_Cabin_Pressure_IHab (IHab)"]
        },
        # # Unknown Anomaly <-- equal effect in all direction
        # "Unknown Anomaly": {
        #     'probabilities': {
        #         True: { # probabilities when the anomaly is present
        #             'Exceeds_UpperWarningLimit': 0.2,
        #             'Exceeds_UpperCautionLimit': 0.2,
        #             'Nominal': 0.2,
        #             'Exceeds_LowerCautionLimit': 0.2,
        #             'Exceeds_LowerWarningLimit': 0.2
        #         },
        #         False: { # probabilities when the anomaly is absent
        #             'Exceeds_UpperWarningLimit': 0.0025,
        #             'Exceeds_UpperCautionLimit': 0.015,
        #             'Nominal': 0.965,
        #             'Exceeds_LowerCautionLimit': 0.015,
        #             'Exceeds_LowerWarningLimit': 0.0025
        #         },
        #     },
        #     'value_ranges': measurement_ranges["Total_Cabin_Pressure_IHab (IHab)"]
        # },
    },
    "Total_Cabin_Pressure_HALO (HALO)": {
        # Spatial probabilities
        "Total_Cabin_Pressure_IHab (IHab)": {
            'probabilities': {
                'Exceeds_UpperWarningLimit': {
                    'Exceeds_UpperWarningLimit': 0.88,
                    'Exceeds_UpperCautionLimit': 0.1,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Exceeds_UpperCautionLimit': {
                    'Exceeds_UpperWarningLimit': 0.1,
                    'Exceeds_UpperCautionLimit': 0.87,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Nominal': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.02,
                    'Nominal': 0.9598,
                    'Exceeds_LowerCautionLimit': 0.02,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Exceeds_LowerCautionLimit': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.87,
                    'Exceeds_LowerWarningLimit': 0.1
                },
                'Exceeds_LowerWarningLimit': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.1,
                    'Exceeds_LowerWarningLimit': 0.88
                },
            },
            'value_ranges': measurement_ranges["Total_Cabin_Pressure_HALO (HALO)"]
        },
        # Temporal probabilities
        "Total_Cabin_Pressure_HALO (HALO) (t-1)": {
            'probabilities': {
                'Exceeds_UpperWarningLimit': {
                    'Exceeds_UpperWarningLimit': 0.87,
                    'Exceeds_UpperCautionLimit': 0.11,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Exceeds_UpperCautionLimit': {
                    'Exceeds_UpperWarningLimit': 0.11,
                    'Exceeds_UpperCautionLimit': 0.86,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.001,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Nominal': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.02,
                    'Nominal': 0.9598,
                    'Exceeds_LowerCautionLimit': 0.02,
                    'Exceeds_LowerWarningLimit': 0.0001
                },
                'Exceeds_LowerCautionLimit': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.0289,
                    'Exceeds_LowerCautionLimit': 0.86,
                    'Exceeds_LowerWarningLimit': 0.11
                },
                'Exceeds_LowerWarningLimit': {
                    'Exceeds_UpperWarningLimit': 0.0001,
                    'Exceeds_UpperCautionLimit': 0.001,
                    'Nominal': 0.0189,
                    'Exceeds_LowerCautionLimit': 0.11,
                    'Exceeds_LowerWarningLimit': 0.87
                },
            },
            'value_ranges': measurement_ranges["Total_Cabin_Pressure_HALO (HALO)"]
        },
        # Anomaly probabilities
        "Loss of Pressure (HALO)": {
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
            'value_ranges': measurement_ranges["Total_Cabin_Pressure_HALO (HALO)"]
        } #,
        # # Unknown Anomaly <-- equal effect in all direction
        # "Unknown Anomaly": {
        #     'probabilities': {
        #         True: { # probabilities when the anomaly is present
        #             'Exceeds_UpperWarningLimit': 0.2,
        #             'Exceeds_UpperCautionLimit': 0.2,
        #             'Nominal': 0.2,
        #             'Exceeds_LowerCautionLimit': 0.2,
        #             'Exceeds_LowerWarningLimit': 0.2
        #         },
        #         False: { # probabilities when the anomaly is absent
        #             'Exceeds_UpperWarningLimit': 0.0025,
        #             'Exceeds_UpperCautionLimit': 0.015,
        #             'Nominal': 0.965,
        #             'Exceeds_LowerCautionLimit': 0.015,
        #             'Exceeds_LowerWarningLimit': 0.0025
        #         },
        #     },
        #     'value_ranges': measurement_ranges["Total_Cabin_Pressure_HALO (HALO)"]
        # }
    }
}

# Add probabilities for all (t-1) versions of the parameters, ensuring that the value ranges are correctly tied
# to those for the (t-1) parameter (even though they are currently identical to the current parameter ranges)
def add_temporal_probabilities(probability_dict, measurement_ranges):
    new_entries = {} # create an empty dictionary for (t-1) parameter probabilities
    for parameter, anomalies in probability_dict.items():
        temporal_parameter = f"{parameter} (t-1)"
        if temporal_parameter in measurement_ranges:
            new_entries[temporal_parameter] = {} # set up an empty dictionary entry for each (t-1) parameter
            for anomaly, data in anomalies.items():
                # Don't add an anomaly if it is for the temporal probabilities between a parameter and its value at (t-1)
                if "(t-1)" in anomaly: # or "(IHab)" in anomaly:
                    continue
                if "(IHab)" in anomaly and "(HALO)" in parameter:
                    continue
                new_entries[temporal_parameter] [anomaly] = {
                    'probabilities': data['probabilities'],
                    'value_ranges': measurement_ranges[temporal_parameter]
                }
        else:
            print(f"Warning: temporal parameter {temporal_parameter} not found in measurement_ranges")
    probability_dict.update(new_entries)

# Add (t-1) parameter probabilities to dictionary
add_temporal_probabilities(reduced_probability_dict, measurement_ranges)

# Ensure that all of the temporal probabilities added above sum to 1.0
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
check_probabilities_sum(reduced_probability_dict)

# Create a function to redistribute the probabilities defined above when splitting them into high and low variables
# This function has been adjusted to accomodate both the binary anomaly (flat probability structure) and multistate
# parameter probabilities (nested probability structure)
def adjusted_probabilities(states, all_states, probabilities):
    # First, check if the probability structure is nested, as for the multistate parameter parent nodes
    if any(isinstance(v, dict) for v in probabilities.values()):
        # Create an empty dictionary for nested parent probabilities
        adjusted_nested = {} 
        for parent_state, child_probs in probabilities.items():
            # For each parent state, run the flat adjustment to access the probabilities
            adjusted = adjusted_probabilities(states, all_states, child_probs)
            adjusted_nested[parent_state] = adjusted
        return adjusted_nested

    # If probability structure is flat, proceed as before
    # Find the states not included in the current group
    excluded_states = [state for state in all_states if state not in states]

    # Sum the probabilities of 'Nominal' and the excluded states
    adjusted_nominal_probability = sum([probabilities[state] for state in excluded_states + ['Nominal']])

    # Initialize a dictionary for the adjusted probabilities
    adjusted_probs = {}

    # Add 'Nominal' as the first state in the dictionary
    adjusted_probs['Nominal'] = adjusted_nominal_probability

    # Add the rest of the states (excluding 'Nominal')
    for state in states:
        if state != 'Nominal':
            adjusted_probs[state] = probabilities[state]

    return adjusted_probs

# Create a function to split each CPT into two, corresponding to 'high X' and 'low X' 
# for each parameter and each associated parent anomaly
def split_CPT(probabilities, value_ranges, parameter):
    # Define all states the parameters can take, to process which grouping is summed with the nominal probabilities
    all_states = ['Exceeds_UpperWarningLimit', 'Exceeds_UpperCautionLimit', 'Nominal', 'Exceeds_LowerCautionLimit', 'Exceeds_LowerWarningLimit']

    # Define the high and low groups, structured to ensure that the 'Nominal' state is
    # the minimum value of the ordinal variable
    high_states = ['Nominal', 'Exceeds_UpperCautionLimit', 'Exceeds_UpperWarningLimit']
    low_states = ['Nominal', 'Exceeds_LowerCautionLimit', 'Exceeds_LowerWarningLimit']

    # Initialize dictionaries for the high and low split probabilities. These dictionaries capture
    # all combinations of parent anomalies being True or False, along with any parent spatial/temporal
    # parameters being in one of the five possible states
    split_probabilities = {}

    # Check if the parent node being iterated over is a binary anomaly (True or False) or a multi-state parameter
    if isinstance(probabilities, dict) and all(isinstance(k, bool) for k in probabilities.keys()):
        # In the case that binary anomalies are being considered, conduct same process as used before the addition of parameter parent nodes
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
    else:
        adjusted_high = adjusted_probabilities(high_states, all_states, probabilities)
        adjusted_low = adjusted_probabilities(low_states, all_states, probabilities)

        # Split the value ranges for each parameter into high and low groups
        high_value_ranges = {state: value_ranges[state] for state in high_states}
        low_value_ranges = {state: value_ranges[state] for state in low_states}

        # Rename the high and low groupings based on the parameter currently being assessed
        high_key = f'high {parameter}'
        low_key = f'low {parameter}'

        # Store the adjusted high and low probabilities under their respective keys
        split_probabilities = {
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

            # Add temporal probabilities
            if "(t-1)" in anomaly:
                # Essentially duplicate the split_CPT function specifically for the (t-1) parents of parameters
                all_states = ['Exceeds_UpperWarningLimit', 'Exceeds_UpperCautionLimit', 'Nominal', 'Exceeds_LowerCautionLimit', 'Exceeds_LowerWarningLimit']
                high_states = ['Nominal', 'Exceeds_UpperCautionLimit', 'Exceeds_UpperWarningLimit']
                low_states = ['Nominal', 'Exceeds_LowerCautionLimit', 'Exceeds_LowerWarningLimit']

                # Split the original nested CPT by only keeping the relevant parent states
                high_parent_probs = {k: v for k, v in probabilities.items() if k in high_states}
                low_parent_probs = {k: v for k, v in probabilities.items() if k in low_states}

                # Adjust the probabilities for each child node to fit under the new high/low parent structure
                adjusted_high = {ps: adjusted_probabilities(high_states, all_states, child_probs) for ps, child_probs in high_parent_probs.items()}
                adjusted_low = {ps: adjusted_probabilities(low_states, all_states, child_probs) for ps, child_probs in low_parent_probs.items()}

                # UPDATED ON 10/22/2025
                # Extract the probabilities related to the high X variable
                split_probability_dict[parameter][f"high {anomaly}"] = {
                    f"high {parameter}": {
                        'probabilities' : adjusted_high,
                        'value_ranges': {
                            s: value_ranges[s] for s in high_states
                        }
                    }
                }
                # Extract the probabilities related to the low X variable
                split_probability_dict[parameter][f"low {anomaly}"] = {
                    f"low {parameter}": {
                        'probabilities' : adjusted_low,
                        'value_ranges': {
                            s: value_ranges[s] for s in low_states
                        }
                    }
                }
                continue

            # UPDATED ON 10/23/2025
            # Add spatial probabilities
            if parameter.endswith("(HALO)") and anomaly.endswith("(IHab)"):

                parameter_base = parameter.replace("(HALO)", "").strip()
                anomaly_base = anomaly.replace("(IHab)", "").strip()

                # UPDATED ON 11/05/2025
                if parameter_base.endswith("_HALO") and anomaly_base.endswith("_IHab"):
                    parameter_base = parameter_base.replace("_HALO", "").strip()
                    anomaly_base = anomaly_base.replace("_IHab", "").strip()

                # Confirm that the parameter and anomaly correspond to the same measurement
                if parameter_base == anomaly_base:
                    # print(f"Processing (IHab) parent for (HALO) parameter: {parameter} <-- {anomaly}")

                    # Essentially duplicate the split_CPT function specifically for the (t-1) parents of parameters
                    all_states = ['Exceeds_UpperWarningLimit', 'Exceeds_UpperCautionLimit', 'Nominal', 'Exceeds_LowerCautionLimit', 'Exceeds_LowerWarningLimit']
                    high_states = ['Nominal', 'Exceeds_UpperCautionLimit', 'Exceeds_UpperWarningLimit']
                    low_states = ['Nominal', 'Exceeds_LowerCautionLimit', 'Exceeds_LowerWarningLimit']

                    # Split the original nested CPT by only keeping the relevant parent states
                    high_parent_probs = {k: v for k, v in probabilities.items() if k in high_states}
                    low_parent_probs = {k: v for k, v in probabilities.items() if k in low_states}

                    # Adjust the probabilities for each child node to fit under the new high/low parent structure
                    adjusted_high = {ps: adjusted_probabilities(high_states, all_states, child_probs) for ps, child_probs in high_parent_probs.items()}
                    adjusted_low = {ps: adjusted_probabilities(low_states, all_states, child_probs) for ps, child_probs in low_parent_probs.items()}

                    # Extract the probabilities related to the high X variable
                    split_probability_dict[parameter][f"high {anomaly}"] = {
                        f"high {parameter}": {
                            'probabilities' : adjusted_high,
                            'value_ranges': {
                                s: value_ranges[s] for s in high_states
                            }
                        }
                    }
                    # Extract the probabilities related to the low X variable
                    split_probability_dict[parameter][f"low {anomaly}"] = {
                        f"low {parameter}": {
                            'probabilities' : adjusted_low,
                            'value_ranges': {
                                s: value_ranges[s] for s in low_states
                            }
                        }
                    }
                    continue

            # Split the CPTs for each anomaly being present (True) or absent (False)
            split_CPTs = split_CPT(probabilities, value_ranges, parameter)

            # If the probabilities being added stem from a binary parent anomaly, use the same approach as before
            if all(isinstance(k, bool) for k in split_CPTs.keys()):
                # Add the split CPTs (both True and False) to the split dictionary
                split_probability_dict[parameter][anomaly] = {
                    'False': split_CPTs[False],
                    'True': split_CPTs[True]
                }
            # Otherwise, access the nested probabilties for a multistate parameter parent
            else:
                split_probability_dict[parameter][anomaly] = split_CPTs

    return split_probability_dict

# Split the original probability dictionary into high and low dictionaries for each parameter
reduced_split_probability_dict = process_probability_dict(reduced_probability_dict)
current_dir = os.path.dirname(os.path.abspath(__file__))
output_file_path = os.path.join(current_dir, "reduced_split_probabilities_dict.json")

# Store probability dictionary as a .json file
with open(output_file_path, "w") as file:
    json.dump(reduced_split_probability_dict, file)