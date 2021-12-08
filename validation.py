# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 2021

@author: Hibiki Kimura
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import log_output as lgo
from param_database import params
import csv

# read data
#stat_data = pd.read_csv('results_stat_all.csv')
stat_data = pd.read_csv('results_stat_1temp_all.csv')
dyn_data=pd.read_csv('./PerformanceMap/results_dyn_all.csv')

# confirm teh setting of both, stat and dyn
stat_COP = []; dyn_COP=[]
stat_Qflow=[]; dyn_Qflow=[]
for i in range(len(stat_data)):
    if stat_data['T_heat'][i]==dyn_data['T_heat'][i] and stat_data['T_cool'][i]==dyn_data['T_cool'][i] and stat_data['T_chill'][i]==dyn_data['T_chill'][i] and stat_data['t_Cycle'][i]==dyn_data['t_Cycle'][i]:
        stat_COP.append(stat_data['COP'][i]); dyn_COP.append(dyn_data['COP'][i])
        stat_Qflow.append(stat_data['Q_flow_cool_avg'][i]); dyn_Qflow.append(dyn_data['Q_flow_cool_avg'][i])

print(len(stat_Qflow))
print(len(dyn_Qflow))
# COP figure
plt.figure()
plt.title('COP')
plt.scatter(dyn_COP,stat_COP,color='b', s=0.6)

#plt.plot([0,1],[0,0.9], color='r')
#plt.plot([0,1],[0,1.1],color='r')
plt.plot([0,2500],[0,2500],color='r',lw=3)
plt.xlabel('COP_dyn',fontsize=15)
plt.ylabel('COP_SteadyState',fontsize=15)
plt.ylim(0.2,1)
plt.xlim(0.2,1)

# SCP figure
plt.figure()
plt.title('Q_flow cool')
plt.scatter(dyn_Qflow,stat_Qflow,color='b',s=0.6)

#lt.plot([0,2500],[0,2250], color='r')
#plt.plot([0,2500],[0,2750],color='r')
plt.plot([0,2500],[0,2500],color='r',lw=3)
plt.xlim(500,max(dyn_data['Q_flow_cool_avg'])+100)
plt.ylim(500,max(stat_data['Q_flow_cool_avg'])+100)
plt.xlabel('Qflow_dyn',fontsize=15)
plt.ylabel('Qflow_SteadyState',fontsize=15)
plt.show()




