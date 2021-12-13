"""
Created on Fri Oct  2021
@author Hibiki Kimura
"""

import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import log_output as lg
lg.basicConfig(filename="pickle.log",level=lg.DEBUG)
np.set_printoptions(threshold=np.inf)

with open("results_400s.pickle", mode = 'rb') as f:
    results = pickle.load(f)

tCycle_temp = []; COP_temp = []; Qflow_temp = []
for i in range(len(results)):
        if (results[i]['T_chill'][-1] == [291.15]) & (results[i]['T_cool'][-1] == [300.15]) & (results[i]['T_heat'][-1] == [358.15]):
                lg.debug(results[i])
"""
pics = glob.glob('./*.pickle')
results = []
for pic in pics:
        with open(pic, mode = 'rb') as f:
                print(pic)
                results.extend(pickle.load(f))
# the data included in the pickle file
# ('time', '<f8'), ('T_chill', '<f8'), ('T_cool', '<f8'), ('T_heat', '<f8'), ('t_Cycle', '<f8'), ('summary.H_flow_evaporator', '<f8'), ('Q_flow_cool_avg', '<f8'), ('COP', '<f8'), ('stopTime', '<f8')]),

# configuration of the three temperature of adsorption chiller (degree C)
heat  = 85
cool  = 27 
chill = 18

# extract the data of that temperature above
tCycle_temp = []; COP_temp = []; Qflow_temp = []
for i in range(len(results)):
        if (results[i]['T_chill'][-1] == [273.15 + chill]) & (results[i]['T_cool'][-1] == [273.15 + cool]) & (results[i]['T_heat'][-1] == [273.15 + heat]):
                tCycle_temp.append(results[i]['t_Cycle'][-1])
                COP_temp.append(results[i]['COP'][-1])
                Qflow_temp.append(results[i]['Q_flow_cool_avg'][-1])

# summarize in a pickle file              
temp = []
temp.extend([tCycle_temp,COP_temp,Qflow_temp])
results_dyn = pd.DataFrame(temp, index = ['t_Cycle','COP','Q_flow_cool_avg']).T
results_dyn_T = results_dyn.sort_values('t_Cycle')
#with open('./SCP_COP/results_dyn_{}{}{}.pickle'.format(heat,cool,chill), mode = 'wb') as f:
        #pickle.dump(results_dyn_T,f)

plt.figure()
plt.scatter(COP_temp,Qflow_temp)
plt.show()"""
