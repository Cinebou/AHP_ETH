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
        self.stat_data = pd.read_csv('./Results/Silica_water_stat.csv')
        self.dyn_data=pd.read_csv('./Results/dyn_Silica_all.csv')

    
    def __initResult(self):
        self.stat_COP = []; self.dyn_COP=[]
        self.stat_Qflow=[]; self.dyn_Qflow=[]

    def __appendResults(self):
        self.stat_COP.append(self.COP_s_temp)
        self.stat_Qflow.append(self.Qflow_s_temp)
        self.dyn_COP.append(self.COP_d_temp)
        self.dyn_Qflow.append(self.Qflow_d_temp)


    """ calculate ARE
    """
    def ARE_COP(self):
        errorCOP = abs(self.COP_d_temp - self.COP_s_temp)/self.COP_d_temp
        return errorCOP


    def ARE_Qflow(self):
        errorQflow = abs(self.Qflow_d_temp - self.Qflow_s_temp)/self.Qflow_d_temp
        return errorQflow

    def RMSD(self, dyn_COP_A, stat_COP_A, dyn_COP_B, stat_COP_B, dyn_Q_A,stat_Q_A, dyn_Q_B, stat_Q_B):
        dyn_Qh_A = dyn_Q_A / dyn_COP_A
        stat_Qh_A = stat_Q_A / stat_COP_A
        dyn_Qh_B = dyn_Q_B / dyn_COP_B
        stat_Qh_B = stat_Q_B / stat_COP_B

        rmsd_Q = (dyn_Q_A - stat_Q_A)**2 + (dyn_Q_B - stat_Q_B)**2
        rmsd_Qh = (dyn_Qh_A - stat_Qh_A)**2 + (dyn_Qh_B - stat_Qh_B)**2
        return (sum(rmsd_Qh)+sum(rmsd_Q)) / len(dyn_COP_A)/2

    def RMSD_one(self, dyn_COP_A, stat_COP_A, dyn_Q_A,stat_Q_A):
        dyn_Qh_A = dyn_Q_A / dyn_COP_A
        stat_Qh_A = stat_Q_A / stat_COP_A

        rmsd_Q = (dyn_Q_A - stat_Q_A)**2 
        rmsd_Qh = (dyn_Qh_A - stat_Qh_A)**2 
        return (sum(rmsd_Qh)+sum(rmsd_Q)) / len(dyn_COP_A)
    
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


    def ARE_one(COP_dyn_903010,Qflow_chill_dyn_903010,COP_stat_903010,Qflow_chill_stat_903010):
        RE = abs(COP_dyn_903010 - COP_stat_903010)/COP_dyn_903010 + abs(Qflow_chill_dyn_903010 - Qflow_chill_stat_903010)/Qflow_chill_dyn_903010
        return sum(RE)/len(RE)

    def ARE(COP_dyn_852718,Qflow_chill_dyn_852718,COP_stat_852718,Qflow_chill_stat_852718,COP_dyn_903010,Qflow_chill_dyn_903010,COP_stat_903010,Qflow_chill_stat_903010):
        RE = abs(COP_dyn_852718 - COP_stat_852718)/COP_dyn_852718 + abs(Qflow_chill_dyn_852718 - Qflow_chill_stat_852718)/Qflow_chill_dyn_852718 + abs(COP_dyn_903010 - COP_stat_903010)/COP_dyn_903010 + abs(Qflow_chill_dyn_903010 - Qflow_chill_stat_903010)/Qflow_chill_dyn_903010
        return sum(RE)/len(RE)/2




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

        # error function
        COPerror_sum = 0
        Qerror_sum = 0
        count=0; max_dev_COP = 0; max_dev_Qflow=0
        for index, row in self.stat_data.iterrows():
            # take the data from stat_file
            T_chill_s = row['T_chill']
            T_reject_s = row['T_cool']
            T_heat_s = row['T_heat']
            t_Cycle_s = int(row['t_Cycle'])
            self.COP_s_temp = float(row['COP'])
            self.Qflow_s_temp = float(row['Q_flow_cool_avg'])

            # take the data from dyn file, which has equibalent settings
            dyn_line = self.dyn_data[(self.dyn_data['T_chill']==T_chill_s) & (self.dyn_data['T_reject']==T_reject_s) &\
                 (self.dyn_data['T_heat']==T_heat_s) & (self.dyn_data['t_Cycle']==t_Cycle_s)]
            self.COP_d_temp = float(dyn_line['COP'])
            self.Qflow_d_temp = float(dyn_line['Qflows'])

            # add the results
            if self.COP_d_temp>0.3:
                self.__appendResults()
                COPerror_sum += self.ARE_COP()
                Qerror_sum   += self.ARE_Qflow()
                count+=1
                max_dev_COP = max(max_dev_COP,self.ARE_COP())
                max_dev_Qflow=max(max_dev_Qflow,self.ARE_Qflow())

        # evaluate the deviation
        COPerror_sum /= count
        Qerror_sum /= count
        print('ARE of COP is :  ', COPerror_sum)
        print('ARE of Qcool is :  ', Qerror_sum)
        print('max deviation in COP is : ', max_dev_COP)
        print('max deviation in Qflow is  ', max_dev_Qflow)
        self.show_graph_multiple()


    def show_graph_multiple(self):
        # COP figure
        plt.figure()
        plt.plot([0,1],[0,0.9], color='r',lw=1)
        plt.plot([0,1],[0,1.1], color='r',lw=1)
        plt.scatter(self.dyn_COP,self.stat_COP,color='b', s=2.5)

        plt.plot([0,1],[0,1],color='orange',lw=2)
        plt.xlabel('$COP^{dyn}$',fontsize=15)
        plt.ylabel('$COP^{stat}$',fontsize=15)
        plt.ylim(0,0.65)
        plt.xlim(0,0.65)
        plt.rcParams['figure.subplot.bottom'] = 0.15
        plt.rcParams['lines.linewidth'] = 3

        plt.savefig('Fig/COP_silica.eps')

        # SCP figure
        plt.figure()
        plt.plot([0,2500],[0,2250], color='r',lw=1)
        plt.plot([0,2500],[0,2750], color='r',lw=1)
        plt.scatter(self.dyn_Qflow,self.stat_Qflow,color='b',s=2.5)

        plt.plot([0,1500],[0,1500],color='orange',lw=2)
        plt.xlabel('$Q_{cool}^{dyn}$  in  W',fontsize=15)
        plt.ylabel('$Q_{cool}^{stat}$  in  W',fontsize=15)
        plt.ylim(0,2500)
        plt.xlim(0,2000)
        plt.rcParams['figure.subplot.bottom'] = 0.15
        plt.rcParams['lines.linewidth'] = 3

        plt.savefig('Fig/Qflow_silica.eps')
        plt.show() 

def main():
    VL = Validater()
    VL.validate_data()


if __name__ == '__main__':
    main()


