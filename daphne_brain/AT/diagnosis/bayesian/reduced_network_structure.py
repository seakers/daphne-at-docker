# reduced_network_struture.py
# Author: Joshua Elston
# Last Edited: 03/03/2026

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

from collections import defaultdict

reduced_network = [
    # Biological Filter Saturation (IHab) <-- point source for failure
    ("Biological Filter Saturation (IHab)", "high ppCO2_IHab (IHab)"), ("Biological Filter Saturation (IHab)", "high ppCO2_IHab (IHab) (t-1)"),
    ("Biological Filter Saturation (IHab)", "high ppO2_IHab (IHab)"), ("Biological Filter Saturation (IHab)", "high ppO2_IHab (IHab) (t-1)"),
    ("Biological Filter Saturation (IHab)", "low ppCO2_IHab (IHab)"), ("Biological Filter Saturation (IHab)", "low ppCO2_IHab (IHab) (t-1)"),
    ("Biological Filter Saturation (IHab)", "low ppO2_IHab (IHab)"), ("Biological Filter Saturation (IHab)", "low ppO2_IHab (IHab) (t-1)"),
    ("Biological Filter Saturation (IHab)", "[HIDDEN] BFS Component"),

    # Biological Filter Saturation (Habitat) <-- symptoms manifested throughout Gateway
    ("Biological Filter Saturation (Habitat)", "high ppCO2_IHab (IHab)"), ("Biological Filter Saturation (Habitat)", "high ppCO2_IHab (IHab) (t-1)"),
    ("Biological Filter Saturation (Habitat)", "high ppO2_IHab (IHab)"), ("Biological Filter Saturation (Habitat)", "high ppO2_IHab (IHab) (t-1)"),
    ("Biological Filter Saturation (Habitat)", "low ppCO2_IHab (IHab)"), ("Biological Filter Saturation (Habitat)", "low ppCO2_IHab (IHab) (t-1)"),
    ("Biological Filter Saturation (Habitat)", "low ppO2_IHab (IHab)"), ("Biological Filter Saturation (Habitat)", "low ppO2_IHab (IHab) (t-1)"),
    ("Biological Filter Saturation (Habitat)", "high ppCO2_HALO (HALO)"), ("Biological Filter Saturation (Habitat)", "high ppCO2_HALO (HALO) (t-1)"),
    ("Biological Filter Saturation (Habitat)", "high ppO2_HALO (HALO)"), ("Biological Filter Saturation (Habitat)", "high ppO2_HALO (HALO) (t-1)"),
    ("Biological Filter Saturation (Habitat)", "low ppCO2_HALO (HALO)"), ("Biological Filter Saturation (Habitat)", "low ppCO2_HALO (HALO) (t-1)"),
    ("Biological Filter Saturation (Habitat)", "low ppO2_HALO (HALO)"), ("Biological Filter Saturation (Habitat)", "low ppO2_HALO (HALO) (t-1)"),
    ("Biological Filter Saturation (Habitat)", "[HIDDEN] BFS Component"),

    # CDRA Failure (IHab) <-- point source for failure
    ("CDRA Failure (IHab)", "high Humidity_IHab (IHab)"), ("CDRA Failure (IHab)", "high Humidity_IHab (IHab) (t-1)"), 
    ("CDRA Failure (IHab)", "high ppCO2_IHab (IHab)"), ("CDRA Failure (IHab)", "high ppCO2_IHab (IHab) (t-1)"), 
    ("CDRA Failure (IHab)", "high ppO2_IHab (IHab)"), ("CDRA Failure (IHab)", "high ppO2_IHab (IHab) (t-1)"), 
    ("CDRA Failure (IHab)", "low Humidity_IHab (IHab)"), ("CDRA Failure (IHab)", "low Humidity_IHab (IHab) (t-1)"),
    ("CDRA Failure (IHab)", "low ppCO2_IHab (IHab)"), ("CDRA Failure (IHab)", "low ppCO2_IHab (IHab) (t-1)"),
    ("CDRA Failure (IHab)", "low ppO2_IHab (IHab)"), ("CDRA Failure (IHab)", "low ppO2_IHab (IHab) (t-1)"),
    ("CDRA Failure (IHab)", "[HIDDEN] CDRA Failure Component"),

    # CDRA Failure (Habitat) <-- symptoms manifested throughout Gateway
    ("CDRA Failure (Habitat)", "high Humidity_IHab (IHab)"), ("CDRA Failure (Habitat)", "high Humidity_IHab (IHab) (t-1)"), 
    ("CDRA Failure (Habitat)", "high ppCO2_IHab (IHab)"), ("CDRA Failure (Habitat)", "high ppCO2_IHab (IHab) (t-1)"), 
    ("CDRA Failure (Habitat)", "high ppO2_IHab (IHab)"), ("CDRA Failure (Habitat)", "high ppO2_IHab (IHab) (t-1)"), 
    ("CDRA Failure (Habitat)", "low Humidity_IHab (IHab)"), ("CDRA Failure (Habitat)", "low Humidity_IHab (IHab) (t-1)"),
    ("CDRA Failure (Habitat)", "low ppCO2_IHab (IHab)"), ("CDRA Failure (Habitat)", "low ppCO2_IHab (IHab) (t-1)"),
    ("CDRA Failure (Habitat)", "low ppO2_IHab (IHab)"), ("CDRA Failure (Habitat)", "low ppO2_IHab (IHab) (t-1)"),
    ("CDRA Failure (Habitat)", "high Humidity_HALO (HALO)"), ("CDRA Failure (Habitat)", "high Humidity_HALO (HALO) (t-1)"),
    ("CDRA Failure (Habitat)", "high ppCO2_HALO (HALO)"), ("CDRA Failure (Habitat)", "high ppCO2_HALO (HALO) (t-1)"),
    ("CDRA Failure (Habitat)", "high ppO2_HALO (HALO)"), ("CDRA Failure (Habitat)", "high ppO2_HALO (HALO) (t-1)"),
    ("CDRA Failure (Habitat)", "low Humidity_HALO (HALO)"), ("CDRA Failure (Habitat)", "low Humidity_HALO (HALO) (t-1)"),
    ("CDRA Failure (Habitat)", "low ppCO2_HALO (HALO)"), ("CDRA Failure (Habitat)", "low ppCO2_HALO (HALO) (t-1)"),
    ("CDRA Failure (Habitat)", "low ppO2_HALO (HALO)"), ("CDRA Failure (Habitat)", "low ppO2_HALO (HALO) (t-1)"),
    ("CDRA Failure (Habitat)", "[HIDDEN] CDRA Failure Component"),

    # # CDRA LiOH Canister Saturation (IHab) <-- for parameter learning, proposing to remove the 'LiOH CO2 Saturation parameter, as that could be the additional evidence
    # ("CDRA LiOH Canister Saturation (IHab)", "high ppCO2_IHab (IHab)"), ("CDRA LiOH Canister Saturation (IHab)", "high ppCO2_IHab (IHab) (t-1)"),
    # ("CDRA LiOH Canister Saturation (IHab)", "high ppO2_IHab (IHab)"), ("CDRA LiOH Canister Saturation (IHab)", "high ppO2_IHab (IHab) (t-1)"),
    # ("CDRA LiOH Canister Saturation (IHab)", "high LiOH CO2 Saturation"), ("CDRA LiOH Canister Saturation (IHab)", "high LiOH CO2 Saturation (t-1)"),
    # ("CDRA LiOH Canister Saturation (IHab)", "low ppCO2_IHab (IHab)"), ("CDRA LiOH Canister Saturation (IHab)", "low ppCO2_IHab (IHab) (t-1)"),
    # ("CDRA LiOH Canister Saturation (IHab)", "low ppO2_IHab (IHab)"), ("CDRA LiOH Canister Saturation (IHab)", "low ppO2_IHab (IHab) (t-1)"),
    # ("CDRA LiOH Canister Saturation (IHab)", "low LiOH CO2 Saturation"), ("CDRA LiOH Canister Saturation (IHab)", "low LiOH CO2 Saturation (t-1)"),
    # ("CDRA LiOH Canister Saturation (IHab)", "[HIDDEN] CDRA LiOH Canister Saturation Component"), # <-- propose just changing name to '[HIDDEN] LiOH CO2 Canister Saturation'

    # # CDRA LiOH Canister Saturation (HALO)
    # ("CDRA LiOH Canister Saturation (HALO)", "high ppCO2_HALO (HALO)"), ("CDRA LiOH Canister Saturation (HALO)", "high ppCO2_HALO (HALO) (t-1)"),
    # ("CDRA LiOH Canister Saturation (HALO)", "high ppO2_HALO (HALO)"), ("CDRA LiOH Canister Saturation (HALO)", "high ppO2_HALO (HALO) (t-1)"),
    # ("CDRA LiOH Canister Saturation (HALO)", "high LiOH CO2 Saturation"), ("CDRA LiOH Canister Saturation (HALO)", "high LiOH CO2 Saturation (t-1)"),
    # ("CDRA LiOH Canister Saturation (HALO)", "low ppCO2_HALO (HALO)"), ("CDRA LiOH Canister Saturation (HALO)", "low ppCO2_HALO (HALO) (t-1)"),
    # ("CDRA LiOH Canister Saturation (HALO)", "low ppO2_HALO (HALO)"), ("CDRA LiOH Canister Saturation (HALO)", "low ppO2_HALO (HALO) (t-1)"),
    # ("CDRA LiOH Canister Saturation (HALO)", "low LiOH CO2 Saturation"), ("CDRA LiOH Canister Saturation (HALO)", "low LiOH CO2 Saturation (t-1)"),
    # ("CDRA LiOH Canister Saturation (HALO)", "[HIDDEN] CDRA LiOH Canister Saturation Component"),

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

    # # Unknown Anomaly (tied to all parameters) <-- already done below
    # ("Unknown Anomaly", "high Humidity_IHab (IHab)"), ("Unknown Anomaly", "low Humidity_IHab (IHab)"),
    # ("Unknown Anomaly", "high Humidity_HALO (HALO)"), ("Unknown Anomaly", "low Humidity_HALO (HALO)"),
    # ("Unknown Anomaly", "high ppCO2_IHab (IHab)"), ("Unknown Anomaly", "low ppCO2_IHab (IHab)"),
    # ("Unknown Anomaly", "hihg ppCO2_HALO (HALO)"), ("Unknown Anomaly", "low ppCO2_HALO (HALO)"),
    # ("Unknown Anomaly", "high ppO2_IHab (IHab)"), ("Unknown Anomaly", "low ppO2_IHab (IHab)"),
    # ("Unknown Anomaly", "high ppO2_HALO (HALO)"), ("Unknown Anomaly", "low ppO2_HALO (HALO)"),
    # ("Unknown Anomaly", "high Total_Cabin_Pressure_IHab (IHab)"), ("Unknown Anomaly", "low Total_Cabin_Pressure_IHab (IHab)"),
    # ("Unknown Anomaly", "high Total_Cabin_Pressure_HALO (HALO)"), ("Unknown Anomaly", "low Total_Cabin_Pressure_HALO (HALO)")
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


## NEW CODE ON 02/11/2026
# Create new edges between all parameters and the 'Unknown Anomaly' Node
ua_edges = []
for _, parameters in network_dict.items():
    for parameter in parameters:
        if parameter.startswith("[HIDDEN]"):
            continue
        ua_edges.append(("Unknown Anomaly", parameter))
# Merge edges into existing network
reduced_network.extend(ua_edges)
reduced_network.sort()

# NOTE: Re-commented out to retain Groups
# # Add nodes for subgroups related to NAP node
# # Flipped such that the NAP node is a child of the groups, as its state is deterministic based on the status of the subgroups
# no_anomalies_nodes = [
#     ("Biological Filter Saturation (IHab)", "No Anomalies Present"),
#     ("Biological Filter Saturation (Habitat)", "No Anomalies Present"),
#     ("CDRA Failure (IHab)", "No Anomalies Present"),
#     ("CDRA Failure (Habitat)", "No Anomalies Present"),
#     ("Emergency O2 System Maintenance (IHab)", "No Anomalies Present"),
#     ("Emergency O2 System Maintenance (HALO)", "No Anomalies Present"),
#     ("Excess CO2 in Cabin (IHab)", "No Anomalies Present"),
#     ("Excess CO2 in Cabin (HALO)", "No Anomalies Present"),
#     ("Loss of Pressure (IHab)", "No Anomalies Present"),
#     ("Loss of Pressure (HALO)", "No Anomalies Present"),
#     ("Unknown Anomaly", "No Anomalies Present")
# ]

# for nap in no_anomalies_nodes:
#     reduced_network.append(nap)


# COMMENTED OUT ON 02/11/2026 TO SEE IF REDUCED NETWORK CAN BE BUILT W/O SUBGROUPS
# # Add combined failure nodes to the network (done here to prevent previous (t-1) automation from impacting anomalies)
# # Updated on 11/01/2025 to correct relationships between high-level and level-specific anomalies (flipping the order)
# combined_failure_nodes = [
#     # Biological Filter Saturation (Combined)
#     ("Biological Filter Saturation (IHab)", "Biological Filter Saturation"),
#     ("Biological Filter Saturation (HALO)", "Biological Filter Saturation"),

#     # CDRA Failure (Combined)
#     ("CDRA Failure (IHab)", "CDRA Failure"),
#     ("CDRA Failure (HALO)", "CDRA Failure"),

#     # Emergency O2 System Maintenance (Combined)
#     ("Emergency O2 System Maintenance (IHab)", "Emergency O2 System Maintenance"),
#     ("Emergency O2 System Maintenance (HALO)", "Emergency O2 System Maintenance"),

#     # Excess CO2 in Cabin (Combined)
#     ("Excess CO2 in Cabin (IHab)", "Excess CO2 in Cabin"),
#     ("Excess CO2 in Cabin (HALO)", "Excess CO2 in Cabin"),

#     # Loss of Pressure (Combined)
#     ("Loss of Pressure (IHab)", "Loss of Pressure"),
#     ("Loss of Pressure (HALO)", "Loss of Pressure"),
# ]

# # Extract the new parent node names
# new_nodes = {parent for parent, _ in combined_failure_nodes}

# # Add any new nodes to the network_dict (parents not already keys)
# for node in new_nodes:
#     if node not in network_dict:
#         network_dict[node] = set()  # initialize an empty set of children

# # Now safely add edges to the network_dict
# for parent, child in combined_failure_nodes:
#     network_dict[parent].add(child)

# # Merge edges back into the main network list
# for parent, children in network_dict.items():
#     for child in children:
#         edge = (parent, child)
#         if edge not in reduced_network:   # avoid duplicates
#             reduced_network.append(edge)

# reduced_network.sort()

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
    ("CDRA Failure (IHab)", "Group 1"),
    ("CDRA Failure (Habitat)", "Group 1"),
    ("Emergency O2 System Maintenance (IHab)", "Group 1"),
    ("Emergency O2 System Maintenance (HALO)", "Group 1"),
    ("Excess CO2 in Cabin (IHab)", "Group 1"),
    ("Excess CO2 in Cabin (HALO)", "Group 1"),
    
    # Group 2: Trace Contaminants
   
    # Group 3: Water
    ("Biological Filter Saturation (IHab)", "Group 3"),
    ("Biological Filter Saturation (Habitat)", "Group 3"),
    
    # Group 4: Power
    
    # Group 5: MOXIE
    
    # Group 6: Main Cabin Fan
    
    # Group 7: Decompression
    ("Loss of Pressure (IHab)", "Group 7"),
    ("Loss of Pressure (HALO)", "Group 7")
]

for group in group_nodes:
    reduced_network.append(group)

# # Add nodes for subgroups related to NAP node
# # Flipped such that the NAP node is a child of the groups, as its state is deterministic based on the status of the subgroups
no_anomalies_nodes = [
    ("Group 1", "No Anomalies Present"),
    # ("Group 2", "No Anomalies Present"),
    ("Group 3", "No Anomalies Present"),
    # ("Group 4", "No Anomalies Present"),
    # ("Group 5", "No Anomalies Present"),
    # ("Group 6", "No Anomalies Present"),
    ("Group 7", "No Anomalies Present"),
    ("Unknown Anomaly", "No Anomalies Present")
]

for nap in no_anomalies_nodes:
    reduced_network.append(nap)