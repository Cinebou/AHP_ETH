"""
Created on Fri Oct 1 2021
@author Hibiki Kimura
"""

import pickle
import matplotlib.pyplot as plt
import glob
import pandas as pd

pics = glob.glob('./*.pickle')
results = []
for pic in pics:
        with open(pic, mode = 'rb') as f:
                print(pic)
                results.extend(pickle.load(f))
# the data included in the pickle file
# T_heat : 333.15 ~ 363.15 K, 31 points
# T_chill : 288.15 ~ 313.15 K, 26 points 
# T_cool : 283.15 ~ 293.15 K, 11 points
# t_cycle : 300 ~ 50000sec, 19 points
# total num points = 31 * 26 * 11 * 19 = 168454
# ('time', '<f8'), ('T_chill', '<f8'), ('T_cool', '<f8'), ('T_heat', '<f8'), ('t_Cycle', '<f8'), ('summary.H_flow_evaporator', '<f8'), ('Q_flow_cool_avg', '<f8'), ('COP', '<f8'), ('stopTime', '<f8')]),

# configuration of the three temperature of adsorption chiller (degree C)
heat  = 85
cool  = 27 
chill = 18

# extract the data of that temperature above
tCycle = []; COP = []; Qflow = []; T_heat=[]; T_chill=[]; T_cool=[]
for i in range(len(results)):
        T_heat.append(results[i]['T_heat'][-1])
        T_chill.append(results[i]['T_chill'][-1])
        T_cool.append(results[i]['T_cool'][-1])
        tCycle.append(results[i]['t_Cycle'][-1])
        COP.append(results[i]['COP'][-1])
        Qflow.append(results[i]['Q_flow_cool_avg'][-1])

# summarize in a pickle file              
temp = []
temp.extend([T_heat, T_cool, T_chill, tCycle, COP, Qflow])
results_dyn = pd.DataFrame(temp, index = ['T_heat', 'T_cool', 'T_chill','t_Cycle','COP','Q_flow_cool_avg']).T
results_dyn = results_dyn.sort_values(['T_heat','T_cool', 'T_chill','t_Cycle'])
results_dyn.to_csv('results_dyn_all.csv')

