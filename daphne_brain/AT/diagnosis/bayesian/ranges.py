# ranges.py
# Author: Joshua Elston
# Last Edited: 12/11/2024

# Stores the measurement_ranges dictionary --> called in probabilities.py

# 35 (out of 65 distinct (and 79 total)) measurement ranges from Neo4j are summarized below. The criteria for including these measurements are:
#   1) Must be a unique measurement (those measured independently for L1 and L2 in HERA only mentioned once) <-- such measurements are also identified with notes
#   2) Measurement must be included in Neo4j
#   3) Measurement must be related to at least one anomaly in Neo4j
# Measurements not satisfying either criterion 2 or 3 are included in the [UNUSED]ranges.py script

# NOTE: H2O pH, LiOH CO2 Saturation, and MOXIE Telemetry Quality are all associated with anomalies within Neo4j, but are not
# included in the HSS on Kazuki's lab machine. They are still reported here to match the KG, but this discrepancy should be
# resolved in future

# Example bound meanings are shown for ppO2 (lines 227-233)

# Create a dictionary to store the measurement ranges for each of the parameters being measured
measurement_ranges = {
    "2-butanone": {
        'Exceeds_UpperWarningLimit': (0.1, None, True, False),
        'Exceeds_UpperCautionLimit': (0.04, 0.1, True, False),
        'Nominal': (-1, 0.04, False, False), # Nominal: 0 ppm
        'Exceeds_LowerCautionLimit': (-2, -1, False, True),
        'Exceeds_LowerWarningLimit': (None, -2, False, True)
    },
    "Acetaldehyde": {
        'Exceeds_UpperWarningLimit': (0.4, None, True, False),
        'Exceeds_UpperCautionLimit': (0.28, 0.4, True, False),
        'Nominal': (-1, 0.28, False, False), # Nominal: 0.17 ppm
        'Exceeds_LowerCautionLimit': (-2, -1, False, True),
        'Exceeds_LowerWarningLimit': (None, -2, False, True)
    },
    "Aux Cabin Fan #1": {
        'Exceeds_UpperWarningLimit': (4000, None, True, False),
        'Exceeds_UpperCautionLimit': (3900, 4000, True, False),
        'Nominal': (3500, 3900, False, False), # Nominal: 3880 rpm
        'Exceeds_LowerCautionLimit': (1500, 3500, False, True),
        'Exceeds_LowerWarningLimit': (None, 1500, False, True)
    },
    "Aux Cabin Fan #2": {
        'Exceeds_UpperWarningLimit': (4000, None, True, False),
        'Exceeds_UpperCautionLimit': (3900, 4000, True, False),
        'Nominal': (3500, 3900, False, False), # Nominal: 3879 rpm
        'Exceeds_LowerCautionLimit': (1500, 3500, False, True),
        'Exceeds_LowerWarningLimit': (None, 1500, False, True)
    },
    "Cabin Temperature": { # NOTE: Only one Temperature value is stored, though it is separately measured on L1 and L2
        'Exceeds_UpperWarningLimit': (87.7, None, True, False),
        'Exceeds_UpperCautionLimit': (79, 87.7, True, False),
        'Nominal': (68, 79, False, False), # Nominal: 72.3°F (L1 = L2)
        'Exceeds_LowerCautionLimit': (64, 68, False, True),
        'Exceeds_LowerWarningLimit': (None, 64, False, True)
    },
    "Dichloromethane": {
        'Exceeds_UpperWarningLimit': (0.16, None, True, False),
        'Exceeds_UpperCautionLimit': (0.1, 0.16, True, False),
        'Nominal': (-1, 0.1, False, False), # Nominal: 0.05 ppm
        'Exceeds_LowerCautionLimit': (-2, -1, False, True),
        'Exceeds_LowerWarningLimit': (None, -2, False, True)
    },
    "Fuel Cell #1 Current": {
        'Exceeds_UpperWarningLimit': (75, None, True, False),
        'Exceeds_UpperCautionLimit': (68, 75, True, False),
        'Nominal': (55, 68, False, False), # Nominal: 60.2 amps
        'Exceeds_LowerCautionLimit': (48, 55, False, True),
        'Exceeds_LowerWarningLimit': (None, 48, False, True)        
    },
    "Fuel Cell #1 PQM": {
        'Exceeds_UpperWarningLimit': (120, None, True, False),
        'Exceeds_UpperCautionLimit': (110, 120, True, False),
        'Nominal': (85, 110, False, False), # Nominal: 100%
        'Exceeds_LowerCautionLimit': (70, 85, False, True),
        'Exceeds_LowerWarningLimit': (None, 70, False, True)
    },
    "Fuel Cell #1 Stack Out Temp": {
        'Exceeds_UpperWarningLimit': (1350, None, True, False),
        'Exceeds_UpperCautionLimit': (1250, 1350, True, False),
        'Nominal': (1050, 1250, False, False), # Nominal: 1125°F
        'Exceeds_LowerCautionLimit': (950, 1050, False, True),
        'Exceeds_LowerWarningLimit': (None, 950, False, True)
    },
    "Fuel Cell #1 Voltage": {
        'Exceeds_UpperWarningLimit': (30.2, None, True, False),
        'Exceeds_UpperCautionLimit': (29, 30.2, True, False),
        'Nominal': (27.6, 29, False, False), # Nominal: 28.6 Vdc
        'Exceeds_LowerCautionLimit': (25.2, 27.6, False, True),
        'Exceeds_LowerWarningLimit': (None, 25.2, False, True)
    },
    "Fuel Cell #2 Current": {
        'Exceeds_UpperWarningLimit': (75, None, True, False),
        'Exceeds_UpperCautionLimit': (68, 75, True, False),
        'Nominal': (55, 68, False, False), # Nominal: 60.2 amps
        'Exceeds_LowerCautionLimit': (48, 55, False, True),
        'Exceeds_LowerWarningLimit': (None, 48, False, True)
    },
    "Fuel Cell #2 PQM": {
        'Exceeds_UpperWarningLimit': (120, None, True, False),
        'Exceeds_UpperCautionLimit': (110, 120, True, False),
        'Nominal': (85, 110, False, False), # Nominal: 99.99%
        'Exceeds_LowerCautionLimit': (70, 85, False, True),
        'Exceeds_LowerWarningLimit': (None, 70, False, True)
    },
    "Fuel Cell #2 Stack Out Temp": {
        'Exceeds_UpperWarningLimit': (1350, None, True, False),
        'Exceeds_UpperCautionLimit': (1250, 1350, True, False),
        'Nominal': (1050, 1250, False, False), # Nominal: 1125°F
        'Exceeds_LowerCautionLimit': (950, 1050, False, True),
        'Exceeds_LowerWarningLimit': (None, 950, False, True)
    },
    "Fuel Cell #2 Voltage": {
        'Exceeds_UpperWarningLimit': (30.2, None, True, False),
        'Exceeds_UpperCautionLimit': (29, 30.2, True, False),
        'Nominal': (27.6, 29, False, False), # Nominal: 28.6 Vdc
        'Exceeds_LowerCautionLimit': (25.2, 27.6, False, True),
        'Exceeds_LowerWarningLimit': (None, 25.2, False, True)
    },
    "H2O (Crew)": {
        'Exceeds_UpperWarningLimit': (5, None, True, False),
        'Exceeds_UpperCautionLimit': (4.5, 5, True, False),
        'Nominal': (2.5, 4.5, False, False), # Nominal: 3.6 gal
        'Exceeds_LowerCautionLimit': (2, 2.5, False, True),
        'Exceeds_LowerWarningLimit': (None, 2, False, True)
    },
    # NOTE: H2O pH appears in Neo4j in relation to the WRS Off-nominal pH Level anomaly, but is not mentioned on the HSS machine
    "H2O pH": {
        'Exceeds_UpperWarningLimit': (9, None, True, False),
        'Exceeds_UpperCautionLimit': (8, 9, True, False),
        'Nominal': (6, 8, False, False), # Nominal: 7 pH
        'Exceeds_LowerCautionLimit': (5, 6, False, True),
        'Exceeds_LowerWarningLimit': (None, 5, False, True)
    },
    "HMCTS": {
        'Exceeds_UpperWarningLimit': (1.7, None, True, False),
        'Exceeds_UpperCautionLimit': (1.2, 1.7, True, False),
        'Nominal': (-1, 1.2, False, False), # Nominal: 0.66 ppm
        'Exceeds_LowerCautionLimit': (-2, -1, False, True),
        'Exceeds_LowerWarningLimit': (None, -2, False, True)
    },
    "Humidity": { # NOTE: Only one Humidity value is stored, though it is separately measured on L1 and L2
        'Exceeds_UpperWarningLimit': (70, None, True, False),
        'Exceeds_UpperCautionLimit': (61, 70, True, False),
        'Nominal': (50, 61, False, False), # Nominal: 52.01% (L1 = L2)
        'Exceeds_LowerCautionLimit': (40, 50, False, True),
        'Exceeds_LowerWarningLimit': (None, 40, False, True)
    },
    # NOTE: LiOH CO2 Saturation appears in Neo4j in relation to the CDRA LiOH Canister Saturation anomaly, but is not mentioned on the HSS machine
    "LiOH CO2 Saturation": {
        'Exceeds_UpperWarningLimit': (80, None, True, False),
        'Exceeds_UpperCautionLimit': (60, 80, True, False),
        'Nominal': (-40, 60, False, False), # Nominal: 0%
        'Exceeds_LowerCautionLimit': (-60, -40, False, True),
        'Exceeds_LowerWarningLimit': (None, -60, False, True)
    },
    "Main Cabin Fan #1": {
        'Exceeds_UpperWarningLimit': (9000, None, True, False),
        'Exceeds_UpperCautionLimit': (8500, 9000, True, False),
        'Nominal': (3700, 8500, False, False), # Nominal: 4052 rpm
        'Exceeds_LowerCautionLimit': (1900, 3700, False, True),
        'Exceeds_LowerWarningLimit': (None, 1900, False, True)
    },
    "Main Cabin Fan #2": {
        'Exceeds_UpperWarningLimit': (9000, None, True, False),
        'Exceeds_UpperCautionLimit': (8500, 9000, True, False),
        'Nominal': (3700, 8500, False, False), # Nominal: 4050 rpm
        'Exceeds_LowerCautionLimit': (1900, 3700, False, True),
        'Exceeds_LowerWarningLimit': (None, 1900, False, True)
    },
    "MOXIE Compressor Temp": {
        'Exceeds_UpperWarningLimit': (180, None, True, False),
        'Exceeds_UpperCautionLimit': (170, 180, True, False),
        'Nominal': (140, 170, False, False), # Nominal: 160°F
        'Exceeds_LowerCautionLimit': (120, 140, False, True),
        'Exceeds_LowerWarningLimit': (None, 120, False, True)
    },
    # NOTE: MOXIE Telemetry Quality appears in Neo4j in relation to the MOXIE Antenna Failure, but is not mentioned on the HSS machine
    "MOXIE Telemetry Quality": {
        'Exceeds_UpperWarningLimit': (105, None, True, False),
        'Exceeds_UpperCautionLimit': (102, 105, True, False),
        'Nominal': (75, 102, False, False), # Nominal: 99.9%
        'Exceeds_LowerCautionLimit': (20, 75, False, True),
        'Exceeds_LowerWarningLimit': (None, 20, False, True)
    },
    "n_Butanol": {
        'Exceeds_UpperWarningLimit': (0.1, None, True, False),
        'Exceeds_UpperCautionLimit': (0.07, 0.1, True, False),
        'Nominal': (-1, 0.07, False, False), # Nominal: 0.02 ppm
        'Exceeds_LowerCautionLimit': (-2, -1, False, True),
        'Exceeds_LowerWarningLimit': (None, -2, False, True)
    },
    "PDU 4 Bank 1": { # NOTE: In spreadsheet, listed as "PDU 4 Bank1" <-- check if this is the same in Neo4j
        'Exceeds_UpperWarningLimit': (30, None, True, False),
        'Exceeds_UpperCautionLimit': (25, 30, True, False),
        'Nominal': (5, 25, False, False), # Nominal: 20.1 amps
        'Exceeds_LowerCautionLimit': (2, 5, False, True),
        'Exceeds_LowerWarningLimit': (None, 2, False, True)
    },
    "PDU 5 Bank 1": {
        'Exceeds_UpperWarningLimit': (30, None, True, False),
        'Exceeds_UpperCautionLimit': (25, 30, True, False),
        'Nominal': (5, 25, False, False), # Nominal: 20 amps
        'Exceeds_LowerCautionLimit': (2, 5, False, True),
        'Exceeds_LowerWarningLimit': (None, 2, False, True)
    },
    "ppCO2": { # NOTE: Only one ppCO2 value is stored, though it is separately measured on L1 and L2
        'Exceeds_UpperWarningLimit': (6, None, True, False),
        'Exceeds_UpperCautionLimit': (4.5, 6, True, False),
        'Nominal': (-1, 4.5, False, False), # Nominal: 2.59 mmHG (L1 = L2)
        'Exceeds_LowerCautionLimit': (-2, -1, False, True),
        'Exceeds_LowerWarningLimit': (None, -2, False, True)
    },
    "ppH2": { # NOTE: Only one ppH2 value is stored, though it is separately measured on L1 and L2
        'Exceeds_UpperWarningLimit': (0.1, None, True, False),
        'Exceeds_UpperCautionLimit': (0.07, 0.1, True, False),
        'Nominal': (0.02, 0.07, False, False), # Nominal: 0.04 mmHG (L1 = L2)
        'Exceeds_LowerCautionLimit': (0.01, 0.02, False, True),
        'Exceeds_LowerWarningLimit': (None, 0.01, False, True)
    },
    "ppN2": { # NOTE: Only one ppN2 value is stored, though it is separately measured on L1 and L2
        'Exceeds_UpperWarningLimit': (600, None, True, False),
        'Exceeds_UpperCautionLimit': (591, 600, True, False),
        'Nominal': (480, 591, False, False), # NOTE: L1 Nominal: 581.75 mmHG, L2 Nominal: 581.84 mmHG
        'Exceeds_LowerCautionLimit': (220.1, 480, False, True),
        'Exceeds_LowerWarningLimit': (None, 220.1, False, True)
    },
    "ppO2": { # NOTE: Only one ppO2 value is stored, though it is separately measured on L1 and L2
        'Exceeds_UpperWarningLimit': (185, None, True, False), # ≥ 185
        'Exceeds_UpperCautionLimit': (175, 185, True, False), # 175 ≤ ppO2 < 185
        'Nominal': (155, 175, False, False), # 155 < ppO2 < 175 --> NOTE: L1 Nominal: 163.79 mmHG, L2 Nominal: 163.81 mmHG
        'Exceeds_LowerCautionLimit': (145, 155, False, True), # 145 < ppO2 ≤ 155
        'Exceeds_LowerWarningLimit': (None, 145, False, True) # ≤ 145
    },
    "Pressure": { # NOTE: Only one Pressure value is stored, though it is separately measured on L1 and L2
        'Exceeds_UpperWarningLimit': (1.5, None, True, False),
        'Exceeds_UpperCautionLimit': (1.15, 1.5, True, False),
        'Nominal': (0.89, 1.15, False, False), # NOTE: L1 Nominal: 0.99 atm, L2 Nominal: 0.98 atm
        'Exceeds_LowerCautionLimit': (0.58, 0.89, False, True),
        'Exceeds_LowerWarningLimit': (None, 0.58, False, True)
    },
    "SOXIE Stack Temp": {
        'Exceeds_UpperWarningLimit': (1670, None, True, False),
        'Exceeds_UpperCautionLimit': (1629, 1670, True, False),
        'Nominal': (1333, 1629, False, False), # Nominal: 1481°F
        'Exceeds_LowerCautionLimit': (1292, 1333, False, True),
        'Exceeds_LowerWarningLimit': (None, 1292, False, True)
    },
    "Total Cabin Pressure": { # NOTE: Only one Total Cabin Pressure value is stored, though it is separately measured on L1 and L2
        'Exceeds_UpperWarningLimit': (15.2, None, True, False),
        'Exceeds_UpperCautionLimit': (14.9, 15.2, True, False),
        'Nominal': (14.55, 14.9, False, False), # Nominal: 14.7 psi (L1 = L2)
        'Exceeds_LowerCautionLimit': (12.7, 14.55, False, True),
        'Exceeds_LowerWarningLimit': (None, 12.7, False, True)
    },
    "WRS Delivery Pump": {
        'Exceeds_UpperWarningLimit': (3, None, True, False),
        'Exceeds_UpperCautionLimit': (2.8, 3, True, False),
        'Nominal': (1.8, 2.8, False, False), # Nominal: 2.5 gal/hr
        'Exceeds_LowerCautionLimit': (1, 1.8, False, True),
        'Exceeds_LowerWarningLimit': (None, 1, False, True)
    },
    "WRS Valve Flow": {
        'Exceeds_UpperWarningLimit': (9.5, None, True, False),
        'Exceeds_UpperCautionLimit': (8, 9.5, True, False),
        'Nominal': (4, 8, False, False), # Nominal: 6 gal/hr
        'Exceeds_LowerCautionLimit': (2, 4, False, True),
        'Exceeds_LowerWarningLimit': (None, 2, False, True)
    }
}

##
# Function to test that symptom ranges are correctly returned
def get_measurement_range(symptom, value):
    # Check if the symptom exists in the dictionary
    if symptom not in measurement_ranges:
        return f"Symptom '{symptom}' is not defined."
    
    for range_name, (min_val, max_val, min_inclusive, max_inclusive) in measurement_ranges[symptom].items():
        if (min_inclusive and value >= min_val or not min_inclusive and value > min_val) and \
           (max_inclusive and (max_val is None or value <= max_val) or not max_inclusive and (max_val is None or value < max_val)):
            return range_name 
    return 'Value is outside of defined ranges.'

# # Prompt the user for an input to test the ranges
# try:
#     symptom_input = input("Enter the symptom you want to test (e.g., 'ppO2'): ").strip()
#     value_input = float(input(f"Enter the {symptom_input} value: "))
#     result = get_measurement_range(symptom_input, value_input)
#     print(f"The {symptom_input} value {value_input} falls into the range: {result}")
# except ValueError:
#     print("Please enter a valid numerical value.")
# print()