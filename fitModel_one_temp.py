# -*- coding: utf-8 -*-
"""
Created on Tue 01 Feb

@author: Hibiki Kimura
"""

import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt
import time
import SteadyStateAKM
import log_output as lgo
from validation import Validater
from param_database import params
from pprint import pprint

# cycle time list is imported from 'generatePerformanceMap_steadyState'
from generatePerformanceMap_steadyState import cycle_time_list


class fitting:
    def __init__(self,cycle_time_list):
        self.vl = Validater()
        self.param_data = params()
        self.Qflow_chill_dyn_A = None
        self.Qflow_heat_dyn_A = None
        self.cycle_time_list = cycle_time_list
        self.__read()

    # read the dynamic simulation results
    def __read(self):
        t_cycle_dyn_A, self.Qflow_chill_dyn_A, self.COP_dyn_A = Validater.read_pickle('./PerformanceMap/SCP_COP/dyn_data_Silica123_water_903010.pickle')
        self.Qflow_heat_dyn_A = self.Qflow_chill_dyn_A/self.COP_dyn_A
    

    # set the parameters for fitting, and cycle time
    def params_set(self,param, corr, t_cycle):
        param_point = param.copy()
        param_point['alphaA_evp_o'] = corr[0]
        param_point['alphaA_evp_i'] = corr[0]
        param_point['alphaA_cond_o'] = corr[1]
        param_point['alphaA_cond_i'] = corr[1]
        param_point['alphaA_ads_o'] = corr[2]
        param_point['alphaA_ads_i'] = corr[2]

        param_point['D_eff'] = corr[3]
        param_point['corr_sor_c'] = corr[4]
        param_point['corr_HX_c'] = corr[5]
        param_point['corr_sor_t'] = corr[6]
        param_point['corr_HX_t'] = corr[7]
        
        param_point['t_cycle'] = t_cycle
        return param_point

    # set temperature for simulation
    def temp_set(self, param, Heat, Reject, Chill):
        param_point = param.copy()
        param_point['T_evp_in'] = Chill + 273.15
        param_point['T_ads_in'] = Reject + 273.15
        param_point['T_cond_in'] = Reject + 273.15
        param_point['T_des_in'] = Heat + 273.15
        return param_point


    # calculate short-cut model for two triples lines
    def performance(self,corr,cycle_time_list, logout = False):
        param = self.param_data.Silica123_water
        param_list = [self.params_set(param,corr,t_cycle_i) for t_cycle_i in cycle_time_list]

        # set temperature in 90, 30, 10
        param_A = [self.temp_set(p, 90, 30, 10) for p in param_list]
        AKM_A = [SteadyStateAKM.adsorptionChiller_steadyState(**param_i) for param_i in param_A]


        # initial guess
        var_guess = np.array([283.15,303.15,303.15,363.15,0.2,0.05])

        # solve
        [AKM_i.solve(var_guess) for AKM_i in AKM_A]

        # results
        Qflow_chill_A = np.array([AKM_i.Q_flow_evp for AKM_i in AKM_A])
        Qflow_heat_A  = np.array([AKM_i.Q_flow_des for AKM_i in AKM_A])

        # output parameters, defalut off
        if logout:
            for AKM_i in AKM_A:
                lgo.log_output_excel(AKM_i)

        return Qflow_chill_A, Qflow_heat_A


    # calculate difference between target dynamic simulation and short-cut simulation
    def lsq_perf(self, corr):
        Qflow_chill_stat_A, Qflow_heat_stat_A = self.performance(corr,self.cycle_time_list)
        QcoolA_error = abs(Qflow_chill_stat_A - self.Qflow_chill_dyn_A) / self.Qflow_chill_dyn_A
        QheatA_error = abs(Qflow_heat_stat_A  - self.Qflow_heat_dyn_A)  / self.Qflow_heat_dyn_A
        
        lsq_Qflows = np.concatenate((QcoolA_error,QheatA_error))
        return lsq_Qflows


    # summarize the results
    def show_fit_map(self, fitted_params):
        # calculate from fitted parameters
        Qflow_chill_stat_A, Qflow_heat_stat_A = self.performance(fitted_params,cycle_time_list)
        COP_stat_A=Qflow_chill_stat_A/Qflow_heat_stat_A

        # calculate the average relative error
        error = Validater.ARE_one_temp(self.COP_dyn_A, self.Qflow_chill_dyn_A, COP_stat_A, Qflow_chill_stat_A)
        print('total',error)

        # show the fitted performance map
        plt.figure()
        plt.plot(self.COP_dyn_A, self.Qflow_chill_dyn_A, 'bo',  label='dyn  $90^{\circ}C \quad 30^{\circ}C \quad 10^{\circ}C$')
        plt.plot(COP_stat_A,     Qflow_chill_stat_A,     'b-',  label='stat $90^{\circ}C \quad 30^{\circ}C \quad 10^{\circ}C$')

        plt.xlabel('COP',fontsize=15)
        plt.ylabel('$\dot{Q}_{cool}$  in  W',fontsize=15)
        plt.legend(fontsize = 12)
        plt.rcParams['figure.subplot.bottom'] = 0.15
        plt.rcParams['lines.linewidth'] = 3

        plt.savefig('Fig/fitting_silica_one_temp.eps')
        plt.show()


def main():
    time_st = time.time()
    fit = fitting(cycle_time_list)

    # initial guess for the fitting parameters
    corr0 = np.array([176, 3174, 151, 1.8e-10,  1, 1, 0.01, 0.01])
    
    # boundary for the fittings
    bounds = ([50,50,50,1e-11,0,0,0,0],[10000,10000,10000,1e-9,5,5,1,1])

    # conduct fitting
    res_perf = least_squares(fit.lsq_perf, corr0, bounds=bounds,  verbose=1)

    # fitting results
    fitted_params = res_perf.x

    # output the fitting parameter into the console
    print(fitted_params)

    time_end = time.time()  
    print("calculation time ::  ",time_end - time_st," sec")

    #fitted_params = [1.07899936e+02, 3.30200086e+03, 3.16025449e+02, 3.72926712e-10, 6.33222288e-01, 3.73305009e-01, 7.37539599e-04, 5.59730376e-02]
    fit.show_fit_map(fitted_params)


if __name__=='__main__':
    main()
