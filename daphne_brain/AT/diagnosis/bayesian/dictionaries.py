# dictionaries.py
# Author: Joshua Elston
# Last Updated: 10/17/2025

# Stores dictionaries with relationships between subgroups and their related anomalies. Additionally stores No Anomalies Present and its relationship to the different subgroups.
# Called in add_cpds to compute the CPDs to be added to the Bayesian network.
# Changes on 10/17/2025 to include combined failures across multiple levels

combined_failure_dict = {
    "Biological Filter Saturation": [
        "Biological Filter Saturation (L1)",
        "Biological Filter Saturation (L2)"
    ],
    "CDRA Failure": [
        "CDRA Failure (L1)",
        "CDRA Failure (L2)"
    ],
    "CDRA LiOH Canister Saturation": [
        "CDRA LiOH Canister Saturation (L1)",
        "CDRA LiOH Canister Saturation (L2)"
    ],
    "Electrolysis System Failure": [
        "Electrolysis System Failure (L1)",
        "Electrolysis System Failure (L2)"
    ],
    "Emergency O2 System Maintenance": [
        "Emergency O2 System Maintenance (L1)",
        "Emergency O2 System Maintenance (L2)"
    ],
    "Excess CO2 in Cabin": [
        "Excess CO2 in Cabin (L1)",
        "Excess CO2 in Cabin (L2)"
    ],
    "Excess Gas Leak": [
        "Excess Gas Leak (L1)",
        "Excess Gas Leak (L2)"
    ],
    "Excess Water Vapor Pressure in Cabin": [
        "Excess Water Vapor Pressure in Cabin (L1)",
        "Excess Water Vapor Pressure in Cabin (L2)"
    ],
    "Loss of Pressure": [
        "Loss of Pressure (L1)",
        "Loss of Pressure (L2)"
    ],
    "Main Cabin Fan Failure": [
        "Main Cabin Fan Failure (L1)",
        "Main Cabin Fan Failure (L2)"
    ],
    "N2 Tank Burst": [
        "N2 Tank Burst (L1)",
        "N2 Tank Burst (L2)"
    ],
    "PDU 4 Failure": [
        "PDU 4 Failure (L1)",
        "PDU 4 Failure (L2)"
    ],
    "PDU 5 Failure": [
        "PDU 5 Failure (L1)",
        "PDU 5 Failure (L2)"
    ],
    "RWGSR Malfunction": [
        "RWGSR Malfunction (L1)",
        "RWGSR Malfunction (L2)"
    ]
}

subgroup_dict = {
     "Group 1": [
         "CDRA Failure",
         "CDRA LiOH Canister Saturation",
         "Emergency O2 System Maintenance",
         "Excess CO2 in Cabin",
         "Excess Water Vapor Pressure in Cabin",
         "RWGSR Malfunction"
     ],
     "Group 2": [
          "Excess Gas Leak",
          "TCCS Auxiliary Fan #1 Failure",
          "TCCS Auxiliary Fan #2 Failure",
          "TCCS Auxiliary Fan at Reduced Capacity",
          "TCCS Filter Clog",
          "Trace Contaminants"
     ],
     "Group 3": [
          "Biological Filter Saturation",
          "Electrolysis System Failure",
          "SPE System Maintenance",
          "WRS Failure",
          "WRS Maintenance",
          "WRS Off-nominal pH Level"
     ],
     "Group 4": [
          "Fuel Cell #1 and PDU Failure",
          "Fuel Cell #2 and PDU Failure",
          "Fuel Cell Degrade",
          "Fuel Cell Failure",
          "PDU 4 Failure",
          "PDU 5 Failure"
     ],
     "Group 5": [
          "MOXIE Antenna Failure",
          "MOXIE ECM Failure",
          "MOXIE Fan Failure"
     ],
     "Group 6": [
          "Main Cabin Fan Failure",
          "Reduced Main Cabin Fan #1 Capacity"
     ],
     "Group 7": [
          "Loss of Pressure",
          "N2 Tank Burst"
     ]
}

nap_dict = {
     "No Anomalies Present": [
          "Group 1",
          "Group 2",
          "Group 3",
          "Group 4",
          "Group 5",
          "Group 6",
          "Group 7"
     ]
}