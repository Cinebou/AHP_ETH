# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 14:04:47 2021

@author: droskosch
"""

from pylab import *
import Fluid_RP10_2 as fl
from fluidProp import VLEFluid

"""
    Gr: List containing two strings of symbols of the state that shall be inserted, e.g., ["T","s"] -> Input: temperature and spec. entropy
    In: List of values of the state variables defined in Gr
    Out: List containing strings of symbols of the state variables that shall be computed, e.g., ["T","lam"] -> Output: temperature and heat conductivity
    Name: String of the fluid name as defined in the list below
    Eh: String concerning the uni system
    
    Supported input combinations of Gr
         ["T","p"]  temperature, pressure   
         ["T","x"]  temperature, steam quality
         ["T","v"]  temperature, spec. volume
         ["p","v"]  pressure, spec. volume
         ["p","x"]  pressure, steam quality
         ["p","h"]  pressure, spec. enthalpy
         ["p","s"]  pressure, spec. entropy
    
    Supported outputs (Out) 
        T    temperature                        
        p    pressure                             
        v    spec. volume                        
        u    spec. internal energy                
        h    spec. enthalpy                      
        s    spec. entrop                         
        q    steam quality                       
        dvis dynamic viscosity                   
        kvis kinematic viscosity                   
        lam  heat conductivity                     
        Pr   Prandtl-number
        cp0  isobaric ideal gas heat capacity     
        cp   isobaric heat capacity                
        M    molar mass                            
        
    Units for in- and output, defined by Eh
    
       Eh= "default"  "CBar"   "CKPa"   "mol"
                      ¦        ¦        ¦
        T     K        C        C        K
        p     Pa       bar      kPa      Pa
        v     m3/kg    m3/kg    m3/kg    m3/mol
        u     J/kg     kJ/kg    kJ/kg    J/mol
        h     J/kg     kJ/kg    kJ/kg    J/mol
        s     J/kg/K   kJ/kg/K  kJ/kg/K  J/mol/K
        q     kg/kg    kg/kg    kg/kg    mol/mol
        dvis  Pa s     Pa s     Pa s     Pa s
        kvis  m2/s     m2/s     m2/s     m2/s
        lam   W/m/K    kW/m/K   kW/m/K   W/m/K
        Pr   
        cp0   J/kg/K   kJ/kg/K  kJ/kg/K  J/mol/K
        cp    J/kg/K   kJ/kg/K  kJ/kg/K  J/mol/K
        M     kg/mol   kg/mol   kg/mol   kg/mol
    
    """


### Fluidnamen herausfinden
#print(fl.getNames())
### Dampfdruck von Wasser bei T=150°C in kPa

T=300.
q=1 #steam quality
fluid="water"

z=fl.zs(["T","q"],[T,q],["T",'p','v','u','h','s','BETA','q'],fluid,Eh="default")
print(z)

q=0 #liquid quality
z=fl.zs(["T","q"],[T,q],["T",'p','v','u','h','s','BETA','q'],fluid,Eh="default")
print(z)

import numpy as np
import matplotlib.pyplot as plt
import pickle

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

T =300
eg_fluid = AKM.fluidProp.calc_VLE_T(T)
eg_fluid_l = AKM.fluidProp.calc_VLE_liquid_T(T)
print(
    ' h_v :  ',eg_fluid.h_v,'\n',
    'p_v :  ',eg_fluid.p_v,'\n',
    'd_l :  ',eg_fluid_l.d_l,'\n',
    'arfa :  ',eg_fluid.arfa)


p = 100000
p_fluid = AKM.fluidProp.calc_VLE_p(p)
print( 'h_v  : ', p_fluid.h_v)

p = 1000
T = 300
pT_fluid = AKM.fluidProp.calc_fluidProp_pT(p,T)
print( ' h: ',pT_fluid.h)

