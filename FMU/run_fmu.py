from pyfmi import load_fmu
import matplotlib.pyplot as plt
import pandas as pd
from scipy import integrate
import csv

"""Simulation time is determined in the 'rap' in Sim"""

class Sim:
    def __init__(self, file_name, rap, t_Cycle = None, final_time=None, model = None, opts=None, COP=None, Qflow=None, dt = 0.25):
        self.file_name = file_name
        self.t_Cycle = t_Cycle
        self.rap = rap
        self.final_time = final_time
        self.model = model
        self.opts = opts
        self.dt = dt

        # sorbent mass for per one bed
        self.mass_sor = 2.236 

        #initialize the recording dataframe
        columns=["t_Cycle", "T_chill", "T_reject", "T_heat", "COP", "Qflows"]
        self.res_frame = pd.DataFrame(columns=columns,index=None)

        #initilizing recording file
        self.csvFile = "Results/saving"+self.file_name.replace(".fmu","").replace("./FMU/","")+".csv"
        self.res_frame.to_csv(self.csvFile, mode='w')

        # results
        self.COP = COP
        self.Qflow = Qflow


    def __loadFMU(self):
        self.model = load_fmu(self.file_name)

        # define the tolarance of simulation
        self.opts = self.model.simulate_options()
        

    # set tolarance and time(dt)
    def __set_options(self):
        self.opts["CVode_options"]["atol"] = 1e-6
        #self.opts["CVode_options"]["store_event_points"] = False
        #self.opts['ncp'] = int(self.t_Cycle / self.dt)


    # run the simulation
    def simulate_fmu(self, point):
        # initialize the model
        self.__loadFMU()
        self.model.initialize()

        #assemble settings in the fmu file
        self.set_in_fmu(point)
        self.__set_options()
        print('T Heat: ',point[2],'  T reject: ',point[1], '  T chill: ',point[0],'  t_cycle: ',point[3])

        # run the fmu file
        self.res = self.model.simulate(final_time=self.final_time, options = self.opts)
        result = self.proc()
        return result

    # set simulation parameters, it can be changed in DYMOLA
    def set_in_fmu(self,point):
        # import data settings
        self.T_chill  = point[0] + 273.15
        self.T_reject = point[1] + 273.15
        self.T_heat   = point[2] + 273.15
        self.t_Cycle  = point[3]
        self.final_time = self.t_Cycle * self.rap
        
        #set in fmu configuration
        self.model.set('period_bed1',   self.t_Cycle)
        self.model.set('period_bed2',   self.t_Cycle)
        self.model.set('T_evp_in',      self.T_chill)
        self.model.set('T_cond_in',     self.T_reject)
        self.model.set('T_ads_in__T_des_in', self.T_reject - self.T_heat)
        self.model.set('T_des_in',      self.T_heat)
        self.model.set('T_des_in__T_ads_in', self.T_heat - self.T_reject)
        self.model.set('T_ads_in',      self.T_reject)


    # data processing
    def proc(self):
        # get the results of the simulation
        self.t = self.res['time']
        self.COP_series = self.res['adsorptionChiller.summary.COP']
        self.SP_sor_series = self.res['adsorptionChiller.summary.SP_sor']
        self.calc_Q_avg()
        #self.calc_flow()
        """
        self.show_COP()
        self.show_Qflow()
        """
        summary = [self.t_Cycle, self.T_chill, self.T_reject, self.T_heat, self.COP, self.Qflow]

        #save data temporaliry
        self.save_data(summary)
        return summary


    # add data to saving*.csv
    def save_data(self, resdata):
        with open(self.csvFile, mode='a',newline="") as f:
            writer = csv.writer(f)
            writer.writerow(resdata)
        return 0

    
    # calculate from defined function, the list returns the time sequence, [-1] is the final time
    def calc_Q_avg(self):
        self.Qflow = self.SP_sor_series[-1] * self.mass_sor * 2
        self.COP   = self.COP_series[-1]
        return 0


    # time vs. COP graph
    def show_COP(self):
        plt.figure()
        plt.plot(self.t,self.COP_series)
        plt.show()


    # time vs. Q flows graph
    def show_Qflow(self):
        Q_evp = self.res['adsorptionChiller.summary.evaporator.Q_flow_wallTVLE']
        Q_ads1 = self.res['adsorptionChiller.summary.adsorberBedOne.Q_flow_wallTwpair']
        Q_ads2 = self.res['adsorptionChiller.summary.adsorberBedTwo.Q_flow_wallTwpair']
        plt.figure()
        plt.plot(self.t,Q_evp)
        plt.plot(self.t,Q_ads1)
        plt.plot(self.t,Q_ads2)
        plt.show()


    # calculate Q_flow from only last rap, it might not work
    def calc_flow(self):
        Q_evp = self.res['adsorptionChiller.summary.evaporator.DH_liquid']
        Q_ads1 = self.res['adsorptionChiller.summary.Q_flow_ads1_input']

        """ take out the final rap data """
        last_rap_start_time = self.final_time - self.t_Cycle/2
        Q_in = []; Q_out = []; last_t = []
        for i in range(len(self.t)):
            if self.t[i] > last_rap_start_time:
                last_t.append(self.t[i])
                Q_out.append(Q_evp[i])
                Q_in.append(Q_ads1[i])
        
        """ take integral over time """
        Tot_Q_out = integrate.cumtrapz(Q_out, last_t, initial = 0)[-1]
        Tot_Q_in  = integrate.cumtrapz(Q_in,  last_t, initial = 0)[-1]
        
        """ calculate capacities """
        self.Qflow = Tot_Q_out / (self.t_Cycle/2)
        self.Qheat = Tot_Q_in / (self.t_Cycle/2)
        self.COP = self.Qflow / self.Qheat

        print('COP : ', self.COP, '\nQflow : ',self.Qflow)

        return 0