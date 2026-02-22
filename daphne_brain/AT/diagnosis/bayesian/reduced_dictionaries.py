# reduced_dictionaries.py
# Author: Joshua Elston
# Last Updated: 02/09/2026

# Condensed dictionaries for relationships between:
# - Combined failures
# - Subgroups and related anomalies
# - No Anomalies Present and subgroups

# Called in reduced_add_cpds.py

combined_failure_dict = {
    "Biological Filter Saturation": [
        "Biological Filter Saturation (IHab)",
        "Biological Filter Saturation (HALO)"
    ],
    "CDRA Failure": [
        "CDRA Failure (IHab)",
        "CDRA Failure (HALO)"
    ],
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
        "CDRA Failure",
        "Emergency O2 System Maintenance",
        "Excess CO2 in Cabin",
        ],
    #  "Group 2": [
        # ],
    "Group 3": [
        "Biological Filter Saturation",
        ],
#  "Group 4": [
    # ],
#  "Group 5": [
    # ],
#  "Group 6": [
    # ],
    "Group 7": [
        "Loss of Pressure"
    ]
}

nap_dict = {
    "No Anomalies Present": [
        "Group 1",
    #   "Group 2",
        "Group 3",
    #   "Group 4",
    #   "Group 5",
    #   "Group 6",
        "Group 7"
    ]
}