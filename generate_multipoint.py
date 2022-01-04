# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 2021

@author: Hibiki Kimura
"""
import pandas as pd
import generatePerformanceMap_steadyState as gMap
import SteadyStateAKM
from param_database import params
from generatePerformanceMap_steadyState import cycle_time_list


# cycle time list is imported from 'generatePerformanceMap_steadyState'
num_t = len(cycle_time_list)


""" calculation of all data temperature triples
"""
def calc_all():
    """ temperature range """
    heat_init,  heat_fin  = 85, 87
    cool_init,  cool_fin  = 30, 31
    chill_init, chill_fin = 10, 15

    results_stat = pd.DataFrame([], index = ['T_heat', 'T_cool', 'T_chill','t_Cycle','COP','Q_flow_cool_avg']).T

    for T_heat in range(heat_init,heat_fin+1):        
        for T_cool in range(cool_init,cool_fin+1):        
            for T_chill in range(chill_init,chill_fin+1):  
                result_temp = T3_cap(T_heat+273.15, T_cool+273.15, T_chill+273.15)
                results_stat = pd.concat([results_stat, result_temp])

    return results_stat



""" calculate 'Qflow vs. COP graph' of each temperature settings
"""
def T3_cap(T_heat, T_cool, T_chill):
    """ generate and initialze the AKM instance for each calculation """
    param = params()
    AKM = SteadyStateAKM.adsorptionChiller_steadyState(**param.Silica123_water_case1)

    """ reset the temperature setting """
    AKM.T_des_in = T_heat;  AKM.T_ads_in = T_cool;  AKM.T_cond_in = T_cool;  AKM.T_evp_in = T_chill

    """ calculate the capacities """
    COP, Qflow = gMap.calc_map(AKM)

    """ return the pandas list """
    t3 = []
    t3.extend([[T_heat]*num_t, [T_cool]*num_t, [T_chill]*num_t, list(cycle_time_list), list(COP), list(Qflow)])
    results_t3 = pd.DataFrame(t3, index = ['T_heat', 'T_cool', 'T_chill','t_Cycle','COP','Q_flow_cool_avg']).T
    print(results_t3)
    
    return results_t3


""" calc multiple points and store in .csv file
"""
def main():
    stat_data_point = calc_all()
    result = stat_data_point.sort_values(['T_heat','T_cool', 'T_chill','t_Cycle'])
    result.to_csv('Results/testCase.csv')


if __name__=='__main__':
    main()

