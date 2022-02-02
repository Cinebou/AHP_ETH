from pylab import *
import Fluid_RP10_2 as fl
from fluidProp import VLEFluid
import numpy as np
import SteadyStateAKM
param = {'m_flow_evp':0.191,
         'm_flow_cond':0.111,
         'm_flow_ads':0.166,
         'm_flow_des':0.163,
         'alphaA_evp_o':176,
         'alphaA_cond_o':3174,
         'alphaA_ads_o':331,
         'alphaA_evp_i':1000,
         'alphaA_cond_i':1575,
         'alphaA_ads_i':3000,
         'D_eff':1.8e-10,
         'm_sor':2.236,
         'r_particle':0.00045,
         'm_HX':4.211,
         'm_fl':0.94,
         'T_evp_in':291.15,
         'T_cond_in':300.15,
         'T_ads_in':300.15,
         'T_des_in':358.15,
         't_cycle':1000}

AKM = SteadyStateAKM.adsorptionChiller_steadyState(**param)
AKM.fluidProp = VLEFluid('water')

x = 0.2
T = 300
h_ads = AKM.wp.calc_h_ads_xT(x,T)
#print("h_ads  : ",h_ads)

num_point = 100
X = np.linspace(0.01,0.3,num_point)
h = np.zeros(len(X))
h_l = np.zeros(len(X))
h_v = np.zeros(len(X))
d_h = np.zeros(len(X))
for i in range(len(X)):
    h[i] = AKM.wp.calc_h_ads_xT(X[i], T)
    h_v[i] = AKM.fluidProp.calc_VLE_T(T).h_v
    h_l[i] = AKM.fluidProp.calc_VLE_liquid_T(T).h_l
    d_h[i] = h_v[i] - h[i]
    if i > 0:
        if h[i] > 0 and h[i-1] < 0:
            print(" X =~ 0 : x = ",X[i])
plt.figure()
plt.plot(X, h, label = "enthalpy of adsorbed water")
plt.plot(X, h_v - h_l, label = "enthalpy of vapor - liquid")
plt.plot(X,h_v - h,label = "delta heat of adsorption")
plt.legend()
plt.show()
