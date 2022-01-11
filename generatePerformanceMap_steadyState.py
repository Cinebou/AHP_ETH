# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 12:35:04 2020

@author: gibelhaus
"""
import numpy as np
import SteadyStateAKM
import log_output as lgo
from param_database import params
import time
import matplotlib.pyplot as plt

#%% cycle time
# cycle_time_list = [500,600,700,800,900,1000,1100,1150,1200,1250,1300,1400]  # 13 points, SILIca gel 123
cycle_time_list = [500,600,700,800,900,1000,1100,1150,1200,1250,1300,1400] # 12 points, AQSOA
# cycle_time_list = [300,400,500,600,700,800,1000,1200,1400,1600,1800,2000,2500,3000,3200,3500,4000,4500,5000] # Andrej

""" solving the AKM for all cycle time list, return list
"""
def calc_map(AKM_i):
    # prepare the data list
    t_cycle_array=np.array(cycle_time_list)
    Q_flow_chill = np.empty(len(cycle_time_list))
    COP = np.empty((len(cycle_time_list)))

    # initial guess of the variables, temperature should be around HTF input temperature
    var_guess = np.array([AKM_i.T_evp_in,AKM_i.T_cond_in,AKM_i.T_ads_in,AKM_i.T_des_in,0.2,0.05])

    for num, t_cycle in enumerate(t_cycle_array):
        AKM_i.t_cycle = t_cycle
        AKM_i.solve(var_guess)
        Q_flow_chill[num] = AKM_i.Q_flow_evp * 2
        COP[num] = AKM_i.COP
        #lgo.log_output_excel(AKM_i)

    return COP, Q_flow_chill


""" calculate one line, example code
"""
def main():
    time_sta = time.time()
    param = params()
    AKM_852718 = SteadyStateAKM.adsorptionChiller_steadyState(**param.Silica123_water_case1)
    COP_stat_852718, Qflow_chill_stat_852718 = calc_map(AKM_852718)
    time_end = time.time()

    print("calculation time ::  ",time_end - time_sta," sec")
    print("calc time for each case  :  ", (time_end - time_sta)/len(COP_stat_852718))
    show_Q_COP(COP_stat_852718,Qflow_chill_stat_852718)
    return 0


""" plot the capacities
"""
def show_Q_COP(COP,Qflow):
    plt.figure()
    plt.scatter(COP,Qflow)
    plt.show()
    return 0


""" parameters can be changed here, 
"""
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



if __name__ == "__main__":
    main()
