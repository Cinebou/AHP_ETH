import numpy as np
import matplotlib.pyplot as plt
from adsEqui_refprop import workingpair
from fluidProp import VLEFluid
wp=workingpair('AqsoaZ02_water')
fluidProp = VLEFluid('water')


num_point = 1000
A = np.linspace(0,2500000,num_point)
W = np.zeros(len(A))
for i in range(len(A)):
    W[i] = wp.calc_poreVol(A[i])
fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(A/1000, W*1000)

W_inv = np.linspace(np.min(W),np.max(W),len(A))
A_inv = np.zeros(len(W_inv))
for i in range(len(W_inv)):
    A_inv[i] = wp.calc_adsPot(W_inv[i])
plt.plot(A_inv/1000, W_inv*1000, label = "adsPot")
plt.xlabel('A $[ J / g_{adsorbate} ]$', fontsize=18)
plt.ylabel('W $[ cm^3 / g_{adsorbent} ]$', fontsize=18)
ax.set_ylim(0,0.45)
ax.set_xlim(0,2250)
ax.grid(which = "minor", axis = "x", color = "black",alpha = 0.8, linestyle = "--", linewidth = 0.5)
ax.grid(which = "minor", axis = "y", color = "black",alpha = 0.8,linestyle = "--", linewidth = 0.5)
plt.xticks(fontsize = 11)
plt.yticks(fontsize = 11)

plt.savefig('Ads_pot_aqsoa.eps')
plt.show()