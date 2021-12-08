# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 14:55:16 2020

@author: gibelhaus
"""
if __name__=='__main__':

    import pickle
    import autosim
    import numpy as np

    import matplotlib.pyplot as plt

    fmu='AdsorptionChillerLTT_0Ref.fmu'

    sim=autosim.sim.SimulationTask()

    sim.loadFMU(fmu, True)

    t_Cycle = 1000

    sim.setTimeHorizon(startTime=0,
                       stopTime=6*t_Cycle,
                       relativeTolerance=0.000001)

    p={'T_chill': [273.15 + 10],
       'T_heat': [273.15 + 90],
       'T_cool': [273.15 + 30],
       't_Cycle': [200 + i*50 for i in range(0,501)]
       }

    sim.setParameters(p, {'par': 't_Cycle', 'factor': 6})

    output=['Q_flow_cool_avg',
            'COP',
            'summary.H_flow_evaporator'
            ]

    sim.selectOutputVariables(output)

    results=sim.solve(processNumber=3, timeoutSim=120)

    Q_flow_chill = np.array([results[i]['Q_flow_cool_avg'][-1] for i in range(0,len(results))])

    COP = np.array([results[i]['COP'][-1] for i in range(0,len(results))])

    plt.plot(COP,Q_flow_chill)

    with open('results_903010.pickle', 'wb') as f:
        # Pickle the 'results' list using the highest protocol available.
        pickle.dump(results, f, pickle.HIGHEST_PROTOCOL)

    # with open('results.pickle', 'rb') as f:
    #     # Read the pickled data
    #     results = pickle.load(f)
