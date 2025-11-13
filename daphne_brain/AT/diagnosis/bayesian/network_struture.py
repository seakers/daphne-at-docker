# network_struture.py
# Author: Joshua Elston
# Last Updated: 11/05/2025

# Define Bayesian network structure --> called in ECLSS_Bayesian_Network.py

# Define the Bayesian network structure ("ANOMALY", "high/low PARAMETER")
# There are 31 anomalies and 79 measurements present in Neo4j. Of these 79 measurements, 35 are unique and directly related to one of the
# 31 aforementioned anomalies, meaning the total network structure below consists of 31 anomalies and 43 measurements. These have been
# updated to include the 8 parameters whose values are measured separately in IHab and HALO.
# (See ranges.py for more details)
# 31 hidden nodes, each uniquely related to a specific anomaly, are added with connections to all network anomalies to accurately reflect
# changes in entropy when querying the network with additional evidence. The addition of these hidden node connections is achieved using
# the for loop at the bottom of the script
# Changes on 10/17/2025 split failures into different levels if they have symptoms measured seperately
# within IHab and HALO in order for the probabilities to accurately reflect the presence of a failure
# This is the case for 14 anomalies, who have seperate IHab and HALO failures while also being combined into
# a single anomaly at the end
# Changes on 11/01/2025 updated the temporal and spatial parameters to be high X and low X to maintain consistency with network nodes
# Changes on 11/05/2025 to reflect naming convention for Gateway (L1 -- > IHab, L2 --> HALO)

from collections import defaultdict

network = [
    # Biological Filter Saturation (IHab)
    ("Biological Filter Saturation (IHab)", "high ppCO2_IHab (IHab)"), ("Biological Filter Saturation (IHab)", "high ppCO2_IHab (IHab) (t-1)"),
    ("Biological Filter Saturation (IHab)", "high ppO2_IHab (IHab)"), ("Biological Filter Saturation (IHab)", "high ppO2_IHab (IHab) (t-1)"),
    ("Biological Filter Saturation (IHab)", "low ppCO2_IHab (IHab)"), ("Biological Filter Saturation (IHab)", "low ppCO2_IHab (IHab) (t-1)"),
    ("Biological Filter Saturation (IHab)", "low ppO2_IHab (IHab)"), ("Biological Filter Saturation (IHab)", "low ppO2_IHab (IHab) (t-1)"),
    ("Biological Filter Saturation (IHab)", "[HIDDEN] BFS Component"),

    # Biological Filter Saturation (HALO)
    ("Biological Filter Saturation (HALO)", "high ppCO2_HALO (HALO)"), ("Biological Filter Saturation (HALO)", "high ppCO2_HALO (HALO) (t-1)"),
    ("Biological Filter Saturation (HALO)", "high ppO2_HALO (HALO)"), ("Biological Filter Saturation (HALO)", "high ppO2_HALO (HALO) (t-1)"),
    ("Biological Filter Saturation (HALO)", "low ppCO2_HALO (HALO)"), ("Biological Filter Saturation (HALO)", "low ppCO2_HALO (HALO) (t-1)"),
    ("Biological Filter Saturation (HALO)", "low ppO2_HALO (HALO)"), ("Biological Filter Saturation (HALO)", "low ppO2_HALO (HALO) (t-1)"),
    ("Biological Filter Saturation (HALO)", "[HIDDEN] BFS Component"),

    # CDRA Failure (IHab)
    ("CDRA Failure (IHab)", "high Humidity_IHab (IHab)"), ("CDRA Failure (IHab)", "high Humidity_IHab (IHab) (t-1)"), 
    ("CDRA Failure (IHab)", "high ppCO2_IHab (IHab)"), ("CDRA Failure (IHab)", "high ppCO2_IHab (IHab) (t-1)"), 
    ("CDRA Failure (IHab)", "high ppO2_IHab (IHab)"), ("CDRA Failure (IHab)", "high ppO2_IHab (IHab) (t-1)"), 
    ("CDRA Failure (IHab)", "low Humidity_IHab (IHab)"), ("CDRA Failure (IHab)", "low Humidity_IHab (IHab) (t-1)"),
    ("CDRA Failure (IHab)", "low ppCO2_IHab (IHab)"), ("CDRA Failure (IHab)", "low ppCO2_IHab (IHab) (t-1)"),
    ("CDRA Failure (IHab)", "low ppO2_IHab (IHab)"), ("CDRA Failure (IHab)", "low ppO2_IHab (IHab) (t-1)"),
    ("CDRA Failure (IHab)", "[HIDDEN] CDRA Failure Component"),

    # CDRA Failure (HALO)
    ("CDRA Failure (HALO)", "high Humidity_HALO (HALO)"), ("CDRA Failure (HALO)", "high Humidity_HALO (HALO) (t-1)"),
    ("CDRA Failure (HALO)", "high ppCO2_HALO (HALO)"), ("CDRA Failure (HALO)", "high ppCO2_HALO (HALO) (t-1)"),
    ("CDRA Failure (HALO)", "high ppO2_HALO (HALO)"), ("CDRA Failure (HALO)", "high ppO2_HALO (HALO) (t-1)"),
    ("CDRA Failure (HALO)", "low Humidity_HALO (HALO)"), ("CDRA Failure (HALO)", "low Humidity_HALO (HALO) (t-1)"),
    ("CDRA Failure (HALO)", "low ppCO2_HALO (HALO)"), ("CDRA Failure (HALO)", "low ppCO2_HALO (HALO) (t-1)"),
    ("CDRA Failure (HALO)", "low ppO2_HALO (HALO)"), ("CDRA Failure (HALO)", "low ppO2_HALO (HALO) (t-1)"),
    ("CDRA Failure (HALO)", "[HIDDEN] CDRA Failure Component"),

    # CDRA LiOH Canister Saturation (IHab)
    ("CDRA LiOH Canister Saturation (IHab)", "high ppCO2_IHab (IHab)"), ("CDRA LiOH Canister Saturation (IHab)", "high ppCO2_IHab (IHab) (t-1)"),
    ("CDRA LiOH Canister Saturation (IHab)", "high ppO2_IHab (IHab)"), ("CDRA LiOH Canister Saturation (IHab)", "high ppO2_IHab (IHab) (t-1)"),
    ("CDRA LiOH Canister Saturation (IHab)", "high LiOH CO2 Saturation"), ("CDRA LiOH Canister Saturation (IHab)", "high LiOH CO2 Saturation (t-1)"),
    ("CDRA LiOH Canister Saturation (IHab)", "low ppCO2_IHab (IHab)"), ("CDRA LiOH Canister Saturation (IHab)", "low ppCO2_IHab (IHab) (t-1)"),
    ("CDRA LiOH Canister Saturation (IHab)", "low ppO2_IHab (IHab)"), ("CDRA LiOH Canister Saturation (IHab)", "low ppO2_IHab (IHab) (t-1)"),
    ("CDRA LiOH Canister Saturation (IHab)", "low LiOH CO2 Saturation"), ("CDRA LiOH Canister Saturation (IHab)", "low LiOH CO2 Saturation (t-1)"),
    ("CDRA LiOH Canister Saturation (IHab)", "[HIDDEN] CDRA LiOH Canister Saturation Component"),

    # CDRA LiOH Canister Saturation (HALO)
    ("CDRA LiOH Canister Saturation (HALO)", "high ppCO2_HALO (HALO)"), ("CDRA LiOH Canister Saturation (HALO)", "high ppCO2_HALO (HALO) (t-1)"),
    ("CDRA LiOH Canister Saturation (HALO)", "high ppO2_HALO (HALO)"), ("CDRA LiOH Canister Saturation (HALO)", "high ppO2_HALO (HALO) (t-1)"),
    ("CDRA LiOH Canister Saturation (HALO)", "high LiOH CO2 Saturation"), ("CDRA LiOH Canister Saturation (HALO)", "high LiOH CO2 Saturation (t-1)"),
    ("CDRA LiOH Canister Saturation (HALO)", "low ppCO2_HALO (HALO)"), ("CDRA LiOH Canister Saturation (HALO)", "low ppCO2_HALO (HALO) (t-1)"),
    ("CDRA LiOH Canister Saturation (HALO)", "low ppO2_HALO (HALO)"), ("CDRA LiOH Canister Saturation (HALO)", "low ppO2_HALO (HALO) (t-1)"),
    ("CDRA LiOH Canister Saturation (HALO)", "low LiOH CO2 Saturation"), ("CDRA LiOH Canister Saturation (HALO)", "low LiOH CO2 Saturation (t-1)"),
    ("CDRA LiOH Canister Saturation (HALO)", "[HIDDEN] CDRA LiOH Canister Saturation Component"),

    # Electrolysis System Failure (IHab)
    ("Electrolysis System Failure (IHab)", "high H2O (Crew)"), ("Electrolysis System Failure (IHab)", "high H2O (Crew) (t-1)"),
    ("Electrolysis System Failure (IHab)", "high ppO2_IHab (IHab)"), ("Electrolysis System Failure (IHab)", "high ppO2_IHab (IHab) (t-1)"), 
    ("Electrolysis System Failure (IHab)", "low H2O (Crew)"), ("Electrolysis System Failure (IHab)", "low H2O (Crew) (t-1)"),
    ("Electrolysis System Failure (IHab)", "low ppO2_IHab (IHab)"), ("Electrolysis System Failure (IHab)", "low ppO2_IHab (IHab) (t-1)"),
    ("Electrolysis System Failure (IHab)", "[HIDDEN] Electrolysis System Failure Component"),

    # Electrolysis System Failure (HALO)
    ("Electrolysis System Failure (HALO)", "high H2O (Crew)"), ("Electrolysis System Failure (HALO)", "high H2O (Crew) (t-1)"),
    ("Electrolysis System Failure (HALO)", "high ppO2_HALO (HALO)"), ("Electrolysis System Failure (HALO)", "high ppO2_HALO (HALO) (t-1)"),
    ("Electrolysis System Failure (HALO)", "low H2O (Crew)"), ("Electrolysis System Failure (HALO)", "low H2O (Crew) (t-1)"),
    ("Electrolysis System Failure (HALO)", "low ppO2_HALO (HALO)"), ("Electrolysis System Failure (HALO)", "low ppO2_HALO (HALO) (t-1)"),
    ("Electrolysis System Failure (HALO)", "[HIDDEN] Electrolysis System Failure Component"),

    # Emergency O2 System Maintenance (IHab)
    ("Emergency O2 System Maintenance (IHab)", "high ppO2_IHab (IHab)"), ("Emergency O2 System Maintenance (IHab)", "high ppO2_IHab (IHab) (t-1)"),
    ("Emergency O2 System Maintenance (IHab)", "low ppO2_IHab (IHab)"), ("Emergency O2 System Maintenance (IHab)", "low ppO2_IHab (IHab) (t-1)"),
    ("Emergency O2 System Maintenance (IHab)", "[HIDDEN] Emergency O2 System Maintenance Component"),

    # Emergency O2 System Maintenance (HALO)
    ("Emergency O2 System Maintenance (HALO)", "high ppO2_HALO (HALO)"), ("Emergency O2 System Maintenance (HALO)", "high ppO2_HALO (HALO) (t-1)"),
    ("Emergency O2 System Maintenance (HALO)", "low ppO2_HALO (HALO)"), ("Emergency O2 System Maintenance (HALO)", "low ppO2_HALO (HALO) (t-1)"),
    ("Emergency O2 System Maintenance (HALO)", "[HIDDEN] Emergency O2 System Maintenance Component"),

    # Excess CO2 in Cabin (IHab)
    ("Excess CO2 in Cabin (IHab)", "high ppCO2_IHab (IHab)"), ("Excess CO2 in Cabin (IHab)", "high ppCO2_IHab (IHab) (t-1)"),
    ("Excess CO2 in Cabin (IHab)", "low ppCO2_IHab (IHab)"), ("Excess CO2 in Cabin (IHab)", "low ppCO2_IHab (IHab) (t-1)"),
    ("Excess CO2 in Cabin (IHab)", "[HIDDEN] Excess CO2 in Cabin Component"),

    # Excess CO2 in Cabin (HALO)
    ("Excess CO2 in Cabin (HALO)", "high ppCO2_HALO (HALO)"), ("Excess CO2 in Cabin (HALO)", "high ppCO2_HALO (HALO) (t-1)"),
    ("Excess CO2 in Cabin (HALO)", "low ppCO2_HALO (HALO)"), ("Excess CO2 in Cabin (HALO)", "low ppCO2_HALO (HALO) (t-1)"),
    ("Excess CO2 in Cabin (HALO)", "[HIDDEN] Excess CO2 in Cabin Component"),

    # Excess Gas Leak (IHab)
    ("Excess Gas Leak (IHab)", "high ppH2 (IHab)"), ("Excess Gas Leak (IHab)", "high ppH2 (IHab) (t-1)"),
    ("Excess Gas Leak (IHab)", "low ppH2 (IHab)"), ("Excess Gas Leak (IHab)", "low ppH2 (IHab) (t-1)"),
    ("Excess Gas Leak (IHab)", "[HIDDEN] Excess Gas Leak Component"),

    # Excess Gas Leak (HALO)
    ("Excess Gas Leak (HALO)", "high ppH2 (HALO)"), ("Excess Gas Leak (HALO)", "high ppH2 (HALO) (t-1)"),
    ("Excess Gas Leak (HALO)", "low ppH2 (HALO)"), ("Excess Gas Leak (HALO)", "low ppH2 (HALO) (t-1)"),
    ("Excess Gas Leak (HALO)", "[HIDDEN] Excess Gas Leak Component"),

    # Excess Water Vapor Pressure in Cabin (IHab)
    ("Excess Water Vapor Pressure in Cabin (IHab)", "high Cabin Temperature (IHab)"), ("Excess Water Vapor Pressure in Cabin (IHab)", "high Cabin Temperature (IHab) (t-1)"), 
    ("Excess Water Vapor Pressure in Cabin (IHab)", "high Humidity_IHab (IHab)"), ("Excess Water Vapor Pressure in Cabin (IHab)", "high Humidity_IHab (IHab) (t-1)"),
    ("Excess Water Vapor Pressure in Cabin (IHab)", "low Cabin Temperature (IHab)"), ("Excess Water Vapor Pressure in Cabin (IHab)", "low Cabin Temperature (IHab) (t-1)"),
    ("Excess Water Vapor Pressure in Cabin (IHab)", "low Humidity_IHab (IHab)"), ("Excess Water Vapor Pressure in Cabin (IHab)", "low Humidity_IHab (IHab) (t-1)"),
    ("Excess Water Vapor Pressure in Cabin (IHab)", "[HIDDEN] Excess Water Vapor Pressure in Cabin Component"),

    # Excess Water Vapor Pressure in Cabin (HALO)
    ("Excess Water Vapor Pressure in Cabin (HALO)", "high Cabin Temperature (HALO)"), ("Excess Water Vapor Pressure in Cabin (HALO)", "high Cabin Temperature (HALO) (t-1)"),
    ("Excess Water Vapor Pressure in Cabin (HALO)", "high Humidity_HALO (HALO)"), ("Excess Water Vapor Pressure in Cabin (HALO)", "high Humidity_HALO (HALO) (t-1)"),
    ("Excess Water Vapor Pressure in Cabin (HALO)", "low Cabin Temperature (HALO)"), ("Excess Water Vapor Pressure in Cabin (HALO)", "low Cabin Temperature (HALO) (t-1)"),
    ("Excess Water Vapor Pressure in Cabin (HALO)", "low Humidity_HALO (HALO)"), ("Excess Water Vapor Pressure in Cabin (HALO)", "low Humidity_HALO (HALO) (t-1)"),
    ("Excess Water Vapor Pressure in Cabin (HALO)", "[HIDDEN] Excess Water Vapor Pressure in Cabin Component"),

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

    # Loss of Pressure (IHab)
    ("Loss of Pressure (IHab)", "high ppN2 (IHab)"), ("Loss of Pressure (IHab)", "high ppN2 (IHab) (t-1)"), 
    ("Loss of Pressure (IHab)", "high ppO2_IHab (IHab)"), ("Loss of Pressure (IHab)", "high ppO2_IHab (IHab) (t-1)"), 
    ("Loss of Pressure (IHab)", "high Pressure (IHab)"), ("Loss of Pressure (IHab)", "high Pressure (IHab) (t-1)"), 
    ("Loss of Pressure (IHab)", "high Total_Cabin_Pressure_IHab (IHab)"), ("Loss of Pressure (IHab)", "high Total_Cabin_Pressure_IHab (IHab) (t-1)"),
    ("Loss of Pressure (IHab)", "low ppN2 (IHab)"), ("Loss of Pressure (IHab)", "low ppN2 (IHab) (t-1)"),
    ("Loss of Pressure (IHab)", "low ppO2_IHab (IHab)"), ("Loss of Pressure (IHab)", "low ppO2_IHab (IHab) (t-1)"),
    ("Loss of Pressure (IHab)", "low Pressure (IHab)"), ("Loss of Pressure (IHab)", "low Pressure (IHab) (t-1)"), 
    ("Loss of Pressure (IHab)", "low Total_Cabin_Pressure_IHab (IHab)"), ("Loss of Pressure (IHab)", "low Total_Cabin_Pressure_IHab (IHab) (t-1)"),
    ("Loss of Pressure (IHab)", "[HIDDEN] Loss of Pressure Component"),

    # Loss of Pressure (HALO)
    ("Loss of Pressure (HALO)", "high ppN2 (HALO)"), ("Loss of Pressure (HALO)", "high ppN2 (HALO) (t-1)"),
    ("Loss of Pressure (HALO)", "high ppO2_HALO (HALO)"), ("Loss of Pressure (HALO)", "high ppO2_HALO (HALO) (t-1)"),
    ("Loss of Pressure (HALO)", "high Pressure (HALO)"), ("Loss of Pressure (HALO)", "high Pressure (HALO) (t-1)"),
    ("Loss of Pressure (HALO)", "high Total_Cabin_Pressure_HALO (HALO)"), ("Loss of Pressure (HALO)", "high Total_Cabin_Pressure_HALO (HALO) (t-1)"),
    ("Loss of Pressure (HALO)", "low ppN2 (HALO)"), ("Loss of Pressure (HALO)", "low ppN2 (HALO) (t-1)"),
    ("Loss of Pressure (HALO)", "low ppO2_HALO (HALO)"), ("Loss of Pressure (HALO)", "low ppO2_HALO (HALO) (t-1)"),
    ("Loss of Pressure (HALO)", "low Pressure (HALO)"), ("Loss of Pressure (HALO)", "low Pressure (HALO) (t-1)"),
    ("Loss of Pressure (HALO)", "low Total_Cabin_Pressure_HALO (HALO)"), ("Loss of Pressure (HALO)", "low Total_Cabin_Pressure_HALO (HALO) (t-1)"),
    ("Loss of Pressure (HALO)", "[HIDDEN] Loss of Pressure Component"),

    # Main Cabin Fan Failure (IHab)
    ("Main Cabin Fan Failure (IHab)", "high Cabin Temperature (IHab)"), ("Main Cabin Fan Failure (IHab)", "high Cabin Temperature (IHab) (t-1)"),
    ("Main Cabin Fan Failure (IHab)", "high Humidity_IHab (IHab)"), ("Main Cabin Fan Failure (IHab)", "high Humidity_IHab (IHab) (t-1)"),
    ("Main Cabin Fan Failure (IHab)", "high Main Cabin Fan #2"), ("Main Cabin Fan Failure (IHab)", "high Main Cabin Fan #2 (t-1)"),
    ("Main Cabin Fan Failure (IHab)", "low Cabin Temperature (IHab)"), ("Main Cabin Fan Failure (IHab)", "low Cabin Temperature (IHab) (t-1)"),
    ("Main Cabin Fan Failure (IHab)", "low Humidity_IHab (IHab)"), ("Main Cabin Fan Failure (IHab)", "low Humidity_IHab (IHab) (t-1)"),
    ("Main Cabin Fan Failure (IHab)", "low Main Cabin Fan #2"), ("Main Cabin Fan Failure (IHab)", "low Main Cabin Fan #2 (t-1)"),
    ("Main Cabin Fan Failure (IHab)", "[HIDDEN] Main Cabin Fan Failure Component"),

    # Main Cabin Fan Failure (HALO)
    ("Main Cabin Fan Failure (HALO)", "high Cabin Temperature (HALO)"), ("Main Cabin Fan Failure (HALO)", "high Cabin Temperature (HALO) (t-1)"),
    ("Main Cabin Fan Failure (HALO)", "high Humidity_HALO (HALO)"), ("Main Cabin Fan Failure (HALO)", "high Humidity_HALO (HALO) (t-1)"),
    ("Main Cabin Fan Failure (HALO)", "high Main Cabin Fan #2"), ("Main Cabin Fan Failure (HALO)", "high Main Cabin Fan #2 (t-1)"),
    ("Main Cabin Fan Failure (HALO)", "low Cabin Temperature (HALO)"), ("Main Cabin Fan Failure (HALO)", "low Cabin Temperature (HALO) (t-1)"),
    ("Main Cabin Fan Failure (HALO)", "low Humidity_HALO (HALO)"), ("Main Cabin Fan Failure (HALO)", "low Humidity_HALO (HALO) (t-1)"),
    ("Main Cabin Fan Failure (HALO)", "low Main Cabin Fan #2"), ("Main Cabin Fan Failure (HALO)", "low Main Cabin Fan #2 (t-1)"),
    ("Main Cabin Fan Failure (HALO)", "[HIDDEN] Main Cabin Fan Failure Component"),

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

    # N2 Tank Burst (IHab)
    ("N2 Tank Burst (IHab)", "high ppN2 (IHab)"), ("N2 Tank Burst (IHab)", "high ppN2 (IHab) (t-1)"),  
    ("N2 Tank Burst (IHab)", "high Pressure (IHab)"), ("N2 Tank Burst (IHab)", "high Pressure (IHab) (t-1)"),
    ("N2 Tank Burst (IHab)", "high Total_Cabin_Pressure_IHab (IHab)"), ("N2 Tank Burst (IHab)", "high Total_Cabin_Pressure_IHab (IHab) (t-1)"),
    ("N2 Tank Burst (IHab)", "low ppN2 (IHab)"), ("N2 Tank Burst (IHab)", "low ppN2 (IHab) (t-1)"),
    ("N2 Tank Burst (IHab)", "low Pressure (IHab)"), ("N2 Tank Burst (IHab)", "low Pressure (IHab) (t-1)"),
    ("N2 Tank Burst (IHab)", "low Total_Cabin_Pressure_IHab (IHab)"), ("N2 Tank Burst (IHab)", "low Total_Cabin_Pressure_IHab (IHab) (t-1)"),
    ("N2 Tank Burst (IHab)", "[HIDDEN] N2 Tank Burst Component"),

    # N2 Tank Burst (HALO)
    ("N2 Tank Burst (HALO)", "high ppN2 (HALO)"), ("N2 Tank Burst (HALO)", "high ppN2 (HALO) (t-1)"),
    ("N2 Tank Burst (HALO)", "high Pressure (HALO)"), ("N2 Tank Burst (HALO)", "high Pressure (HALO) (t-1)"),
    ("N2 Tank Burst (HALO)", "high Total_Cabin_Pressure_HALO (HALO)"), ("N2 Tank Burst (HALO)", "high Total_Cabin_Pressure_HALO (HALO) (t-1)"),
    ("N2 Tank Burst (HALO)", "low ppN2 (HALO)"), ("N2 Tank Burst (HALO)", "low ppN2 (HALO) (t-1)"),
    ("N2 Tank Burst (HALO)", "low Pressure (HALO)"), ("N2 Tank Burst (HALO)", "low Pressure (HALO) (t-1)"),
    ("N2 Tank Burst (HALO)", "low Total_Cabin_Pressure_HALO (HALO)"), ("N2 Tank Burst (HALO)", "low Total_Cabin_Pressure_HALO (HALO) (t-1)"),
    ("N2 Tank Burst (HALO)", "[HIDDEN] N2 Tank Burst Component"),

    # PDU 4 Failure (IHab)
    # NOTE: In Neo4j, PDU 5 Bank 1 is mentioned as a symptom for a PDU 4 Failure, but PDU 4 Bank 1 is not mentioned for a PDU 5 failure;
    # given that this is likely an incorrect relationship, the structure below only includes the PDU related to a specific failure
    # (i.e., PDU 4 Bank 1 for a PDU 4 Failure and PDU 5 Bank 1 for a PDU 5 Failure)
    ("PDU 4 Failure (IHab)", "high 2-butanone"), ("PDU 4 Failure (IHab)", "high 2-butanone (t-1)"), 
    ("PDU 4 Failure (IHab)", "high Acetaldehyde"), ("PDU 4 Failure (IHab)", "high Acetaldehyde (t-1)"),
    ("PDU 4 Failure (IHab)", "high Aux Cabin Fan #2"), ("PDU 4 Failure (IHab)", "high Aux Cabin Fan #2 (t-1)"),
    ("PDU 4 Failure (IHab)", "high Cabin Temperature (IHab)"), ("PDU 4 Failure (IHab)", "high Cabin Temperature (IHab) (t-1)"),
    ("PDU 4 Failure (IHab)", "high Humidity_IHab (IHab)"), ("PDU 4 Failure (IHab)", "high Humidity_IHab (IHab) (t-1)"),
    ("PDU 4 Failure (IHab)", "high Main Cabin Fan #2"), ("PDU 4 Failure (IHab)", "high Main Cabin Fan #2 (t-1)"),
    ("PDU 4 Failure (IHab)", "high PDU 4 Bank 1"), ("PDU 4 Failure (IHab)", "high PDU 4 Bank 1 (t-1)"),
    ("PDU 4 Failure (IHab)", "low 2-butanone"), ("PDU 4 Failure (IHab)", "low 2-butanone (t-1)"), 
    ("PDU 4 Failure (IHab)", "low Acetaldehyde"), ("PDU 4 Failure (IHab)", "low Acetaldehyde (t-1)"), 
    ("PDU 4 Failure (IHab)", "low Aux Cabin Fan #2"), ("PDU 4 Failure (IHab)", "low Aux Cabin Fan #2 (t-1)"),
    ("PDU 4 Failure (IHab)", "low Cabin Temperature (IHab)"), ("PDU 4 Failure (IHab)", "low Cabin Temperature (IHab) (t-1)"),
    ("PDU 4 Failure (IHab)", "low Humidity_IHab (IHab)"), ("PDU 4 Failure (IHab)", "low Humidity_IHab (IHab) (t-1)"),
    ("PDU 4 Failure (IHab)", "low Main Cabin Fan #2"), ("PDU 4 Failure (IHab)", "low Main Cabin Fan #2 (t-1)"),
    ("PDU 4 Failure (IHab)", "low PDU 4 Bank 1"), ("PDU 4 Failure (IHab)", "low PDU 4 Bank 1 (t-1)"),
    ("PDU 4 Failure (IHab)", "[HIDDEN] PDU 4 Failure Component"),

    # PDU 4 Failure (HALO)
    ("PDU 4 Failure (HALO)", "high 2-butanone"), ("PDU 4 Failure (HALO)", "high 2-butanone (t-1)"), 
    ("PDU 4 Failure (HALO)", "high Acetaldehyde"), ("PDU 4 Failure (HALO)", "high Acetaldehyde (t-1)"),
    ("PDU 4 Failure (HALO)", "high Aux Cabin Fan #2"), ("PDU 4 Failure (HALO)", "high Aux Cabin Fan #2 (t-1)"),
    ("PDU 4 Failure (HALO)", "high Cabin Temperature (HALO)"), ("PDU 4 Failure (HALO)", "high Cabin Temperature (HALO) (t-1)"),
    ("PDU 4 Failure (HALO)", "high Humidity_HALO (HALO)"), ("PDU 4 Failure (HALO)", "high Humidity_HALO (HALO) (t-1)"),
    ("PDU 4 Failure (HALO)", "high Main Cabin Fan #2"), ("PDU 4 Failure (HALO)", "high Main Cabin Fan #2 (t-1)"), 
    ("PDU 4 Failure (HALO)", "high PDU 4 Bank 1"), ("PDU 4 Failure (HALO)", "high PDU 4 Bank 1 (t-1)"),
    ("PDU 4 Failure (HALO)", "low 2-butanone"), ("PDU 4 Failure (HALO)", "low 2-butanone (t-1)"),
    ("PDU 4 Failure (HALO)", "low Acetaldehyde"), ("PDU 4 Failure (HALO)", "low Acetaldehyde (t-1)"),
    ("PDU 4 Failure (HALO)", "low Aux Cabin Fan #2"), ("PDU 4 Failure (HALO)", "low Aux Cabin Fan #2 (t-1)"),
    ("PDU 4 Failure (HALO)", "low Cabin Temperature (HALO)"), ("PDU 4 Failure (HALO)", "low Cabin Temperature (HALO) (t-1)"),
    ("PDU 4 Failure (HALO)", "low Humidity_HALO (HALO)"), ("PDU 4 Failure (HALO)", "low Humidity_HALO (HALO) (t-1)"),
    ("PDU 4 Failure (HALO)", "low Main Cabin Fan #2"), ("PDU 4 Failure (HALO)", "low Main Cabin Fan #2 (t-1)"),
    ("PDU 4 Failure (HALO)", "low PDU 4 Bank 1"), ("PDU 4 Failure (HALO)", "low PDU 4 Bank 1 (t-1)"),
    ("PDU 4 Failure (HALO)", "[HIDDEN] PDU 4 Failure Component"),

    # PDU 5 Failure (IHab)
    ("PDU 5 Failure (IHab)", "high 2-butanone"), ("PDU 5 Failure (IHab)", "high 2-butanone (t-1)"),
    ("PDU 5 Failure (IHab)", "high Acetaldehyde"), ("PDU 5 Failure (IHab)", "high Acetaldehyde (t-1)"),
    ("PDU 5 Failure (IHab)", "high Aux Cabin Fan #2"), ("PDU 5 Failure (IHab)", "high Aux Cabin Fan #2 (t-1)"),
    ("PDU 5 Failure (IHab)", "high Cabin Temperature (IHab)"), ("PDU 5 Failure (IHab)", "high Cabin Temperature (IHab) (t-1)"),
    ("PDU 5 Failure (IHab)", "high Humidity_IHab (IHab)"), ("PDU 5 Failure (IHab)", "high Humidity_IHab (IHab) (t-1)"),
    ("PDU 5 Failure (IHab)", "high Main Cabin Fan #2"), ("PDU 5 Failure (IHab)", "high Main Cabin Fan #2 (t-1)"),
    ("PDU 5 Failure (IHab)", "high PDU 5 Bank 1"), ("PDU 5 Failure (IHab)", "high PDU 5 Bank 1 (t-1)"),
    ("PDU 5 Failure (IHab)", "low 2-butanone"), ("PDU 5 Failure (IHab)", "low 2-butanone (t-1)"),
    ("PDU 5 Failure (IHab)", "low Acetaldehyde"), ("PDU 5 Failure (IHab)", "low Acetaldehyde (t-1)"),
    ("PDU 5 Failure (IHab)", "low Aux Cabin Fan #2"), ("PDU 5 Failure (IHab)", "low Aux Cabin Fan #2 (t-1)"),
    ("PDU 5 Failure (IHab)", "low Cabin Temperature (IHab)"), ("PDU 5 Failure (IHab)", "low Cabin Temperature (IHab) (t-1)"),
    ("PDU 5 Failure (IHab)", "low Humidity_IHab (IHab)"), ("PDU 5 Failure (IHab)", "low Humidity_IHab (IHab) (t-1)"),
    ("PDU 5 Failure (IHab)", "low Main Cabin Fan #2"), ("PDU 5 Failure (IHab)", "low Main Cabin Fan #2 (t-1)"),
    ("PDU 5 Failure (IHab)", "low PDU 5 Bank 1"), ("PDU 5 Failure (IHab)", "low PDU 5 Bank 1 (t-1)"),
    ("PDU 5 Failure (IHab)", "[HIDDEN] PDU 5 Failure Component"),

    # PDU 5 Failure (HALO)
    ("PDU 5 Failure (HALO)", "high 2-butanone"), ("PDU 5 Failure (HALO)", "high 2-butanone (t-1)"),
    ("PDU 5 Failure (HALO)", "high Acetaldehyde"), ("PDU 5 Failure (HALO)", "high Acetaldehyde (t-1)"),
    ("PDU 5 Failure (HALO)", "high Aux Cabin Fan #2"), ("PDU 5 Failure (HALO)", "high Aux Cabin Fan #2 (t-1)"),
    ("PDU 5 Failure (HALO)", "high Cabin Temperature (HALO)"), ("PDU 5 Failure (HALO)", "high Cabin Temperature (HALO) (t-1)"),
    ("PDU 5 Failure (HALO)", "high Humidity_HALO (HALO)"), ("PDU 5 Failure (HALO)", "high Humidity_HALO (HALO) (t-1)"),
    ("PDU 5 Failure (HALO)", "high Main Cabin Fan #2"), ("PDU 5 Failure (HALO)", "high Main Cabin Fan #2 (t-1)"),
    ("PDU 5 Failure (HALO)", "high PDU 5 Bank 1"), ("PDU 5 Failure (HALO)", "high PDU 5 Bank 1 (t-1)"),
    ("PDU 5 Failure (HALO)", "low 2-butanone"), ("PDU 5 Failure (HALO)", "low 2-butanone (t-1)"),
    ("PDU 5 Failure (HALO)", "low Acetaldehyde"), ("PDU 5 Failure (HALO)", "low Acetaldehyde (t-1)"),
    ("PDU 5 Failure (HALO)", "low Aux Cabin Fan #2"), ("PDU 5 Failure (HALO)", "low Aux Cabin Fan #2 (t-1)"),
    ("PDU 5 Failure (HALO)", "low Cabin Temperature (HALO)"), ("PDU 5 Failure (HALO)", "low Cabin Temperature (HALO) (t-1)"),
    ("PDU 5 Failure (HALO)", "low Humidity_HALO (HALO)"), ("PDU 5 Failure (HALO)", "low Humidity_HALO (HALO) (t-1)"),
    ("PDU 5 Failure (HALO)", "low Main Cabin Fan #2"), ("PDU 5 Failure (HALO)", "low Main Cabin Fan #2 (t-1)"),
    ("PDU 5 Failure (HALO)", "low PDU 5 Bank 1"), ("PDU 5 Failure (HALO)", "low PDU 5 Bank 1 (t-1)"),
    ("PDU 5 Failure (HALO)", "[HIDDEN] PDU 5 Failure Component"),

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

    # RWGSR Malfunction (IHab)
    ("RWGSR Malfunction (IHab)", "high H2O (Crew)"), ("RWGSR Malfunction (IHab)", "high H2O (Crew) (t-1)"),
    ("RWGSR Malfunction (IHab)", "high ppCO2_IHab (IHab)"), ("RWGSR Malfunction (IHab)", "high ppCO2_IHab (IHab) (t-1)"),
    ("RWGSR Malfunction (IHab)", "high ppO2_IHab (IHab)"), ("RWGSR Malfunction (IHab)", "high ppO2_IHab (IHab) (t-1)"),
    ("RWGSR Malfunction (IHab)", "low H2O (Crew)"), ("RWGSR Malfunction (IHab)", "low H2O (Crew) (t-1)"),
    ("RWGSR Malfunction (IHab)", "low ppCO2_IHab (IHab)"), ("RWGSR Malfunction (IHab)", "low ppCO2_IHab (IHab) (t-1)"),
    ("RWGSR Malfunction (IHab)", "low ppO2_IHab (IHab)"), ("RWGSR Malfunction (IHab)", "low ppO2_IHab (IHab) (t-1)"),
    ("RWGSR Malfunction (IHab)", "[HIDDEN] RWGSR Malfunction Component"),

    # RWGSR Malfunction (HALO)
    ("RWGSR Malfunction (HALO)", "high H2O (Crew)"), ("RWGSR Malfunction (HALO)", "high H2O (Crew) (t-1)"),
    ("RWGSR Malfunction (HALO)", "high ppCO2_HALO (HALO)"), ("RWGSR Malfunction (HALO)", "high ppCO2_HALO (HALO) (t-1)"),
    ("RWGSR Malfunction (HALO)", "high ppO2_HALO (HALO)"), ("RWGSR Malfunction (HALO)", "high ppO2_HALO (HALO) (t-1)"),
    ("RWGSR Malfunction (HALO)", "low H2O (Crew)"), ("RWGSR Malfunction (HALO)", "low H2O (Crew) (t-1)"),
    ("RWGSR Malfunction (HALO)", "low ppCO2_HALO (HALO)"), ("RWGSR Malfunction (HALO)", "low ppCO2_HALO (HALO) (t-1)"),
    ("RWGSR Malfunction (HALO)", "low ppO2_HALO (HALO)"), ("RWGSR Malfunction (HALO)", "low ppO2_HALO (HALO) (t-1)"),
    ("RWGSR Malfunction (HALO)", "[HIDDEN] RWGSR Malfunction Component"),

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

# Add combined failure nodes to the network (done here to prevent previous (t-1) automation from impacting anomalies)
# Updated on 11/01/2025 to correct relationships between high-level and level-specific anomalies (flipping the order)
combined_failure_nodes = [
    # Biological Filter Saturation (Combined)
    ("Biological Filter Saturation (IHab)", "Biological Filter Saturation"),
    ("Biological Filter Saturation (HALO)", "Biological Filter Saturation"),

    # CDRA Failure (Combined)
    ("CDRA Failure (IHab)", "CDRA Failure"),
    ("CDRA Failure (HALO)", "CDRA Failure"),

    # CDRA LiOH Canister Saturation (Combined)
    ("CDRA LiOH Canister Saturation (IHab)", "CDRA LiOH Canister Saturation"),
    ("CDRA LiOH Canister Saturation (HALO)", "CDRA LiOH Canister Saturation"),

    # Electrolysis System Failure (Combined)
    ("Electrolysis System Failure (IHab)", "Electrolysis System Failure"),
    ("Electrolysis System Failure (HALO)", "Electrolysis System Failure"),

    # Emergency O2 System Maintenance (Combined)
    ("Emergency O2 System Maintenance (IHab)", "Emergency O2 System Maintenance"),
    ("Emergency O2 System Maintenance (HALO)", "Emergency O2 System Maintenance"),

    # Excess CO2 in Cabin (Combined)
    ("Excess CO2 in Cabin (IHab)", "Excess CO2 in Cabin"),
    ("Excess CO2 in Cabin (HALO)", "Excess CO2 in Cabin"),

    # Excess Gas Leak (Combined)
    ("Excess Gas Leak (IHab)", "Excess Gas Leak"),
    ("Excess Gas Leak (HALO)", "Excess Gas Leak"),

    # Excess Water Vapor Pressure in Cabin (Combined)
    ("Excess Water Vapor Pressure in Cabin (IHab)", "Excess Water Vapor Pressure in Cabin"),
    ("Excess Water Vapor Pressure in Cabin (HALO)", "Excess Water Vapor Pressure in Cabin"),

    # Loss of Pressure (Combined)
    ("Loss of Pressure (IHab)", "Loss of Pressure"),
    ("Loss of Pressure (HALO)", "Loss of Pressure"),

    # Main Cabin Fan Failure (Combined)
    ("Main Cabin Fan Failure (IHab)", "Main Cabin Fan Failure"),
    ("Main Cabin Fan Failure (HALO)", "Main Cabin Fan Failure"),

    # N2 Tank Burst (Combined)
    ("N2 Tank Burst (IHab)", "N2 Tank Burst"),
    ("N2 Tank Burst (HALO)", "N2 Tank Burst"),

    # PDU 4 Failure (Combined)
    ("PDU 4 Failure (IHab)", "PDU 4 Failure"),
    ("PDU 4 Failure (HALO)", "PDU 4 Failure"),

    # PDU 5 Failure (Combined)
    ("PDU 5 Failure (IHab)", "PDU 5 Failure"),
    ("PDU 5 Failure (HALO)", "PDU 5 Failure"),

    # RWGSR Malfunction (Combined)
    ("RWGSR Malfunction (IHab)", "RWGSR Malfunction"),
    ("RWGSR Malfunction (HALO)", "RWGSR Malfunction")
]

# Extract the new parent node names
new_nodes = {parent for parent, _ in combined_failure_nodes}

# Add any new nodes to the network_dict (parents not already keys)
for node in new_nodes:
    if node not in network_dict:
        network_dict[node] = set()  # initialize an empty set of children

# Now safely add edges to the network_dict
for parent, child in combined_failure_nodes:
    network_dict[parent].add(child)

# Merge edges back into the main network list
for parent, children in network_dict.items():
    for child in children:
        edge = (parent, child)
        if edge not in network:   # avoid duplicates
            network.append(edge)

network.sort()

# Add connections between temporal variables (e.g., ppO2_IHab (IHab) (t-1) and ppO2_IHab (IHab)). Note that the previous
# time step parameter is added first, as the older measurement has an impact on the current reading
# Updated on 10/23/2025 such that temporal parameters are high X and low X, maintaining consistency with network nodes
temporal_nodes = [
    ("high 2-butanone (t-1)", "high 2-butanone"), ("low 2-butanone (t-1)", "low 2-butanone"), 
    ("high Acetaldehyde (t-1)", "high Acetaldehyde"), ("low Acetaldehyde (t-1)", "low Acetaldehyde"),
    ("high Aux Cabin Fan #1 (t-1)", "high Aux Cabin Fan #1"), ("low Aux Cabin Fan #1 (t-1)", "low Aux Cabin Fan #1"), 
    ("high Aux Cabin Fan #2 (t-1)", "high Aux Cabin Fan #2"), ("low Aux Cabin Fan #2 (t-1)", "low Aux Cabin Fan #2"),
    ("high Cabin Temperature (IHab) (t-1)", "high Cabin Temperature (IHab)"), ("low Cabin Temperature (IHab) (t-1)", "low Cabin Temperature (IHab)"),
    ("high Cabin Temperature (HALO) (t-1)", "high Cabin Temperature (HALO)"), ("low Cabin Temperature (HALO) (t-1)", "low Cabin Temperature (HALO)"),
    ("high Dichloromethane (t-1)", "high Dichloromethane"), ("low Dichloromethane (t-1)", "low Dichloromethane"),
    ("high Fuel Cell #1 Current (t-1)", "high Fuel Cell #1 Current"), ("low Fuel Cell #1 Current (t-1)", "low Fuel Cell #1 Current"),
    ("high Fuel Cell #1 PQM (t-1)", "high Fuel Cell #1 PQM"), ("low Fuel Cell #1 PQM (t-1)", "low Fuel Cell #1 PQM"),
    ("high Fuel Cell #1 Stack Out Temp (t-1)", "high Fuel Cell #1 Stack Out Temp"), ("low Fuel Cell #1 Stack Out Temp (t-1)", "low Fuel Cell #1 Stack Out Temp"),
    ("high Fuel Cell #1 Voltage (t-1)", "high Fuel Cell #1 Voltage"), ("low Fuel Cell #1 Voltage (t-1)", "low Fuel Cell #1 Voltage"), 
    ("high Fuel Cell #2 Current (t-1)", "high Fuel Cell #2 Current"), ("low Fuel Cell #2 Current (t-1)", "low Fuel Cell #2 Current"),
    ("high Fuel Cell #2 PQM (t-1)", "high Fuel Cell #2 PQM"), ("low Fuel Cell #2 PQM (t-1)", "low Fuel Cell #2 PQM"), 
    ("high Fuel Cell #2 Stack Out Temp (t-1)", "high Fuel Cell #2 Stack Out Temp"), ("low Fuel Cell #2 Stack Out Temp (t-1)", "low Fuel Cell #2 Stack Out Temp"),
    ("high Fuel Cell #2 Voltage (t-1)", "high Fuel Cell #2 Voltage"), ("low Fuel Cell #2 Voltage (t-1)", "low Fuel Cell #2 Voltage"), 
    ("high H2O (Crew) (t-1)", "high H2O (Crew)"), ("low H2O (Crew) (t-1)", "low H2O (Crew)"),
    ("high H2O pH (t-1)", "high H2O pH"), ("low H2O pH (t-1)", "low H2O pH"),
    ("high HMCTS (t-1)", "high HMCTS"), ("low HMCTS (t-1)", "low HMCTS"),
    ("high Humidity_IHab (IHab) (t-1)", "high Humidity_IHab (IHab)"), ("low Humidity_IHab (IHab) (t-1)", "low Humidity_IHab (IHab)"),
    ("high Humidity_HALO (HALO) (t-1)", "high Humidity_HALO (HALO)"), ("low Humidity_HALO (HALO) (t-1)", "low Humidity_HALO (HALO)"),
    ("high LiOH CO2 Saturation (t-1)", "high LiOH CO2 Saturation"), ("low LiOH CO2 Saturation (t-1)", "low LiOH CO2 Saturation"), 
    ("high Main Cabin Fan #1 (t-1)", "high Main Cabin Fan #1"), ("low Main Cabin Fan #1 (t-1)", "low Main Cabin Fan #1"),
    ("high Main Cabin Fan #2 (t-1)", "high Main Cabin Fan #2"), ("low Main Cabin Fan #2 (t-1)", "low Main Cabin Fan #2"),
    ("high MOXIE Compressor Temp (t-1)", "high MOXIE Compressor Temp"), ("low MOXIE Compressor Temp (t-1)", "low MOXIE Compressor Temp"),
    ("high MOXIE Telemetry Quality (t-1)", "high MOXIE Telemetry Quality"), ("low MOXIE Telemetry Quality (t-1)", "low MOXIE Telemetry Quality"),
    ("high n_Butanol (t-1)", "high n_Butanol"), ("low n_Butanol (t-1)", "low n_Butanol"),
    ("high PDU 4 Bank 1 (t-1)", "high PDU 4 Bank 1"), ("low PDU 4 Bank 1 (t-1)", "low PDU 4 Bank 1"),
    ("high PDU 5 Bank 1 (t-1)", "high PDU 5 Bank 1"), ("low PDU 5 Bank 1 (t-1)", "low PDU 5 Bank 1"),
    ("high ppCO2_IHab (IHab) (t-1)", "high ppCO2_IHab (IHab)"), ("low ppCO2_IHab (IHab) (t-1)", "low ppCO2_IHab (IHab)"), 
    ("high ppCO2_HALO (HALO) (t-1)", "high ppCO2_HALO (HALO)"), ("low ppCO2_HALO (HALO) (t-1)", "low ppCO2_HALO (HALO)"),
    ("high ppH2 (IHab) (t-1)", "high ppH2 (IHab)"), ("low ppH2 (IHab) (t-1)", "low ppH2 (IHab)"), 
    ("high ppH2 (HALO) (t-1)", "high ppH2 (HALO)"), ("low ppH2 (HALO) (t-1)", "low ppH2 (HALO)"),
    ("high ppN2 (IHab) (t-1)", "high ppN2 (IHab)"), ("low ppN2 (IHab) (t-1)", "low ppN2 (IHab)"),
    ("high ppN2 (HALO) (t-1)", "high ppN2 (HALO)"), ("low ppN2 (HALO) (t-1)", "low ppN2 (HALO)"),
    ("high ppO2_IHab (IHab) (t-1)", "high ppO2_IHab (IHab)"), ("low ppO2_IHab (IHab) (t-1)", "low ppO2_IHab (IHab)"),
    ("high ppO2_HALO (HALO) (t-1)", "high ppO2_HALO (HALO)"), ("low ppO2_HALO (HALO) (t-1)", "low ppO2_HALO (HALO)"),
    ("high Pressure (IHab) (t-1)", "high Pressure (IHab)"), ("low Pressure (IHab) (t-1)", "low Pressure (IHab)"),
    ("high Pressure (HALO) (t-1)", "high Pressure (HALO)"), ("low Pressure (HALO) (t-1)", "low Pressure (HALO)"),
    ("high SOXIE Stack Temp (t-1)", "high SOXIE Stack Temp"), ("low SOXIE Stack Temp (t-1)", "low SOXIE Stack Temp"), 
    ("high Total_Cabin_Pressure_IHab (IHab) (t-1)", "high Total_Cabin_Pressure_IHab (IHab)"), ("low Total_Cabin_Pressure_IHab (IHab) (t-1)", "low Total_Cabin_Pressure_IHab (IHab)"),
    ("high Total_Cabin_Pressure_HALO (HALO) (t-1)", "high Total_Cabin_Pressure_HALO (HALO)"), ("low Total_Cabin_Pressure_HALO (HALO) (t-1)", "low Total_Cabin_Pressure_HALO (HALO)"),
    ("high WRS Delivery Pump (t-1)", "high WRS Delivery Pump"), ("low WRS Delivery Pump (t-1)", "low WRS Delivery Pump"),
    ("high WRS Valve Flow (t-1)", "high WRS Valve Flow"), ("low WRS Valve Flow (t-1)", "low WRS Valve Flow")
]

for edge in temporal_nodes:
    network.append(edge)

# Add connections between spatial variables (e.g., ppO2_IHab (IHab) and ppO2_HALO (HALO)). Note that these connections
# are only added one way (from IHab to HALO), as these relationships are assumed to be symmetrical (same effect
# both ways). 
# NOTE: Confirm that this effect is observed when adding partial telemetry values.
# Updated on 10/23/2025 such that spatial parameters are high X and low X, maintaining consistency with network nodes
spatial_nodes = [
    ("high Cabin Temperature (IHab)", "high Cabin Temperature (HALO)"), ("low Cabin Temperature (IHab)", "low Cabin Temperature (HALO)"),
    ("high Humidity_IHab (IHab)", "high Humidity_HALO (HALO)"), ("low Humidity_IHab (IHab)", "low Humidity_HALO (HALO)"),
    ("high ppCO2_IHab (IHab)", "high ppCO2_HALO (HALO)"), ("low ppCO2_IHab (IHab)", "low ppCO2_HALO (HALO)"),
    ("high ppH2 (IHab)", "high ppH2 (HALO)"), ("low ppH2 (IHab)", "low ppH2 (HALO)"),
    ("high ppN2 (IHab)", "high ppN2 (HALO)"), ("low ppN2 (IHab)", "low ppN2 (HALO)"),
    ("high ppO2_IHab (IHab)", "high ppO2_HALO (HALO)"), ("low ppO2_IHab (IHab)", "low ppO2_HALO (HALO)"),
    ("high Pressure (IHab)", "high Pressure (HALO)"), ("low Pressure (IHab)", "low Pressure (HALO)"),
    ("high Total_Cabin_Pressure_IHab (IHab)", "high Total_Cabin_Pressure_HALO (HALO)"), ("low Total_Cabin_Pressure_IHab (IHab)", "low Total_Cabin_Pressure_HALO (HALO)"),
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