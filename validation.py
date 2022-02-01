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
from math import isnan


class Validater:
    def __init__(self,stat_COP = None, dyn_COP=None,stat_Qflow=None, dyn_Qflow=None):
        self.stat_COP  = stat_COP
        self.dyn_COP   = dyn_COP
        self.statQflow = stat_Qflow
        self.dyn_Qflow = dyn_Qflow

    def __readData(self):
        # read data
        self.stat_data = pd.read_csv('./Results/Silica_water_stat_cool.csv')
        self.dyn_data=pd.read_csv('./Results/dyn_Silica_all.csv')

    
    def __initResult(self):
        self.stat_COP = []; self.dyn_COP=[]
        self.stat_Qflow=[]; self.dyn_Qflow=[]
        self.COPerror_sum = 0
        self.Qerror_sum = 0
        self.max_dev_COP = 0 
        self.max_dev_Qflow=0
        header = 'T_chill, T_reject, T_heat, t_Cycle, dyn_COP, dyn_Qflow'
        lgo.log_excel_msg(header)

    def __appendResults(self):
        self.stat_COP.append(self.COP_s_temp)
        self.stat_Qflow.append(self.Qflow_s_temp)
        self.dyn_COP.append(self.COP_d_temp)
        self.dyn_Qflow.append(self.Qflow_d_temp)


    """ calculate ARE (average relative error)
    """
    def ARE_COP(self):
        errorCOP = abs(self.COP_d_temp - self.COP_s_temp)/self.COP_d_temp
        return errorCOP


    def ARE_Qflow(self):
        errorQflow = abs(self.Qflow_d_temp - self.Qflow_s_temp)/self.Qflow_d_temp
        return errorQflow


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

    # calculate average relative error for fitting performance map
    def ARE(COP_dyn_A,Qflow_chill_dyn_A,COP_stat_A,Qflow_chill_stat_A,COP_dyn_B,Qflow_chill_dyn_B,COP_stat_B,Qflow_chill_stat_B):
        RE_COP = abs(COP_dyn_A - COP_stat_A)/COP_dyn_A + abs(COP_dyn_B - COP_stat_B)/COP_dyn_B
        RE_Q   = abs(Qflow_chill_dyn_A - Qflow_chill_stat_A)/Qflow_chill_dyn_A + abs(Qflow_chill_dyn_B - Qflow_chill_stat_B)/Qflow_chill_dyn_B
        return (RE_COP + RE_Q) / len(RE_COP) / 2


    # compare the dynamic and short-cut model one by one
    def validate_data(self):
        self.__readData()
        self.__initResult()

        # error count
        nan_count=0
        # for each data in stat file, compare with the dynamic simulation
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

            # if the stat value is not NAN, move on to processing data. if not, record on log file
            if (not isnan(self.COP_s_temp)) and (not isnan(self.Qflow_s_temp)):
                self.arrange_results()

            else:
                nan_count+=1
                self.record_error(T_chill_s, T_reject_s, T_heat_s, t_Cycle_s)
                
        self.print_results(nan_count)
        self.show_graph_multiple()


    # append to the results list, calculate max and average deviation
    def arrange_results(self):
        self.__appendResults()
        self.COPerror_sum += self.ARE_COP()
        self.Qerror_sum   += self.ARE_Qflow()
        self.max_dev_COP = max(self.max_dev_COP,self.ARE_COP())
        self.max_dev_Qflow=max(self.max_dev_Qflow,self.ARE_Qflow())
        return 0


    # record error on 'Log/validate.csv'
    def record_error(self, T_chill_s, T_reject_s, T_heat_s, t_Cycle_s):
        msg = '{},{},{},{}, {},{}'.format(T_chill_s, T_reject_s, T_heat_s, t_Cycle_s, self.COP_d_temp, self.Qflow_d_temp)
        lgo.log_excel_msg(msg)
        return 0


    # output the summary of the results on console
    def print_results(self, nan_count):
        num_data = len(self.stat_data) - nan_count
        self.COPerror_sum /= num_data
        self.Qerror_sum /= num_data
        print('ARE of COP is :  ', self.COPerror_sum)
        print('ARE of Qcool is :  ', self.Qerror_sum)
        print('max deviation in COP is : ', self.max_dev_COP)
        print('max deviation in Qflow is  ', self.max_dev_Qflow)
        print('nan points : ',nan_count,' / ',len(self.stat_data))
        return 0


    # show the performace map comparison of COP and cooling capacity
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

        plt.savefig('Fig/COP_silica_cool.eps')

        # SCP figure
        plt.figure()
        plt.plot([0,2500],[0,2250], color='r',lw=1)
        plt.plot([0,2500],[0,2750], color='r',lw=1)
        plt.scatter(self.dyn_Qflow,self.stat_Qflow,color='b',s=2.5)

        plt.plot([0,1500],[0,1500],color='orange',lw=2)
        plt.xlabel('$\dot{Q}_{cool}^{dyn}$  in  W',fontsize=15)
        plt.ylabel('$\dot{Q}_{cool}^{stat}$  in  W',fontsize=15)
        plt.ylim(0,1500)
        plt.xlim(0,1500)
        plt.rcParams['figure.subplot.bottom'] = 0.15
        plt.rcParams['lines.linewidth'] = 3

        plt.savefig('Fig/Qflow_silica_cool.eps')
        plt.show() 



def main():
    VL = Validater()
    VL.validate_data()

if __name__ == '__main__':
    main()