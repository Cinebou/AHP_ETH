# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 13:13:11 2020

@author: gibelhaus
"""
import numpy as np
import matplotlib.pyplot as plt

import adsEqui_refprop as adsEqui

from fluidProp import VLEFluid

wp=adsEqui.workingpair('Silicagel123_water')

fluidProp = VLEFluid('water')

# A=np.linspace(17e3,194e4,100)
# wp.set_adsPot(A)
#plt.plot(wp.A,wp.W)

import scipy.constants as const

def plot_isotherm(T,T_for_p):
    p_s = fluidProp.calc_VLE_T(T + 273.15).p_v
    p=np.linspace(1,p_s,1000)
    x = [0]*len(p)
    for i in range(len(p)):
        wp.set_pT(p[i],T + 273.15)
        x[i] = wp.x * 2.236    
    plt.plot(p/p_s,x,label='T = {}  ℃'.format(T))  # x_axis: p/p0,   y_axis: kg/
    
    p_sat = fluidProp.calc_VLE_T(T_for_p + 273.15).p_v
    wp.set_pT(p_sat, T + 273.15)
    #plt.scatter(p_sat/p_s, wp.x * 2.236, s  =30)
    plt.legend(fontsize=12)
    plt.xlabel('$p / p_{o}$', fontsize = 18)
    plt.ylabel('$M [kg_{water} / bed]$', fontsize=18)
    
    
    return wp.x * 2.236

fig=plt.figure()
max903010 = plot_isotherm(30, 10)
max852718 = plot_isotherm(90, 30)
"""
min903010 = plot_isotherm(90, 30)
min852718 = plot_isotherm(85, 27)
print('diff 903010:  ',max903010-min903010)
print('diff 852718:  ',max852718-min852718)
"""
plt.xticks(fontsize = 11)
plt.yticks(fontsize = 11)
plt.savefig('isotherm_silica.eps')
plt.show()


