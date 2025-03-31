# prior_probabilities.py
# Author: Joshua Elston
# Last Edited: 12/12/2024

# Prior probabilities for network anomalies --> called in ECLSS Bayesian Network.py
# From Neo4j, contains prior probabilities for 31 unique anomalies
# These probabilities have been determined by hand, so tweaks may be required if unexpected results occur

# Prior probabilities of anomalies:
prior_probabilities = {
    "Biological Filter Saturation": 10**-4,
    "CDRA Failure": 10**-4,
    "CDRA LiOH Canister Saturation": 10**-3,
    "Electrolysis System Failure": 10**-4,
    "Emergency O2 System Maintenance": 10**-4,
    "Excess CO2 in Cabin": 10**-4,
    "Excess Gas Leak": 10**-5,
    "Excess Water Vapor Pressure in Cabin": 10**-4,
    "Fuel Cell #1 and PDU Failure": 10**-4,
    "Fuel Cell #2 and PDU Failure": 10**-4,
    "Fuel Cell Degrade": 10**-3,
    "Fuel Cell Failure": 10**-4,
    "Loss of Pressure": 10**-5,
    "Main Cabin Fan Failure": 10**-3,
    "MOXIE Antenna Failure": 10**-4,
    "MOXIE ECM Failure": 10**-4,
    "MOXIE Fan Failure": 10**-4,
    "N2 Tank Burst": 10**-5,
    "PDU 4 Failure": 10**-4,
    "PDU 5 Failure": 10**-4,
    "Reduced Main Cabin Fan #1 Capacity": 10**-2,
    "RWGSR Malfunction": 10**-4,
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