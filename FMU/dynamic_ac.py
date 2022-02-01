import numpy as np
from run_fmu import Sim 
import pickle
import matplotlib.pyplot as plt
import csv
from time import time



def main():
    global T_chill_min, T_chill_max, T_reject_min, T_reject_max, T_heat_min, T_heat_max
    global cycle_time_list

    time_st = time()
    # setting of the temperature triple, it should be 'int', by 2℃
    
    T_chill_min , T_chill_max  = 10, 20
    T_reject_min, T_reject_max = 13,13
    T_heat_min  , T_heat_max   = 60, 90
    """
    T_chill_min , T_chill_max  = 10, 20
    T_reject_min, T_reject_max = 24, 40
    T_heat_min  , T_heat_max   = 60, 90
    
    T_chill_min , T_chill_max  = 10,10
    T_reject_min, T_reject_max = 30,30
    T_heat_min  , T_heat_max   = 90,90
    
    T_chill_min , T_chill_max  = 18,18
    T_reject_min, T_reject_max = 27,27
    T_heat_min  , T_heat_max   = 85,90
    """

    #setting of the cycle time 
    cycle_time_list = [500,600,700,800,900,1000,1100,1150,1200,1250,1300,1400] # 12 point
    #restarting point, default = 0 ( when simulation stops in the middle, you can restart from there)
    restart = 0
    # set temp and time setting
    d_point = set_params(restart)

    # fmu file of dynamic simulation
    fmu_file = './FMU/Silica123_water.fmu'
    # how many cycle you simulate, define the simulating time length
    rap = 40

    # run the fmu file in each settings
    Simulator = Sim(fmu_file, rap)
    results_dyn = np.array([Sim.simulate_fmu(Simulator,point) for point in d_point])
    
    time_fin=time()
    print('calculation time : ', time_fin-time_st)
    print('calculation time for one case  : ', (time_fin-time_st)/len(results_dyn))
    show_map(results_dyn)

    #save the data as a total
    with open('./Results/dyn_data_Silica123_water_.pickle', 'wb') as f:
        pickle.dump(results_dyn, f, pickle.HIGHEST_PROTOCOL)
    return 0


def set_params(restart_point):
    # data range of each params, including the end point, by 2 ℃
    chill_range  = np.arange(T_chill_min , T_chill_max+1 , 2)
    reject_range = np.arange(T_reject_min, T_reject_max+1, 2)
    heat_range   = np.arange(T_heat_min  , T_heat_max+1  , 2)
    time_range   = np.array(cycle_time_list)

    # arrange in the 'params'
    params = [[i, j , k, l] for l in time_range  for k in heat_range  for j in reject_range  for i in chill_range]
    Sim_list=feasible_region(params)
    SortedSim = sorted(Sim_list, key=lambda x:(x[0], x[2],x[1]))
    
    # store the calc points in .csv
    #pd.Series(SortedSim).to_csv('calc_points.csv')
    with open('calc_points.csv', mode='w',newline="") as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerows(SortedSim)

    # restart from 
    SortedSim = SortedSim[restart_point:]
    return SortedSim


# excluding the unfeasible data set
def feasible_region(params):
    sim_list=[]
    for param in params:
        chill=param[0]; reject=param[1]; heat=param[2]
        """Mahbubul Muttakin, Sourav Mitra et al. International Journal of Heat and Mass Transfer, 122, 7 2018, Fig 8"""
        # the feasible region of heating temp and rejecting temp
        if (heat > 2.4928*reject - 13.768):
            if chill<reject<heat: 
                sim_list.append(param)

    return sim_list


def show_map(results):
    COPs = results[:,4]
    Qflows=results[:,5]
    plt.figure()
    plt.scatter(COPs,Qflows)
    plt.show()

if __name__ == "__main__":
    main()