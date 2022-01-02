# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 14:52:58 2020

@author: gibelhaus
"""
from Balance_Equation import Balance_equation
import numpy as np
from scipy import optimize
import adsEqui_refprop as adsEqui
from fluidProp import VLEFluid


class adsorptionChiller_steadyState:
    """Steady state adsorption chiller model
    
    Class describing a steady state two-bed adsorption chiller
    """
    
    def __init__(self,m_flow_evp=None,m_flow_cond=None,m_flow_ads=None,m_flow_des=None,
                 cp_W = 4184,c_sor = 1000,cp_HX = 379,
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
        self.c_sor = c_sor
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
        
        self.mcp_sor = self.m_flow_sor*self.c_sor
        self.mcp_HX = self.m_flow_HX*self.cp_HX
        

    def __EqSystem(self,var):
        """Define the equation system, all unit is W (J/s)
        """
        BEQ = Balance_equation(self,var)
        F = np.empty((6))           
        F[0] = BEQ.energy_evp()
        F[1] = BEQ.energy_cond()
        F[2] = BEQ.energy_ads()
        F[3] = BEQ.energy_des()
        F[4] = BEQ.mass_in_bed()
        F[5] = BEQ.two_mv_speed()
        return F


    def solve(self,var_guess):
        self.__internalParameters()
        var = optimize.root(self.__EqSystem,var_guess)
        self.T_evp, self.T_cond, self.T_ads, self.T_des, self.X_ads, self.X_des = var.x
        self.__calcHeatFlows()
        return var
            

    # summarize the results
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
        #lgo.log_output_eq(self)

    