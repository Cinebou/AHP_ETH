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
stat_data = pd.read_csv('./Results/results_stat_andrej.csv')
dyn_data=pd.read_csv('./Results/results_dyn_all.csv')


# key temperature triple
def temp_valid(i):
    global dyn_data, stat_data
    Heat = stat_data['T_heat'][i]; Cool = stat_data['T_cool'][i]; Chill = stat_data['T_chill'][i]; t_Cycle = stat_data['t_Cycle'][i]
    if Heat==dyn_data['T_heat'][i] and Cool==dyn_data['T_cool'][i] and Chill==dyn_data['T_chill'][i] and t_Cycle==dyn_data['t_Cycle'][i]:

        #if Heat > Cool > Chill:
        return True
    return False

def All_ARE():
    global stat_COP, stat_Qflow, dyn_COP, dyn_Qflow
    error = 0
    for i in range(len(stat_COP)):
        errorCOP = abs(stat_COP[i] - dyn_COP[i])/dyn_COP[i]
        errorQflow = abs(stat_Qflow[i] - dyn_Qflow[i])/dyn_Qflow[i]
        error += (errorCOP+errorQflow)
    return error / len(stat_COP)


# confirm the setting of both, stat and dyn
stat_COP = []; dyn_COP=[]
stat_Qflow=[]; dyn_Qflow=[]
error_count = 0
max_deviation = 0.4
for i in range(len(stat_data)):
    if temp_valid(i):
        stat_COP.append(stat_data['COP'][i]); dyn_COP.append(dyn_data['COP'][i])
        stat_Qflow.append(stat_data['Q_flow_cool_avg'][i]); dyn_Qflow.append(dyn_data['Q_flow_cool_avg'][i])

        #if abs((stat_data['COP'][i]-dyn_data['COP'][i])/dyn_data['COP'][i]) > max_deviation or abs((stat_data['Q_flow_cool_avg'][i]-dyn_data['Q_flow_cool_avg'][i])/dyn_data['Q_flow_cool_avg'][i]) > max_deviation:
        #if stat_data['Q_flow_cool_avg'][i] >500 and dyn_data['Q_flow_cool_avg'][i] > 1000 and stat_data['Q_flow_cool_avg'][i] < dyn_data['Q_flow_cool_avg'][i] - 500:
        #if stat_data['COP'][i] < 0 and dyn_data['COP'][i] > 0.25:
        if stat_data['COP'][i] < -0.5:
            msg = '{},{},{},{},{},{}, {}, {}'.format(i, stat_data['T_heat'][i], stat_data['T_cool'][i], stat_data['T_chill'][i], stat_data['COP'][i], stat_data['Q_flow_cool_avg'][i], dyn_data['COP'][i], dyn_data['Q_flow_cool_avg'][i] )
            lgo.log_excel_msg(msg)
            error_count += 1


print("num_error =  ", error_count, "  error_rate = ", error_count/len(stat_data))
print('data point = ', len(stat_COP))
print("Average relative error of all points  = ",All_ARE())




# COP figure
plt.figure()
plt.title('COP')
plt.scatter(dyn_COP,stat_COP,color='b', s=0.6)

#plt.plot([0,1],[0,0.9], color='r')
#plt.plot([0,1],[0,1.1],color='r')
plt.plot([0,1],[0,1],color='r',lw=3)
plt.xlabel('COP_dyn',fontsize=15)
plt.ylabel('COP_SteadyState',fontsize=15)
plt.ylim(-1,1)
plt.xlim(-1,1)

# SCP figure
plt.figure()
plt.title('Q_flow cool')
plt.scatter(dyn_Qflow,stat_Qflow,color='b',s=0.6)

#lt.plot([0,2500],[0,2250], color='r')
#plt.plot([0,2500],[0,2750],color='r')
plt.plot([0,2500],[0,2500],color='r',lw=3)
#plt.xlim(-500,max(dyn_data['Q_flow_cool_avg'])+100)
#plt.ylim(-500,max(stat_data['Q_flow_cool_avg'])+100)
plt.xlabel('Qflow_dyn',fontsize=15)
plt.ylabel('Qflow_SteadyState',fontsize=15)
plt.show()




