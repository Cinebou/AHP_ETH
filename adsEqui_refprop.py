# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 12:57:57 2020

@author: gibelhaus
"""
import numpy as np
import scipy.constants as const
from scipy import optimize

from workingpair_database import wp_db
from fluidProp import VLEFluid

class workingpair:
    """Working pair

    Class containing the states of the working pair and 
    corresponding functions
    """

    def __init__(self, name):
        """Constructor

        Instantiate the working pair

        name: String defining name of the working pair
        """

        self.wp_type = wp_db[name]
        self.fluidProp = VLEFluid("water")
        self.VLE_T = None
        self.W = None
        self.A = None
        self.x = None
        self.T = None
        self.p = None
        self.dh_bond = None
        self.h_ads = None
        self.u_ads = None
        self.dh_ads = None
        self.MolarW = self.fluidProp.get_molar_mass()  # kg/mol

    def set_adsPot(self, A):
        """Sets the adsorption potential

        A:       Array_like adsorption potential in J/kg
        """
        self.A = A
        self.W = self.calc_poreVol(A)

    def set_poreVol(self, W):
        """Sets the pore volume

        W:       Array_like pore volume in m^3/kg
        """
        self.W = W
        self.A = self.calc_adsPot(W)

    def calc_poreVol(self, A):
        """Calculates the pore volume

        A:       Array_like adsorption potential in J/kg

        returns: NumPy array   
        """
        W = self.charFunc(A)
        return W

    def calc_adsPot(self, W):
        """Calculates the adsorption potential

        W:       Array_like pore volume in m^3/kg

        returns: NumPy array   
        """
        A = self.charFunc(W, inverse=True)
        return A

    def charFunc(self, arg, inverse=False):
        """Characteristic function, the interaction between adsorption potential and loading volume

        arg:     Array_like function argument, one of A or W
        inverse: Boolean switching between classical and inverse form

        returns: NumPy array
        """
        if self.wp_type.func == 'arctan':
            c1, c2, c3, c4 = self.wp_type.coeff
            if not inverse:
                W = c1/np.pi * (np.arctan((arg-c2)/c3) + np.pi/2) + c4
                return W
            else:
                A = c3 * np.tan((arg-c4)*np.pi/c1 - np.pi/2) + c2
                return A
        else:
            pass

    def charFunc_der(self, arg, inverse=False):
        """Characteristic function

        arg:     Array_like function argument, one of A or W
        inverse: Boolean switching between classical and inverse form

        returns: NumPy array
        """
        if self.wp_type.func == 'arctan':
            c1, c2, c3, c4 = self.wp_type.coeff
            if not inverse:
                dWdA = c1 / (np.pi*c3 * (1 + (arg-c2)**2 / c3**2))
                return dWdA
            else:
                dAdW = c3*np.pi/c1 / (np.cos((arg-c4) * np.pi/c1 - np.pi/2))**2
                return dAdW
        else:
            pass

    def set_xT(self, x, T, unit_T='K'):
        """Sets loading and temperature

        x:      Array_like loading in kg/kg
        T:      Array_like temperature in K
        unit_T: String defining unit of temperature input 'K' or 'C'
        """
        self.x = x
        if unit_T == 'K':
            self.T = T
        elif unit_T == 'C':
            self.T = T + 273.15
        else:
            pass

        self.p = self.calc_p_xT(self.x, self.T)
        self.W = self.calc_W_xT(self.x, self.T)
        self.A = self.calc_adsPot(self.W)

        self.__set_fluidProp()

    def set_pT(self, p, T, unit_T='K'):
        """Sets pressure and temperature

        p:      Array_like pressure in Pa
        T:      Array_like temperature in K
        unit_T: String defining unit of temperature input 'K' or 'C'
        """
        self.p = p
        if unit_T == 'K':
            self.T = T
        elif unit_T == 'C':
            self.T = T + 273.15
        else:
            pass

        self.x = self.calc_x_pT(self.p, self.T)
        self.A = self.calc_A_pT(self.p, self.T)
        self.W = self.calc_poreVol(self.A)
        self.__set_fluidProp()

    def set_px(self, p, x):
        """Sets pressure and loading

        p:      Array_like pressure in Pa
        x:      Array_like loading in kg/kg
        """
        self.p = p
        self.x = x
        self.T = self.calc_T_px(self.p, self.x)
        self.A = self.calc_A_pT(self.p, self.T)
        self.W = self.calc_W_xT(self.x, self.T)

        self.__set_fluidProp()

    def __set_fluidProp(self):
        self.VLE_l_T = self.fluidProp.calc_VLE_liquid_T(self.T)
        self.dh_bond = self.calc_dh_bond(self.A, self.T, 'A')
        self.h_ads = self.VLE_l_T.h_l + self.dh_bond
        self.u_ads = self.h_ads - self.p/self.VLE_l_T.d_l
        #self.adsorptive.setState_pTxi(np.maximum(10,self.p), self.T)
        #self.dh_ads = self.adsorptive.h - self.h_ads

    def calc_W_xT(self, x, T, unit_T='K'):
        """Calculates the pore volume

        x:      Array_like loading in kg/kg
        T:      Array_like temperature in K
        unit_T: String defining unit of temperature input 'K' or 'C'

        returns: NumPy array   
        """
        if unit_T == 'K':
            T = T
        elif unit_T == 'C':
            T = T + 273.15
        else:
            pass

        VLE_l = self.fluidProp.calc_VLE_liquid_T(T)
        W = x/VLE_l.d_l
        return W

    def calc_A_pT(self, p, T, unit_T='K'):
        """Calculates the adsorption potential

        p:      Array_like pressure in Pa
        T:      Array_like temperature in K
        unit_T: String defining unit of temperature input 'K' or 'C'

        returns: NumPy array   
        """
        if unit_T == 'K':
            T = T
        elif unit_T == 'C':
            T = T + 273.15
        else:
            pass

        VLE = self.fluidProp.calc_VLE_T(T)
        A = - const.R/self.MolarW * T * np.log(p/VLE.p_v)
        return A

    def calc_p_xT(self, x, T, unit_T='K'):
        """Calculates the pressure

        x:      Array_like loading in kg/kg
        T:      Array_like temperature in K
        unit_T: String defining unit of temperature input 'K' or 'C'

        returns: NumPy array   
        """
        if unit_T == 'K':
            T = T
        elif unit_T == 'C':
            T = T + 273.15
        else:
            pass

        W = self.calc_W_xT(x, T)
        A = self.calc_adsPot(W)

        VLE = self.fluidProp.calc_VLE_T(T)
        p = VLE.p_v * np.exp(-A/(const.R/self.MolarW)/T)
        return p

    def calc_x_pT(self, p, T, unit_T='K'):
        """Calculates the loading

        p:      Array_like pressure in Pa
        T:      Array_like temperature in K
        unit_T: String defining unit of temperature input 'K' or 'C'

        returns: NumPy array   
        """
        if unit_T == 'K':
            T = T
        elif unit_T == 'C':
            T = T + 273.15
        else:
            pass

        A = self.calc_A_pT(p, T)
        W = self.calc_poreVol(A)

        VLE_l = self.fluidProp.calc_VLE_liquid_T(T)
        x = W * VLE_l.d_l
        return x

    def calc_T_px(self, p, x):
        """Calculates the temperature

        p:      Array_like pressure in Pa
        x:      Array_like loading in kg/kg

        returns: NumPy array   
        """
        p = p
        x = x

        def f(T):
            return self.calc_adsPot(self.calc_W_xT(x, T)) - \
                (const.R/self.MolarW)*T * \
                np.log(self.fluidProp.calc_VLE_T(T).p_v/p)

        if not np.isscalar(p):
            x0 = 320 * np.ones(p.size)
        elif not np.isscalar(x):
            x0 = 320 * np.ones(x.size)
        else:
            x0 = 320

        res = optimize.newton(f, x0)

        return res

    def calc_dh_bond(self, arg, T, A_W='A', unit_T='K'):
        """Calculates the specific bonding enthalpy

        arg:     Array_like function argument, one of A or W
        T:       Array_like temperature in K
        A_W:     String to define input, one of 'A' or 'W'
        unit_T: String defining unit of temperature input 'K' or 'C'

        returns: NumPy array
        """
        if unit_T == 'K':
            T = T
        elif unit_T == 'C':
            T = T + 273.15
        else:
            pass

        arfa = self.fluidProp.calc_VLE_liquid_T(T).arfa  # arfa = tharmal expansion
        
        if A_W == 'A':
            A = arg
            W = self.calc_poreVol(A)
            dh_bond =  - A + T*arfa*W / self.charFunc_der(A)
        elif A_W == 'W':
            W = arg
            A = self.calc_adsPot(W)
            dh_bond =  - A + T*arfa*W * self.charFunc_der(W, inverse=True)
        else:
            pass

        return dh_bond

    def calc_h_ads_xT(self, x, T, unit_T='K'):
        """Calculates the specific enthalpy of adsorbate

        x:      Array_like loading in kg/kg
        T:      Array_like temperature in K
        unit_T: String defining unit of temperature input 'K' or 'C'

        returns: NumPy array
        """
        if unit_T == 'K':
            T = T
        elif unit_T == 'C':
            T = T + 273.15
        else:
            pass

        W = self.calc_W_xT(x, T)
        A = self.calc_adsPot(W)
        dh_bond = self.calc_dh_bond(A,T)
        h_ads = self.fluidProp.calc_VLE_liquid_T(T).h_l + dh_bond

        #print("A : ",A," W : ",W)
        #print(  dh_bond , ",dh_bond, ", self.fluidProp.calc_VLE_liquid_T(T).h_l ,",self.fluidProp.calc_VLE_liquid_T(T).h_l, " ,h_ads, ",h_ads")

        return h_ads
