# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 2021

@author: Hibiki Kimura
"""
import pandas as pd
import generatePerformanceMap_steadyState as gMap
import SteadyStateAKM
from param_database import params


cycle_time_list = [400,500,600,700,800,1000,1200,1400,1600,1800,2000,2500,3000,3200,3500,4000,4500,5000]
num_t = len(cycle_time_list)


def calc_all():
    results_stat = pd.DataFrame([], index = ['T_heat', 'T_cool', 'T_chill','t_Cycle','COP','Q_flow_cool_avg']).T
    for i in range(31):         # T_heat  31
        for j in range(26):     # T_cool  26
            for k in range(11): # T_chill 11
                T_heat = 333.15 + i;   T_cool = 288.15 + j;  T_chill = 283.15 + k
                result_temp = T3_cap(T_heat, T_cool, T_chill)
                results_stat = pd.concat([results_stat, result_temp])
    return results_stat


def T3_cap(T_heat, T_cool, T_chill):
    param = params()
    AKM = SteadyStateAKM.adsorptionChiller_steadyState(**param.Andrej)
    AKM.T_des_in = T_heat;  AKM.T_ads_in = T_cool;  AKM.T_cond_in = T_cool;  AKM.T_evp_in = T_chill
    COP, Qflow = gMap.calc_map(AKM)
    t3 = []
    t3.extend([[T_heat]*num_t, [T_cool]*num_t, [T_chill]*num_t, list(cycle_time_list), list(COP), list(Qflow)])
    results_t3 = pd.DataFrame(t3, index = ['T_heat', 'T_cool', 'T_chill','t_Cycle','COP','Q_flow_cool_avg']).T
    print(results_t3)
    return results_t3


def main():
    stat_data_point = calc_all()
    result = stat_data_point.sort_values(['T_heat','T_cool', 'T_chill','t_Cycle'])
    result.to_csv('results/results_stat2.csv')


if __name__=='__main__':
    main()

