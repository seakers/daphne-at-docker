# reduced_dictionaries.py
# Author: Joshua Elston
# Last Updated: 03/06/2026

# Condensed dictionaries for relationships between:
# - Combined failures
# - Subgroups and related anomalies
# - No Anomalies Present and subgroups

# Called in reduced_add_cpds.py <-- NOTE: currently NOT called, but
# need to update if this is to be used in the future

# UPDATES:
# Updated on 03/03/2026 to experiment with defining all anomalies within 
# subgroups to see impacts on run time
# Updated on 03/04/2026 to add "Unknown Anomaly" as a parent of "No Anomalies Present"
# Updated on 03/06/2026 to replace "No Anomalies Present" node with "Unknown Anomaly"

combined_failure_dict = {
    # "Biological Filter Saturation": [
    #     "Biological Filter Saturation (IHab)",
    #     "Biological Filter Saturation (HALO)"
    # ],
    # "CDRA Failure": [
    #     "CDRA Failure (IHab)",
    #     "CDRA Failure (HALO)"
    # ],
    "Emergency O2 System Maintenance": [
        "Emergency O2 System Maintenance (IHab)",
        "Emergency O2 System Maintenance (HALO)"
    ],
    "Excess CO2 in Cabin": [
        "Excess CO2 in Cabin (IHab)",
        "Excess CO2 in Cabin (HALO)"
    ],
    "Loss of Pressure": [
        "Loss of Pressure (IHab)",
        "Loss of Pressure (HALO)"
    ]
}

subgroup_dict = {
    "Group 1": [
        "CDRA Failure (IHab)",
        "CDRA Failure (Habitat)",
        "Emergency O2 System Maintenance (IHab)",
        "Emergency O2 System Maintenance (HALO)",
        "Excess CO2 in Cabin (IHab)",
        "Excess CO2 in Cabin (HALO)"
        ],
    #  "Group 2": [
        # ],
    "Group 3": [
        "Biological Filter Saturation (IHab)",
        "Biological Filter Saturation (Habitat)"
        ],
#  "Group 4": [
    # ],
#  "Group 5": [
    # ],
#  "Group 6": [
    # ],
    "Group 7": [
        "Loss of Pressure (IHab)",
        "Loss of Pressure (HALO)"
    ]
}

# NOTE: Updated on 03/06/2026 to replace "No Anomalies Present" with "Unknown Anomaly"
unknown_anomaly_dict = {
    "Unknown Anomaly": [
        "Group 1",
    #   "Group 2",
        "Group 3",
    #   "Group 4",
    #   "Group 5",
    #   "Group 6",
        "Group 7" #,
        # "Unknown Anomaly"
    ]
}