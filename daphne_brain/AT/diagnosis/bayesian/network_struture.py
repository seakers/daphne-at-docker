# network_struture.py
# Author: Joshua Elston
# Last Updated: 03/27/2025

# Define Bayesian network structure --> called in ECLSS_Bayesian_Network.py

# Define the Bayesian network structure ("ANOMALY", "high/low PARAMETER")
# There are 31 anomalies and 79 measurements present in Neo4j. Of these 79 measurements, 35 are unique and directly related to one of the
# 31 aforementioned anomalies, meaning the total network structure below consists of 31 anomalies and 35 measurements.
# (See ranges.py for more details)
# 31 hidden nodes, each uniquely related to a specific anomaly, are added with connections to all network anomalies to accurately reflect
# changes in entropy when querying the network with additional evidence. The addition of these hidden node connections is achieved using
# the for loop at the bottom of the script
network = [
    # Biological Filter Saturation
    ("Biological Filter Saturation", "high ppCO2"), ("Biological Filter Saturation", "high ppO2"),
    ("Biological Filter Saturation", "low ppCO2"), ("Biological Filter Saturation", "low ppO2"),
    ("Biological Filter Saturation", "[HIDDEN] BFS Component"),

    # CDRA Failure
    ("CDRA Failure", "high Humidity"), ("CDRA Failure", "high ppCO2"), ("CDRA Failure", "high ppO2"),
    ("CDRA Failure", "low Humidity"), ("CDRA Failure", "low ppCO2"), ("CDRA Failure", "low ppO2"),
    ("CDRA Failure", "[HIDDEN] CDRA Failure Component"),

    # CDRA LiOH Canister Saturation
    ("CDRA LiOH Canister Saturation", "high ppCO2"), ("CDRA LiOH Canister Saturation", "high ppO2"), ("CDRA LiOH Canister Saturation", "high LiOH CO2 Saturation"),
    ("CDRA LiOH Canister Saturation", "low ppCO2"), ("CDRA LiOH Canister Saturation", "low ppO2"), ("CDRA LiOH Canister Saturation", "low LiOH CO2 Saturation"),
    ("CDRA LiOH Canister Saturation", "[HIDDEN] CDRA LiOH Canister Saturation Component"),

    # Electrolysis System Failure
    ("Electrolysis System Failure", "high H2O (Crew)"), ("Electrolysis System Failure", "high ppO2"),
    ("Electrolysis System Failure", "low H2O (Crew)"), ("Electrolysis System Failure", "low ppO2"),
    ("Electrolysis System Failure", "[HIDDEN] Electrolysis System Failure Component"),

    # Emergency O2 System Maintenance
    ("Emergency O2 System Maintenance", "high ppO2"),
    ("Emergency O2 System Maintenance", "low ppO2"),
    ("Emergency O2 System Maintenance", "[HIDDEN] Emergency O2 System Maintenance Component"),

    # Excess CO2 in Cabin
    ("Excess CO2 in Cabin", "high ppCO2"),
    ("Excess CO2 in Cabin", "low ppCO2"),
    ("Excess CO2 in Cabin", "[HIDDEN] Excess CO2 in Cabin Component"),

    # Excess Gas Leak
    ("Excess Gas Leak", "high ppH2"),
    ("Excess Gas Leak", "low ppH2"),
    ("Excess Gas Leak", "[HIDDEN] Excess Gas Leak Component"),

    # Excess Water Vapor Pressure in Cabin
    ("Excess Water Vapor Pressure in Cabin", "high Cabin Temperature"), ("Excess Water Vapor Pressure in Cabin", "high Humidity"),
    ("Excess Water Vapor Pressure in Cabin", "low Cabin Temperature"), ("Excess Water Vapor Pressure in Cabin", "low Humidity"),
    ("Excess Water Vapor Pressure in Cabin", "[HIDDEN] Excess Water Vapor Pressure in Cabin Component"),

    # Fuel Cell #1 and PDU Failure
    ("Fuel Cell #1 and PDU Failure", "high 2-butanone"), ("Fuel Cell #1 and PDU Failure", "high Acetaldehyde"), 
    ("Fuel Cell #1 and PDU Failure", "high Aux Cabin Fan #2"), ("Fuel Cell #1 and PDU Failure", "high Fuel Cell #1 Current"),
    ("Fuel Cell #1 and PDU Failure", "high Fuel Cell #1 PQM"), ("Fuel Cell #1 and PDU Failure", "high Fuel Cell #1 Stack Out Temp"), 
    ("Fuel Cell #1 and PDU Failure", "high Fuel Cell #1 Voltage"), ("Fuel Cell #1 and PDU Failure", "high Main Cabin Fan #2"), 
    ("Fuel Cell #1 and PDU Failure", "high PDU 4 Bank 1"),
    ("Fuel Cell #1 and PDU Failure", "low 2-butanone"), ("Fuel Cell #1 and PDU Failure", "low Acetaldehyde"), 
    ("Fuel Cell #1 and PDU Failure", "low Aux Cabin Fan #2"), ("Fuel Cell #1 and PDU Failure", "low Fuel Cell #1 Current"),
    ("Fuel Cell #1 and PDU Failure", "low Fuel Cell #1 PQM"), ("Fuel Cell #1 and PDU Failure", "low Fuel Cell #1 Stack Out Temp"), 
    ("Fuel Cell #1 and PDU Failure", "low Fuel Cell #1 Voltage"), ("Fuel Cell #1 and PDU Failure", "low Main Cabin Fan #2"),
    ("Fuel Cell #1 and PDU Failure", "low PDU 4 Bank 1"),
    ("Fuel Cell #1 and PDU Failure", "[HIDDEN] Fuel Cell #1 and PDU Failure Component"),

    # Fuel Cell #2 and PDU Failure
    ("Fuel Cell #2 and PDU Failure", "high 2-butanone"), ("Fuel Cell #2 and PDU Failure", "high Acetaldehyde"), 
    ("Fuel Cell #2 and PDU Failure", "high Aux Cabin Fan #1"), ("Fuel Cell #2 and PDU Failure", "high Fuel Cell #2 Current"),
    ("Fuel Cell #2 and PDU Failure", "high Fuel Cell #2 PQM"), ("Fuel Cell #2 and PDU Failure", "high Fuel Cell #2 Stack Out Temp"),
    ("Fuel Cell #2 and PDU Failure", "high Fuel Cell #2 Voltage"), ("Fuel Cell #2 and PDU Failure", "high Main Cabin Fan #1"), 
    ("Fuel Cell #2 and PDU Failure", "high PDU 5 Bank 1"),
    ("Fuel Cell #2 and PDU Failure", "low 2-butanone"), ("Fuel Cell #2 and PDU Failure", "low Acetaldehyde"),
    ("Fuel Cell #2 and PDU Failure", "low Aux Cabin Fan #1"), ("Fuel Cell #2 and PDU Failure", "low Fuel Cell #2 Current"),
    ("Fuel Cell #2 and PDU Failure", "low Fuel Cell #2 PQM"), ("Fuel Cell #2 and PDU Failure", "low Fuel Cell #2 Stack Out Temp"),
    ("Fuel Cell #2 and PDU Failure", "low Fuel Cell #2 Voltage"), ("Fuel Cell #2 and PDU Failure", "low Main Cabin Fan #1"), 
    ("Fuel Cell #2 and PDU Failure", "low PDU 5 Bank 1"),
    ("Fuel Cell #2 and PDU Failure", "[HIDDEN] Fuel Cell #2 and PDU Failure Component"),

    # Fuel Cell Degrade
    ("Fuel Cell Degrade", "high Fuel Cell #2 Current"), ("Fuel Cell Degrade", "high Fuel Cell #2 Stack Out Temp"),
    ("Fuel Cell Degrade", "high Fuel Cell #2 PQM"), ("Fuel Cell Degrade", "high Fuel Cell #2 Voltage"),
    ("Fuel Cell Degrade", "low Fuel Cell #2 Current"), ("Fuel Cell Degrade", "low Fuel Cell #2 Stack Out Temp"),
    ("Fuel Cell Degrade", "low Fuel Cell #2 PQM"), ("Fuel Cell Degrade", "low Fuel Cell #2 Voltage"),
    ("Fuel Cell Degrade", "[HIDDEN] Fuel Cell Degrade Component"),

    # Fuel Cell Failure
    ("Fuel Cell Failure", "high Fuel Cell #2 Current"), ("Fuel Cell Failure", "high Fuel Cell #2 Stack Out Temp"),
    ("Fuel Cell Failure", "high Fuel Cell #2 PQM"), ("Fuel Cell Failure", "high Fuel Cell #2 Voltage"),
    ("Fuel Cell Failure", "low Fuel Cell #2 Current"), ("Fuel Cell Failure", "low Fuel Cell #2 Stack Out Temp"),
    ("Fuel Cell Failure", "low Fuel Cell #2 PQM"), ("Fuel Cell Failure", "low Fuel Cell #2 Voltage"),
    ("Fuel Cell Failure", "[HIDDEN] Fuel Cell Failure Component"),

    # Loss of Pressure
    ("Loss of Pressure", "high ppN2"), ("Loss of Pressure", "high ppO2"), ("Loss of Pressure", "high Pressure"), ("Loss of Pressure", "high Total Cabin Pressure"),
    ("Loss of Pressure", "low ppN2"), ("Loss of Pressure", "low ppO2"), ("Loss of Pressure", "low Pressure"), ("Loss of Pressure", "low Total Cabin Pressure"),
    ("Loss of Pressure", "[HIDDEN] Loss of Pressure Component"),

    # Main Cabin Fan Failure
    ("Main Cabin Fan Failure", "high Cabin Temperature"), ("Main Cabin Fan Failure", "high Humidity"), ("Main Cabin Fan Failure", "high Main Cabin Fan #2"),
    ("Main Cabin Fan Failure", "low Cabin Temperature"), ("Main Cabin Fan Failure", "low Humidity"), ("Main Cabin Fan Failure", "low Main Cabin Fan #2"),
    ("Main Cabin Fan Failure", "[HIDDEN] Main Cabin Fan Failure Component"),

    # MOXIE Antenna Failure
    ("MOXIE Antenna Failure", "high MOXIE Compressor Temp"), ("MOXIE Antenna Failure", "high SOXIE Stack Temp"), ("MOXIE Antenna Failure", "high MOXIE Telemetry Quality"),
    ("MOXIE Antenna Failure", "low MOXIE Compressor Temp"), ("MOXIE Antenna Failure", "low SOXIE Stack Temp"), ("MOXIE Antenna Failure", "low MOXIE Telemetry Quality"),
    ("MOXIE Antenna Failure", "[HIDDEN] MOXIE Antenna Failure Component"),

    # MOXIE ECM Failure
    ("MOXIE ECM Failure", "high SOXIE Stack Temp"),
    ("MOXIE ECM Failure", "low SOXIE Stack Temp"),
    ("MOXIE ECM Failure", "[HIDDEN] MOXIE ECM Failure Component"),

    # MOXIE Fan Failure
    ("MOXIE Fan Failure", "high MOXIE Compressor Temp"),
    ("MOXIE Fan Failure", "low MOXIE Compressor Temp"),
    ("MOXIE Fan Failure", "[HIDDEN] MOXIE Fan Failure Component"),

    # N2 Tank Burst
    ("N2 Tank Burst", "high ppN2"), ("N2 Tank Burst", "high Pressure"), ("N2 Tank Burst", "high Total Cabin Pressure"),
    ("N2 Tank Burst", "low ppN2"), ("N2 Tank Burst", "low Pressure"), ("N2 Tank Burst", "low Total Cabin Pressure"),
    ("N2 Tank Burst", "[HIDDEN] N2 Tank Burst Component"),

    # PDU 4 Failure
    # NOTE: In Neo4j, PDU 5 Bank 1 is mentioned as a symptom for a PDU 4 Failure, but PDU 4 Bank 1 is not mentioned for a PDU 5 failure;
    # given that this is likely an incorrect relationship, the structure below only includes the PDU related to a specific failure
    # (i.e., PDU 4 Bank 1 for a PDU 4 Failure and PDU 5 Bank 1 for a PDU 5 Failure)
    ("PDU 4 Failure", "high 2-butanone"), ("PDU 4 Failure", "high Acetaldehyde"), ("PDU 4 Failure", "high Aux Cabin Fan #2"),
    ("PDU 4 Failure", "high Cabin Temperature"), ("PDU 4 Failure", "high Humidity"), ("PDU 4 Failure", "high Main Cabin Fan #2"), 
    ("PDU 4 Failure", "high PDU 4 Bank 1"),
    ("PDU 4 Failure", "low 2-butanone"), ("PDU 4 Failure", "low Acetaldehyde"), ("PDU 4 Failure", "low Aux Cabin Fan #2"),
    ("PDU 4 Failure", "low Cabin Temperature"), ("PDU 4 Failure", "low Humidity"), ("PDU 4 Failure", "low Main Cabin Fan #2"), 
    ("PDU 4 Failure", "low PDU 4 Bank 1"),
    ("PDU 4 Failure", "[HIDDEN] PDU 4 Failure Component"),

    # PDU 5 Failure
    ("PDU 5 Failure", "high 2-butanone"), ("PDU 5 Failure", "high Acetaldehyde"), ("PDU 5 Failure", "high Aux Cabin Fan #2"),
    ("PDU 5 Failure", "high Cabin Temperature"), ("PDU 5 Failure", "high Humidity"), ("PDU 5 Failure", "high Main Cabin Fan #2"), 
    ("PDU 5 Failure", "high PDU 5 Bank 1"),
    ("PDU 5 Failure", "low 2-butanone"), ("PDU 5 Failure", "low Acetaldehyde"), ("PDU 5 Failure", "low Aux Cabin Fan #2"),
    ("PDU 5 Failure", "low Cabin Temperature"), ("PDU 5 Failure", "low Humidity"), ("PDU 5 Failure", "low Main Cabin Fan #2"),
    ("PDU 5 Failure", "low PDU 5 Bank 1"),
    ("PDU 5 Failure", "[HIDDEN] PDU 5 Failure Component"),

    # Reduced Main Cabin Fan #1 Capacity
    ("Reduced Main Cabin Fan #1 Capacity", "high 2-butanone"), ("Reduced Main Cabin Fan #1 Capacity", "high HMCTS"), 
    ("Reduced Main Cabin Fan #1 Capacity", "high Main Cabin Fan #1"), ("Reduced Main Cabin Fan #1 Capacity", "high n_Butanol"),
    ("Reduced Main Cabin Fan #1 Capacity", "low 2-butanone"), ("Reduced Main Cabin Fan #1 Capacity", "low HMCTS"), 
    ("Reduced Main Cabin Fan #1 Capacity", "low Main Cabin Fan #1"), ("Reduced Main Cabin Fan #1 Capacity", "low n_Butanol"),
    ("Reduced Main Cabin Fan #1 Capacity", "[HIDDEN] Reduced Main Cabin Fan #1 Capacity Component"),

    # RWGSR Malfunction
    ("RWGSR Malfunction", "high H2O (Crew)"), ("RWGSR Malfunction", "high ppCO2"), ("RWGSR Malfunction", "high ppO2"),
    ("RWGSR Malfunction", "low H2O (Crew)"), ("RWGSR Malfunction", "low ppCO2"), ("RWGSR Malfunction", "low ppO2"),
    ("RWGSR Malfunction", "[HIDDEN] RWGSR Malfunction Component"), 

    # SPE System Maintenance
    ("SPE System Maintenance", "high H2O (Crew)"),
    ("SPE System Maintenance", "low H2O (Crew)"),
    ("SPE System Maintenance", "[HIDDEN] SPE System Maintenance Component"),

    # TCCS Auxiliary Fan #1 Failure
    ("TCCS Auxiliary Fan #1 Failure", "high 2-butanone"), ("TCCS Auxiliary Fan #1 Failure", "high Acetaldehyde"), ("TCCS Auxiliary Fan #1 Failure", "high Aux Cabin Fan #1"),
    ("TCCS Auxiliary Fan #1 Failure", "low 2-butanone"), ("TCCS Auxiliary Fan #1 Failure", "low Acetaldehyde"), ("TCCS Auxiliary Fan #1 Failure", "low Aux Cabin Fan #1"),
    ("TCCS Auxiliary Fan #1 Failure", "[HIDDEN] TCCS Auxiliary Fan #1 Failure Component"),

    # TCCS Auxiliary Fan #2 Failure
    ("TCCS Auxiliary Fan #2 Failure", "high 2-butanone"), ("TCCS Auxiliary Fan #2 Failure", "high Acetaldehyde"), ("TCCS Auxiliary Fan #2 Failure", "high Aux Cabin Fan #2"),
    ("TCCS Auxiliary Fan #2 Failure", "low 2-butanone"), ("TCCS Auxiliary Fan #2 Failure", "low Acetaldehyde"), ("TCCS Auxiliary Fan #2 Failure", "low Aux Cabin Fan #2"),
    ("TCCS Auxiliary Fan #2 Failure", "[HIDDEN] TCCS Auxiliary Fan #2 Failure Component"),

    # TCCS Auxiliary Fan at Reduced Capacity
    ("TCCS Auxiliary Fan at Reduced Capacity", "high Acetaldehyde"), ("TCCS Auxiliary Fan at Reduced Capacity", "high Aux Cabin Fan #2"),
    ("TCCS Auxiliary Fan at Reduced Capacity", "high Dichloromethane"), ("TCCS Auxiliary Fan at Reduced Capacity", "high n_Butanol"),
    ("TCCS Auxiliary Fan at Reduced Capacity", "low Acetaldehyde"), ("TCCS Auxiliary Fan at Reduced Capacity", "low Aux Cabin Fan #2"),
    ("TCCS Auxiliary Fan at Reduced Capacity", "low Dichloromethane"), ("TCCS Auxiliary Fan at Reduced Capacity", "low n_Butanol"),
    ("TCCS Auxiliary Fan at Reduced Capacity", "[HIDDEN] TCCS Auxiliary Fan at Reduced Capacity Component"),

    # TCCS Filter Clog
    ("TCCS Filter Clog", "high 2-butanone"), ("TCCS Filter Clog", "high Acetaldehyde"), ("TCCS Filter Clog", "high Dichloromethane"), ("TCCS Filter Clog", "high HMCTS"),
    ("TCCS Filter Clog", "low 2-butanone"), ("TCCS Filter Clog", "low Acetaldehyde"), ("TCCS Filter Clog", "low Dichloromethane"), ("TCCS Filter Clog", "low HMCTS"),
    ("TCCS Filter Clog", "[HIDDEN] TCCS Filter Clog Component"),

    # Trace Contaminants
    ("Trace Contaminants", "high 2-butanone"),
    ("Trace Contaminants", "low 2-butanone"),
    ("Trace Contaminants", "[HIDDEN] Trace Contaminants Component"),

    # WRS Failure
    ("WRS Failure", "high WRS Delivery Pump"), ("WRS Failure", "high WRS Valve Flow"),
    ("WRS Failure", "low WRS Delivery Pump"), ("WRS Failure", "low WRS Valve Flow"),
    ("WRS Failure", "[HIDDEN] WPA Pump Flow Rate"),

    # WRS Maintenance
    ("WRS Maintenance", "high H2O (Crew)"), ("WRS Maintenance", "high WRS Valve Flow"),
    ("WRS Maintenance", "low H2O (Crew)"), ("WRS Maintenance", "low WRS Valve Flow"),
    ("WRS Maintenance", "[HIDDEN] Multifiltration Bed Saturation"),

    # WRS Off-nominal pH Level
    ("WRS Off-nominal pH Level", "high H2O pH"),
    ("WRS Off-nominal pH Level", "low H2O pH"),
    ("WRS Off-nominal pH Level", "[HIDDEN] Ion Exchange Bed Status")
]

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