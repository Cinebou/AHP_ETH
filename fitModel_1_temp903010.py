# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 13:58:30 2020

@author: gibelhaus
"""

import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt
import time
import SteadyStateAKM
import log_output as lgo
from validation import Validater
from generatePerformanceMap_steadyState import cycle_time_list

# cycle time list is imported from 'generatePerformanceMap_steadyState'
time_sta = time.time()

#%% Read results from dynamic simulation
#t_cycle_dyn_852718, Qflow_chill_dyn_852718, COP_dyn_852718 = Validater.read_pickle('./PerformanceMap/SCP_COP/dyn_data_Silica123_water_852718.pickle')
t_cycle_dyn_903010, Qflow_chill_dyn_903010, COP_dyn_903010 = Validater.read_pickle('./PerformanceMap/SCP_COP/dyn_data_Silica123_water_903010.pickle')
#Qflow_heat_dyn_852718 = Qflow_chill_dyn_852718/COP_dyn_852718
Qflow_heat_dyn_903010 = Qflow_chill_dyn_903010/COP_dyn_903010


def performance(corr,cycle_time_list, logout = False):

    var_guess = np.array([291.15,303.15,303.15,348.15,0.2,0.05])

    """
    param_852718 = [{
              'm_flow_evp':0.191, 
              'm_flow_cond':0.111,
              'm_flow_ads':0.166,
              'm_flow_des':0.166,
              'm_sor':2.236,
              'r_particle':0.00045,
              'cp_HX':379,
              'cp_W':4184,
              'm_HX':6.2,

              # working pair
              'sorbent':'Silicagel123_water',
              'cp_sor':1000,
              'fluid':'water',

              # 85 27 18
              'T_evp_in':291.15,
              'T_cond_in':300.15,
              'T_ads_in':300.15,
              'T_des_in':358.15,
              't_cycle':t_cycle_i,

              'alphaA_evp_o':corr[0],
              'alphaA_cond_o':corr[1],
              'alphaA_ads_o':corr[2],
              'alphaA_evp_i':corr[0],
              'alphaA_cond_i':corr[1],
              'alphaA_ads_i':corr[2],
              'D_eff':corr[3],
              'corr_sor_c': corr[4],
              'corr_sor_t': corr[6],
              'corr_HX_c': corr[5],
              'corr_HX_t':corr[7]
              } for t_cycle_i in cycle_time_list]
    
    
    AKM_852718 = [SteadyStateAKM.adsorptionChiller_steadyState(**param_i) for param_i in param_852718]
    
    [AKM_i.solve(var_guess) for AKM_i in AKM_852718]
    
    Qflow_chill_852718 = np.array([AKM_i.Q_flow_evp for AKM_i in AKM_852718])
    
    Qflow_heat_852718 = np.array([AKM_i.Q_flow_des for AKM_i in AKM_852718])
    """
    param_903010 = [{
              'm_flow_evp':0.191, 
              'm_flow_cond':0.111,
              'm_flow_ads':0.166,
              'm_flow_des':0.166,
              'm_sor':2.236,
              'r_particle':0.00045,
              'cp_HX':379,
              'cp_W':4184,
              'm_HX':6.2,

              # working pair
              'sorbent':'Silicagel123_water',
              'cp_sor':1000,
              'fluid':'water',

              # 903010
              'T_evp_in':283.15,
              'T_cond_in':303.15,
              'T_ads_in':303.15,
              'T_des_in':363.15,
              't_cycle':t_cycle_i,

              'alphaA_evp_o':corr[0],
              'alphaA_cond_o':corr[1],
              'alphaA_ads_o':corr[2],
              'alphaA_evp_i':corr[0],
              'alphaA_cond_i':corr[1],
              'alphaA_ads_i':corr[2],
              'D_eff':corr[3],
              'corr_sor_c': corr[4],
              'corr_sor_t': corr[6],
              'corr_HX_c': corr[5],
              'corr_HX_t':corr[7]
              } for t_cycle_i in cycle_time_list]
    
    AKM_903010 = [SteadyStateAKM.adsorptionChiller_steadyState(**param_i) for param_i in param_903010]
    
    [AKM_i.solve(var_guess) for AKM_i in AKM_903010]
    
    Qflow_chill_903010 = np.array([AKM_i.Q_flow_evp for AKM_i in AKM_903010])
    
    Qflow_heat_903010 = np.array([AKM_i.Q_flow_des for AKM_i in AKM_903010])

    #Qflow_chill_903010 = 2*Qflow_chill_903010; Qflow_heat_903010 = 2*Qflow_heat_903010
    
    if logout:
        for AKM_i in AKM_903010:
            lgo.log_output_excel(AKM_i)
        #for AKM_j in AKM_852718:
        #    lgo.log_output_excel(AKM_j)

    return Qflow_chill_903010, Qflow_heat_903010

def lsq_perf(corr,Qflow_chill_target_903010,Qflow_heat_target_903010):
    Qflow_chill_903010, Qflow_heat_903010 = performance(corr,cycle_time_list)
    lsq_Qflows = np.concatenate((Qflow_chill_903010-Qflow_chill_target_903010,Qflow_heat_903010-Qflow_heat_target_903010))
    return lsq_Qflows

corr0 = np.array([173, 3174, 151, 1.8e-10, 0.7 , 0.461, 0.1, 0.1])
bounds = ([50,50,50,1e-11,0,0,0,0],[10000,10000,10000,1e-9,5,5,1,1])
args = (Qflow_chill_dyn_903010,Qflow_heat_dyn_903010)
#res_perf = least_squares(lsq_perf, corr0, bounds=bounds, args=args,  verbose=1)



time_end = time.time()
print("calculation time ::  ",time_end - time_sta," sec")
#print(res_perf.x)

# silica gel 123 hibiki
x_1temp = [1.00537394e+02, 3.42943168e+03, 5.05362201e+02, 2.39364061e-10, 2.56628646e-01, 5.37264184e-01, 8.22035411e-03, 5.17084931e-02]

#%% Plot results
plt.figure()
#Qflow_chill_stat_903010, Qflow_heat_stat_903010, = performance(res_perf.x,cycle_time_list)
Qflow_chill_stat_903010, Qflow_heat_stat_903010, = performance(x_1temp,cycle_time_list)
#COP_stat_852718=Qflow_chill_stat_852718/Qflow_heat_stat_852718
COP_stat_903010=Qflow_chill_stat_903010/Qflow_heat_stat_903010
#plt.plot(COP_dyn_852718,Qflow_chill_dyn_852718,'bo',label='dyn 85 27 18')
#plt.plot(COP_stat_852718,Qflow_chill_stat_852718,'b-',label='stat 85 27 18')
plt.plot(COP_dyn_903010,Qflow_chill_dyn_903010,'ro',label='dynamic')
plt.plot(COP_stat_903010,Qflow_chill_stat_903010,'r-',label='short-cut')

plt.xlabel('COP',fontsize=15)
plt.ylabel('$Q_{cool}$ in W',fontsize=15)
plt.xlim(0.18,0.29)
plt.ylim(400,600)
plt.legend(fontsize = 15)

error = Validater.ARE_one(COP_dyn_903010,Qflow_chill_dyn_903010,COP_stat_903010,Qflow_chill_stat_903010)
print(error)
vl = Validater()
RMSD = vl.RMSD_one(COP_dyn_903010,COP_stat_903010,Qflow_chill_dyn_903010,Qflow_chill_stat_903010)
print('RMSD = ', RMSD)
plt.savefig('Fig/fitting_silica_1temp.eps')
plt.show()

