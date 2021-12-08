# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 12:35:04 2020

@author: gibelhaus
"""
from re import A
import numpy as np
import matplotlib.pyplot as plt
import pickle
import SteadyStateAKM
import log_output as lgo
from param_database import params
import time
time_sta = time.time()

#%% Read results from dynamic simulation
t_cycle_dyn_852718, Qflow_chill_dyn_852718, COP_dyn_852718 = lgo.read_pickle('./PerformanceMap/SCP_COP/results_dyn_852718.pickle')
t_cycle_dyn_903010, Qflow_chill_dyn_903010, COP_dyn_903010 = lgo.read_pickle('./PerformanceMap/SCP_COP/results_dyn_903010.pickle')

param = params()
AKM_852718 = SteadyStateAKM.adsorptionChiller_steadyState(**param.p852718)
AKM_903010 = SteadyStateAKM.adsorptionChiller_steadyState(**param.p903010)

def param_set(AKM_i,params):
    AKM_i.alphaA_evp_o  = params[0]
    AKM_i.alphaA_evp_i  = params[0]
    AKM_i.alphaA_cond_o = params[1]
    AKM_i.alphaA_cond_i = params[1]
    AKM_i.alphaA_ads_o  = params[2]
    AKM_i.alphaA_ads_i  = params[2] * 10
    AKM_i.D_eff = params[3]
    AKM_i.corr_sor = params[4]
    AKM_i.corr_HX  = params[5]
    return 0

def calc_map(AKM_i):
    var_guess = np.array([291.15,300.15,300.15,358.15,0.2,0.05])
    t_cycle_dyn_903010, Qflow_chill_dyn_903010, COP_dyn_903010 = lgo.read_pickle('./PerformanceMap/SCP_COP/results_dyn_903010.pickle')
    t_cycle_array=np.array(t_cycle_dyn_903010); Q_flow_chill = np.empty(t_cycle_dyn_903010.size); COP = np.empty(t_cycle_dyn_903010.size)
    #fitted_params = [1.26281335e+02, 3.07708529e+03, 3.62063043e+02, 6.14056817e-10, 7.29550500e-01, 1.03393888e+00]
    #param_set(AKM_i,fitted_params)
    for num, t_cycle in enumerate(t_cycle_array):
        AKM_i.t_cycle = t_cycle
        AKM_i.solve(var_guess)
        Q_flow_chill[num] = AKM_i.Q_flow_evp * 2
        COP[num] = AKM_i.COP
        #lgo.log_output_excel(AKM_i)
    return COP, Q_flow_chill

#COP_stat_852718, Qflow_chill_stat_852718 = calc_map(AKM_852718)
#COP_stat_903010, Qflow_chill_stat_903010 = calc_map(AKM_903010)

time_end = time.time()
print("calculation time ::  ",time_end - time_sta," sec")

"""
error = lgo.ARE(COP_dyn_852718,Qflow_chill_dyn_852718,COP_stat_852718,Qflow_chill_stat_852718,COP_dyn_903010,Qflow_chill_dyn_903010,COP_stat_903010,Qflow_chill_stat_903010)
print(error)
plt.plot(COP_dyn_903010,Qflow_chill_dyn_903010,'ro')
plt.plot(COP_dyn_852718,Qflow_chill_dyn_852718,'bo')
plt.plot(COP_stat_903010, Qflow_chill_stat_903010,'r-')
plt.plot(COP_stat_852718, Qflow_chill_stat_852718,'b-')
plt.show()
"""
"""
results_stat={'t_cycle': t_cycle_array, 'Q_flow_chill': Q_flow_chill, 'COP': COP}
with open('results_stat.pickle', 'wb') as f:
        # Pickle the 'results' list using the highest protocol available.
        pickle.dump(results/results_stat, f, pickle.HIGHEST_PROTOCOL)
"""
