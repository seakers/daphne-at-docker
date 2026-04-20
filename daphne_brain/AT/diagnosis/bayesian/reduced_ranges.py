# reduced_ranges.py
# Author: Joshua Elston
# Last Edited: 04/20/2026

# Stores the measurement_ranges dictionary --> called in probabilities.py

# 43 (out of 65 distinct (and 79 total)) measurement ranges from Neo4j are summarized below. The criteria for including these measurements are:
#   1) Must be a unique measurement (those measured independently for IHab and HALO in HERA are now split into individual entries)
#   2) Measurement must be included in Neo4j
#   3) Measurement must be related to at least one anomaly in Neo4j
# Measurements not satisfying either criterion 2 or 3 are included in the [UNUSED]ranges.py script

# NOTE: H2O pH, LiOH CO2 Saturation, and MOXIE Telemetry Quality are all associated with anomalies within Neo4j, but are not
# included in the HSS on Kazuki's lab machine. They are still reported here to match the KG, but this discrepancy should be
# resolved in future
# NOTE: For the addition of parameter ranges for (t-1) variables, a copy of measurement_ranges is made, with all
# previous time step parameters having the same ranges. This enables quick adaptability if additional parameters
# are added or name changes are required

# Example bound meanings are shown for ppO2_IHab (IHab) (lines 268-273)

# Changes on 11/05/2025 to reflect naming convention for Gateway (L1 -- > IHab, L2 --> HALO)
# Update also reflects parameter naming as seen in Biosim (ex: ppCO2_IHab (IHab))
# Updated on 04/20/2026 to reflect reduced network structure

# Create a dictionary to store the measurement ranges for each of the parameters being measured
measurement_ranges = {
    "Humidity_IHab (IHab)": {
        'Exceeds_UpperWarningLimit': (70, None, True, False),
        'Exceeds_UpperCautionLimit': (55, 70, True, False),
        'Nominal': (50, 55, False, False), # Nominal: 52.01% (IHab = HALO)
        'Exceeds_LowerCautionLimit': (40, 50, False, True),
        'Exceeds_LowerWarningLimit': (None, 40, False, True)
    },
    "Humidity_HALO (HALO)": {
        'Exceeds_UpperWarningLimit': (70, None, True, False),
        'Exceeds_UpperCautionLimit': (55, 70, True, False),
        'Nominal': (50, 55, False, False), # Nominal: 52.01% (IHab = HALO)
        'Exceeds_LowerCautionLimit': (40, 50, False, True),
        'Exceeds_LowerWarningLimit': (None, 40, False, True)
    },
    "ppCO2_IHab (IHab)": {
        'Exceeds_UpperWarningLimit': (1.88, None, True, False),
        'Exceeds_UpperCautionLimit': (1.13, 1.88, True, False),
        'Nominal': (0.2, 1.13, False, False), # Nominal: 2.59 mmHg (IHab = HALO)
        'Exceeds_LowerCautionLimit': (0, 0.2, False, True),
        'Exceeds_LowerWarningLimit': (None, 0, False, True)
    },
    "ppCO2_HALO (HALO)": {
        'Exceeds_UpperWarningLimit': (1.88, None, True, False),
        'Exceeds_UpperCautionLimit': (1.13, 1.88, True, False),
        'Nominal': (0.2, 1.13, False, False), # Nominal: 2.59 mmHg (IHab = HALO)
        'Exceeds_LowerCautionLimit': (0, 0.2, False, True),
        'Exceeds_LowerWarningLimit': (None, 0, False, True)
    },
    "ppO2_IHab (IHab)": {
        'Exceeds_UpperWarningLimit': (185, None, True, False), # ≥ 185
        'Exceeds_UpperCautionLimit': (175, 185, True, False), # 175 ≤ ppO2 < 185
        'Nominal': (155, 175, False, False), # 155 < ppO2 < 175 --> Nominal: 163.79 mmHg
        'Exceeds_LowerCautionLimit': (145, 155, False, True), # 145 < ppO2 ≤ 155
        'Exceeds_LowerWarningLimit': (None, 145, False, True) # ≤ 145
    },
    "ppO2_HALO (HALO)": {
        'Exceeds_UpperWarningLimit': (185, None, True, False),
        'Exceeds_UpperCautionLimit': (175, 185, True, False),
        'Nominal': (155, 175, False, False), # Nominal: 163.81 mmHg
        'Exceeds_LowerCautionLimit': (145, 155, False, True),
        'Exceeds_LowerWarningLimit': (None, 145, False, True)
    },
    "Total_Cabin_Pressure_IHab (IHab)": {
        'Exceeds_UpperWarningLimit': (15.2, None, True, False),
        'Exceeds_UpperCautionLimit': (14.9, 15.2, True, False),
        'Nominal': (14.55, 14.9, False, False), # Nominal: 14.7 psi (IHab = HALO)
        'Exceeds_LowerCautionLimit': (12.7, 14.55, False, True),
        'Exceeds_LowerWarningLimit': (None, 12.7, False, True)
    },
    "Total_Cabin_Pressure_HALO (HALO)": {
        'Exceeds_UpperWarningLimit': (15.2, None, True, False),
        'Exceeds_UpperCautionLimit': (14.9, 15.2, True, False),
        'Nominal': (14.55, 14.9, False, False), # Nominal: 14.7 psi (IHab = HALO)
        'Exceeds_LowerCautionLimit': (12.7, 14.55, False, True),
        'Exceeds_LowerWarningLimit': (None, 12.7, False, True)
    }
}

# Duplicate the 'current' parameter ranges to capture the temporal changes with the (t-1) variables
temporal_ranges = {}

for parameter, ranges in measurement_ranges.items():
    temporal_ranges[parameter] = ranges
    temporal_ranges[f"{parameter} (t-1)"] = ranges
# Reassign values to measurement_ranges dictionary for subsequent reference elsewhere in code
measurement_ranges = temporal_ranges