# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 2021

@author: Hibiki Kimura
"""
import pandas as pd
import matplotlib.pyplot as plt
import log_output as lgo
import pickle 
import numpy as np


class Validater:
    def __init__(self,stat_COP = None, dyn_COP=None,stat_Qflow=None, dyn_Qflow=None):
        self.stat_COP  = stat_COP
        self.dyn_COP   = dyn_COP
        self.statQflow = stat_Qflow
        self.dyn_Qflow = dyn_Qflow

    def __readData(self):
        # read data
        self.stat_data = pd.read_csv('./Results/Silicagel123_stat.csv')
        self.dyn_data=pd.read_csv('./Results/dyn_Silica123_water.csv')

    
    def __initResult(self):
        self.stat_COP = []; self.dyn_COP=[]
        self.stat_Qflow=[]; self.dyn_Qflow=[]

    def __appendResults(self):
        self.stat_COP.append(self.COP_s_temp)
        self.stat_Qflow.append(self.Qflow_s_temp)
        self.dyn_COP.append(self.COP_d_temp)
        self.dyn_Qflow.append(self.Qflow_d_temp)


    """ calculate RMSD from two data line, A and B is two temperature settings
    for the fitting figure"""

    def RMSD_Qflow(Qflow_A_dyn,Qflow_A_stat,  Qflow_B_dyn,Qflow_B_stat):
        """ the number of cycle time of dyn and stat should be same """
        assert(len(Qflow_A_dyn) != len(Qflow_A_stat))

        SD_Q_A   = (Qflow_A_dyn - Qflow_A_stat)**2 / len(Qflow_A_dyn)
        SD_Q_B   = (Qflow_B_dyn - Qflow_B_stat)**2 / len(Qflow_B_dyn)
        return (SD_Q_A + SD_Q_B) / 2

    def RMSD_COP(COP_A_dyn,COP_A_stat,  COP_B_dyn,COP_B_stat):
        """ the number of cycle time of dyn and stat should be same """
        assert(len(COP_A_dyn) != len(COP_A_stat))

        SD_COP_A = (COP_A_dyn - COP_A_stat)**2 / len(COP_A_dyn)
        SD_COP_B = (COP_B_dyn - COP_B_stat)**2 / len(COP_B_dyn)
        return (SD_COP_A + SD_COP_B) / 2

    
    """ read the results pickle file and return the numpy array """
    def read_pickle(file):
        with open(file, 'rb') as f:
                results = pickle.load(f)
        t_cycle=[]
        Qflow=[]
        COP=[]
        for line in results:
            t_cycle.append(line[0])
            Qflow.append(line[5])
            COP.append(line[4])
        return np.array(t_cycle), np.array(Qflow), np.array(COP)  


    def ARE(COP_dyn_852718,Qflow_chill_dyn_852718,COP_stat_852718,Qflow_chill_stat_852718,COP_dyn_903010,Qflow_chill_dyn_903010,COP_stat_903010,Qflow_chill_stat_903010):
        RE = abs(COP_dyn_852718 - COP_stat_852718)/COP_dyn_852718 + abs(Qflow_chill_dyn_852718 - Qflow_chill_stat_852718)/Qflow_chill_dyn_852718 + abs(COP_dyn_903010 - COP_stat_903010)/COP_dyn_903010 + abs(Qflow_chill_dyn_903010 - Qflow_chill_stat_903010)/Qflow_chill_dyn_903010
        return sum(RE)/len(RE)




    """ check the key temperature triple and cycle time are the same and in order
        if the setting is correct, return True
        'i' is the index of the data 
    """
    def temp_valid(self, i):
        Heat = self.stat_data['T_heat'][i]
        Cool = self.stat_data['T_cool'][i]
        Chill = self.stat_data['T_chill'][i]
        t_Cycle = self.stat_data['t_Cycle'][i]

        ''' confirm the param setting is the same between dyn and stat'''
        if Heat==self.dyn_data['T_heat'][i] and Cool==self.dyn_data['T_cool'][i] and Chill==self.dyn_data['T_chill'][i] and t_Cycle==self.dyn_data['t_Cycle'][i]:
            ''' the temperature should be in order '''
            if Heat > Cool > Chill:
                return True
        return False


    def All_ARE(self):
        error = 0
        for i in range(len(self.stat_COP)):
            errorCOP = abs(self.stat_COP[i] - self.dyn_COP[i])/self.dyn_COP[i]
            errorQflow = abs(self.stat_Qflow[i] - self.dyn_Qflow[i])/self.dyn_Qflow[i]
            error += (errorCOP+errorQflow)
        return error / len(self.stat_COP)
              

    def validate_data(self):
        self.__readData()
        self.__initResult()

        for index, row in self.stat_data.iterrows():
            # take the data from stat_file
            T_chill_s = row['T_chill']
            T_reject_s = row['T_cool']
            T_heat_s = row['T_heat']
            t_Cycle_s = int(row['t_Cycle'])
            self.COP_s_temp = row['COP']
            self.Qflow_s_temp = row['Q_flow_cool_avg']

            # take the data from dyn file, which has equibalent settings
            dyn_line = self.dyn_data[(self.dyn_data['T_chill']==T_chill_s) & (self.dyn_data['T_reject']==T_reject_s) &\
                 (self.dyn_data['T_heat']==T_heat_s) & (self.dyn_data['t_Cycle']==t_Cycle_s)]
            self.COP_d_temp = dyn_line['COP']
            self.Qflow_d_temp = dyn_line['Qflows']

            # add the results
            self.__appendResults()
        self.show_graph_multiple()



    def show_graph_multiple(self):
        # COP figure
        plt.figure()
        plt.title('COP')
        plt.scatter(self.dyn_COP,self.stat_COP,color='b', s=0.6)

        plt.plot([0,1],[0,0.9], color='r')
        plt.plot([0,1],[0,1.1],color='r')
        plt.plot([0,1],[0,1],color='r',lw=3)
        plt.xlabel('COP_dyn',fontsize=15)
        plt.ylabel('COP_SteadyState',fontsize=15)
        plt.ylim(0,0.8)
        plt.xlim(0,0.8)

        # SCP figure
        plt.figure()
        plt.title('Q_flow cool')
        plt.scatter(self.dyn_Qflow,self.stat_Qflow,color='b',s=0.6)

        plt.plot([0,2500],[0,2250], color='r')
        plt.plot([0,2500],[0,2750],color='r')
        plt.plot([0,2500],[0,2500],color='r',lw=3)
        plt.xlabel('Qflow_dyn',fontsize=15)
        plt.ylabel('Qflow_SteadyState',fontsize=15)
        plt.ylim(0,1500)
        plt.xlim(0,1500)
        plt.show()  

def main():
    VL = Validater()
    VL.validate_data()


if __name__ == '__main__':
    main()


