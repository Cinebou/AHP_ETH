# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 14:52:58 2020

@author: gibelhaus
"""
import numpy as np
from scipy import optimize
import adsEqui_refprop as adsEqui
from fluidProp import VLEFluid
import math


class adsorptionChiller_steadyState:
    """Steady state adsorption chiller model
    
    Class describing a steady state two-bed adsorption chiller
    """
    
    def __init__(self,m_flow_evp=None,m_flow_cond=None,m_flow_ads=None,m_flow_des=None,
                 cp_W = 4184,cp_sor = 1000,cp_HX = 379,
                 alphaA_evp_o=None,alphaA_cond_o=None,alphaA_ads_o=None,D_eff=None,
                 alphaA_evp_i=None,alphaA_cond_i=None,alphaA_ads_i=None,
                 m_sor=None,r_particle=None,m_HX=None,m_fl=None,
                 T_evp_in=None,T_cond_in=None,T_ads_in=None,T_des_in=None,t_cycle=None,
                 corr_sor_c=1,corr_sor_t=0, corr_HX_c=1,corr_HX_t=0):
        """Constructor
        Instantiate the adsorption chiller
        """
        #Mass flows of the heat transfer circuits
        self.m_flow_evp = m_flow_evp
        self.m_flow_cond = m_flow_cond
        self.m_flow_ads = m_flow_ads
        self.m_flow_des = m_flow_des
        
        #Specific heat capacities
        self.cp_W = cp_W
        self.cp_sor = cp_sor
        self.cp_HX = cp_HX
        
        #Heat and mass transfer coefficients
        self.alphaA_evp_o = alphaA_evp_o
        self.alphaA_cond_o = alphaA_cond_o
        self.alphaA_ads_o = alphaA_ads_o
        self.D_eff = D_eff
        self.alphaA_evp_i = alphaA_evp_i
        self.alphaA_cond_i = alphaA_cond_i
        self.alphaA_ads_i = alphaA_ads_i
        
        #Adsorpber geometry
        self.m_sor = m_sor
        self.r_particle = r_particle
        self.m_HX = m_HX
        
        #Define working pair and fluid
        self.wp = adsEqui.workingpair('Silicagel123_water')
        self.fluidProp = VLEFluid('water')
        
        #Operating parameters
        self.T_evp_in = T_evp_in
        self.T_cond_in = T_cond_in
        self.T_ads_in = T_ads_in
        self.T_des_in = T_des_in
        self.t_cycle = t_cycle
        
        #Set correction facotrs for simulated mass flows
        self.corr_sor_c = corr_sor_c
        self.corr_sor_t = corr_sor_t
        self.corr_HX_c = corr_HX_c
        self.corr_HX_t = corr_HX_t

        # optimizer recorder, which is used for blocking value returned when it's NAN value
        initial_block_value = 10000
        self.F_values = [initial_block_value]*6
        
        self.__internalParameters()
        

    def __internalParameters(self):
        """Calculates internal parameters
        """
        #Set correction facotrs for simulated mass flows
        self.corr_sor = self.corr_sor_c + self.corr_sor_t * (self.t_cycle)**0.5
        self.corr_HX = self.corr_HX_c + self.corr_HX_t * (self.t_cycle)**0.5

        self.mcp_evp = self.m_flow_evp*self.cp_W
        self.mcp_cond = self.m_flow_cond*self.cp_W
        self.mcp_ads = self.m_flow_ads*self.cp_W
        self.mcp_des = self.m_flow_des*self.cp_W
        
        self.kA_evp = 1/(1/self.alphaA_evp_o + 1/self.alphaA_evp_i)
        self.kA_cond = 1/(1/self.alphaA_cond_o + 1/self.alphaA_cond_i)
        self.kA_ads = 1/(1/self.alphaA_ads_o + 1/self.alphaA_ads_i)
        
        self.beta_LDF = 15*self.D_eff/(self.r_particle**2) * self.m_sor # kg/s
        
        self.NTU_evp = self.kA_evp/self.mcp_evp
        self.NTU_cond = self.kA_cond/self.mcp_cond
        self.NTU_ads = self.kA_ads/self.mcp_ads
        self.NTU_des = self.kA_ads/self.mcp_des

        self.m_flow_sor = self.m_sor/self.t_cycle*2*self.corr_sor
        self.m_flow_HX = self.m_HX/self.t_cycle*2*self.corr_HX
        
        self.mcp_sor = self.m_flow_sor*self.cp_sor
        self.mcp_HX = self.m_flow_HX*self.cp_HX
        

    def __EqSystem(self,var):
        """Define the equation system, all unit is W (J/s)
        """
        self.variables_set(var)
        F = np.empty((6))           
        F[0] = self.energy_evp()
        F[1] = self.energy_cond()
        F[2] = self.energy_ads()
        F[3] = self.energy_des()
        F[4] = self.mass_in_bed()
        F[5] = self.two_mv_speed()
        return F

    """
    """
    def variables_set(self, var):
        self.T_evp=var[0]
        self.T_cond=var[1]
        self.T_ads=var[2]
        self.T_des=var[3]
        self.X_ads=var[4]
        self.X_des=var[5]
        return 0


    """ circulation speed of working fluids between evaporator and adsorber, kg/s
    """
    def mv_ads(self):
        p_evp = self.fluidProp.calc_VLE_T(self.T_evp).p_v
        X_ads_eq = self.wp.calc_x_pT(p_evp,self.T_ads)
        mv = self.beta_LDF * (X_ads_eq - self.X_ads)
        return mv


    """ circulation speed of working fluids between desorber and condenser, kg/s
    """
    def mv_des(self):
        p_cond = self.fluidProp.calc_VLE_T(self.T_cond).p_v
        X_des_eq = self.wp.calc_x_pT(p_cond, self.T_des)
        mv = self.beta_LDF * (self.X_des - X_des_eq)
        return mv


    """ the energy taken by heat trasfer fluids from each component
    """
    def HTF_energy(self, component):
        if component == 'evp':
            T_in  = self.T_evp_in
            T_out = self.T_evp
            mcp   = self.mcp_evp
            NTU   = self.NTU_evp

        if component == 'ads':
            T_in  = self.T_ads_in
            T_out = self.T_ads
            mcp   = self.mcp_ads
            NTU   = self.NTU_ads

        if component == 'des':
            T_in  = self.T_des_in
            T_out = self.T_des
            mcp   = self.mcp_des
            NTU   = self.NTU_des

        if component == 'cond':
            T_in  = self.T_cond_in
            T_out = self.T_cond
            mcp   = self.mcp_cond
            NTU   = self.NTU_cond

        heatHTF = mcp * (T_in - T_out) * (1 - np.exp(-NTU))
        return heatHTF


    """ inner heat exchange cycle """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Be careful for the direction of the current, (des - ads)
        Adsorber : positive + 
        Desorber : negative -"""

    """ heat exchange of sorbent mass between adsorber and desorber """
    def HX_sor(self):
        heatX = self.mcp_sor*(self.T_des-self.T_ads) 
        return heatX

    """ heat exchange of heat transfer fluids between adsorber and desorber """
    def HX_fluids(self):
        h_des = self.wp.calc_h_ads_xT(self.X_des,self.T_des)
        h_ads = self.wp.calc_h_ads_xT(self.X_ads,self.T_ads)
        heatX = self.m_flow_sor * (self.X_des*h_des - self.X_ads*h_ads) 
        return heatX

    """ heat exchange of heat exchanger(container) between adsorber and desorber """
    def HX_heatExchanger(self):
        T_HX_des = self.T_des + self.mcp_des/self.alphaA_ads_o*(self.T_des_in-self.T_des)*(1-np.exp(-self.NTU_des))
        T_HX_ads = self.T_ads + self.mcp_ads/self.alphaA_ads_o*(self.T_ads_in-self.T_ads)*(1-np.exp(-self.NTU_ads))
        heatX = self.mcp_HX*(T_HX_des - T_HX_ads)
        return heatX

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


    """ 6 balance equations. If the value becomes NAN, return unfeasible high value.
    """
    """ F[0] """
    def energy_evp(self):
        # enthalpy of in and out
        h_in = self.fluidProp.calc_VLE_liquid_T(self.T_cond).h_l
        h_out = self.fluidProp.calc_VLE_T(self.T_evp).h_v

        # energy balance 
        eq = self.HTF_energy('evp') + self.mv_ads() * (h_in - h_out)
        f0 = self.nan_block(0,eq)
        return f0


    """ F[1] """
    def energy_cond(self):
        # enthalpy of in and out
        p_des = self.wp.calc_p_xT(self.X_des,self.T_des)
        h_in = self.fluidProp.calc_fluidProp_pT(p_des,self.T_des).h
        h_out = self.fluidProp.calc_VLE_liquid_T(self.T_cond).h_l

        # energy balance 
        eq = self.HTF_energy('cond') + self.mv_des() * (h_in - h_out)
        f1 = self.nan_block(1,eq)
        return f1


    """ F[2] """
    def energy_ads(self):
        #enthalpy from evaporator
        h_in = self.fluidProp.calc_VLE_T(self.T_evp).h_v

        # energy balance 
        eq = self.HTF_energy('ads') + self.mv_ads()*h_in + self.HX_sor() + self.HX_fluids() + self.HX_heatExchanger()
        f2 = self.nan_block(2,eq)
        return f2


    """ F[3] """
    def energy_des(self):
        # enthalpy to desorber
        h_out = self.fluidProp.calc_fluidProp_pT(self.wp.calc_p_xT(self.X_des,self.T_des),self.T_des).h

        # energy balance 
        eq = self.HTF_energy('des') - self.mv_des()*h_out - self.HX_sor() - self.HX_fluids() - self.HX_heatExchanger()
        f3 = self.nan_block(3,eq)
        return f3

    
    """ F[4] """
    def mass_in_bed(self):
        # mass balance
        eq = self.mv_des() + self.m_flow_sor * (self.X_des - self.X_ads)
        f4 = self.nan_block(4,eq)
        return f4


    """ F[5] """
    def two_mv_speed(self):
        eq = self.mv_ads() - self.mv_des()
        f5 = self.nan_block(5,eq)
        return f5


    """ if eq_value is NAN, return high value so that it's blocked.
        if not, save the value and return the original value.
    """
    def nan_block(self,eq_number,eq_value):
        if math.isnan(eq_value):
            return self.F_values[eq_number] * 5
        else:
            self.F_values[eq_number] = eq_value
            return eq_value


    """ Solver of the optimization and decide the anser of the variables
    """
    def solve(self,var_guess):
        self.__internalParameters()
        var = optimize.root(self.__EqSystem,var_guess)
        self.T_evp, self.T_cond, self.T_ads, self.T_des, self.X_ads, self.X_des = var.x
        self.__calcHeatFlows()
        return var
            

    """ summarize the results
    """
    def __calcHeatFlows(self):
        self.T_evp_out = self.T_evp + (self.T_evp_in - self.T_evp)*np.exp(-self.NTU_evp)
        self.T_cond_out = self.T_cond + (self.T_cond_in - self.T_cond)*np.exp(-self.NTU_cond)
        self.T_ads_out = self.T_ads + (self.T_ads_in - self.T_ads)*np.exp(-self.NTU_ads)
        self.T_des_out = self.T_des + (self.T_des_in - self.T_des)*np.exp(-self.NTU_des)
        
        self.Q_flow_evp = self.mcp_evp*(self.T_evp_in - self.T_evp_out)
        self.Q_flow_cond = self.mcp_cond*(self.T_cond_in - self.T_cond_out)
        self.Q_flow_ads = self.mcp_ads*(self.T_ads_in - self.T_ads_out)
        self.Q_flow_des = self.mcp_des*(self.T_des_in - self.T_des_out)
        
        self.COP = self.Q_flow_evp/self.Q_flow_des
        self.SCP = self.Q_flow_evp/self.m_sor
    