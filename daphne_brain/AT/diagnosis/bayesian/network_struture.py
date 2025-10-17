# network_struture.py
# Author: Joshua Elston
# Last Updated: 10/16/2025

# Define Bayesian network structure --> called in ECLSS_Bayesian_Network.py

# Define the Bayesian network structure ("ANOMALY", "high/low PARAMETER")
# There are 31 anomalies and 79 measurements present in Neo4j. Of these 79 measurements, 35 are unique and directly related to one of the
# 31 aforementioned anomalies, meaning the total network structure below consists of 31 anomalies and 43 measurements. These have been
# updated to include the 8 parameters whose values are measured separately on L1 and L2.
# (See ranges.py for more details)
# 31 hidden nodes, each uniquely related to a specific anomaly, are added with connections to all network anomalies to accurately reflect
# changes in entropy when querying the network with additional evidence. The addition of these hidden node connections is achieved using
# the for loop at the bottom of the script
# Changes on 10/16/2025 split failures into different levels if they have symptoms measured seperately
# on L1 and L2 in order for the probabilities to accurately reflect the presence of a failure
# This is the case for 14 anomalies, who have seperate L1 and L2 failures while also being combined into
# a single anomaly at the end

from collections import defaultdict

network = [
    # Biological Filter Saturation (L1)
    ("Biological Filter Saturation (L1)", "high ppCO2 (L1)"), ("Biological Filter Saturation (L1)", "high ppCO2 (L1) (t-1)"),
    ("Biological Filter Saturation (L1)", "high ppO2 (L1)"), ("Biological Filter Saturation (L1)", "high ppO2 (L1) (t-1)"),
    ("Biological Filter Saturation (L1)", "low ppCO2 (L1)"), ("Biological Filter Saturation (L1)", "low ppCO2 (L1) (t-1)"),
    ("Biological Filter Saturation (L1)", "low ppO2 (L1)"), ("Biological Filter Saturation (L1)", "low ppO2 (L1) (t-1)"),
    ("Biological Filter Saturation (L1)", "[HIDDEN] BFS Component"),

    # Biological Filter Saturation (L2)
    ("Biological Filter Saturation (L2)", "high ppCO2 (L2)"), ("Biological Filter Saturation (L2)", "high ppCO2 (L2) (t-1)"),
    ("Biological Filter Saturation (L2)", "high ppO2 (L2)"), ("Biological Filter Saturation (L2)", "high ppO2 (L2) (t-1)"),
    ("Biological Filter Saturation (L2)", "low ppCO2 (L2)"), ("Biological Filter Saturation (L2)", "low ppCO2 (L2) (t-1)"),
    ("Biological Filter Saturation (L2)", "low ppO2 (L2)"), ("Biological Filter Saturation (L2)", "low ppO2 (L2) (t-1)"),
    ("Biological Filter Saturation (L2)", "[HIDDEN] BFS Component"),

    # Biological Filter Saturation (Combined)
    ("Biological Filter Saturation", "Biological Filter Saturation (L1)"),
    ("Biological Filter Saturation", "Biological Filter Saturation (L2)"),

    # CDRA Failure (L1)
    ("CDRA Failure (L1)", "high Humidity (L1)"), ("CDRA Failure (L1)", "high Humidity (L1) (t-1)"), 
    ("CDRA Failure (L1)", "high ppCO2 (L1)"), ("CDRA Failure (L1)", "high ppCO2 (L1) (t-1)"), 
    ("CDRA Failure (L1)", "high ppO2 (L1)"), ("CDRA Failure (L1)", "high ppO2 (L1) (t-1)"), 
    ("CDRA Failure (L1)", "low Humidity (L1)"), ("CDRA Failure (L1)", "low Humidity (L1) (t-1)"),
    ("CDRA Failure (L1)", "low ppCO2 (L1)"), ("CDRA Failure (L1)", "low ppCO2 (L1) (t-1)"),
    ("CDRA Failure (L1)", "low ppO2 (L1)"), ("CDRA Failure (L1)", "low ppO2 (L1) (t-1)"),
    ("CDRA Failure (L1)", "[HIDDEN] CDRA Failure Component"),

    # CDRA Failure (L2)
    ("CDRA Failure (L2)", "high Humidity (L2)"), ("CDRA Failure (L2)", "high Humidity (L2) (t-1)"),
    ("CDRA Failure (L2)", "high ppCO2 (L2)"), ("CDRA Failure (L2)", "high ppCO2 (L2) (t-1)"),
    ("CDRA Failure (L2)", "high ppO2 (L2)"), ("CDRA Failure (L2)", "high ppO2 (L2) (t-1)"),
    ("CDRA Failure (L2)", "low Humidity (L2)"), ("CDRA Failure (L2)", "low Humidity (L2) (t-1)"),
    ("CDRA Failure (L2)", "low ppCO2 (L2)"), ("CDRA Failure (L2)", "low ppCO2 (L2) (t-1)"),
    ("CDRA Failure (L2)", "low ppO2 (L2)"), ("CDRA Failure (L2)", "low ppO2 (L2) (t-1)"),
    ("CDRA Failure (L2)", "[HIDDEN] CDRA Failure Component"),

    # CDRA Failure (Combined)
    ("CDRA Failure", "CDRA Failure (L1)"),
    ("CDRA Failure", "CDRA Failure (L2)"),

    # CDRA LiOH Canister Saturation (L1)
    ("CDRA LiOH Canister Saturation (L1)", "high ppCO2 (L1)"), ("CDRA LiOH Canister Saturation (L1)", "high ppCO2 (L1) (t-1)"),
    ("CDRA LiOH Canister Saturation (L1)", "high ppO2 (L1)"), ("CDRA LiOH Canister Saturation (L1)", "high ppO2 (L1) (t-1)"),
    ("CDRA LiOH Canister Saturation (L1)", "high LiOH CO2 Saturation"), ("CDRA LiOH Canister Saturation (L1)", "high LiOH CO2 Saturation (t-1)"),
    ("CDRA LiOH Canister Saturation (L1)", "low ppCO2 (L1)"), ("CDRA LiOH Canister Saturation (L1)", "low ppCO2 (L1) (t-1)"),
    ("CDRA LiOH Canister Saturation (L1)", "low ppO2 (L1)"), ("CDRA LiOH Canister Saturation (L1)", "low ppO2 (L1) (t-1)"),
    ("CDRA LiOH Canister Saturation (L1)", "low LiOH CO2 Saturation"), ("CDRA LiOH Canister Saturation (L1)", "low LiOH CO2 Saturation (t-1)"),
    ("CDRA LiOH Canister Saturation (L1)", "[HIDDEN] CDRA LiOH Canister Saturation Component"),

    # CDRA LiOH Canister Saturation (L2)
    ("CDRA LiOH Canister Saturation (L2)", "high ppCO2 (L2)"), ("CDRA LiOH Canister Saturation (L2)", "high ppCO2 (L2) (t-1)"),
    ("CDRA LiOH Canister Saturation (L2)", "high ppO2 (L2)"), ("CDRA LiOH Canister Saturation (L2)", "high ppO2 (L2) (t-1)"),
    ("CDRA LiOH Canister Saturation (L2)", "high LiOH CO2 Saturation"), ("CDRA LiOH Canister Saturation (L2)", "high LiOH CO2 Saturation (t-1)"),
    ("CDRA LiOH Canister Saturation (L2)", "low ppCO2 (L2)"), ("CDRA LiOH Canister Saturation (L2)", "low ppCO2 (L2) (t-1)"),
    ("CDRA LiOH Canister Saturation (L2)", "low ppO2 (L2)"), ("CDRA LiOH Canister Saturation (L2)", "low ppO2 (L2) (t-1)"),
    ("CDRA LiOH Canister Saturation (L2)", "low LiOH CO2 Saturation"), ("CDRA LiOH Canister Saturation (L2)", "low LiOH CO2 Saturation (t-1)"),
    ("CDRA LiOH Canister Saturation (L2)", "[HIDDEN] CDRA LiOH Canister Saturation Component"),

    # CDRA LiOH Canister Saturation (Combined)
    ("CDRA LiOH Canister Saturation", "CDRA LiOH Canister Saturation (L1)"),
    ("CDRA LiOH Canister Saturation", "CDRA LiOH Canister Saturation (L2)"),

    # Electrolysis System Failure (L1)
    ("Electrolysis System Failure (L1)", "high H2O (Crew)"), ("Electrolysis System Failure (L1)", "high H2O (Crew) (t-1)"),
    ("Electrolysis System Failure (L1)", "high ppO2 (L1)"), ("Electrolysis System Failure (L1)", "high ppO2 (L1) (t-1)"), 
    ("Electrolysis System Failure (L1)", "low H2O (Crew)"), ("Electrolysis System Failure (L1)", "low H2O (Crew) (t-1)"),
    ("Electrolysis System Failure (L1)", "low ppO2 (L1)"), ("Electrolysis System Failure (L1)", "low ppO2 (L1) (t-1)"),
    ("Electrolysis System Failure (L1)", "[HIDDEN] Electrolysis System Failure Component"),

    # Electrolysis System Failure (L2)
    ("Electrolysis System Failure (L2)", "high H2O (Crew)"), ("Electrolysis System Failure (L2)", "high H2O (Crew) (t-1)"),
    ("Electrolysis System Failure (L2)", "high ppO2 (L2)"), ("Electrolysis System Failure (L2)", "high ppO2 (L2) (t-1)"),
    ("Electrolysis System Failure (L2)", "low H2O (Crew)"), ("Electrolysis System Failure (L2)", "low H2O (Crew) (t-1)"),
    ("Electrolysis System Failure (L2)", "low ppO2 (L2)"), ("Electrolysis System Failure (L2)", "low ppO2 (L2) (t-1)"),
    ("Electrolysis System Failure (L2)", "[HIDDEN] Electrolysis System Failure Component"),

    # Electrolysis System Failure (Combined)
    ("Electrolysis System Failure", "Electrolysis System Failure (L1)"),
    ("Electrolysis System Failure", "Electrolysis System Failure (L2)"),

    # Emergency O2 System Maintenance
    ("Emergency O2 System Maintenance (L1)", "high ppO2 (L1)"), ("Emergency O2 System Maintenance (L1)", "high ppO2 (L1) (t-1)"),
    ("Emergency O2 System Maintenance (L1)", "low ppO2 (L1)"), ("Emergency O2 System Maintenance (L1)", "low ppO2 (L1) (t-1)"),
    ("Emergency O2 System Maintenance (L1)", "[HIDDEN] Emergency O2 System Maintenance Component"),

    # Emergency O2 System Maintenance (L2)
    ("Emergency O2 System Maintenance (L2)", "high ppO2 (L2)"), ("Emergency O2 System Maintenance (L2)", "high ppO2 (L2) (t-1)"),
    ("Emergency O2 System Maintenance (L2)", "low ppO2 (L2)"), ("Emergency O2 System Maintenance (L2)", "low ppO2 (L2) (t-1)"),
    ("Emergency O2 System Maintenance (L2)", "[HIDDEN] Emergency O2 System Maintenance Component"),

    # Emergency O2 System Maintenance (Combined)
    ("Emergency O2 System Maintenance", "Emergency O2 System Maintenance (L1)"),
    ("Emergency O2 System Maintenance", "Emergency O2 System Maintenance (L2)"),

    # Excess CO2 in Cabin (L1)
    ("Excess CO2 in Cabin (L1)", "high ppCO2 (L1)"), ("Excess CO2 in Cabin (L1)", "high ppCO2 (L1) (t-1)"),
    ("Excess CO2 in Cabin (L1)", "low ppCO2 (L1)"), ("Excess CO2 in Cabin (L1)", "low ppCO2 (L1) (t-1)"),
    ("Excess CO2 in Cabin (L1)", "[HIDDEN] Excess CO2 in Cabin Component"),

    # Excess CO2 in Cabin (L2)
    ("Excess CO2 in Cabin (L2)", "high ppCO2 (L2)"), ("Excess CO2 in Cabin (L2)", "high ppCO2 (L2) (t-1)"),
    ("Excess CO2 in Cabin (L2)", "low ppCO2 (L2)"), ("Excess CO2 in Cabin (L2)", "low ppCO2 (L2) (t-1)"),
    ("Excess CO2 in Cabin (L2)", "[HIDDEN] Excess CO2 in Cabin Component"),

    # Excess CO2 in Cabin (Combined)
    ("Excess CO2 in Cabin", "Excess CO2 in Cabin (L1)"),
    ("Excess CO2 in Cabin", "Excess CO2 in Cabin (L2)"),

    # Excess Gas Leak (L1)
    ("Excess Gas Leak (L1)", "high ppH2 (L1)"), ("Excess Gas Leak (L1)", "high ppH2 (L1) (t-1)"),
    ("Excess Gas Leak (L1)", "low ppH2 (L1)"), ("Excess Gas Leak (L1)", "low ppH2 (L1) (t-1)"),
    ("Excess Gas Leak (L1)", "[HIDDEN] Excess Gas Leak Component"),

    # Excess Gas Leak (L2)
    ("Excess Gas Leak (L2)", "high ppH2 (L2)"), ("Excess Gas Leak (L2)", "high ppH2 (L2) (t-1)"),
    ("Excess Gas Leak (L2)", "low ppH2 (L2)"), ("Excess Gas Leak (L2)", "low ppH2 (L2) (t-1)"),
    ("Excess Gas Leak (L2)", "[HIDDEN] Excess Gas Leak Component"),

    # Excess Gas Leak (Combined)
    ("Excess Gas Leak", "Excess Gas Leak (L1)"),
    ("Excess Gas Leak", "Excess Gas Leak (L2)"),

    # Excess Water Vapor Pressure in Cabin (L1)
    ("Excess Water Vapor Pressure in Cabin (L1)", "high Cabin Temperature (L1)"), ("Excess Water Vapor Pressure in Cabin (L1)", "high Cabin Temperature (L1) (t-1)"), 
    ("Excess Water Vapor Pressure in Cabin (L1)", "high Humidity (L1)"), ("Excess Water Vapor Pressure in Cabin (L1)", "high Humidity (L1) (t-1)"),
    ("Excess Water Vapor Pressure in Cabin (L1)", "low Cabin Temperature (L1)"), ("Excess Water Vapor Pressure in Cabin (L1)", "low Cabin Temperature (L1) (t-1)"),
    ("Excess Water Vapor Pressure in Cabin (L1)", "low Humidity (L1)"), ("Excess Water Vapor Pressure in Cabin (L1)", "low Humidity (L1) (t-1)"),
    ("Excess Water Vapor Pressure in Cabin (L1)", "[HIDDEN] Excess Water Vapor Pressure in Cabin Component"),

    # Excess Water Vapor Pressure in Cabin (L2)
    ("Excess Water Vapor Pressure in Cabin (L2)", "high Cabin Temperature (L2)"), ("Excess Water Vapor Pressure in Cabin (L2)", "high Cabin Temperature (L2) (t-1)"),
    ("Excess Water Vapor Pressure in Cabin (L2)", "high Humidity (L2)"), ("Excess Water Vapor Pressure in Cabin (L2)", "high Humidity (L2) (t-1)"),
    ("Excess Water Vapor Pressure in Cabin (L2)", "low Cabin Temperature (L2)"), ("Excess Water Vapor Pressure in Cabin (L2)", "low Cabin Temperature (L2) (t-1)"),
    ("Excess Water Vapor Pressure in Cabin (L2)", "low Humidity (L2)"), ("Excess Water Vapor Pressure in Cabin (L2)", "low Humidity (L2) (t-1)"),
    ("Excess Water Vapor Pressure in Cabin (L2)", "[HIDDEN] Excess Water Vapor Pressure in Cabin Component"),
  
    # Excess Water Vapor Pressure in Cabin (Combined)
    ("Excess Water Vapor Pressure in Cabin", "Excess Water Vapor Pressure in Cabin (L1)"),
    ("Excess Water Vapor Pressure in Cabin", "Excess Water Vapor Pressure in Cabin (L2)"),

    # Fuel Cell #1 and PDU Failure
    ("Fuel Cell #1 and PDU Failure", "high 2-butanone"), ("Fuel Cell #1 and PDU Failure", "high 2-butanone (t-1)"),
    ("Fuel Cell #1 and PDU Failure", "high Acetaldehyde"), ("Fuel Cell #1 and PDU Failure", "high Acetaldehyde (t-1)"),
    ("Fuel Cell #1 and PDU Failure", "high Aux Cabin Fan #2"), ("Fuel Cell #1 and PDU Failure", "high Aux Cabin Fan #2 (t-1)"),
    ("Fuel Cell #1 and PDU Failure", "high Fuel Cell #1 Current"), ("Fuel Cell #1 and PDU Failure", "high Fuel Cell #1 Current (t-1)"),
    ("Fuel Cell #1 and PDU Failure", "high Fuel Cell #1 PQM"), ("Fuel Cell #1 and PDU Failure", "high Fuel Cell #1 PQM (t-1)"), 
    ("Fuel Cell #1 and PDU Failure", "high Fuel Cell #1 Stack Out Temp"), ("Fuel Cell #1 and PDU Failure", "high Fuel Cell #1 Stack Out Temp (t-1)"),
    ("Fuel Cell #1 and PDU Failure", "high Fuel Cell #1 Voltage"), ("Fuel Cell #1 and PDU Failure", "high Fuel Cell #1 Voltage (t-1)"), 
    ("Fuel Cell #1 and PDU Failure", "high Main Cabin Fan #2"), ("Fuel Cell #1 and PDU Failure", "high Main Cabin Fan #2 (t-1)"),
    ("Fuel Cell #1 and PDU Failure", "high PDU 4 Bank 1"), ("Fuel Cell #1 and PDU Failure", "high PDU 4 Bank 1 (t-1)"),
    ("Fuel Cell #1 and PDU Failure", "low 2-butanone"), ("Fuel Cell #1 and PDU Failure", "low 2-butanone (t-1)"),
    ("Fuel Cell #1 and PDU Failure", "low Acetaldehyde"), ("Fuel Cell #1 and PDU Failure", "low Acetaldehyde (t-1)"),
    ("Fuel Cell #1 and PDU Failure", "low Aux Cabin Fan #2"), ("Fuel Cell #1 and PDU Failure", "low Aux Cabin Fan #2 (t-1)"),
    ("Fuel Cell #1 and PDU Failure", "low Fuel Cell #1 Current"), ("Fuel Cell #1 and PDU Failure", "low Fuel Cell #1 Current (t-1)"),
    ("Fuel Cell #1 and PDU Failure", "low Fuel Cell #1 PQM"), ("Fuel Cell #1 and PDU Failure", "low Fuel Cell #1 PQM (t-1)"),
    ("Fuel Cell #1 and PDU Failure", "low Fuel Cell #1 Stack Out Temp"), ("Fuel Cell #1 and PDU Failure", "low Fuel Cell #1 Stack Out Temp (t-1)"),
    ("Fuel Cell #1 and PDU Failure", "low Fuel Cell #1 Voltage"), ("Fuel Cell #1 and PDU Failure", "low Fuel Cell #1 Voltage (t-1)"),
    ("Fuel Cell #1 and PDU Failure", "low Main Cabin Fan #2"), ("Fuel Cell #1 and PDU Failure", "low Main Cabin Fan #2 (t-1)"),
    ("Fuel Cell #1 and PDU Failure", "low PDU 4 Bank 1"), ("Fuel Cell #1 and PDU Failure", "low PDU 4 Bank 1 (t-1)"),
    ("Fuel Cell #1 and PDU Failure", "[HIDDEN] Fuel Cell #1 and PDU Failure Component"),

    # Fuel Cell #2 and PDU Failure
    ("Fuel Cell #2 and PDU Failure", "high 2-butanone"), ("Fuel Cell #2 and PDU Failure", "high 2-butanone (t-1)"),
    ("Fuel Cell #2 and PDU Failure", "high Acetaldehyde"), ("Fuel Cell #2 and PDU Failure", "high Acetaldehyde (t-1)"),
    ("Fuel Cell #2 and PDU Failure", "high Aux Cabin Fan #1"), ("Fuel Cell #2 and PDU Failure", "high Aux Cabin Fan #1 (t-1)"),
    ("Fuel Cell #2 and PDU Failure", "high Fuel Cell #2 Current"), ("Fuel Cell #2 and PDU Failure", "high Fuel Cell #2 Current (t-1)"),
    ("Fuel Cell #2 and PDU Failure", "high Fuel Cell #2 PQM"), ("Fuel Cell #2 and PDU Failure", "high Fuel Cell #2 PQM (t-1)"),
    ("Fuel Cell #2 and PDU Failure", "high Fuel Cell #2 Stack Out Temp"), ("Fuel Cell #2 and PDU Failure", "high Fuel Cell #2 Stack Out Temp (t-1)"),
    ("Fuel Cell #2 and PDU Failure", "high Fuel Cell #2 Voltage"), ("Fuel Cell #2 and PDU Failure", "high Fuel Cell #2 Voltage (t-1)"),
    ("Fuel Cell #2 and PDU Failure", "high Main Cabin Fan #1"), ("Fuel Cell #2 and PDU Failure", "high Main Cabin Fan #1 (t-1)"),
    ("Fuel Cell #2 and PDU Failure", "high PDU 5 Bank 1"), ("Fuel Cell #2 and PDU Failure", "high PDU 5 Bank 1 (t-1)"),
    ("Fuel Cell #2 and PDU Failure", "low 2-butanone"), ("Fuel Cell #2 and PDU Failure", "low 2-butanone (t-1)"),
    ("Fuel Cell #2 and PDU Failure", "low Acetaldehyde"), ("Fuel Cell #2 and PDU Failure", "low Acetaldehyde (t-1)"),
    ("Fuel Cell #2 and PDU Failure", "low Aux Cabin Fan #1"), ("Fuel Cell #2 and PDU Failure", "low Aux Cabin Fan #1 (t-1)"),
    ("Fuel Cell #2 and PDU Failure", "low Fuel Cell #2 Current"), ("Fuel Cell #2 and PDU Failure", "low Fuel Cell #2 Current (t-1)"),
    ("Fuel Cell #2 and PDU Failure", "low Fuel Cell #2 PQM"), ("Fuel Cell #2 and PDU Failure", "low Fuel Cell #2 PQM (t-1)"), 
    ("Fuel Cell #2 and PDU Failure", "low Fuel Cell #2 Stack Out Temp"), ("Fuel Cell #2 and PDU Failure", "low Fuel Cell #2 Stack Out Temp (t-1)"),
    ("Fuel Cell #2 and PDU Failure", "low Fuel Cell #2 Voltage"), ("Fuel Cell #2 and PDU Failure", "low Fuel Cell #2 Voltage (t-1)"),
    ("Fuel Cell #2 and PDU Failure", "low Main Cabin Fan #1"), ("Fuel Cell #2 and PDU Failure", "low Main Cabin Fan #1 (t-1)"),
    ("Fuel Cell #2 and PDU Failure", "low PDU 5 Bank 1"), ("Fuel Cell #2 and PDU Failure", "low PDU 5 Bank 1 (t-1)"),
    ("Fuel Cell #2 and PDU Failure", "[HIDDEN] Fuel Cell #2 and PDU Failure Component"),

    # Fuel Cell Degrade
    ("Fuel Cell Degrade", "high Fuel Cell #2 Current"), ("Fuel Cell Degrade", "high Fuel Cell #2 Current (t-1)"),
    ("Fuel Cell Degrade", "high Fuel Cell #2 Stack Out Temp"), ("Fuel Cell Degrade", "high Fuel Cell #2 Stack Out Temp (t-1)"),
    ("Fuel Cell Degrade", "high Fuel Cell #2 PQM"), ("Fuel Cell Degrade", "high Fuel Cell #2 PQM (t-1)"),
    ("Fuel Cell Degrade", "high Fuel Cell #2 Voltage"), ("Fuel Cell Degrade", "high Fuel Cell #2 Voltage (t-1)"),
    ("Fuel Cell Degrade", "low Fuel Cell #2 Current"), ("Fuel Cell Degrade", "low Fuel Cell #2 Current (t-1)"),
    ("Fuel Cell Degrade", "low Fuel Cell #2 Stack Out Temp"), ("Fuel Cell Degrade", "low Fuel Cell #2 Stack Out Temp (t-1)"),
    ("Fuel Cell Degrade", "low Fuel Cell #2 PQM"), ("Fuel Cell Degrade", "low Fuel Cell #2 PQM (t-1)"),
    ("Fuel Cell Degrade", "low Fuel Cell #2 Voltage"), ("Fuel Cell Degrade", "low Fuel Cell #2 Voltage (t-1)"),
    ("Fuel Cell Degrade", "[HIDDEN] Fuel Cell Degrade Component"),

    # Fuel Cell Failure
    ("Fuel Cell Failure", "high Fuel Cell #2 Current"), ("Fuel Cell Failure", "high Fuel Cell #2 Current (t-1)"),
    ("Fuel Cell Failure", "high Fuel Cell #2 Stack Out Temp"), ("Fuel Cell Failure", "high Fuel Cell #2 Stack Out Temp (t-1)"),
    ("Fuel Cell Failure", "high Fuel Cell #2 PQM"), ("Fuel Cell Failure", "high Fuel Cell #2 PQM (t-1)"),
    ("Fuel Cell Failure", "high Fuel Cell #2 Voltage"), ("Fuel Cell Failure", "high Fuel Cell #2 Voltage (t-1)"),
    ("Fuel Cell Failure", "low Fuel Cell #2 Current"), ("Fuel Cell Failure", "low Fuel Cell #2 Current (t-1)"),
    ("Fuel Cell Failure", "low Fuel Cell #2 Stack Out Temp"), ("Fuel Cell Failure", "low Fuel Cell #2 Stack Out Temp (t-1)"),
    ("Fuel Cell Failure", "low Fuel Cell #2 PQM"), ("Fuel Cell Failure", "low Fuel Cell #2 PQM (t-1)"),
    ("Fuel Cell Failure", "low Fuel Cell #2 Voltage"), ("Fuel Cell Failure", "low Fuel Cell #2 Voltage (t-1)"),
    ("Fuel Cell Failure", "[HIDDEN] Fuel Cell Failure Component"),

    # Loss of Pressure (L1)
    ("Loss of Pressure (L1)", "high ppN2 (L1)"), ("Loss of Pressure (L1)", "high ppN2 (L1) (t-1)"), 
    ("Loss of Pressure (L1)", "high ppO2 (L1)"), ("Loss of Pressure (L1)", "high ppO2 (L1) (t-1)"), 
    ("Loss of Pressure (L1)", "high Pressure (L1)"), ("Loss of Pressure (L1)", "high Pressure (L1) (t-1)"), 
    ("Loss of Pressure (L1)", "high Total Cabin Pressure (L1)"), ("Loss of Pressure (L1)", "high Total Cabin Pressure (L1) (t-1)"),
    ("Loss of Pressure (L1)", "low ppN2 (L1)"), ("Loss of Pressure (L1)", "low ppN2 (L1) (t-1)"),
    ("Loss of Pressure (L1)", "low ppO2 (L1)"), ("Loss of Pressure (L1)", "low ppO2 (L1) (t-1)"),
    ("Loss of Pressure (L1)", "low Pressure (L1)"), ("Loss of Pressure (L1)", "low Pressure (L1) (t-1)"), 
    ("Loss of Pressure (L1)", "low Total Cabin Pressure (L1)"), ("Loss of Pressure (L1)", "low Total Cabin Pressure (L1) (t-1)"),
    ("Loss of Pressure (L1)", "[HIDDEN] Loss of Pressure Component"),

    # Loss of Pressure (L2)
    ("Loss of Pressure (L2)", "high ppN2 (L2)"), ("Loss of Pressure (L2)", "high ppN2 (L2) (t-1)"),
    ("Loss of Pressure (L2)", "high ppO2 (L2)"), ("Loss of Pressure (L2)", "high ppO2 (L2) (t-1)"),
    ("Loss of Pressure (L2)", "high Pressure (L2)"), ("Loss of Pressure (L2)", "high Pressure (L2) (t-1)"),
    ("Loss of Pressure (L2)", "high Total Cabin Pressure (L2)"), ("Loss of Pressure (L2)", "high Total Cabin Pressure (L2) (t-1)"),
    ("Loss of Pressure (L2)", "low ppN2 (L2)"), ("Loss of Pressure (L2)", "low ppN2 (L2) (t-1)"),
    ("Loss of Pressure (L2)", "low ppO2 (L2)"), ("Loss of Pressure (L2)", "low ppO2 (L2) (t-1)"),
    ("Loss of Pressure (L2)", "low Pressure (L2)"), ("Loss of Pressure (L2)", "low Pressure (L2) (t-1)"),
    ("Loss of Pressure (L2)", "low Total Cabin Pressure (L2)"), ("Loss of Pressure (L2)", "low Total Cabin Pressure (L2) (t-1)"),
    ("Loss of Pressure (L2)", "[HIDDEN] Loss of Pressure Component"),

    # Loss of Pressure (Combined)
    ("Loss of Pressure", "Loss of Pressure (L1)"),
    ("Loss of Pressure", "Loss of Pressure (L2)"),

    # Main Cabin Fan Failure (L1)
    ("Main Cabin Fan Failure (L1)", "high Cabin Temperature (L1)"), ("Main Cabin Fan Failure (L1)", "high Cabin Temperature (L1) (t-1)"),
    ("Main Cabin Fan Failure (L1)", "high Humidity (L1)"), ("Main Cabin Fan Failure (L1)", "high Humidity (L1) (t-1)"),
    ("Main Cabin Fan Failure (L1)", "high Main Cabin Fan #2"), ("Main Cabin Fan Failure (L1)", "high Main Cabin Fan #2 (t-1)"),
    ("Main Cabin Fan Failure (L1)", "low Cabin Temperature (L1)"), ("Main Cabin Fan Failure (L1)", "low Cabin Temperature (L1) (t-1)"),
    ("Main Cabin Fan Failure (L1)", "low Humidity (L1)"), ("Main Cabin Fan Failure (L1)", "low Humidity (L1) (t-1)"),
    ("Main Cabin Fan Failure (L1)", "low Main Cabin Fan #2"), ("Main Cabin Fan Failure (L1)", "low Main Cabin Fan #2 (t-1)"),
    ("Main Cabin Fan Failure (L1)", "[HIDDEN] Main Cabin Fan Failure Component"),

    # Main Cabin Fan Failure (L2)
    ("Main Cabin Fan Failure (L2)", "high Cabin Temperature (L2)"), ("Main Cabin Fan Failure (L2)", "high Cabin Temperature (L2) (t-1)"),
    ("Main Cabin Fan Failure (L2)", "high Humidity (L2)"), ("Main Cabin Fan Failure (L2)", "high Humidity (L2) (t-1)"),
    ("Main Cabin Fan Failure (L2)", "high Main Cabin Fan #2"), ("Main Cabin Fan Failure (L2)", "high Main Cabin Fan #2 (t-1)"),
    ("Main Cabin Fan Failure (L2)", "low Cabin Temperature (L2)"), ("Main Cabin Fan Failure (L2)", "low Cabin Temperature (L2) (t-1)"),
    ("Main Cabin Fan Failure (L2)", "low Humidity (L2)"), ("Main Cabin Fan Failure (L2)", "low Humidity (L2) (t-1)"),
    ("Main Cabin Fan Failure (L2)", "low Main Cabin Fan #2"), ("Main Cabin Fan Failure (L2)", "low Main Cabin Fan #2 (t-1)"),
    ("Main Cabin Fan Failure (L2)", "[HIDDEN] Main Cabin Fan Failure Component"),

    # Main Cabin Fan Failure (Combined)
    ("Main Cabin Fan Failure", "Main Cabin Fan Failure (L1)"),
    ("Main Cabin Fan Failure", "Main Cabin Fan Failure (L2)"),

    # MOXIE Antenna Failure
    ("MOXIE Antenna Failure", "high MOXIE Compressor Temp"), ("MOXIE Antenna Failure", "high MOXIE Compressor Temp (t-1)"), 
    ("MOXIE Antenna Failure", "high SOXIE Stack Temp"), ("MOXIE Antenna Failure", "high SOXIE Stack Temp (t-1)"),
    ("MOXIE Antenna Failure", "high MOXIE Telemetry Quality"), ("MOXIE Antenna Failure", "high MOXIE Telemetry Quality (t-1)"),
    ("MOXIE Antenna Failure", "low MOXIE Compressor Temp"), ("MOXIE Antenna Failure", "low MOXIE Compressor Temp (t-1)"), 
    ("MOXIE Antenna Failure", "low SOXIE Stack Temp"), ("MOXIE Antenna Failure", "low SOXIE Stack Temp (t-1)"),
    ("MOXIE Antenna Failure", "low MOXIE Telemetry Quality"), ("MOXIE Antenna Failure", "low MOXIE Telemetry Quality (t-1)"),
    ("MOXIE Antenna Failure", "[HIDDEN] MOXIE Antenna Failure Component"),

    # MOXIE ECM Failure
    ("MOXIE ECM Failure", "high SOXIE Stack Temp"), ("MOXIE ECM Failure", "high SOXIE Stack Temp (t-1)"),
    ("MOXIE ECM Failure", "low SOXIE Stack Temp"), ("MOXIE ECM Failure", "low SOXIE Stack Temp (t-1)"),
    ("MOXIE ECM Failure", "[HIDDEN] MOXIE ECM Failure Component"),

    # MOXIE Fan Failure
    ("MOXIE Fan Failure", "high MOXIE Compressor Temp"), ("MOXIE Fan Failure", "high MOXIE Compressor Temp (t-1)"),
    ("MOXIE Fan Failure", "low MOXIE Compressor Temp"), ("MOXIE Fan Failure", "low MOXIE Compressor Temp (t-1)"),
    ("MOXIE Fan Failure", "[HIDDEN] MOXIE Fan Failure Component"),

    # N2 Tank Burst (L1)
    ("N2 Tank Burst (L1)", "high ppN2 (L1)"), ("N2 Tank Burst (L1)", "high ppN2 (L1) (t-1)"),  
    ("N2 Tank Burst (L1)", "high Pressure (L1)"), ("N2 Tank Burst (L1)", "high Pressure (L1) (t-1)"),
    ("N2 Tank Burst (L1)", "high Total Cabin Pressure (L1)"), ("N2 Tank Burst (L1)", "high Total Cabin Pressure (L1) (t-1)"),
    ("N2 Tank Burst (L1)", "low ppN2 (L1)"), ("N2 Tank Burst (L1)", "low ppN2 (L1) (t-1)"),
    ("N2 Tank Burst (L1)", "low Pressure (L1)"), ("N2 Tank Burst (L1)", "low Pressure (L1) (t-1)"),
    ("N2 Tank Burst (L1)", "low Total Cabin Pressure (L1)"), ("N2 Tank Burst (L1)", "low Total Cabin Pressure (L1) (t-1)"),
    ("N2 Tank Burst (L1)", "[HIDDEN] N2 Tank Burst Component"),

    # N2 Tank Burst (L2)
    ("N2 Tank Burst (L2)", "high ppN2 (L2)"), ("N2 Tank Burst (L2)", "high ppN2 (L2) (t-1)"),
    ("N2 Tank Burst (L2)", "high Pressure (L2)"), ("N2 Tank Burst (L2)", "high Pressure (L2) (t-1)"),
    ("N2 Tank Burst (L2)", "high Total Cabin Pressure (L2)"), ("N2 Tank Burst (L2)", "high Total Cabin Pressure (L2) (t-1)"),
    ("N2 Tank Burst (L2)", "low ppN2 (L2)"), ("N2 Tank Burst (L2)", "low ppN2 (L2) (t-1)"),
    ("N2 Tank Burst (L2)", "low Pressure (L2)"), ("N2 Tank Burst (L2)", "low Pressure (L2) (t-1)"),
    ("N2 Tank Burst (L2)", "low Total Cabin Pressure (L2)"), ("N2 Tank Burst (L2)", "low Total Cabin Pressure (L2) (t-1)"),
    ("N2 Tank Burst (L2)", "[HIDDEN] N2 Tank Burst Component"),

    # N2 Tank Burst (Combined)
    ("N2 Tank Burst", "N2 Tank Burst (L1)"),
    ("N2 Tank Burst", "N2 Tank Burst (L2)"),

    # PDU 4 Failure
    # NOTE: In Neo4j, PDU 5 Bank 1 is mentioned as a symptom for a PDU 4 Failure, but PDU 4 Bank 1 is not mentioned for a PDU 5 failure;
    # given that this is likely an incorrect relationship, the structure below only includes the PDU related to a specific failure
    # (i.e., PDU 4 Bank 1 for a PDU 4 Failure and PDU 5 Bank 1 for a PDU 5 Failure)
    ("PDU 4 Failure (L1)", "high 2-butanone"), ("PDU 4 Failure (L1)", "high 2-butanone (t-1)"), 
    ("PDU 4 Failure (L1)", "high Acetaldehyde"), ("PDU 4 Failure (L1)", "high Acetaldehyde (t-1)"),
    ("PDU 4 Failure (L1)", "high Aux Cabin Fan #2"), ("PDU 4 Failure (L1)", "high Aux Cabin Fan #2 (t-1)"),
    ("PDU 4 Failure (L1)", "high Cabin Temperature (L1)"), ("PDU 4 Failure (L1)", "high Cabin Temperature (L1) (t-1)"),
    ("PDU 4 Failure (L1)", "high Humidity (L1)"), ("PDU 4 Failure (L1)", "high Humidity (L1) (t-1)"),
    ("PDU 4 Failure (L1)", "high Main Cabin Fan #2"), ("PDU 4 Failure (L1)", "high Main Cabin Fan #2 (t-1)"),
    ("PDU 4 Failure (L1)", "high PDU 4 Bank 1"), ("PDU 4 Failure (L1)", "high PDU 4 Bank 1 (t-1)"),
    ("PDU 4 Failure (L1)", "low 2-butanone"), ("PDU 4 Failure (L1)", "low 2-butanone (t-1)"), 
    ("PDU 4 Failure (L1)", "low Acetaldehyde"), ("PDU 4 Failure (L1)", "low Acetaldehyde (t-1)"), 
    ("PDU 4 Failure (L1)", "low Aux Cabin Fan #2"), ("PDU 4 Failure (L1)", "low Aux Cabin Fan #2 (t-1)"),
    ("PDU 4 Failure (L1)", "low Cabin Temperature (L1)"), ("PDU 4 Failure (L1)", "low Cabin Temperature (L1) (t-1)"),
    ("PDU 4 Failure (L1)", "low Humidity (L1)"), ("PDU 4 Failure (L1)", "low Humidity (L1) (t-1)"),
    ("PDU 4 Failure (L1)", "low Main Cabin Fan #2"), ("PDU 4 Failure (L1)", "low Main Cabin Fan #2 (t-1)"),
    ("PDU 4 Failure (L1)", "low PDU 4 Bank 1"), ("PDU 4 Failure (L1)", "low PDU 4 Bank 1 (t-1)"),
    ("PDU 4 Failure (L1)", "[HIDDEN] PDU 4 Failure Component"),

    # PDU 4 Failure (L2)
    ("PDU 4 Failure (L2)", "high 2-butanone"), ("PDU 4 Failure (L2)", "high 2-butanone (t-1)"), 
    ("PDU 4 Failure (L2)", "high Acetaldehyde"), ("PDU 4 Failure (L2)", "high Acetaldehyde (t-1)"),
    ("PDU 4 Failure (L2)", "high Aux Cabin Fan #2"), ("PDU 4 Failure (L2)", "high Aux Cabin Fan #2 (t-1)"),
    ("PDU 4 Failure (L2)", "high Cabin Temperature (L2)"), ("PDU 4 Failure (L2)", "high Cabin Temperature (L2) (t-1)"),
    ("PDU 4 Failure (L2)", "high Humidity (L2)"), ("PDU 4 Failure (L2)", "high Humidity (L2) (t-1)"),
    ("PDU 4 Failure (L2)", "high Main Cabin Fan #2"), ("PDU 4 Failure (L2)", "high Main Cabin Fan #2 (t-1)"), 
    ("PDU 4 Failure (L2)", "high PDU 4 Bank 1"), ("PDU 4 Failure (L2)", "high PDU 4 Bank 1 (t-1)"),
    ("PDU 4 Failure (L2)", "low 2-butanone"), ("PDU 4 Failure (L2)", "low 2-butanone (t-1)"),
    ("PDU 4 Failure (L2)", "low Acetaldehyde"), ("PDU 4 Failure (L2)", "low Acetaldehyde (t-1)"),
    ("PDU 4 Failure (L2)", "low Aux Cabin Fan #2"), ("PDU 4 Failure (L2)", "low Aux Cabin Fan #2 (t-1)"),
    ("PDU 4 Failure (L2)", "low Cabin Temperature (L2)"), ("PDU 4 Failure (L2)", "low Cabin Temperature (L2) (t-1)"),
    ("PDU 4 Failure (L2)", "low Humidity (L2)"), ("PDU 4 Failure (L2)", "low Humidity (L2) (t-1)"),
    ("PDU 4 Failure (L2)", "low Main Cabin Fan #2"), ("PDU 4 Failure (L2)", "low Main Cabin Fan #2 (t-1)"),
    ("PDU 4 Failure (L2)", "low PDU 4 Bank 1"), ("PDU 4 Failure (L2)", "low PDU 4 Bank 1 (t-1)"),
    ("PDU 4 Failure (L2)", "[HIDDEN] PDU 4 Failure Component"),

    # PDU 4 Failure (Combined)
    ("PDU 4 Failure", "PDU 4 Failure (L1)"),
    ("PDU 4 Failure", "PDU 4 Failure (L2)"),

    # PDU 5 Failure (L1)
    ("PDU 5 Failure (L1)", "high 2-butanone"), ("PDU 5 Failure (L1)", "high 2-butanone (t-1)"),
    ("PDU 5 Failure (L1)", "high Acetaldehyde"), ("PDU 5 Failure (L1)", "high Acetaldehyde (t-1)"),
    ("PDU 5 Failure (L1)", "high Aux Cabin Fan #2"), ("PDU 5 Failure (L1)", "high Aux Cabin Fan #2 (t-1)"),
    ("PDU 5 Failure (L1)", "high Cabin Temperature (L1)"), ("PDU 5 Failure (L1)", "high Cabin Temperature (L1) (t-1)"),
    ("PDU 5 Failure (L1)", "high Humidity (L1)"), ("PDU 5 Failure (L1)", "high Humidity (L1) (t-1)"),
    ("PDU 5 Failure (L1)", "high Main Cabin Fan #2"), ("PDU 5 Failure (L1)", "high Main Cabin Fan #2 (t-1)"),
    ("PDU 5 Failure (L1)", "high PDU 5 Bank 1"), ("PDU 5 Failure (L1)", "high PDU 5 Bank 1 (t-1)"),
    ("PDU 5 Failure (L1)", "low 2-butanone"), ("PDU 5 Failure (L1)", "low 2-butanone (t-1)"),
    ("PDU 5 Failure (L1)", "low Acetaldehyde"), ("PDU 5 Failure (L1)", "low Acetaldehyde (t-1)"),
    ("PDU 5 Failure (L1)", "low Aux Cabin Fan #2"), ("PDU 5 Failure (L1)", "low Aux Cabin Fan #2 (t-1)"),
    ("PDU 5 Failure (L1)", "low Cabin Temperature (L1)"), ("PDU 5 Failure (L1)", "low Cabin Temperature (L1) (t-1)"),
    ("PDU 5 Failure (L1)", "low Humidity (L1)"), ("PDU 5 Failure (L1)", "low Humidity (L1) (t-1)"),
    ("PDU 5 Failure (L1)", "low Main Cabin Fan #2"), ("PDU 5 Failure (L1)", "low Main Cabin Fan #2 (t-1)"),
    ("PDU 5 Failure (L1)", "low PDU 5 Bank 1"), ("PDU 5 Failure (L1)", "low PDU 5 Bank 1 (t-1)"),
    ("PDU 5 Failure (L1)", "[HIDDEN] PDU 5 Failure Component"),

    # PDU 5 Failure (L2)
    ("PDU 5 Failure (L2)", "high 2-butanone"), ("PDU 5 Failure (L2)", "high 2-butanone (t-1)"),
    ("PDU 5 Failure (L2)", "high Acetaldehyde"), ("PDU 5 Failure (L2)", "high Acetaldehyde (t-1)"),
    ("PDU 5 Failure (L2)", "high Aux Cabin Fan #2"), ("PDU 5 Failure (L2)", "high Aux Cabin Fan #2 (t-1)"),
    ("PDU 5 Failure (L2)", "high Cabin Temperature (L2)"), ("PDU 5 Failure (L2)", "high Cabin Temperature (L2) (t-1)"),
    ("PDU 5 Failure (L2)", "high Humidity (L2)"), ("PDU 5 Failure (L2)", "high Humidity (L2) (t-1)"),
    ("PDU 5 Failure (L2)", "high Main Cabin Fan #2"), ("PDU 5 Failure (L2)", "high Main Cabin Fan #2 (t-1)"),
    ("PDU 5 Failure (L2)", "high PDU 5 Bank 1"), ("PDU 5 Failure (L2)", "high PDU 5 Bank 1 (t-1)"),
    ("PDU 5 Failure (L2)", "low 2-butanone"), ("PDU 5 Failure (L2)", "low 2-butanone (t-1)"),
    ("PDU 5 Failure (L2)", "low Acetaldehyde"), ("PDU 5 Failure (L2)", "low Acetaldehyde (t-1)"),
    ("PDU 5 Failure (L2)", "low Aux Cabin Fan #2"), ("PDU 5 Failure (L2)", "low Aux Cabin Fan #2 (t-1)"),
    ("PDU 5 Failure (L2)", "low Cabin Temperature (L2)"), ("PDU 5 Failure (L2)", "low Cabin Temperature (L2) (t-1)"),
    ("PDU 5 Failure (L2)", "low Humidity (L2)"), ("PDU 5 Failure (L2)", "low Humidity (L2) (t-1)"),
    ("PDU 5 Failure (L2)", "low Main Cabin Fan #2"), ("PDU 5 Failure (L2)", "low Main Cabin Fan #2 (t-1)"),
    ("PDU 5 Failure (L2)", "low PDU 5 Bank 1"), ("PDU 5 Failure (L2)", "low PDU 5 Bank 1 (t-1)"),
    ("PDU 5 Failure (L2)", "[HIDDEN] PDU 5 Failure Component"),

    # PDU 5 Failure (Combined)
    ("PDU 5 Failure", "PDU 5 Failure (L1)"),
    ("PDU 5 Failure", "PDU 5 Failure (L2)"),

    # Reduced Main Cabin Fan #1 Capacity
    ("Reduced Main Cabin Fan #1 Capacity", "high 2-butanone"), ("Reduced Main Cabin Fan #1 Capacity", "high 2-butanone (t-1)"),
    ("Reduced Main Cabin Fan #1 Capacity", "high HMCTS"), ("Reduced Main Cabin Fan #1 Capacity", "high HMCTS (t-1)"),
    ("Reduced Main Cabin Fan #1 Capacity", "high Main Cabin Fan #1"), ("Reduced Main Cabin Fan #1 Capacity", "high Main Cabin Fan #1 (t-1)"),
    ("Reduced Main Cabin Fan #1 Capacity", "high n_Butanol"), ("Reduced Main Cabin Fan #1 Capacity", "high n_Butanol (t-1)"),
    ("Reduced Main Cabin Fan #1 Capacity", "low 2-butanone"), ("Reduced Main Cabin Fan #1 Capacity", "low 2-butanone (t-1)"),
    ("Reduced Main Cabin Fan #1 Capacity", "low HMCTS"), ("Reduced Main Cabin Fan #1 Capacity", "low HMCTS (t-1)"),
    ("Reduced Main Cabin Fan #1 Capacity", "low Main Cabin Fan #1"), ("Reduced Main Cabin Fan #1 Capacity", "low Main Cabin Fan #1 (t-1)"),
    ("Reduced Main Cabin Fan #1 Capacity", "low n_Butanol"), ("Reduced Main Cabin Fan #1 Capacity", "low n_Butanol (t-1)"),
    ("Reduced Main Cabin Fan #1 Capacity", "[HIDDEN] Reduced Main Cabin Fan #1 Capacity Component"),

    # RWGSR Malfunction (L1)
    ("RWGSR Malfunction (L1)", "high H2O (Crew)"), ("RWGSR Malfunction (L1)", "high H2O (Crew) (t-1)"),
    ("RWGSR Malfunction (L1)", "high ppCO2 (L1)"), ("RWGSR Malfunction (L1)", "high ppCO2 (L1) (t-1)"),
    ("RWGSR Malfunction (L1)", "high ppO2 (L1)"), ("RWGSR Malfunction (L1)", "high ppO2 (L1) (t-1)"),
    ("RWGSR Malfunction (L1)", "low H2O (Crew)"), ("RWGSR Malfunction (L1)", "low H2O (Crew) (t-1)"),
    ("RWGSR Malfunction (L1)", "low ppCO2 (L1)"), ("RWGSR Malfunction (L1)", "low ppCO2 (L1) (t-1)"),
    ("RWGSR Malfunction (L1)", "low ppO2 (L1)"), ("RWGSR Malfunction (L1)", "low ppO2 (L1) (t-1)"),
    ("RWGSR Malfunction (L1)", "[HIDDEN] RWGSR Malfunction Component"),

    # RWGSR Malfunction (L2)
    ("RWGSR Malfunction (L2)", "high H2O (Crew)"), ("RWGSR Malfunction (L2)", "high H2O (Crew) (t-1)"),
    ("RWGSR Malfunction (L2)", "high ppCO2 (L2)"), ("RWGSR Malfunction (L2)", "high ppCO2 (L2) (t-1)"),
    ("RWGSR Malfunction (L2)", "high ppO2 (L2)"), ("RWGSR Malfunction (L2)", "high ppO2 (L2) (t-1)"),
    ("RWGSR Malfunction (L2)", "low H2O (Crew)"), ("RWGSR Malfunction (L2)", "low H2O (Crew) (t-1)"),
    ("RWGSR Malfunction (L2)", "low ppCO2 (L2)"), ("RWGSR Malfunction (L2)", "low ppCO2 (L2) (t-1)"),
    ("RWGSR Malfunction (L2)", "low ppO2 (L2)"), ("RWGSR Malfunction (L2)", "low ppO2 (L2) (t-1)"),
    ("RWGSR Malfunction (L2)", "[HIDDEN] RWGSR Malfunction Component"),

    # RWGSR Malfunction (Combined)
    ("RWGSR Malfunction", "RWGSR Malfunction (L1)"),
    ("RWGSR Malfunction", "RWGSR Malfunction (L2)"),

    # SPE System Maintenance
    ("SPE System Maintenance", "high H2O (Crew)"), ("SPE System Maintenance", "high H2O (Crew) (t-1)"),
    ("SPE System Maintenance", "low H2O (Crew)"), ("SPE System Maintenance", "low H2O (Crew) (t-1)"),
    ("SPE System Maintenance", "[HIDDEN] SPE System Maintenance Component"),

    # TCCS Auxiliary Fan #1 Failure
    ("TCCS Auxiliary Fan #1 Failure", "high 2-butanone"), ("TCCS Auxiliary Fan #1 Failure", "high 2-butanone (t-1)"), 
    ("TCCS Auxiliary Fan #1 Failure", "high Acetaldehyde"), ("TCCS Auxiliary Fan #1 Failure", "high Acetaldehyde (t-1)"),
    ("TCCS Auxiliary Fan #1 Failure", "high Aux Cabin Fan #1"), ("TCCS Auxiliary Fan #1 Failure", "high Aux Cabin Fan #1 (t-1)"),
    ("TCCS Auxiliary Fan #1 Failure", "low 2-butanone"), ("TCCS Auxiliary Fan #1 Failure", "low 2-butanone (t-1)"),
    ("TCCS Auxiliary Fan #1 Failure", "low Acetaldehyde"), ("TCCS Auxiliary Fan #1 Failure", "low Acetaldehyde (t-1)"),
    ("TCCS Auxiliary Fan #1 Failure", "low Aux Cabin Fan #1"), ("TCCS Auxiliary Fan #1 Failure", "low Aux Cabin Fan #1 (t-1)"),
    ("TCCS Auxiliary Fan #1 Failure", "[HIDDEN] TCCS Auxiliary Fan #1 Failure Component"),

    # TCCS Auxiliary Fan #2 Failure
    ("TCCS Auxiliary Fan #2 Failure", "high 2-butanone"), ("TCCS Auxiliary Fan #2 Failure", "high 2-butanone (t-1)"),
    ("TCCS Auxiliary Fan #2 Failure", "high Acetaldehyde"), ("TCCS Auxiliary Fan #2 Failure", "high Acetaldehyde (t-1)"),
    ("TCCS Auxiliary Fan #2 Failure", "high Aux Cabin Fan #2"), ("TCCS Auxiliary Fan #2 Failure", "high Aux Cabin Fan #2 (t-1)"),
    ("TCCS Auxiliary Fan #2 Failure", "low 2-butanone"), ("TCCS Auxiliary Fan #2 Failure", "low 2-butanone (t-1)"),
    ("TCCS Auxiliary Fan #2 Failure", "low Acetaldehyde"), ("TCCS Auxiliary Fan #2 Failure", "low Acetaldehyde (t-1)"),
    ("TCCS Auxiliary Fan #2 Failure", "low Aux Cabin Fan #2"), ("TCCS Auxiliary Fan #2 Failure", "low Aux Cabin Fan #2 (t-1)"),
    ("TCCS Auxiliary Fan #2 Failure", "[HIDDEN] TCCS Auxiliary Fan #2 Failure Component"),

    # TCCS Auxiliary Fan at Reduced Capacity
    ("TCCS Auxiliary Fan at Reduced Capacity", "high Acetaldehyde"), ("TCCS Auxiliary Fan at Reduced Capacity", "high Acetaldehyde (t-1)"),
    ("TCCS Auxiliary Fan at Reduced Capacity", "high Aux Cabin Fan #2"), ("TCCS Auxiliary Fan at Reduced Capacity", "high Aux Cabin Fan #2 (t-1)"),
    ("TCCS Auxiliary Fan at Reduced Capacity", "high Dichloromethane"), ("TCCS Auxiliary Fan at Reduced Capacity", "high Dichloromethane (t-1)"),
    ("TCCS Auxiliary Fan at Reduced Capacity", "high n_Butanol"), ("TCCS Auxiliary Fan at Reduced Capacity", "high n_Butanol (t-1)"),
    ("TCCS Auxiliary Fan at Reduced Capacity", "low Acetaldehyde"), ("TCCS Auxiliary Fan at Reduced Capacity", "low Acetaldehyde (t-1)"),
    ("TCCS Auxiliary Fan at Reduced Capacity", "low Aux Cabin Fan #2"), ("TCCS Auxiliary Fan at Reduced Capacity", "low Aux Cabin Fan #2 (t-1)"),
    ("TCCS Auxiliary Fan at Reduced Capacity", "low Dichloromethane"), ("TCCS Auxiliary Fan at Reduced Capacity", "low Dichloromethane (t-1)"),
    ("TCCS Auxiliary Fan at Reduced Capacity", "low n_Butanol"), ("TCCS Auxiliary Fan at Reduced Capacity", "low n_Butanol (t-1)"),
    ("TCCS Auxiliary Fan at Reduced Capacity", "[HIDDEN] TCCS Auxiliary Fan at Reduced Capacity Component"),

    # TCCS Filter Clog
    ("TCCS Filter Clog", "high 2-butanone"), ("TCCS Filter Clog", "high 2-butanone (t-1)"),
    ("TCCS Filter Clog", "high Acetaldehyde"), ("TCCS Filter Clog", "high Acetaldehyde (t-1)"),
    ("TCCS Filter Clog", "high Dichloromethane"), ("TCCS Filter Clog", "high Dichloromethane (t-1)"),
    ("TCCS Filter Clog", "high HMCTS"), ("TCCS Filter Clog", "high HMCTS (t-1)"),
    ("TCCS Filter Clog", "low 2-butanone"), ("TCCS Filter Clog", "low 2-butanone (t-1)"),
    ("TCCS Filter Clog", "low Acetaldehyde"), ("TCCS Filter Clog", "low Acetaldehyde (t-1)"),
    ("TCCS Filter Clog", "low Dichloromethane"), ("TCCS Filter Clog", "low Dichloromethane (t-1)"),
    ("TCCS Filter Clog", "low HMCTS"), ("TCCS Filter Clog", "low HMCTS (t-1)"),
    ("TCCS Filter Clog", "[HIDDEN] TCCS Filter Clog Component"),

    # Trace Contaminants
    ("Trace Contaminants", "high 2-butanone"), ("Trace Contaminants", "high 2-butanone (t-1)"),
    ("Trace Contaminants", "low 2-butanone"), ("Trace Contaminants", "low 2-butanone (t-1)"),
    ("Trace Contaminants", "[HIDDEN] Trace Contaminants Component"),

    # WRS Failure
    ("WRS Failure", "high WRS Delivery Pump"), ("WRS Failure", "high WRS Delivery Pump (t-1)"),
    ("WRS Failure", "high WRS Valve Flow"), ("WRS Failure", "high WRS Valve Flow (t-1)"),
    ("WRS Failure", "low WRS Delivery Pump"), ("WRS Failure", "low WRS Delivery Pump (t-1)"),
    ("WRS Failure", "low WRS Valve Flow"), ("WRS Failure", "low WRS Valve Flow (t-1)"),
    ("WRS Failure", "[HIDDEN] WPA Pump Flow Rate"),

    # WRS Maintenance
    ("WRS Maintenance", "high H2O (Crew)"), ("WRS Maintenance", "high H2O (Crew) (t-1)"), 
    ("WRS Maintenance", "high WRS Valve Flow"), ("WRS Maintenance", "high WRS Valve Flow (t-1)"),
    ("WRS Maintenance", "low H2O (Crew)"), ("WRS Maintenance", "low H2O (Crew) (t-1)"),
    ("WRS Maintenance", "low WRS Valve Flow"), ("WRS Maintenance", "low WRS Valve Flow (t-1)"),
    ("WRS Maintenance", "[HIDDEN] Multifiltration Bed Saturation"),

    # WRS Off-nominal pH Level
    ("WRS Off-nominal pH Level", "high H2O pH"), ("WRS Off-nominal pH Level", "high H2O pH (t-1)"),
    ("WRS Off-nominal pH Level", "low H2O pH"), ("WRS Off-nominal pH Level", "low H2O pH (t-1)"),
    ("WRS Off-nominal pH Level", "[HIDDEN] Ion Exchange Bed Status")
]

network_dict = defaultdict(set)
for anomaly, parameter in network:
    network_dict[anomaly].add(parameter)

# Create new edges for all (t-1) parameters to their respective parent anomalies
new_edges = [] # create an empty list to store new edges
for anomaly, parameters in network_dict.items():
    for parameter in parameters:
        # Only add new edges for telemetry parameters (i.e., not for additional evidence)
        if parameter.startswith("[HIDDEN]") or "(t-1)" in parameter:
            continue
        temporal_parameter = f"{parameter} (t-1)"
        if temporal_parameter not in parameters:
            new_edges.append((anomaly, temporal_parameter))

# Merge temporal parameter node edges in network
network.extend(new_edges)
network.sort() # sort to keep 'current' and temporal parameters together

# Add connections between temporal variables (e.g., ppO2 (L1) (t-1) and ppO2 (L1)). Note that the previous
# time step parameter is added first, as the older measurement has an impact on the current reading
temporal_nodes = [
    ("high 2-butanone (t-1)", "high 2-butanone"), ("high 2-butanone (t-1)", "low 2-butanone"), 
    ("low 2-butanone (t-1)", "high 2-butanone"), ("low 2-butanone (t-1)", "low 2-butanone"),
    ("Acetaldehyde (t-1)", "high Acetaldehyde"), ("Acetaldehyde (t-1)", "low Acetaldehyde"),
    ("Aux Cabin Fan #1 (t-1)", "high Aux Cabin Fan #1"), ("Aux Cabin Fan #1 (t-1)", "low Aux Cabin Fan #1"), 
    ("Aux Cabin Fan #2 (t-1)", "high Aux Cabin Fan #2"), ("Aux Cabin Fan #2 (t-1)", "low Aux Cabin Fan #2"),
    ("Cabin Temperature (L1) (t-1)", "high Cabin Temperature (L1)"), ("Cabin Temperature (L1) (t-1)", "low Cabin Temperature (L1)"),
    ("Cabin Temperature (L2) (t-1)", "high Cabin Temperature (L2)"), ("Cabin Temperature (L2) (t-1)", "low Cabin Temperature (L2)"),
    ("Dichloromethane (t-1)", "high Dichloromethane"), ("Dichloromethane (t-1)", "low Dichloromethane"),
    ("Fuel Cell #1 Current (t-1)", "high Fuel Cell #1 Current"), ("Fuel Cell #1 Current (t-1)", "low Fuel Cell #1 Current"),
    ("Fuel Cell #1 PQM (t-1)", "high Fuel Cell #1 PQM"), ("Fuel Cell #1 PQM (t-1)", "low Fuel Cell #1 PQM"),
    ("Fuel Cell #1 Stack Out Temp (t-1)", "high Fuel Cell #1 Stack Out Temp"), ("Fuel Cell #1 Stack Out Temp (t-1)", "low Fuel Cell #1 Stack Out Temp"),
    ("Fuel Cell #1 Voltage (t-1)", "high Fuel Cell #1 Voltage"), ("Fuel Cell #1 Voltage (t-1)", "low Fuel Cell #1 Voltage"), 
    ("Fuel Cell #2 Current (t-1)", "high Fuel Cell #2 Current"), ("Fuel Cell #2 Current (t-1)", "low Fuel Cell #2 Current"),
    ("Fuel Cell #2 PQM (t-1)", "high Fuel Cell #2 PQM"), ("Fuel Cell #2 PQM (t-1)", "low Fuel Cell #2 PQM"), 
    ("Fuel Cell #2 Stack Out Temp (t-1)", "high Fuel Cell #2 Stack Out Temp"), ("Fuel Cell #2 Stack Out Temp (t-1)", "low Fuel Cell #2 Stack Out Temp"),
    ("Fuel Cell #2 Voltage (t-1)", "high Fuel Cell #2 Voltage"), ("Fuel Cell #2 Voltage (t-1)", "low Fuel Cell #2 Voltage"), 
    ("H2O (Crew) (t-1)", "high H2O (Crew)"), ("H2O (Crew) (t-1)", "low H2O (Crew)"),
    ("H2O pH (t-1)", "high H2O pH"), ("H2O pH (t-1)", "low H2O pH"),
    ("HMCTS (t-1)", "high HMCTS"), ("HMCTS (t-1)", "low HMCTS"),
    ("Humidity (L1) (t-1)", "high Humidity (L1)"), ("Humidity (L1) (t-1)", "low Humidity (L1)"),
    ("Humidity (L2) (t-1)", "high Humidity (L2)"), ("Humidity (L2) (t-1)", "low Humidity (L2)"),
    ("LiOH CO2 Saturation (t-1)", "high LiOH CO2 Saturation"), ("LiOH CO2 Saturation (t-1)", "low LiOH CO2 Saturation"), 
    ("Main Cabin Fan #1 (t-1)", "high Main Cabin Fan #1"), ("Main Cabin Fan #1 (t-1)", "low Main Cabin Fan #1"),
    ("Main Cabin Fan #2 (t-1)", "high Main Cabin Fan #2"), ("Main Cabin Fan #2 (t-1)", "low Main Cabin Fan #2"),
    ("MOXIE Compressor Temp (t-1)", "high MOXIE Compressor Temp"), ("MOXIE Compressor Temp (t-1)", "low MOXIE Compressor Temp"),
    ("MOXIE Telemetry Quality (t-1)", "high MOXIE Telemetry Quality"), ("MOXIE Telemetry Quality (t-1)", "low MOXIE Telemetry Quality"),
    ("n_Butanol (t-1)", "high n_Butanol"), ("n_Butanol (t-1)", "low n_Butanol"),
    ("PDU 4 Bank 1 (t-1)", "high PDU 4 Bank 1"), ("PDU 4 Bank 1 (t-1)", "low PDU 4 Bank 1"),
    ("PDU 5 Bank 1 (t-1)", "high PDU 5 Bank 1"), ("PDU 5 Bank 1 (t-1)", "low PDU 5 Bank 1"),
    ("ppCO2 (L1) (t-1)", "high ppCO2 (L1)"), ("ppCO2 (L1) (t-1)", "low ppCO2 (L1)"), 
    ("ppCO2 (L2) (t-1)", "high ppCO2 (L2)"), ("ppCO2 (L2) (t-1)", "low ppCO2 (L2)"),
    ("ppH2 (L1) (t-1)", "high ppH2 (L1)"), ("ppH2 (L1) (t-1)", "low ppH2 (L1)"), 
    ("ppH2 (L2) (t-1)", "high ppH2 (L2)"), ("ppH2 (L2) (t-1)", "low ppH2 (L2)"),
    ("ppN2 (L1) (t-1)", "high ppN2 (L1)"), ("ppN2 (L1) (t-1)", "low ppN2 (L1)"),
    ("ppN2 (L2) (t-1)", "high ppN2 (L2)"), ("ppN2 (L2) (t-1)", "low ppN2 (L2)"),
    ("ppO2 (L1) (t-1)", "high ppO2 (L1)"), ("ppO2 (L1) (t-1)", "low ppO2 (L1)"),
    ("ppO2 (L2) (t-1)", "high ppO2 (L2)"), ("ppO2 (L2) (t-1)", "low ppO2 (L2)"),
    ("Pressure (L1) (t-1)", "high Pressure (L1)"), ("Pressure (L1) (t-1)", "low Pressure (L1)"),
    ("Pressure (L2) (t-1)", "high Pressure (L2)"), ("Pressure (L2) (t-1)", "low Pressure (L2)"),
    ("SOXIE Stack Temp (t-1)", "high SOXIE Stack Temp"), ("SOXIE Stack Temp (t-1)", "low SOXIE Stack Temp"), 
    ("Total Cabin Pressure (L1) (t-1)", "high Total Cabin Pressure (L1)"), ("Total Cabin Pressure (L1) (t-1)", "low Total Cabin Pressure (L1)"),
    ("Total Cabin Pressure (L2) (t-1)", "high Total Cabin Pressure (L2)"), ("Total Cabin Pressure (L2) (t-1)", "low Total Cabin Pressure (L2)"),
    ("WRS Delivery Pump (t-1)", "high WRS Delivery Pump"), ("WRS Delivery Pump (t-1)", "low WRS Delivery Pump"),
    ("WRS Valve Flow (t-1)", "high WRS Valve Flow"), ("WRS Valve Flow (t-1)", "low WRS Valve Flow")
]

for edge in temporal_nodes:
    network.append(edge)

# Add connections between spatial variables (e.g., ppO2 (L1) and ppO2 (L2)). Note that these connections
# are only added one way (from L1 to L2), as these relationships are assumed to be symmetrical (same effect
# both ways). 
# NOTE: Confirm that this effect is observed when adding partial telemetry values.
spatial_nodes = [
    ("Cabin Temperature (L1)", "high Cabin Temperature (L2)"), ("Cabin Temperature (L1)", "low Cabin Temperature (L2)"),
    ("Humidity (L1)", "high Humidity (L2)"), ("Humidity (L1)", "low Humidity (L2)"),
    ("ppCO2 (L1)", "high ppCO2 (L2)"), ("ppCO2 (L1)", "low ppCO2 (L2)"),
    ("ppH2 (L1)", "high ppH2 (L2)"), ("ppH2 (L1)", "low ppH2 (L2)"),
    ("ppN2 (L1)", "high ppN2 (L2)"), ("ppN2 (L1)", "low ppN2 (L2)"),
    ("ppO2 (L1)", "high ppO2 (L2)"), ("ppO2 (L1)", "low ppO2 (L2)"),
    ("Pressure (L1)", "high Pressure (L2)"), ("Pressure (L1)", "low Pressure (L2)"),
    ("Total Cabin Pressure (L1)", "high Total Cabin Pressure (L2)"), ("Total Cabin Pressure (L1)", "low Total Cabin Pressure (L2)"),
]

for edge in spatial_nodes:
    network.append(edge)

# Add nodes for anomaly subgroups. Breaking the anomalies into smaller subgroups allows the CPT for 'No Anomalies Present'
# to be computed with less entries.
# Specifically, 2^7 has 128 combinations of parent states, instead of 2^31 yielding 2,147,483,648 combinations
# Flipped such that the groups are child nodes of their related anomalies, as the group state is deterministic based on the status of the related anomalies
group_nodes = [
    # Group 1: Carbon Dioxide Removal
    ("CDRA Failure", "Group 1"),
    ("CDRA LiOH Canister Saturation", "Group 1"),
    ("Emergency O2 System Maintenance", "Group 1"),
    ("Excess CO2 in Cabin", "Group 1"),
    ("Excess Water Vapor Pressure in Cabin", "Group 1"),
    ("RWGSR Malfunction", "Group 1"),

    # Group 2: Trace Contaminants
    ("Excess Gas Leak", "Group 2"),
    ("TCCS Auxiliary Fan #1 Failure", "Group 2"),
    ("TCCS Auxiliary Fan #2 Failure", "Group 2"),
    ("TCCS Auxiliary Fan at Reduced Capacity", "Group 2"),
    ("TCCS Filter Clog", "Group 2"),
    ("Trace Contaminants", "Group 2"),

    # Group 3: Water
    ("Biological Filter Saturation", "Group 3"),
    ("Electrolysis System Failure", "Group 3"),
    ("SPE System Maintenance", "Group 3"),
    ("WRS Failure", "Group 3"),
    ("WRS Maintenance", "Group 3"),
    ("WRS Off-nominal pH Level", "Group 3"),

    # Group 4: Power
    ("Fuel Cell #1 and PDU Failure", "Group 4"),
    ("Fuel Cell #2 and PDU Failure", "Group 4"),
    ("Fuel Cell Degrade", "Group 4"),
    ("Fuel Cell Failure", "Group 4"),
    ("PDU 4 Failure", "Group 4"),
    ("PDU 5 Failure", "Group 4"),

    # Group 5: MOXIE
    ("MOXIE Antenna Failure", "Group 5"),
    ("MOXIE ECM Failure", "Group 5"),
    ("MOXIE Fan Failure", "Group 5"),

    # Group 6: Main Cabin Fan
    ("Main Cabin Fan Failure", "Group 6"),
    ("Reduced Main Cabin Fan #1 Capacity", "Group 6"),

    # Group 7: Decompression
    ("Loss of Pressure", "Group 7"),
    ("N2 Tank Burst", "Group 7")
]

for group in group_nodes:
    network.append(group)

# Add nodes for subgroups related to NAP node
# Flipped such that the NAP node is a child of the groups, as its state is deterministic based on the status of the subgroups
no_anomalies_nodes = [
    ("Group 1", "No Anomalies Present"),
    ("Group 2", "No Anomalies Present"),
    ("Group 3", "No Anomalies Present"),
    ("Group 4", "No Anomalies Present"),
    ("Group 5", "No Anomalies Present"),
    ("Group 6", "No Anomalies Present"),
    ("Group 7", "No Anomalies Present")
]

for nap in no_anomalies_nodes:
    network.append(nap)