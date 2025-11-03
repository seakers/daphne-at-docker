# prior_probabilities.py
# Author: Joshua Elston
# Last Edited: 11/01/2025

# Prior probabilities for network anomalies --> called in ECLSS Bayesian Network.py
# From Neo4j, contains prior probabilities for 31 unique anomalies
# NOTE: These probabilities have been determined by hand, so tweaks may be required if unexpected results occur
# Changes on 11/01/2025 updated the priors to correspond to the level-specific failures (where applicable)
# so that the probabilities influencing the No Anomalies Present calculation were structured correctly

# Prior probabilities of anomalies:
prior_probabilities = {
    # "Biological Filter Saturation": 10**-4,
    "Biological Filter Saturation (L1)": 10**-4,
    "Biological Filter Saturation (L2)": 10**-4,
    # "CDRA Failure": 10**-4,
    "CDRA Failure (L1)": 10**-4,
    "CDRA Failure (L2)": 10**-4,
    # "CDRA LiOH Canister Saturation": 10**-3,
    "CDRA LiOH Canister Saturation (L1)": 10**-3,
    "CDRA LiOH Canister Saturation (L2)": 10**-3,
    # "Electrolysis System Failure": 10**-4,
    "Electrolysis System Failure (L1)": 10**-4,
    "Electrolysis System Failure (L2)": 10**-4,
    # "Emergency O2 System Maintenance": 10**-4,
    "Emergency O2 System Maintenance (L1)": 10**-4,
    "Emergency O2 System Maintenance (L2)": 10**-4,
    # "Excess CO2 in Cabin": 10**-4,
    "Excess CO2 in Cabin (L1)": 10**-4,
    "Excess CO2 in Cabin (L2)": 10**-4,
    # "Excess Gas Leak": 10**-5,
    "Excess Gas Leak (L1)": 10**-5,
    "Excess Gas Leak (L2)": 10**-5,
    # "Excess Water Vapor Pressure in Cabin": 10**-4,
    "Excess Water Vapor Pressure in Cabin (L1)": 10**-4,
    "Excess Water Vapor Pressure in Cabin (L2)": 10**-4,
    "Fuel Cell #1 and PDU Failure": 10**-4,
    "Fuel Cell #2 and PDU Failure": 10**-4,
    "Fuel Cell Degrade": 10**-3,
    "Fuel Cell Failure": 10**-4,
    # "Loss of Pressure": 10**-5,
    "Loss of Pressure (L1)": 10**-5,
    "Loss of Pressure (L2)": 10**-5,
    # "Main Cabin Fan Failure": 10**-3,
    "Main Cabin Fan Failure (L1)": 10**-3,
    "Main Cabin Fan Failure (L2)": 10**-3,
    "MOXIE Antenna Failure": 10**-4,
    "MOXIE ECM Failure": 10**-4,
    "MOXIE Fan Failure": 10**-4,
    # "N2 Tank Burst": 10**-5,
    "N2 Tank Burst (L1)": 10**-5,
    "N2 Tank Burst (L2)": 10**-5,
    # "PDU 4 Failure": 10**-4,
    "PDU 4 Failure (L1)": 10**-4,
    "PDU 4 Failure (L2)": 10**-4,
    # "PDU 5 Failure": 10**-4,
    "PDU 5 Failure (L1)": 10**-4,
    "PDU 5 Failure (L2)": 10**-4,
    "Reduced Main Cabin Fan #1 Capacity": 10**-2,
    # "RWGSR Malfunction": 10**-4,
    "RWGSR Malfunction (L1)": 10**-4,
    "RWGSR Malfunction (L2)": 10**-4,
    "SPE System Maintenance": 10**-2,
    "TCCS Auxiliary Fan #1 Failure": 10**-3,
    "TCCS Auxiliary Fan #2 Failure": 10**-3,
    "TCCS Auxiliary Fan at Reduced Capacity": 10**-2,
    "TCCS Filter Clog": 10**-3,
    "Trace Contaminants": 10**-3,
    "WRS Failure": 10**-4,
    "WRS Maintenance": 10**-2,
    "WRS Off-nominal pH Level": 10**-4
}