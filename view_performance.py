# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 13:58:30 2020

@author: gibelhaus
"""
import numpy as np
import pickle
    
import matplotlib.pyplot as plt

with open('results_stat.pickle', 'rb') as f:
    # Read the pickled data
    results_stat = pickle.load(f)

t_cycle_stat = np.array(results_stat['t_cycle']) 

Q_flow_chill_stat = np.array(results_stat['Q_flow_chill']) 

COP_stat = np.array(results_stat['COP']) 

#Deleting the left side of the pareto frontier
ind_Qmax = Q_flow_chill_stat.argmax()
t_cycle_stat = t_cycle_stat[ind_Qmax:]
t_cycle_stat = t_cycle_stat[ind_Qmax:]
Q_flow_chill_stat = Q_flow_chill_stat[ind_Qmax:]
COP_stat = COP_stat[ind_Qmax:]
COP_stat = COP_stat[ind_Qmax:]
Q_flow_chill_stat = Q_flow_chill_stat[ind_Qmax:]

#Deleting equivalent max COP points
ind_COPmax = np.where(COP_stat<COP_stat.max()*0.99)
t_cycle_stat = t_cycle_stat[ind_COPmax]
Q_flow_chill_stat = Q_flow_chill_stat[ind_COPmax]
COP_stat = COP_stat[ind_COPmax]
COP_stat = COP_stat[ind_COPmax]
Q_flow_chill_stat = Q_flow_chill_stat[ind_COPmax]


plt.plot(COP_stat, Q_flow_chill_stat)
plt.show()