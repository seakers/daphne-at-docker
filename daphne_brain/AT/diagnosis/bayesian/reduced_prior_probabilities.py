# reduced_prior_probabilities.py
# Author: Joshua Elston
# Last Edited: 02/09/2026

# Condensed set of prior probabilities corresponding to the anomalies modeled in Biosim
# to use during parameter learning

# Prior probabilities of anomalies:
reduced_prior_probabilities = {
    "Biological Filter Saturation (IHab)": 10**-4,
    "Biological Filter Saturation (HALO)": 10**-4,
    "CDRA Failure (IHab)": 10**-4,
    "CDRA Failure (HALO)": 10**-4,
    "Emergency O2 System Maintenance (IHab)": 10**-4,
    "Emergency O2 System Maintenance (HALO)": 10**-4,
    "Excess CO2 in Cabin (IHab)": 10**-4,
    "Excess CO2 in Cabin (HALO)": 10**-4,
    "Loss of Pressure (IHab)": 10**-5,
    "Loss of Pressure (HALO)": 10**-5
}