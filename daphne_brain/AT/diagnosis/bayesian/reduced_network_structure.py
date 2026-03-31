# reduced_network_struture.py
# Author: Joshua Elston
# Last Edited: 03/31/2026

# Condensed network structure used to evaluate parameter learning performance from
# Biosim simulation runs (called in learn_probabilities.py)
# Currently contains 5 unique anomalies (10 total), but could be expanded by adding
# additional parameters in the config files (such as H2O, Cabin Temperature, and ppN2/ppH2)

# UPDATES:
# Updated on 02/11/2026 to remove groups and no anomalies present nodes
# Updated on 03/03/2026 to reflect that nodes presently modeled as level-specific when only
# a single point source exists (e.g., only one CDRA onboard) are either from that point source
# or a manifestation of symptoms throughout the habitat. Most Gateway hardware (VCCR and Dehumidifier)
# are located in iHab, while O2 injectors are present in both iHab and HALO.
# Additionally, for anomalies where failures can originate in either module, individual
# module anomaly nodes are retained, without the habitat-wide failure [NEED TO VALIDATE THIS APPROACH]
# Updated on 03/04/2026 to add "Unknown Anomaly" as a parent of "No Anomalies Present"
# Updated on 03/31/2026 to condense all anomalies down to a single node, where all child nodes
# (e.g., from both IHab and HALO) are present; this is used to more accurately learn probabilities
# for the scenario when the hatch is either open or closed; note that a 'Hatch Status' node is also
# added, where a value of '1' indicates an open hatch and '0' indicates a closed hatch

from collections import defaultdict

reduced_network = [
    # Biological Filter Saturation <-- IHab is point source for failure
    ("Biological Filter Saturation", "high ppCO2_IHab (IHab)"), ("Biological Filter Saturation", "high ppCO2_IHab (IHab) (t-1)"),
    ("Biological Filter Saturation", "high ppO2_IHab (IHab)"), ("Biological Filter Saturation", "high ppO2_IHab (IHab) (t-1)"),
    ("Biological Filter Saturation", "low ppCO2_IHab (IHab)"), ("Biological Filter Saturation", "low ppCO2_IHab (IHab) (t-1)"),
    ("Biological Filter Saturation", "low ppO2_IHab (IHab)"), ("Biological Filter Saturation", "low ppO2_IHab (IHab) (t-1)"),
    ("Biological Filter Saturation", "high ppCO2_HALO (HALO)"), ("Biological Filter Saturation", "high ppCO2_HALO (HALO) (t-1)"),
    ("Biological Filter Saturation", "high ppO2_HALO (HALO)"), ("Biological Filter Saturation", "high ppO2_HALO (HALO) (t-1)"),
    ("Biological Filter Saturation", "low ppCO2_HALO (HALO)"), ("Biological Filter Saturation", "low ppCO2_HALO (HALO) (t-1)"),
    ("Biological Filter Saturation", "low ppO2_HALO (HALO)"), ("Biological Filter Saturation", "low ppO2_HALO (HALO) (t-1)"),
    ("Biological Filter Saturation", "Hatch Status"),
    ("Biological Filter Saturation", "[HIDDEN] BFS Component"),

    # CDRA Failure <-- IHab is point source for failure
    ("CDRA Failure", "high Humidity_IHab (IHab)"), ("CDRA Failure", "high Humidity_IHab (IHab) (t-1)"), 
    ("CDRA Failure", "high ppCO2_IHab (IHab)"), ("CDRA Failure", "high ppCO2_IHab (IHab) (t-1)"), 
    ("CDRA Failure", "high ppO2_IHab (IHab)"), ("CDRA Failure", "high ppO2_IHab (IHab) (t-1)"), 
    ("CDRA Failure", "low Humidity_IHab (IHab)"), ("CDRA Failure", "low Humidity_IHab (IHab) (t-1)"),
    ("CDRA Failure", "low ppCO2_IHab (IHab)"), ("CDRA Failure", "low ppCO2_IHab (IHab) (t-1)"),
    ("CDRA Failure", "low ppO2_IHab (IHab)"), ("CDRA Failure", "low ppO2_IHab (IHab) (t-1)"),
    ("CDRA Failure", "high Humidity_HALO (HALO)"), ("CDRA Failure", "high Humidity_HALO (HALO) (t-1)"),
    ("CDRA Failure", "high ppCO2_HALO (HALO)"), ("CDRA Failure", "high ppCO2_HALO (HALO) (t-1)"),
    ("CDRA Failure", "high ppO2_HALO (HALO)"), ("CDRA Failure", "high ppO2_HALO (HALO) (t-1)"),
    ("CDRA Failure", "low Humidity_HALO (HALO)"), ("CDRA Failure", "low Humidity_HALO (HALO) (t-1)"),
    ("CDRA Failure", "low ppCO2_HALO (HALO)"), ("CDRA Failure", "low ppCO2_HALO (HALO) (t-1)"),
    ("CDRA Failure", "low ppO2_HALO (HALO)"), ("CDRA Failure", "low ppO2_HALO (HALO) (t-1)"),
    ("CDRA Failure", "Hatch Status"),
    ("CDRA Failure", "[HIDDEN] CDRA Failure Component"),

    # CDRA LiOH Canister Saturation <-- for parameter learning, proposing to remove the 'LiOH CO2 Saturation parameter,
    # as that could be the additional evidence

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

    # Loss of Pressure (IHab)
    ("Loss of Pressure (IHab)", "high ppCO2_IHab (IHab)"), ("Loss of Pressure (IHab)", "high ppCO2_IHab (IHab) (t-1)"), 
    ("Loss of Pressure (IHab)", "high ppO2_IHab (IHab)"), ("Loss of Pressure (IHab)", "high ppO2_IHab (IHab) (t-1)"), 
    ("Loss of Pressure (IHab)", "high Total_Cabin_Pressure_IHab (IHab)"), ("Loss of Pressure (IHab)", "high Total_Cabin_Pressure_IHab (IHab) (t-1)"),
    ("Loss of Pressure (IHab)", "low ppCO2_IHab (IHab)"), ("Loss of Pressure (IHab)", "low ppCO2_IHab (IHab) (t-1)"),
    ("Loss of Pressure (IHab)", "low ppO2_IHab (IHab)"), ("Loss of Pressure (IHab)", "low ppO2_IHab (IHab) (t-1)"),
    ("Loss of Pressure (IHab)", "low Total_Cabin_Pressure_IHab (IHab)"), ("Loss of Pressure (IHab)", "low Total_Cabin_Pressure_IHab (IHab) (t-1)"),
    ("Loss of Pressure (IHab)", "[HIDDEN] Loss of Pressure Component"),

    # Loss of Pressure (HALO)
    ("Loss of Pressure (HALO)", "high ppCO2_HALO (HALO)"), ("Loss of Pressure (HALO)", "high ppCO2_HALO (HALO) (t-1)"),
    ("Loss of Pressure (HALO)", "high ppO2_HALO (HALO)"), ("Loss of Pressure (HALO)", "high ppO2_HALO (HALO) (t-1)"),
    ("Loss of Pressure (HALO)", "high Total_Cabin_Pressure_HALO (HALO)"), ("Loss of Pressure (HALO)", "high Total_Cabin_Pressure_HALO (HALO) (t-1)"),
    ("Loss of Pressure (HALO)", "low ppCO2_HALO (HALO)"), ("Loss of Pressure (HALO)", "low ppCO2_HALO (HALO) (t-1)"),
    ("Loss of Pressure (HALO)", "low ppO2_HALO (HALO)"), ("Loss of Pressure (HALO)", "low ppO2_HALO (HALO) (t-1)"),
    ("Loss of Pressure (HALO)", "low Total_Cabin_Pressure_HALO (HALO)"), ("Loss of Pressure (HALO)", "low Total_Cabin_Pressure_HALO (HALO) (t-1)"),
    ("Loss of Pressure (HALO)", "[HIDDEN] Loss of Pressure Component"),
]

network_dict = defaultdict(set)
for anomaly, parameter in reduced_network:
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
reduced_network.extend(new_edges)
reduced_network.sort() # sort to keep 'current' and temporal parameters together

# Add connections between temporal variables (e.g., ppO2_IHab (IHab) (t-1) and ppO2_IHab (IHab)). Note that the previous
# time step parameter is added first, as the older measurement has an impact on the current reading
# Updated on 10/23/2025 such that temporal parameters are high X and low X, maintaining consistency with network nodes
temporal_nodes = [
    ("high Humidity_IHab (IHab) (t-1)", "high Humidity_IHab (IHab)"), ("low Humidity_IHab (IHab) (t-1)", "low Humidity_IHab (IHab)"),
    ("high Humidity_HALO (HALO) (t-1)", "high Humidity_HALO (HALO)"), ("low Humidity_HALO (HALO) (t-1)", "low Humidity_HALO (HALO)"),
    ("high ppCO2_IHab (IHab) (t-1)", "high ppCO2_IHab (IHab)"), ("low ppCO2_IHab (IHab) (t-1)", "low ppCO2_IHab (IHab)"), 
    ("high ppCO2_HALO (HALO) (t-1)", "high ppCO2_HALO (HALO)"), ("low ppCO2_HALO (HALO) (t-1)", "low ppCO2_HALO (HALO)"),
    ("high ppO2_IHab (IHab) (t-1)", "high ppO2_IHab (IHab)"), ("low ppO2_IHab (IHab) (t-1)", "low ppO2_IHab (IHab)"),
    ("high ppO2_HALO (HALO) (t-1)", "high ppO2_HALO (HALO)"), ("low ppO2_HALO (HALO) (t-1)", "low ppO2_HALO (HALO)"),
    ("high Total_Cabin_Pressure_IHab (IHab) (t-1)", "high Total_Cabin_Pressure_IHab (IHab)"), ("low Total_Cabin_Pressure_IHab (IHab) (t-1)", "low Total_Cabin_Pressure_IHab (IHab)"),
    ("high Total_Cabin_Pressure_HALO (HALO) (t-1)", "high Total_Cabin_Pressure_HALO (HALO)"), ("low Total_Cabin_Pressure_HALO (HALO) (t-1)", "low Total_Cabin_Pressure_HALO (HALO)"),
]

for edge in temporal_nodes:
    reduced_network.append(edge)

# Add connections between spatial variables (e.g., ppO2_IHab (IHab) and ppO2_HALO (HALO)). Note that these connections
# are only added one way (from IHab to HALO), as these relationships are assumed to be symmetrical (same effect
# both ways). 
# NOTE: Confirm that this effect is observed when adding partial telemetry values.
# Updated on 10/23/2025 such that spatial parameters are high X and low X, maintaining consistency with network nodes
spatial_nodes = [
    ("high Humidity_IHab (IHab)", "high Humidity_HALO (HALO)"), ("low Humidity_IHab (IHab)", "low Humidity_HALO (HALO)"),
    ("high ppCO2_IHab (IHab)", "high ppCO2_HALO (HALO)"), ("low ppCO2_IHab (IHab)", "low ppCO2_HALO (HALO)"),
    ("high ppO2_IHab (IHab)", "high ppO2_HALO (HALO)"), ("low ppO2_IHab (IHab)", "low ppO2_HALO (HALO)"),
    ("high Total_Cabin_Pressure_IHab (IHab)", "high Total_Cabin_Pressure_HALO (HALO)"), ("low Total_Cabin_Pressure_IHab (IHab)", "low Total_Cabin_Pressure_HALO (HALO)"),
]

for edge in spatial_nodes:
    reduced_network.append(edge)

# Add nodes for anomaly subgroups. Breaking the anomalies into smaller subgroups allows the CPT for 'No Anomalies Present'
# to be computed with less entries.
# Specifically, 2^7 has 128 combinations of parent states, instead of 2^31 yielding 2,147,483,648 combinations
# Flipped such that the groups are child nodes of their related anomalies, as the group state is deterministic based on the status of the related anomalies
group_nodes = [
    # Group 1: Carbon Dioxide Removal
    ("CDRA Failure", "Group 1"),
    ("Emergency O2 System Maintenance (IHab)", "Group 1"),
    ("Emergency O2 System Maintenance (HALO)", "Group 1"),
    ("Excess CO2 in Cabin (IHab)", "Group 1"),
    ("Excess CO2 in Cabin (HALO)", "Group 1"),
    
    # Group 2: Trace Contaminants
   
    # Group 3: Water
    ("Biological Filter Saturation", "Group 3"),

    # Group 4: Power
    
    # Group 5: MOXIE
    
    # Group 6: Main Cabin Fan
    
    # Group 7: Decompression
    ("Loss of Pressure (IHab)", "Group 7"),
    ("Loss of Pressure (HALO)", "Group 7")
]

for group in group_nodes:
    reduced_network.append(group)

# NOTE: Updated on 03/05/2026 to replace "No Anomalies Present" with "Unknown Anomaly"
# # Add nodes for subgroups related to Unknown Anomaly node
# # Flipped such that the Unknown Anomaly node is a child of the groups, as its state is deterministic based on the status of the subgroups
unknown_anomaly_nodes = [
    ("Group 1", "Unknown Anomaly"),
    # ("Group 2", "Unknown Anomaly"),
    ("Group 3", "Unknown Anomaly"),
    # ("Group 4", "Unknown Anomaly"),
    # ("Group 5", "Unknown Anomaly"),
    # ("Group 6", "Unknown Anomaly"),
    ("Group 7", "Unknown Anomaly")
    # ("Unknown Anomaly", "Unknown Anomaly")
]

for ua in unknown_anomaly_nodes:
    reduced_network.append(ua)