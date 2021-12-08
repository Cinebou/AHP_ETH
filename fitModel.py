# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 13:58:30 2020

@author: gibelhaus
"""

#%%
import numpy as np
import pickle
from scipy.optimize import least_squares, basinhopping
import matplotlib.pyplot as plt
import time
import SteadyStateAKM
import log_output as lgo

time_sta = time.time()

#%% Read results from dynamic simulation
t_cycle_dyn_852718, Qflow_chill_dyn_852718, COP_dyn_852718 = lgo.read_pickle('./PerformanceMap/SCP_COP/results_dyn_852718.pickle')
t_cycle_dyn_903010, Qflow_chill_dyn_903010, COP_dyn_903010 = lgo.read_pickle('./PerformanceMap/SCP_COP/results_dyn_903010.pickle')
Qflow_heat_dyn_852718 = Qflow_chill_dyn_852718/COP_dyn_852718
Qflow_heat_dyn_903010 = Qflow_chill_dyn_903010/COP_dyn_903010

#%% Fit steady-state model
def performance(corr,t_cycle_852718,t_cycle_903010, logout = False):
    param_852718 = [{'m_flow_evp':0.191,
              'm_flow_cond':0.111,
              'm_flow_ads':0.166,
              'm_flow_des':0.163,
              'alphaA_evp_o':corr[0],
              'alphaA_cond_o':3174,
              'alphaA_ads_o':corr[1],
              'alphaA_evp_i':corr[0],
              'alphaA_cond_i':1575,
              'alphaA_ads_i':corr[1] * 10,
              'D_eff':corr[2],
              'm_sor':2.236,
              'r_particle':0.00045,
              'm_HX':4.211,
              'm_fl':0.94,
              'T_evp_in':291.15,
              'T_cond_in':300.15,
              'T_ads_in':300.15,
              'T_des_in':358.15,
              't_cycle':t_cycle_i,
              'corr_sor_c': corr[3],
              'corr_sor_t':0,
              'corr_HX_c': corr[4],
              'corr_HX_t':0,
              'corr_fl': 0} for t_cycle_i in t_cycle_852718]
    
    
    AKM_852718 = [SteadyStateAKM.adsorptionChiller_steadyState(**param_i) for param_i in param_852718]

    var_guess = np.array([291.15,300.15,300.15,358.15,0.2,0.05])
    
    [AKM_i.solve(var_guess) for AKM_i in AKM_852718]
    
    Qflow_chill_852718 = np.array([AKM_i.Q_flow_evp for AKM_i in AKM_852718])
    
    Qflow_heat_852718 = np.array([AKM_i.Q_flow_des for AKM_i in AKM_852718])
    
    param_903010 = [{'m_flow_evp':0.191,
              'm_flow_cond':0.111,
              'm_flow_ads':0.166,
              'm_flow_des':0.163,
              'alphaA_evp_o':corr[0],
              'alphaA_cond_o':3174,
              'alphaA_ads_o':corr[1],
              'alphaA_evp_i':corr[0],
              'alphaA_cond_i':1575,
              'alphaA_ads_i':corr[1] * 10,
              'D_eff':corr[2],
              'm_sor':2.236,
              'r_particle':0.00045,
              'm_HX':4.211,
              'm_fl':0.94,
              'T_evp_in':283.15,
              'T_cond_in':303.15,
              'T_ads_in':303.15,
              'T_des_in':363.15,
              't_cycle':t_cycle_i,
              'corr_sor_c': corr[3],
              'corr_sor_t':0,
              'corr_HX_c': corr[4],
              'corr_HX_t':0,
              'corr_fl': 0} for t_cycle_i in t_cycle_903010]
    
    AKM_903010 = [SteadyStateAKM.adsorptionChiller_steadyState(**param_i) for param_i in param_903010]
    
    [AKM_i.solve(var_guess) for AKM_i in AKM_903010]
    
    Qflow_chill_903010 = np.array([AKM_i.Q_flow_evp for AKM_i in AKM_903010])
    
    Qflow_heat_903010 = np.array([AKM_i.Q_flow_des for AKM_i in AKM_903010])

    # the short-cut model has only one tank in the system, while dynamic model moght have two tanks
    Qflow_chill_852718 = 2*Qflow_chill_852718; Qflow_heat_852718 = 2*Qflow_heat_852718; Qflow_chill_903010 = 2*Qflow_chill_903010; Qflow_heat_903010 = 2*Qflow_heat_903010
    
    if logout:
        for AKM_i in AKM_903010:
            lgo.log_output_eq(AKM_i)
            lgo.log_output_excel(AKM_i)
        for AKM_j in AKM_852718:
            lgo.log_output_eq(AKM_j)
            lgo.log_output_excel(AKM_j)

    return Qflow_chill_852718, Qflow_heat_852718, Qflow_chill_903010, Qflow_heat_903010

def lsq_perf(corr,t_cycle_852718,t_cycle_903010,Qflow_chill_target_852718,Qflow_heat_target_852718,Qflow_chill_target_903010,Qflow_heat_target_903010):
    Qflow_chill_852718, Qflow_heat_852718, Qflow_chill_903010, Qflow_heat_903010 = performance(corr,t_cycle_852718,t_cycle_903010)
    lsq_Qflows = np.concatenate((Qflow_chill_852718-Qflow_chill_target_852718,Qflow_heat_852718-Qflow_heat_target_852718, Qflow_chill_903010-Qflow_chill_target_903010,Qflow_heat_903010-Qflow_heat_target_903010))
    return lsq_Qflows

corr0 = np.array([1.12059660e+02,4.96532664e+02, 2.99607499e-10, 0.6, 1])

#diff_step = ([1.5,1.5, 4, 1, 0.5, 1, 0.5])
bounds = ([50,50,1e-11,0,0],[10000,10000,1e-9,5,5])
args = (t_cycle_dyn_852718,t_cycle_dyn_903010,Qflow_chill_dyn_852718,Qflow_heat_dyn_852718, Qflow_chill_dyn_903010,Qflow_heat_dyn_903010)
res_perf = least_squares(lsq_perf, corr0, bounds=bounds, args=args,  verbose=1)



time_end = time.time()
print("calculation time ::  ",time_end - time_sta," sec")
print(res_perf.x)

#%% Plot results

plt.figure()

Qflow_chill_stat_852718, Qflow_heat_stat_852718, Qflow_chill_stat_903010, Qflow_heat_stat_903010, = performance(res_perf.x,t_cycle_dyn_852718,t_cycle_dyn_903010, logout = True)

COP_stat_852718=Qflow_chill_stat_852718/Qflow_heat_stat_852718

COP_stat_903010=Qflow_chill_stat_903010/Qflow_heat_stat_903010

plt.plot(COP_dyn_852718,Qflow_chill_dyn_852718,'bo')

plt.plot(COP_stat_852718,Qflow_chill_stat_852718,'b-')

plt.plot(COP_dyn_903010,Qflow_chill_dyn_903010,'ro')

plt.plot(COP_stat_903010,Qflow_chill_stat_903010,'r-')

error = lgo.ARE(COP_dyn_852718,Qflow_chill_dyn_852718,COP_stat_852718,Qflow_chill_stat_852718,COP_dyn_903010,Qflow_chill_dyn_903010,COP_stat_903010,Qflow_chill_stat_903010)
print(error)
plt.show()

# plt.figure()

# Qflow_chill_dyn=np.concatenate((Qflow_chill_dyn_852718,Qflow_chill_dyn_903010))

# Qflow_chill_stat=np.concatenate((Qflow_chill_stat_852718,Qflow_chill_stat_903010))

# plt.scatter(Qflow_chill_dyn,Qflow_chill_stat)

# plt.figure()

# COP_dyn=np.concatenate((COP_dyn_852718,COP_dyn_903010))

# COP_stat=np.concatenate((COP_stat_852718,COP_stat_903010))

# plt.scatter(COP_dyn,COP_stat)"""
