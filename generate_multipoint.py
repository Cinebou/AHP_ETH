# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 2021

@author: Hibiki Kimura
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import generatePerformanceMap_steadyState as gMap
import SteadyStateAKM
import log_output as lgo
from param_database import params
from pprint import pprint

t_cycle_dyn, Qflow_chill_dyn, COP_dyn = lgo.read_pickle('./PerformanceMap/SCP_COP/results_dyn_852718.pickle')

def calc_all():
    results_stat = pd.DataFrame([], index = ['T_heat', 'T_cool', 'T_chill','t_Cycle','COP','Q_flow_cool_avg']).T
    for i in range(31): # T_heat 31
        for j in range(26): # T_cool 26
            for k in range(11): # T_chill 11
                T_heat = 333.15 + i;   T_cool = 288.15 + j;  T_chill = 283.15 + k
                result_temp = T3_cap(T_heat, T_cool, T_chill)
                results_stat = pd.concat([results_stat, result_temp])
    return results_stat


def T3_cap(T_heat, T_cool, T_chill):
    param = params()
    AKM = SteadyStateAKM.adsorptionChiller_steadyState(**param.p903010)
    AKM.T_des_in = T_heat;  AKM.T_ads_in = T_cool;  AKM.T_cond_in = T_cool;  AKM.T_evp_in = T_chill
    COP, Qflow = gMap.calc_map(AKM)
    t3 = []
    t3.extend([[T_heat]*len(t_cycle_dyn), [T_cool]*len(t_cycle_dyn), [T_chill]*len(t_cycle_dyn), list(t_cycle_dyn), list(COP), list(Qflow)])
    results_t3 = pd.DataFrame(t3, index = ['T_heat', 'T_cool', 'T_chill','t_Cycle','COP','Q_flow_cool_avg']).T
    print(results_t3)
    return results_t3

def main():
    stat_data_point = calc_all()
    result = stat_data_point.sort_values(['T_heat','T_cool', 'T_chill','t_Cycle'])
    result.to_csv('results/results_stat2.csv')
    # the way of extend t3 was a bit strange
    # I need further modification and validation

if __name__=='__main__':
    main()