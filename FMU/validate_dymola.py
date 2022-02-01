import pickle
import pandas as pd
import matplotlib.pyplot as plt


def main():
    results_dyn_Hibiki = './Results/dyn_data.pickle'
    t_cycle,T_chill, T_reject, T_heat, COP, Qflow = read_pickle(results_dyn_Hibiki)
    C=[]; S=[]
    for i in range(len(t_cycle)):
        if 80<=T_heat[i]-273.15 and T_heat[i]-273.15<=90 and 25<=T_reject[i]-273.15 and T_reject[i]-273.15<=30 and T_chill[i]-273.15==10 and 400<=t_cycle[i] and t_cycle[i]<=1600:
            C.append(COP[i])
            S.append(Qflow[i])
    print(C)
    plt.plot(C,S)
    plt.show()

    dyn_data=pd.read_csv('results_dyn_all.csv')
    
    #ndrej_graph(dyn_data)
    return 0


def Andrej_graph(data):
    COP_A=[]; SCP_A=[]
    for i in range(len(data)):
        Heat = data['T_heat'][i]-273.15; Cool = data['T_cool'][i]-273.15; Chill = data['T_chill'][i]-273.15
        Time = data['t_Cycle'][i]
        if 80<=Heat and Heat<=90 and 25<=Cool and Cool<=30 and Chill==10 and 400<=Time and Time<=1600:
            COP_A.append(data['COP'][i])
            SCP_A.append(data['Q_flow_cool_avg'][i] / 2 / 2.236)
        
    plt.figure()
    plt.scatter(COP_A, SCP_A)
    plt.show()
    return 0


def read_pickle(file):
        with open(file, 'rb') as f:
                results = pickle.load(f)
        # [self.t_Cycle, self.T_chill, self.T_reject, self.T_heat, self.COP, self.SP_sor]
        t_cycle = results[0]
        T_chill = results[1]
        T_reject = results[2]
        T_heat = results[3]
        COP = results[4]
        Qflow = results[5]
        return t_cycle,T_chill, T_reject, T_heat, Qflow, COP

if __name__ == '__main__':
    main()