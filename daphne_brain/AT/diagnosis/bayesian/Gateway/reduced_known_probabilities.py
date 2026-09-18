# reduced_known_probabilities.py
# Author: Joshua Elston
# Last Edited: 08/31/2026

# Script stores known deterministic CPDs for group-level and
# unknown anomaly nodes in the Biosim ECLSS Bayesian Network.
# These are then stored to the overall network and combined
# with the learned parameter-level CPDs in
# learn_probabilities_threaded.py.
# Updated on 04/30/2026 to include known CPD for No Anomalies Present (trying
# to see if inclusion impacts use of nominal data)
# Updated on 05/03/2026 to include anomaly priors as known probabilities
# Updated on 07/09/2026 to reflect more realistic group (subsystem) names
# Updated on 08/31/2026 to reflect more specific anomaly names

import numpy as np
from pgmpy.factors.discrete import TabularCPD

known_cpds = []

anomaly_priors_dict = {
    'OGA Failure': 10**-4,
    'VCCR Particulate Filter Saturation': 10**-4,
    'O2 Delivery System Malfunction (IHab)': 10**-4,
    'O2 Delivery System Malfunction (HALO)': 10**-4,
    "VCCR Sorbent Bed Saturation": 10**-4,
    'Module Decompression (IHab)': 10**-5,
    'Module Decompression (HALO)': 10**-5
}

for anomaly, prior in anomaly_priors_dict.items():
    anomaly_cpd = TabularCPD(variable=anomaly,
                             variable_card=2,
                             values=[[1 - prior], [prior]])
    known_cpds.append(anomaly_cpd)

# NOTE: Updated on 08/26/26 to experiment with removing know priors
# for subsystem nodes given that they not only depend on anomalies
# but also the associated parameters with those anomalies
# (from earlier summer updates w/ Dani)
ar_true = np.ones(2**5, dtype='float')
ar_true[0] = 0
ar_false = 1 - ar_true
atmos_rev = TabularCPD(variable='Atmosphere Revitalization',
                    variable_card=2,
                    values=np.array([ar_false, ar_true]),
                    evidence=['OGA Failure',
                              'VCCR Particulate Filter Saturation',
                              'O2 Delivery System Malfunction (IHab)',
                              'O2 Delivery System Malfunction (HALO)',
                              'VCCR Sorbent Bed Saturation'],
                    evidence_card=[2,2,2,2,2])
known_cpds.append(atmos_rev)

atmos_control_and_supply = TabularCPD(variable='Atmosphere Control and Supply',
                    variable_card=2,
                    values = [[1, 0, 0, 0], [0, 1, 1, 1]],
                    evidence=['Module Decompression (IHab)', 'Module Decompression (HALO)'],
                    evidence_card=[2,2])
known_cpds.append(atmos_control_and_supply)

ua_false = np.ones(2**2, dtype='float')
ua_false[0] = 0
ua_true = 1 - ua_false
unknown_anomaly = TabularCPD(variable='Unknown Anomaly',
                             variable_card=2,
                             values=np.array([ua_false, ua_true]),
                             evidence=['Atmosphere Revitalization', 'Atmosphere Control and Supply'],
                             evidence_card=[2,2])
known_cpds.append(unknown_anomaly)

# print(known_cpds)