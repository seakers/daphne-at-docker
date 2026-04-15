# reduced_known_probabilities.py
# Author: Joshua Elston
# Last Edited: 04/13/2026

# Script stores known deterministic CPDs for group-level and
# unknown anomaly nodes in the Biosim ECLSS Bayesian Network.
# These are then stored to the overall network and combined
# with the learned parameter-level CPDs in
# learn_probabilities_threaded.py.

import numpy as np
from pgmpy.factors.discrete import TabularCPD

g1_true = np.ones(2**5, dtype='float')
g1_true[0] = 0
g1_false = 1 - g1_true
group1 = TabularCPD(variable='Group 1',
                    variable_card=2,
                    values=np.array([g1_false, g1_true]),
                    evidence=['CDRA Failure',
                    'Emergency O2 System Maintenance (IHab)',
                    'Emergency O2 System Maintenance (HALO)',
                    'Excess CO2 in Cabin (IHab)',
                    'Excess CO2 in Cabin (HALO)'],
                    evidence_card=[2,2,2,2,2])

group3 = TabularCPD(variable='Group 3',
                    variable_card=2,
                    values=[[1, 0], [0, 1]],
                    evidence=['Biological Filter Saturation'],
                    evidence_card=[2])

group7 = TabularCPD(variable='Group 7',
                    variable_card=2,
                    values = [[1, 0, 0, 0], [0, 1, 1, 1]],
                    evidence=['Loss of Pressure (IHab)', 'Loss of Pressure (HALO)'],
                    evidence_card=[2,2])

ua_false = np.ones(2**3, dtype='float')
ua_false[0] = 0
ua_true = 1 - ua_false
unknown_anomaly = TabularCPD(variable='Unknown Anomaly',
                             variable_card=2,
                             values=np.array([ua_false, ua_true]),
                             evidence=['Group 1', 'Group 3', 'Group 7'],
                             evidence_card=[2,2,2])

known_cpds = [group1, group3, group7, unknown_anomaly]