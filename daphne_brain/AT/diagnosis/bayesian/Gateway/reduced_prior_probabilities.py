# reduced_prior_probabilities.py
# Author: Joshua Elston
# Last Edited: 03/06/2026

# Condensed set of prior probabilities corresponding to the anomalies modeled in Biosim
# to use during parameter learning

# UPDATES:
# Updated on 03/03/2026 to reflect that habitat-wide failures (where present) are slightly
# less likely than location-specific failures
# Updated on 03/04/2026 to add a prior probability for an unknown anomaly to occur
# Updated on 03/06/2026 to remove the "Unknown Anomaly" prior, as it replaces "No Anomalies Present"

# Prior probabilities of anomalies:
reduced_prior_probabilities = {
    "Biological Filter Saturation (IHab)": 10**-4,
    "Biological Filter Saturation (Habitat)": 10**-5,
    "CDRA Failure (IHab)": 10**-4,
    "CDRA Failure (Habitat)": 10**-5,
    "Emergency O2 System Maintenance (IHab)": 10**-4,
    "Emergency O2 System Maintenance (HALO)": 10**-4,
    "Excess CO2 in Cabin (IHab)": 10**-4,
    "Excess CO2 in Cabin (HALO)": 10**-4,
    "Loss of Pressure (IHab)": 10**-5,
    "Loss of Pressure (HALO)": 10**-5,
    # "Unknown Anomaly": 10**-4
}