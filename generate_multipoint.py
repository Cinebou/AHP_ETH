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
import time


# cycle time list is imported from 'generatePerformanceMap_steadyState'
num_t = len(cycle_time_list)


""" calculation of all data temperature triples, range is defined by myself
"""
def calc_all_myself():
    """ temperature range 
    """
    heat_init,  heat_fin  = 60, 90
    cool_init,  cool_fin  = 24, 40
    #cool_init,  cool_fin  = 15, 23
    chill_init, chill_fin = 10, 20

    results_stat = pd.DataFrame([], index = ['T_heat', 'T_cool', 'T_chill','t_Cycle','COP','Q_flow_cool_avg']).T

    for T_heat in range(heat_init,heat_fin+1, 2):        
        for T_cool in range(cool_init,cool_fin+1, 2):        
            for T_chill in range(chill_init,chill_fin+1, 2):
                """Mahbubul Muttakin, Sourav Mitra et al. International Journal of Heat and Mass Transfer, 122, 7 2018, Fig 8
                """
                # the feasible region of heating temp and rejecting temp
                if (T_heat > 2.4928*T_cool - 13.768) and (T_heat>T_cool>T_chill): 
                    result_temp = T3_cap(T_heat+273.15, T_cool+273.15, T_chill+273.15)
                    results_stat = pd.concat([results_stat, result_temp])

    return results_stat


""" calculation of all data temperature triples, use the same range as dynamic simulation
"""
def calc_all():
    results_stat = pd.DataFrame([], index = ['T_heat', 'T_cool', 'T_chill','t_Cycle','COP','Q_flow_cool_avg']).T

    # read the calculation points from dynamic simulation
    points = pd.read_csv('calc_points_Silica.csv', header = None)

    # T3_cap can calculate several cycle time in a once, so only the shortest cycle time is transfered to T3_cap
    for index, row in points.iterrows():
        T_chill=row[0]
        T_reject=row[1]
        T_heat=row[2]
        t_Cycle = row[3]
        if t_Cycle == cycle_time_list[0]:
            result_temp = T3_cap(T_heat+273.15, T_reject+273.15, T_chill+273.15)
            results_stat = pd.concat([results_stat, result_temp])
    return results_stat



""" calculate 'Qflow vs. COP graph' of each temperature settings
"""
def T3_cap(T_heat, T_cool, T_chill):
    """ generate and initialze the AKM instance for each calculation """
    param = params()
    AKM = SteadyStateAKM.adsorptionChiller_steadyState(**param.Silica123_water_fit)

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
    time_st = time.time()
    stat_data_point = calc_all_myself()
    result = stat_data_point.sort_values(['T_heat','T_cool', 'T_chill','t_Cycle'])
    result.to_csv('Results/Silica_water_stat_NAN01.csv')

    time_fin = time.time()
    print(' calculation time  : ', time_fin - time_st)
    print(' calc time for one case is : ', (time_fin - time_st)/len(result))


if __name__=='__main__':
    main()

