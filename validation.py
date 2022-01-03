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
        self.stat_data = pd.read_csv('./Results/results_stat_andrej.csv')
        self.dyn_data=pd.read_csv('./Results/results_dyn_all.csv')

    
    def __initResult(self):
        self.stat_COP = []; self.dyn_COP=[]
        self.stat_Qflow=[]; self.dyn_Qflow=[]

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
        t_cycle = np.array(results['t_Cycle'])
        Qflow = np.array(results['Q_flow_cool_avg'])
        COP = np.array(results['COP'])
        return t_cycle, Qflow, COP  


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
        # confirm the setting of both, stat and dyn
        self.__initResult()

        error_count = 0
        max_deviation = 0.4
        for i in range(len(self.stat_data)):
            """ if the setting is correct, add to the results list """
            if self.temp_valid(i): 
                self.stat_COP.append(self.stat_data['COP'][i])
                self.dyn_COP.append(self.dyn_data['COP'][i])
                self.stat_Qflow.append(self.stat_data['Q_flow_cool_avg'][i]) 
                self.dyn_Qflow.append(self.dyn_data['Q_flow_cool_avg'][i])

                """ if the results are deviate a lot, record in the log file to check """
                if abs(self.stat_data['COP'][i] - self.dyn_data['COP'][i])/self.dyn_data['COP'][i] > max_deviation:
                    msg = '{},{},{},{}, {},{},{},{}'.\
                        format(i, self.stat_data['T_heat'][i], self.stat_data['T_cool'][i], self.stat_data['T_chill'][i], \
                                self.stat_data['COP'][i], self.stat_data['Q_flow_cool_avg'][i], self.dyn_data['COP'][i], self.dyn_data['Q_flow_cool_avg'][i] )
                    lgo.log_excel_msg(msg)
                    error_count += 1

        print("num_error =  ", error_count, "  error_rate = ", error_count/len(self.stat_data))
        print('data point = ', len(self.stat_COP))
        print("Average relative error of all points  = ",self.All_ARE())

        self.show_graph_multiple()
        return 0


    def show_graph_multiple(self):
        # COP figure
        plt.figure()
        plt.title('COP')
        plt.scatter(self.dyn_COP,self.stat_COP,color='b', s=0.6)

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
        plt.scatter(self.dyn_Qflow,self.stat_Qflow,color='b',s=0.6)

        #plt.plot([0,2500],[0,2250], color='r')
        #plt.plot([0,2500],[0,2750],color='r')
        plt.plot([0,2500],[0,2500],color='r',lw=3)
        #plt.xlim(-500,max(dyn_data['Q_flow_cool_avg'])+100)
        #plt.ylim(-500,max(stat_data['Q_flow_cool_avg'])+100)
        plt.xlabel('Qflow_dyn',fontsize=15)
        plt.ylabel('Qflow_SteadyState',fontsize=15)
        plt.show()  

def main():
    VL = Validater()
    VL.validate_data()


if __name__ == '__main__':
    main()


