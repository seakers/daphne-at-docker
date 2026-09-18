# reduced_network_struture.py
# Author: Joshua Elston
# Last Edited: 08/27/2026

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
# Updated on 04/13/2026 such that 'Hatch Status' is more accurately named to 'Fan Status' and is a
# parent of parameters measured seperately in different modules for which different anomalies can occur
# Updated on 04/30/2026 to add edges for No Anomalies Present (to see if nominal data from parameter
# learning is correctly added to the dataset)
# Updated on 07/09/2026 to add edges directly between parameters and group nodes (representing different subsystems)
# to better reflect relationships at a subsystem level; also updated subgroup names to more precisely reflect
# actual ECLSS subsystems
# Updated on 08/26/2026 to reflect new anomaly names to be more precise for Gateway architecture
# Biological Filter Saturation --> OGA Failure (hidden node: OGA Status Panel Indicator)
# CDRA Failure --> VCCR Particulate Filter Saturation (hidden node: VCCR Particulate Filter)
# Excess CO2 in Cabin --> VCCR Sorbent Bed Saturation (hidden node: VCCR Sorbent Bed)
# Emergency O2 System Maintenance --> O2 Delivery System Malfunction (hidden node: Cabin O2 Valve Position Indicator) <-- one for each module
# Loss of Pressure --> Module Decompression (hidden node: Module Pressure Leak) <-- one for each module

from collections import defaultdict

reduced_network = [
    # OGA Failure <-- IHab is point source for failure
    ("OGA Failure", "high ppCO2_IHab (IHab)"), ("OGA Failure", "high ppCO2_IHab (IHab) (t-1)"),
    ("OGA Failure", "high ppO2_IHab (IHab)"), ("OGA Failure", "high ppO2_IHab (IHab) (t-1)"),
    ("OGA Failure", "low ppCO2_IHab (IHab)"), ("OGA Failure", "low ppCO2_IHab (IHab) (t-1)"),
    ("OGA Failure", "low ppO2_IHab (IHab)"), ("OGA Failure", "low ppO2_IHab (IHab) (t-1)"),
    ("OGA Failure", "high ppCO2_HALO (HALO)"), ("OGA Failure", "high ppCO2_HALO (HALO) (t-1)"),
    ("OGA Failure", "high ppO2_HALO (HALO)"), ("OGA Failure", "high ppO2_HALO (HALO) (t-1)"),
    ("OGA Failure", "low ppCO2_HALO (HALO)"), ("OGA Failure", "low ppCO2_HALO (HALO) (t-1)"),
    ("OGA Failure", "low ppO2_HALO (HALO)"), ("OGA Failure", "low ppO2_HALO (HALO) (t-1)"),
    # ("OGA Failure", "Hatch Status"),
    ("OGA Failure", "[HIDDEN] OGA Status Panel Indicator"),

    # VCCR Particulate Filter Saturation <-- IHab is point source for failure
    ("VCCR Particulate Filter Saturation", "high Humidity_IHab (IHab)"), ("VCCR Particulate Filter Saturation", "high Humidity_IHab (IHab) (t-1)"), 
    ("VCCR Particulate Filter Saturation", "high ppCO2_IHab (IHab)"), ("VCCR Particulate Filter Saturation", "high ppCO2_IHab (IHab) (t-1)"), 
    ("VCCR Particulate Filter Saturation", "high ppO2_IHab (IHab)"), ("VCCR Particulate Filter Saturation", "high ppO2_IHab (IHab) (t-1)"), 
    ("VCCR Particulate Filter Saturation", "low Humidity_IHab (IHab)"), ("VCCR Particulate Filter Saturation", "low Humidity_IHab (IHab) (t-1)"),
    ("VCCR Particulate Filter Saturation", "low ppCO2_IHab (IHab)"), ("VCCR Particulate Filter Saturation", "low ppCO2_IHab (IHab) (t-1)"),
    ("VCCR Particulate Filter Saturation", "low ppO2_IHab (IHab)"), ("VCCR Particulate Filter Saturation", "low ppO2_IHab (IHab) (t-1)"),
    ("VCCR Particulate Filter Saturation", "high Humidity_HALO (HALO)"), ("VCCR Particulate Filter Saturation", "high Humidity_HALO (HALO) (t-1)"),
    ("VCCR Particulate Filter Saturation", "high ppCO2_HALO (HALO)"), ("VCCR Particulate Filter Saturation", "high ppCO2_HALO (HALO) (t-1)"),
    ("VCCR Particulate Filter Saturation", "high ppO2_HALO (HALO)"), ("VCCR Particulate Filter Saturation", "high ppO2_HALO (HALO) (t-1)"),
    ("VCCR Particulate Filter Saturation", "low Humidity_HALO (HALO)"), ("VCCR Particulate Filter Saturation", "low Humidity_HALO (HALO) (t-1)"),
    ("VCCR Particulate Filter Saturation", "low ppCO2_HALO (HALO)"), ("VCCR Particulate Filter Saturation", "low ppCO2_HALO (HALO) (t-1)"),
    ("VCCR Particulate Filter Saturation", "low ppO2_HALO (HALO)"), ("VCCR Particulate Filter Saturation", "low ppO2_HALO (HALO) (t-1)"),
    # ("VCCR Particulate Filter Saturation", "Hatch Status"),
    ("VCCR Particulate Filter Saturation", "[HIDDEN] VCCR Particulate Filter"),

    # CDRA LiOH Canister Saturation <-- for parameter learning, proposing to remove the 'LiOH CO2 Saturation parameter,
    # as that could be the additional evidence

    # O2 Delivery System Malfunction (IHab)
    ("O2 Delivery System Malfunction (IHab)", "high ppO2_IHab (IHab)"), ("O2 Delivery System Malfunction (IHab)", "high ppO2_IHab (IHab) (t-1)"),
    ("O2 Delivery System Malfunction (IHab)", "low ppO2_IHab (IHab)"), ("O2 Delivery System Malfunction (IHab)", "low ppO2_IHab (IHab) (t-1)"),
    ("O2 Delivery System Malfunction (IHab)", "[HIDDEN] Cabin O2 Valve Position Indicator (IHab)"),

    # O2 Delivery System Malfunction (HALO)
    ("O2 Delivery System Malfunction (HALO)", "high ppO2_HALO (HALO)"), ("O2 Delivery System Malfunction (HALO)", "high ppO2_HALO (HALO) (t-1)"),
    ("O2 Delivery System Malfunction (HALO)", "low ppO2_HALO (HALO)"), ("O2 Delivery System Malfunction (HALO)", "low ppO2_HALO (HALO) (t-1)"),
    ("O2 Delivery System Malfunction (HALO)", "[HIDDEN] Cabin O2 Valve Position Indicator (HALO)"),

    # VCCR Sorbent Bed Saturation
    ("VCCR Sorbent Bed Saturation", "high ppCO2_IHab (IHab)"), ("VCCR Sorbent Bed Saturation", "high ppCO2_IHab (IHab) (t-1)"),
    ("VCCR Sorbent Bed Saturation", "low ppCO2_IHab (IHab)"), ("VCCR Sorbent Bed Saturation", "low ppCO2_IHab (IHab) (t-1)"),
    ("VCCR Sorbent Bed Saturation", "high ppCO2_HALO (HALO)"), ("VCCR Sorbent Bed Saturation", "high ppCO2_HALO (HALO) (t-1)"),
    ("VCCR Sorbent Bed Saturation", "low ppCO2_HALO (HALO)"), ("VCCR Sorbent Bed Saturation", "low ppCO2_HALO (HALO) (t-1)"),
    ("VCCR Sorbent Bed Saturation", "[HIDDEN] VCCR Sorbent Bed"),

    # # VCCR Failure (HALO) # NOTE: VERIFY THAT COMBINING INTO ONE ANOMALY WORKS WITH PL
    # ("VCCR Failure (HALO)", "high ppCO2_HALO (HALO)"), ("VCCR Failure (HALO)", "high ppCO2_HALO (HALO) (t-1)"),
    # ("VCCR Failure (HALO)", "low ppCO2_HALO (HALO)"), ("VCCR Failure (HALO)", "low ppCO2_HALO (HALO) (t-1)"),
    # ("VCCR Failure (HALO)", "[HIDDEN] VCCR Failure Component"),

    # Module Decompression (IHab)
    ("Module Decompression (IHab)", "high ppCO2_IHab (IHab)"), ("Module Decompression (IHab)", "high ppCO2_IHab (IHab) (t-1)"), 
    ("Module Decompression (IHab)", "high ppO2_IHab (IHab)"), ("Module Decompression (IHab)", "high ppO2_IHab (IHab) (t-1)"), 
    ("Module Decompression (IHab)", "high Total_Cabin_Pressure_IHab (IHab)"), ("Module Decompression (IHab)", "high Total_Cabin_Pressure_IHab (IHab) (t-1)"),
    ("Module Decompression (IHab)", "low ppCO2_IHab (IHab)"), ("Module Decompression (IHab)", "low ppCO2_IHab (IHab) (t-1)"),
    ("Module Decompression (IHab)", "low ppO2_IHab (IHab)"), ("Module Decompression (IHab)", "low ppO2_IHab (IHab) (t-1)"),
    ("Module Decompression (IHab)", "low Total_Cabin_Pressure_IHab (IHab)"), ("Module Decompression (IHab)", "low Total_Cabin_Pressure_IHab (IHab) (t-1)"),
    ("Module Decompression (IHab)", "[HIDDEN] Module Pressure Leak (IHab)"),

    # Module Decompression (HALO)
    ("Module Decompression (HALO)", "high ppCO2_HALO (HALO)"), ("Module Decompression (HALO)", "high ppCO2_HALO (HALO) (t-1)"),
    ("Module Decompression (HALO)", "high ppO2_HALO (HALO)"), ("Module Decompression (HALO)", "high ppO2_HALO (HALO) (t-1)"),
    ("Module Decompression (HALO)", "high Total_Cabin_Pressure_HALO (HALO)"), ("Module Decompression (HALO)", "high Total_Cabin_Pressure_HALO (HALO) (t-1)"),
    ("Module Decompression (HALO)", "low ppCO2_HALO (HALO)"), ("Module Decompression (HALO)", "low ppCO2_HALO (HALO) (t-1)"),
    ("Module Decompression (HALO)", "low ppO2_HALO (HALO)"), ("Module Decompression (HALO)", "low ppO2_HALO (HALO) (t-1)"),
    ("Module Decompression (HALO)", "low Total_Cabin_Pressure_HALO (HALO)"), ("Module Decompression (HALO)", "low Total_Cabin_Pressure_HALO (HALO) (t-1)"),
    ("Module Decompression (HALO)", "[HIDDEN] Module Pressure Leak (HALO)"),

    # Add 'Fan Status' as a part of parameters measured seperately in different modules
    ("Fan Status", "high Humidity_IHab (IHab)"), ("Fan Status", "high Humidity_IHab (IHab) (t-1)"), 
    ("Fan Status", "high ppCO2_IHab (IHab)"), ("Fan Status", "high ppCO2_IHab (IHab) (t-1)"),
    ("Fan Status", "high ppO2_IHab (IHab)"), ("Fan Status", "high ppO2_IHab (IHab) (t-1)"),
    ("Fan Status", "high Total_Cabin_Pressure_IHab (IHab)"), ("Fan Status", "high Total_Cabin_Pressure_IHab (IHab) (t-1)"), 
    ("Fan Status", "low Humidity_IHab (IHab)"), ("Fan Status", "low Humidity_IHab (IHab) (t-1)"), 
    ("Fan Status", "low ppCO2_IHab (IHab)"), ("Fan Status", "low ppCO2_IHab (IHab) (t-1)"),
    ("Fan Status", "low ppO2_IHab (IHab)"), ("Fan Status", "low ppO2_IHab (IHab) (t-1)"),
    ("Fan Status", "low Total_Cabin_Pressure_IHab (IHab)"), ("Fan Status", "low Total_Cabin_Pressure_IHab (IHab) (t-1)"), 
    ("Fan Status", "high Humidity_HALO (HALO)"), ("Fan Status", "high Humidity_HALO (HALO) (t-1)"),
    ("Fan Status", "high ppCO2_HALO (HALO)"), ("Fan Status", "high ppCO2_HALO (HALO) (t-1)"),
    ("Fan Status", "high ppO2_HALO (HALO)"), ("Fan Status", "high ppO2_HALO (HALO) (t-1)"),
    ("Fan Status", "high Total_Cabin_Pressure_HALO (HALO)"), ("Fan Status", "high Total_Cabin_Pressure_HALO (HALO) (t-1)"), 
    ("Fan Status", "low Humidity_HALO (HALO)"), ("Fan Status", "low Humidity_HALO (HALO) (t-1)"),
    ("Fan Status", "low ppCO2_HALO (HALO)"), ("Fan Status", "low ppCO2_HALO (HALO) (t-1)"),
    ("Fan Status", "low ppO2_HALO (HALO)"), ("Fan Status", "low ppO2_HALO (HALO) (t-1)"),
    ("Fan Status", "low Total_Cabin_Pressure_HALO (HALO)"), ("Fan Status", "low Total_Cabin_Pressure_HALO (HALO) (t-1)")
]

network_dict = defaultdict(set)
for anomaly, parameter in reduced_network:
    network_dict[anomaly].add(parameter)

# Create new edges for all (t-1) parameters to their respective parent anomalies
new_edges = [] # create an empty list to store new edges
for anomaly, parameters in network_dict.items():
    for parameter in parameters:
        # Only add new edges for telemetry parameters (i.e., not for additional evidence)
        if parameter.startswith("[HIDDEN]") or "(t-1)" in parameter or parameter == "Fan Status":
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
    ("high Total_Cabin_Pressure_HALO (HALO) (t-1)", "high Total_Cabin_Pressure_HALO (HALO)"), ("low Total_Cabin_Pressure_HALO (HALO) (t-1)", "low Total_Cabin_Pressure_HALO (HALO)")
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
    ("high Humidity_IHab (IHab) (t-1)", "high Humidity_HALO (HALO) (t-1)"), ("low Humidity_IHab (IHab) (t-1)", "low Humidity_HALO (HALO) (t-1)"),
    ("high ppCO2_IHab (IHab)", "high ppCO2_HALO (HALO)"), ("low ppCO2_IHab (IHab)", "low ppCO2_HALO (HALO)"),
    ("high ppCO2_IHab (IHab) (t-1)", "high ppCO2_HALO (HALO) (t-1)"), ("low ppCO2_IHab (IHab) (t-1)", "low ppCO2_HALO (HALO) (t-1)"),
    ("high ppO2_IHab (IHab)", "high ppO2_HALO (HALO)"), ("low ppO2_IHab (IHab)", "low ppO2_HALO (HALO)"),
    ("high ppO2_IHab (IHab) (t-1)", "high ppO2_HALO (HALO) (t-1)"), ("low ppO2_IHab (IHab) (t-1)", "low ppO2_HALO (HALO) (t-1)"),
    ("high Total_Cabin_Pressure_IHab (IHab)", "high Total_Cabin_Pressure_HALO (HALO)"), ("low Total_Cabin_Pressure_IHab (IHab)", "low Total_Cabin_Pressure_HALO (HALO)"),
    ("high Total_Cabin_Pressure_IHab (IHab) (t-1)", "high Total_Cabin_Pressure_HALO (HALO) (t-1)"), ("low Total_Cabin_Pressure_IHab (IHab) (t-1)", "low Total_Cabin_Pressure_HALO (HALO) (t-1)")
]

for edge in spatial_nodes:
    reduced_network.append(edge)

# Add subsystem nodes linking different anomalies under the same ECLSS subsystem
subsystem_nodes = [

    # Atmosphere Revitalization
    ("VCCR Particulate Filter Saturation", "Atmosphere Revitalization"),
    ("O2 Delivery System Malfunction (IHab)", "Atmosphere Revitalization"),
    ("O2 Delivery System Malfunction (HALO)", "Atmosphere Revitalization"),
    ("VCCR Sorbent Bed Saturation", "Atmosphere Revitalization"),
    ("OGA Failure", "Atmosphere Revitalization"),

    # Atmosphere Control and Supply
    ("Module Decompression (IHab)", "Atmosphere Control and Supply"),
    ("Module Decompression (HALO)", "Atmosphere Control and Supply")
]

for subsystem in subsystem_nodes:
    reduced_network.append(subsystem)

# NOTE: Updated on 03/05/2026 to replace "No Anomalies Present" with "Unknown Anomaly"
# Add nodes for subgroups related to Unknown Anomaly node
# Flipped such that the Unknown Anomaly node is a child of the groups, as its state is deterministic based on the status of the subgroups
# Updated on 07/09/2026 to change group names to be more representative of spacecraft ECLSS subsystems
unknown_anomaly_nodes = [
    ("Atmosphere Revitalization", "Unknown Anomaly"),
    ("Atmosphere Control and Supply", "Unknown Anomaly")
]

for ua in unknown_anomaly_nodes:
    reduced_network.append(ua)

# NOTE: NEW CODE ON 09/16/2026
# Add edges from subsystems to fault isolation hidden nodes
fault_isolation_nodes = [
    ("Atmosphere Revitalization", "[HIDDEN] Atmosphere Revitalization Fault Isolation"),
    ("Atmosphere Control and Supply", "[HIDDEN] Atmosphere Control and Supply Fault Isolation")
]

for fi in fault_isolation_nodes:
    reduced_network.append(fi)