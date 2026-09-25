# re_network_struture.py
# Author: Joshua Elston
# Last Updated: 03/04/2026

# Define Bayesian network structure --> called in ECLSS_Bayesian_Network.py

# Define the Bayesian network structure ("ANOMALY", "high/low PARAMETER")
# There are 31 anomalies and 79 measurements present in Neo4j. Of these 79 measurements, 35 are unique and directly related to one of the
# 31 aforementioned anomalies, meaning the total network structure below consists of 31 anomalies and 43 measurements. These have been
# updated to include the 8 parameters whose values are measured separately on L1 and L2.
# (See ranges.py for more details)
# 31 hidden nodes, each uniquely related to a specific anomaly, are added with connections to all network anomalies to accurately reflect
# changes in entropy when querying the network with additional evidence. The addition of these hidden node connections is achieved using
# the for loop at the bottom of the script

# UPDATES:
# Changes on 10/17/2025 split failures into different levels if they have symptoms measured seperately
# on L1 and L2 in order for the probabilities to accurately reflect the presence of a failure
# This is the case for 14 anomalies, who have seperate L1 and L2 failures while also being combined into
# a single anomaly at the end
# Changes on 11/01/2025 updated the temporal and spatial parameters to be high X and low X to maintain consistency with network nodes
# Updated on 03/04/2026 to capture unknown anomalies as parents of all parameters and as a standalone input into "No Anomalies Present"

from collections import defaultdict

network = [
    # Biological Filter Saturation
    ("Biological Filter Saturation", "high ppCO2 (L1)"), ("Biological Filter Saturation", "high ppCO2 (L1) (t-1)"),
    ("Biological Filter Saturation", "high ppO2 (L1)"), ("Biological Filter Saturation", "high ppO2 (L1) (t-1)"),
    ("Biological Filter Saturation", "low ppCO2 (L1)"), ("Biological Filter Saturation", "low ppCO2 (L1) (t-1)"),
    ("Biological Filter Saturation", "low ppO2 (L1)"), ("Biological Filter Saturation", "low ppO2 (L1) (t-1)"),
    ("Biological Filter Saturation", "high ppCO2 (L2)"), ("Biological Filter Saturation", "high ppCO2 (L2) (t-1)"),
    ("Biological Filter Saturation", "high ppO2 (L2)"), ("Biological Filter Saturation", "high ppO2 (L2) (t-1)"),
    ("Biological Filter Saturation", "low ppCO2 (L2)"), ("Biological Filter Saturation", "low ppCO2 (L2) (t-1)"),
    ("Biological Filter Saturation", "low ppO2 (L2)"), ("Biological Filter Saturation", "low ppO2 (L2) (t-1)"),
    ("Biological Filter Saturation", "[HIDDEN] Biomass Health"), # UPDATED ON 01/04/2026 FOR IEEE EXAMPLE

    # CDRA Failure
    ("CDRA Failure", "high Humidity (L1)"), ("CDRA Failure", "high Humidity (L1) (t-1)"), 
    ("CDRA Failure", "high ppCO2 (L1)"), ("CDRA Failure", "high ppCO2 (L1) (t-1)"), 
    ("CDRA Failure", "high ppO2 (L1)"), ("CDRA Failure", "high ppO2 (L1) (t-1)"), 
    ("CDRA Failure", "low Humidity (L1)"), ("CDRA Failure", "low Humidity (L1) (t-1)"),
    ("CDRA Failure", "low ppCO2 (L1)"), ("CDRA Failure", "low ppCO2 (L1) (t-1)"),
    ("CDRA Failure", "low ppO2 (L1)"), ("CDRA Failure", "low ppO2 (L1) (t-1)"),
    ("CDRA Failure", "high Humidity (L2)"), ("CDRA Failure", "high Humidity (L2) (t-1)"),
    ("CDRA Failure", "high ppCO2 (L2)"), ("CDRA Failure", "high ppCO2 (L2) (t-1)"),
    ("CDRA Failure", "high ppO2 (L2)"), ("CDRA Failure", "high ppO2 (L2) (t-1)"),
    ("CDRA Failure", "low Humidity (L2)"), ("CDRA Failure", "low Humidity (L2) (t-1)"),
    ("CDRA Failure", "low ppCO2 (L2)"), ("CDRA Failure", "low ppCO2 (L2) (t-1)"),
    ("CDRA Failure", "low ppO2 (L2)"), ("CDRA Failure", "low ppO2 (L2) (t-1)"),
    ("CDRA Failure", "[HIDDEN] CDRA Failure Component"),

    # CDRA LiOH Canister Saturation
    ("CDRA LiOH Canister Saturation", "high ppCO2 (L1)"), ("CDRA LiOH Canister Saturation", "high ppCO2 (L1) (t-1)"),
    ("CDRA LiOH Canister Saturation", "high ppO2 (L1)"), ("CDRA LiOH Canister Saturation", "high ppO2 (L1) (t-1)"),
    ("CDRA LiOH Canister Saturation", "high LiOH CO2 Saturation"), ("CDRA LiOH Canister Saturation", "high LiOH CO2 Saturation (t-1)"),
    ("CDRA LiOH Canister Saturation", "low ppCO2 (L1)"), ("CDRA LiOH Canister Saturation", "low ppCO2 (L1) (t-1)"),
    ("CDRA LiOH Canister Saturation", "low ppO2 (L1)"), ("CDRA LiOH Canister Saturation", "low ppO2 (L1) (t-1)"),
    ("CDRA LiOH Canister Saturation", "low LiOH CO2 Saturation"), ("CDRA LiOH Canister Saturation", "low LiOH CO2 Saturation (t-1)"),
    ("CDRA LiOH Canister Saturation", "high ppCO2 (L2)"), ("CDRA LiOH Canister Saturation", "high ppCO2 (L2) (t-1)"),
    ("CDRA LiOH Canister Saturation", "high ppO2 (L2)"), ("CDRA LiOH Canister Saturation", "high ppO2 (L2) (t-1)"),
    ("CDRA LiOH Canister Saturation", "low ppCO2 (L2)"), ("CDRA LiOH Canister Saturation", "low ppCO2 (L2) (t-1)"),
    ("CDRA LiOH Canister Saturation", "low ppO2 (L2)"), ("CDRA LiOH Canister Saturation", "low ppO2 (L2) (t-1)"),
    ("CDRA LiOH Canister Saturation", "[HIDDEN] CDRA LiOH Canister Saturation Component"),

    # Electrolysis System Failure
    ("Electrolysis System Failure", "high H2O (Crew)"), ("Electrolysis System Failure", "high H2O (Crew) (t-1)"),
    ("Electrolysis System Failure", "high ppO2 (L1)"), ("Electrolysis System Failure", "high ppO2 (L1) (t-1)"), 
    ("Electrolysis System Failure", "high ppO2 (L2)"), ("Electrolysis System Failure", "high ppO2 (L2) (t-1)"),
    ("Electrolysis System Failure", "low H2O (Crew)"), ("Electrolysis System Failure", "low H2O (Crew) (t-1)"),
    ("Electrolysis System Failure", "low ppO2 (L1)"), ("Electrolysis System Failure", "low ppO2 (L1) (t-1)"),
    ("Electrolysis System Failure", "low ppO2 (L2)"), ("Electrolysis System Failure", "low ppO2 (L2) (t-1)"),
    ("Electrolysis System Failure", "[HIDDEN] Electrolysis System Failure Component"),

    # Emergency O2 System Maintenance
    ("Emergency O2 System Maintenance", "high ppO2 (L1)"), ("Emergency O2 System Maintenance", "high ppO2 (L1) (t-1)"),
    ("Emergency O2 System Maintenance", "high ppO2 (L2)"), ("Emergency O2 System Maintenance", "high ppO2 (L2) (t-1)"),
    ("Emergency O2 System Maintenance", "low ppO2 (L1)"), ("Emergency O2 System Maintenance", "low ppO2 (L1) (t-1)"),
    ("Emergency O2 System Maintenance", "low ppO2 (L2)"), ("Emergency O2 System Maintenance", "low ppO2 (L2) (t-1)"),
    ("Emergency O2 System Maintenance", "[HIDDEN] Emergency O2 System Maintenance Component"),

    # Excess CO2 in Cabin
    ("Excess CO2 in Cabin", "high ppCO2 (L1)"), ("Excess CO2 in Cabin", "high ppCO2 (L1) (t-1)"),
    ("Excess CO2 in Cabin", "high ppCO2 (L2)"), ("Excess CO2 in Cabin", "high ppCO2 (L2) (t-1)"),
    ("Excess CO2 in Cabin", "low ppCO2 (L1)"), ("Excess CO2 in Cabin", "low ppCO2 (L1) (t-1)"),
    ("Excess CO2 in Cabin", "low ppCO2 (L2)"), ("Excess CO2 in Cabin", "low ppCO2 (L2) (t-1)"),
    ("Excess CO2 in Cabin", "[HIDDEN] Excess CO2 in Cabin Component"),

    # Excess Gas Leak
    ("Excess Gas Leak", "high ppH2 (L1)"), ("Excess Gas Leak", "high ppH2 (L1) (t-1)"),
    ("Excess Gas Leak", "high ppH2 (L2)"), ("Excess Gas Leak", "high ppH2 (L2) (t-1)"),
    ("Excess Gas Leak", "low ppH2 (L1)"), ("Excess Gas Leak", "low ppH2 (L1) (t-1)"),
    ("Excess Gas Leak", "low ppH2 (L2)"), ("Excess Gas Leak", "low ppH2 (L2) (t-1)"),
    ("Excess Gas Leak", "[HIDDEN] Excess Gas Leak Component"),

    # Excess Water Vapor Pressure in Cabin
    ("Excess Water Vapor Pressure in Cabin", "high Cabin Temperature (L1)"), ("Excess Water Vapor Pressure in Cabin", "high Cabin Temperature (L1) (t-1)"), 
    ("Excess Water Vapor Pressure in Cabin", "high Humidity (L1)"), ("Excess Water Vapor Pressure in Cabin", "high Humidity (L1) (t-1)"),
    ("Excess Water Vapor Pressure in Cabin", "high Cabin Temperature (L2)"), ("Excess Water Vapor Pressure in Cabin", "high Cabin Temperature (L2) (t-1)"),
    ("Excess Water Vapor Pressure in Cabin", "high Humidity (L2)"), ("Excess Water Vapor Pressure in Cabin", "high Humidity (L2) (t-1)"),
    ("Excess Water Vapor Pressure in Cabin", "low Cabin Temperature (L1)"), ("Excess Water Vapor Pressure in Cabin", "low Cabin Temperature (L1) (t-1)"),
    ("Excess Water Vapor Pressure in Cabin", "low Humidity (L1)"), ("Excess Water Vapor Pressure in Cabin", "low Humidity (L1) (t-1)"),
    ("Excess Water Vapor Pressure in Cabin", "low Cabin Temperature (L2)"), ("Excess Water Vapor Pressure in Cabin", "low Cabin Temperature (L2) (t-1)"),
    ("Excess Water Vapor Pressure in Cabin", "low Humidity (L2)"), ("Excess Water Vapor Pressure in Cabin", "low Humidity (L2) (t-1)"),
    ("Excess Water Vapor Pressure in Cabin", "[HIDDEN] Excess Water Vapor Pressure in Cabin Component"),

    # Loss of Pressure
    ("Loss of Pressure", "high ppN2 (L1)"), ("Loss of Pressure", "high ppN2 (L1) (t-1)"), 
    ("Loss of Pressure", "high ppO2 (L1)"), ("Loss of Pressure", "high ppO2 (L1) (t-1)"), 
    ("Loss of Pressure", "high Pressure (L1)"), ("Loss of Pressure", "high Pressure (L1) (t-1)"), 
    ("Loss of Pressure", "high Total Cabin Pressure (L1)"), ("Loss of Pressure", "high Total Cabin Pressure (L1) (t-1)"),
    ("Loss of Pressure", "high ppN2 (L2)"), ("Loss of Pressure", "high ppN2 (L2) (t-1)"),
    ("Loss of Pressure", "high ppO2 (L2)"), ("Loss of Pressure", "high ppO2 (L2) (t-1)"),
    ("Loss of Pressure", "high Pressure (L2)"), ("Loss of Pressure", "high Pressure (L2) (t-1)"),
    ("Loss of Pressure", "high Total Cabin Pressure (L2)"), ("Loss of Pressure", "high Total Cabin Pressure (L2) (t-1)"),
    ("Loss of Pressure", "low ppN2 (L1)"), ("Loss of Pressure", "low ppN2 (L1) (t-1)"),
    ("Loss of Pressure", "low ppO2 (L1)"), ("Loss of Pressure", "low ppO2 (L1) (t-1)"),
    ("Loss of Pressure", "low Pressure (L1)"), ("Loss of Pressure", "low Pressure (L1) (t-1)"), 
    ("Loss of Pressure", "low Total Cabin Pressure (L1)"), ("Loss of Pressure", "low Total Cabin Pressure (L1) (t-1)"),
    ("Loss of Pressure", "low ppN2 (L2)"), ("Loss of Pressure", "low ppN2 (L2) (t-1)"),
    ("Loss of Pressure", "low ppO2 (L2)"), ("Loss of Pressure", "low ppO2 (L2) (t-1)"),
    ("Loss of Pressure", "low Pressure (L2)"), ("Loss of Pressure", "low Pressure (L2) (t-1)"),
    ("Loss of Pressure", "low Total Cabin Pressure (L2)"), ("Loss of Pressure", "low Total Cabin Pressure (L2) (t-1)"),
    ("Loss of Pressure", "[HIDDEN] Loss of Pressure Component"),

    # Main Cabin Fan Failure
    ("Main Cabin Fan Failure", "high Cabin Temperature (L1)"), ("Main Cabin Fan Failure", "high Cabin Temperature (L1) (t-1)"),
    ("Main Cabin Fan Failure", "high Humidity (L1)"), ("Main Cabin Fan Failure", "high Humidity (L1) (t-1)"),
    ("Main Cabin Fan Failure", "high Main Cabin Fan #2"), ("Main Cabin Fan Failure", "high Main Cabin Fan #2 (t-1)"),
    ("Main Cabin Fan Failure", "high Cabin Temperature (L2)"), ("Main Cabin Fan Failure", "high Cabin Temperature (L2) (t-1)"),
    ("Main Cabin Fan Failure", "high Humidity (L2)"), ("Main Cabin Fan Failure", "high Humidity (L2) (t-1)"),
    ("Main Cabin Fan Failure", "low Cabin Temperature (L1)"), ("Main Cabin Fan Failure", "low Cabin Temperature (L1) (t-1)"),
    ("Main Cabin Fan Failure", "low Humidity (L1)"), ("Main Cabin Fan Failure", "low Humidity (L1) (t-1)"),
    ("Main Cabin Fan Failure", "low Main Cabin Fan #2"), ("Main Cabin Fan Failure", "low Main Cabin Fan #2 (t-1)"),
    ("Main Cabin Fan Failure", "low Cabin Temperature (L2)"), ("Main Cabin Fan Failure", "low Cabin Temperature (L2) (t-1)"),
    ("Main Cabin Fan Failure", "low Humidity (L2)"), ("Main Cabin Fan Failure", "low Humidity (L2) (t-1)"),
    ("Main Cabin Fan Failure", "[HIDDEN] Main Cabin Fan Failure Component"),

    # N2 Tank Burst
    ("N2 Tank Burst", "high ppN2 (L1)"), ("N2 Tank Burst", "high ppN2 (L1) (t-1)"),  
    ("N2 Tank Burst", "high Pressure (L1)"), ("N2 Tank Burst", "high Pressure (L1) (t-1)"),
    ("N2 Tank Burst", "high Total Cabin Pressure (L1)"), ("N2 Tank Burst", "high Total Cabin Pressure (L1) (t-1)"),
    ("N2 Tank Burst", "low ppN2 (L1)"), ("N2 Tank Burst", "low ppN2 (L1) (t-1)"),
    ("N2 Tank Burst", "low Pressure (L1)"), ("N2 Tank Burst", "low Pressure (L1) (t-1)"),
    ("N2 Tank Burst", "low Total Cabin Pressure (L1)"), ("N2 Tank Burst", "low Total Cabin Pressure (L1) (t-1)"),
    ("N2 Tank Burst", "high ppN2 (L2)"), ("N2 Tank Burst", "high ppN2 (L2) (t-1)"),
    ("N2 Tank Burst", "high Pressure (L2)"), ("N2 Tank Burst", "high Pressure (L2) (t-1)"),
    ("N2 Tank Burst", "high Total Cabin Pressure (L2)"), ("N2 Tank Burst", "high Total Cabin Pressure (L2) (t-1)"),
    ("N2 Tank Burst", "low ppN2 (L2)"), ("N2 Tank Burst", "low ppN2 (L2) (t-1)"),
    ("N2 Tank Burst", "low Pressure (L2)"), ("N2 Tank Burst", "low Pressure (L2) (t-1)"),
    ("N2 Tank Burst", "low Total Cabin Pressure (L2)"), ("N2 Tank Burst", "low Total Cabin Pressure (L2) (t-1)"),
    ("N2 Tank Burst", "[HIDDEN] N2 Tank Burst Component"),

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

    # RWGSR Malfunction
    ("RWGSR Malfunction", "high H2O (Crew)"), ("RWGSR Malfunction", "high H2O (Crew) (t-1)"),
    ("RWGSR Malfunction", "high ppCO2 (L1)"), ("RWGSR Malfunction", "high ppCO2 (L1) (t-1)"),
    ("RWGSR Malfunction", "high ppO2 (L1)"), ("RWGSR Malfunction", "high ppO2 (L1) (t-1)"),
    ("RWGSR Malfunction", "low H2O (Crew)"), ("RWGSR Malfunction", "low H2O (Crew) (t-1)"),
    ("RWGSR Malfunction", "low ppCO2 (L1)"), ("RWGSR Malfunction", "low ppCO2 (L1) (t-1)"),
    ("RWGSR Malfunction", "low ppO2 (L1)"), ("RWGSR Malfunction", "low ppO2 (L1) (t-1)"),
    ("RWGSR Malfunction", "high ppCO2 (L2)"), ("RWGSR Malfunction", "high ppCO2 (L2) (t-1)"),
    ("RWGSR Malfunction", "high ppO2 (L2)"), ("RWGSR Malfunction", "high ppO2 (L2) (t-1)"),
    ("RWGSR Malfunction", "low ppCO2 (L2)"), ("RWGSR Malfunction", "low ppCO2 (L2) (t-1)"),
    ("RWGSR Malfunction", "low ppO2 (L2)"), ("RWGSR Malfunction", "low ppO2 (L2) (t-1)"),
    ("RWGSR Malfunction", "[HIDDEN] RWGSR Malfunction Component"),

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
# Updated on 10/23/2025 such that temporal parameters are high X and low X, maintaining consistency with network nodes
temporal_nodes = [
    ("high 2-butanone (t-1)", "high 2-butanone"), ("low 2-butanone (t-1)", "low 2-butanone"), 
    ("high Acetaldehyde (t-1)", "high Acetaldehyde"), ("low Acetaldehyde (t-1)", "low Acetaldehyde"),
    ("high Aux Cabin Fan #1 (t-1)", "high Aux Cabin Fan #1"), ("low Aux Cabin Fan #1 (t-1)", "low Aux Cabin Fan #1"), 
    ("high Aux Cabin Fan #2 (t-1)", "high Aux Cabin Fan #2"), ("low Aux Cabin Fan #2 (t-1)", "low Aux Cabin Fan #2"),
    ("high Cabin Temperature (L1) (t-1)", "high Cabin Temperature (L1)"), ("low Cabin Temperature (L1) (t-1)", "low Cabin Temperature (L1)"),
    ("high Cabin Temperature (L2) (t-1)", "high Cabin Temperature (L2)"), ("low Cabin Temperature (L2) (t-1)", "low Cabin Temperature (L2)"),
    ("high Dichloromethane (t-1)", "high Dichloromethane"), ("low Dichloromethane (t-1)", "low Dichloromethane"),
    ("high H2O (Crew) (t-1)", "high H2O (Crew)"), ("low H2O (Crew) (t-1)", "low H2O (Crew)"),
    ("high H2O pH (t-1)", "high H2O pH"), ("low H2O pH (t-1)", "low H2O pH"),
    ("high HMCTS (t-1)", "high HMCTS"), ("low HMCTS (t-1)", "low HMCTS"),
    ("high Humidity (L1) (t-1)", "high Humidity (L1)"), ("low Humidity (L1) (t-1)", "low Humidity (L1)"),
    ("high Humidity (L2) (t-1)", "high Humidity (L2)"), ("low Humidity (L2) (t-1)", "low Humidity (L2)"),
    ("high LiOH CO2 Saturation (t-1)", "high LiOH CO2 Saturation"), ("low LiOH CO2 Saturation (t-1)", "low LiOH CO2 Saturation"), 
    ("high Main Cabin Fan #1 (t-1)", "high Main Cabin Fan #1"), ("low Main Cabin Fan #1 (t-1)", "low Main Cabin Fan #1"),
    ("high Main Cabin Fan #2 (t-1)", "high Main Cabin Fan #2"), ("low Main Cabin Fan #2 (t-1)", "low Main Cabin Fan #2"),
    ("high n_Butanol (t-1)", "high n_Butanol"), ("low n_Butanol (t-1)", "low n_Butanol"),
    ("high ppCO2 (L1) (t-1)", "high ppCO2 (L1)"), ("low ppCO2 (L1) (t-1)", "low ppCO2 (L1)"), 
    ("high ppCO2 (L2) (t-1)", "high ppCO2 (L2)"), ("low ppCO2 (L2) (t-1)", "low ppCO2 (L2)"),
    ("high ppH2 (L1) (t-1)", "high ppH2 (L1)"), ("low ppH2 (L1) (t-1)", "low ppH2 (L1)"), 
    ("high ppH2 (L2) (t-1)", "high ppH2 (L2)"), ("low ppH2 (L2) (t-1)", "low ppH2 (L2)"),
    ("high ppN2 (L1) (t-1)", "high ppN2 (L1)"), ("low ppN2 (L1) (t-1)", "low ppN2 (L1)"),
    ("high ppN2 (L2) (t-1)", "high ppN2 (L2)"), ("low ppN2 (L2) (t-1)", "low ppN2 (L2)"),
    ("high ppO2 (L1) (t-1)", "high ppO2 (L1)"), ("low ppO2 (L1) (t-1)", "low ppO2 (L1)"),
    ("high ppO2 (L2) (t-1)", "high ppO2 (L2)"), ("low ppO2 (L2) (t-1)", "low ppO2 (L2)"),
    ("high Pressure (L1) (t-1)", "high Pressure (L1)"), ("low Pressure (L1) (t-1)", "low Pressure (L1)"),
    ("high Pressure (L2) (t-1)", "high Pressure (L2)"), ("low Pressure (L2) (t-1)", "low Pressure (L2)"),
    ("high Total Cabin Pressure (L1) (t-1)", "high Total Cabin Pressure (L1)"), ("low Total Cabin Pressure (L1) (t-1)", "low Total Cabin Pressure (L1)"),
    ("high Total Cabin Pressure (L2) (t-1)", "high Total Cabin Pressure (L2)"), ("low Total Cabin Pressure (L2) (t-1)", "low Total Cabin Pressure (L2)"),
    ("high WRS Delivery Pump (t-1)", "high WRS Delivery Pump"), ("low WRS Delivery Pump (t-1)", "low WRS Delivery Pump"),
    ("high WRS Valve Flow (t-1)", "high WRS Valve Flow"), ("low WRS Valve Flow (t-1)", "low WRS Valve Flow")
]

for edge in temporal_nodes:
    network.append(edge)

# Add connections between spatial variables (e.g., ppO2 (L1) and ppO2 (L2)). Note that these connections
# are only added one way (from L1 to L2), as these relationships are assumed to be symmetrical (same effect
# both ways). 
# NOTE: Confirm that this effect is observed when adding partial telemetry values.
# Updated on 10/23/2025 such that spatial parameters are high X and low X, maintaining consistency with network nodes
spatial_nodes = [
    ("high Cabin Temperature (L1)", "high Cabin Temperature (L2)"), ("low Cabin Temperature (L1)", "low Cabin Temperature (L2)"),
    ("high Humidity (L1)", "high Humidity (L2)"), ("low Humidity (L1)", "low Humidity (L2)"),
    ("high ppCO2 (L1)", "high ppCO2 (L2)"), ("low ppCO2 (L1)", "low ppCO2 (L2)"),
    ("high ppH2 (L1)", "high ppH2 (L2)"), ("low ppH2 (L1)", "low ppH2 (L2)"),
    ("high ppN2 (L1)", "high ppN2 (L2)"), ("low ppN2 (L1)", "low ppN2 (L2)"),
    ("high ppO2 (L1)", "high ppO2 (L2)"), ("low ppO2 (L1)", "low ppO2 (L2)"),
    ("high Pressure (L1)", "high Pressure (L2)"), ("low Pressure (L1)", "low Pressure (L2)"),
    ("high Total Cabin Pressure (L1)", "high Total Cabin Pressure (L2)"), ("low Total Cabin Pressure (L1)", "low Total Cabin Pressure (L2)"),
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

    # Group 6: Main Cabin Fan
    ("Main Cabin Fan Failure", "Group 6"),
    ("Reduced Main Cabin Fan #1 Capacity", "Group 6"),

    # Group 7: Decompression
    ("Loss of Pressure", "Group 7"),
    ("N2 Tank Burst", "Group 7")
]

for group in group_nodes:
    network.append(group)

# Add nodes for subgroups related to unknown anomaly node
# Flipped such that the unknown anomaly node is a child of the groups, as its state is deterministic based on the status of the subgroups
unknown_anomaly_nodes = [
    ("Group 1", "Unknown Anomaly"),
    ("Group 2", "Unknown Anomaly"),
    ("Group 3", "Unknown Anomaly"),
    ("Group 6", "Unknown Anomaly"),
    ("Group 7", "Unknown Anomaly")
]

for ua in unknown_anomaly_nodes:
    network.append(ua)