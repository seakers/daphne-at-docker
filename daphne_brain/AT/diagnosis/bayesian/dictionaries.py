# dictionaries.py
# Author: Joshua Elston
# Last Updated: 03/27/2025

# Stores dictionaries with relationships between subgorups and their related anomalies. Additionally stores No Anomalies Present and its relationship to the different subgroups.
# Called in add_cpds to compute the CPDs to be added to the Bayesian network.

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