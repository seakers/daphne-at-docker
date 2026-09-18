# dictionaries.py
# Author: Joshua Elston
# Last Updated: 11/05/2025

# Stores dictionaries with relationships between subgroups and their related anomalies. Additionally stores No Anomalies Present and its relationship to the different subgroups.
# Called in add_cpds to compute the CPDs to be added to the Bayesian network.
# Changes on 10/17/2025 to include combined failures across multiple levels
# Changes on 11/05/2025 to reflect naming convention for Gateway (L1 -- > IHab, L2 --> HALO)

combined_failure_dict = {
    "Biological Filter Saturation": [
        "Biological Filter Saturation (IHab)",
        "Biological Filter Saturation (HALO)"
    ],
    "CDRA Failure": [
        "CDRA Failure (IHab)",
        "CDRA Failure (HALO)"
    ],
    "CDRA LiOH Canister Saturation": [
        "CDRA LiOH Canister Saturation (IHab)",
        "CDRA LiOH Canister Saturation (HALO)"
    ],
    "Electrolysis System Failure": [
        "Electrolysis System Failure (IHab)",
        "Electrolysis System Failure (HALO)"
    ],
    "Emergency O2 System Maintenance": [
        "Emergency O2 System Maintenance (IHab)",
        "Emergency O2 System Maintenance (HALO)"
    ],
    "Excess CO2 in Cabin": [
        "Excess CO2 in Cabin (IHab)",
        "Excess CO2 in Cabin (HALO)"
    ],
    "Excess Gas Leak": [
        "Excess Gas Leak (IHab)",
        "Excess Gas Leak (HALO)"
    ],
    "Excess Water Vapor Pressure in Cabin": [
        "Excess Water Vapor Pressure in Cabin (IHab)",
        "Excess Water Vapor Pressure in Cabin (HALO)"
    ],
    "Loss of Pressure": [
        "Loss of Pressure (IHab)",
        "Loss of Pressure (HALO)"
    ],
    "Main Cabin Fan Failure": [
        "Main Cabin Fan Failure (IHab)",
        "Main Cabin Fan Failure (HALO)"
    ],
    "N2 Tank Burst": [
        "N2 Tank Burst (IHab)",
        "N2 Tank Burst (HALO)"
    ],
    "PDU 4 Failure": [
        "PDU 4 Failure (IHab)",
        "PDU 4 Failure (HALO)"
    ],
    "PDU 5 Failure": [
        "PDU 5 Failure (IHab)",
        "PDU 5 Failure (HALO)"
    ],
    "RWGSR Malfunction": [
        "RWGSR Malfunction (IHab)",
        "RWGSR Malfunction (HALO)"
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