# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 14:52:58 2020

@author: gibelhaus
"""
import numpy as np
from scipy import optimize
import adsEqui_refprop as adsEqui

from fluidProp import VLEFluid
import log_output as lgo


class adsorptionChiller_steadyState:
    """Steady state adsorption chiller model
    
    Class describing a steady state two-bed adsorption chiller
    """
    
    def __init__(self,m_flow_evp=None,m_flow_cond=None,m_flow_ads=None,m_flow_des=None,
                 cp_W = 4180,c_sor = 1000,cp_HX = 920,
                 alphaA_evp_o=None,alphaA_cond_o=None,alphaA_ads_o=None,D_eff=None,
                 alphaA_evp_i=None,alphaA_cond_i=None,alphaA_ads_i=None,
                 m_sor=None,r_particle=None,m_HX=None,m_fl=None,
                 T_evp_in=None,T_cond_in=None,T_ads_in=None,T_des_in=None,t_cycle=None,
                 corr_sor_c=1,corr_sor_t=0, corr_HX_c=1,corr_HX_t=0,corr_fl=1):
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
        self.m_fl = m_fl
        
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
        self.corr_fl = corr_fl
        
        self.__internalParameters()
        
    def __internalParameters(self):
        """Calculates internal parameters
        """
        #Set correction facotrs for simulated mass flows
        self.corr_sor = self.corr_sor_c #+ self.corr_sor_t * (self.t_cycle)**0.5
        self.corr_HX = self.corr_HX_c #+ self.corr_HX_t * (self.t_cycle)**0.5

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

        """"""
        self.m_flow_sor = self.m_sor/self.t_cycle*2*self.corr_sor
        self.m_flow_HX = self.m_HX/self.t_cycle*2*self.corr_HX
        self.m_flow_fl = self.m_fl/self.t_cycle*2*self.corr_fl
        
        self.mcp_sor = self.m_flow_sor*self.c_sor
        self.mcp_HX = self.m_flow_HX*self.cp_HX
        self.mcp_fl = self.m_flow_fl*self.cp_W
        
    def __EqSystem(self,var):
        """Define the equation system
        """
        T_evp=var[0]
        T_cond=var[1]
        T_ads=var[2]
        T_des=var[3]
        X_ads=var[4]
        X_des=var[5]
        
        F = np.empty((6)) # all unit is W (J/s)

        # energy balance at evaporator
        F[0] = (self.mcp_evp*(self.T_evp_in-T_evp)*(1-np.exp(-self.NTU_evp))
                + self.beta_LDF*(self.wp.calc_x_pT(self.fluidProp.calc_VLE_T(T_evp).p_v,T_ads)-X_ads)
                *(self.fluidProp.calc_VLE_liquid_T(T_cond).h_l-self.fluidProp.calc_VLE_T(T_evp).h_v)) #+ lgo.log_TP(self,var,"F[0]")

        # energy balance at condeser
        F[1] = (self.mcp_cond*(self.T_cond_in-T_cond)*(1-np.exp(-self.NTU_cond)) 
                + self.beta_LDF*(X_des-self.wp.calc_x_pT(self.fluidProp.calc_VLE_T(T_cond).p_v,T_des))
                *(self.fluidProp.calc_fluidProp_pT(self.wp.calc_p_xT(X_des,T_des),T_des).h-self.fluidProp.calc_VLE_liquid_T(T_cond).h_l)) #+ lgo.log_TP(self,var,"F[1]")
        
        # energy balance at adsorber
        F[2] = (self.mcp_ads*(self.T_ads_in-T_ads)*(1-np.exp(-self.NTU_ads)) 
                + self.beta_LDF
                *(self.wp.calc_x_pT(self.fluidProp.calc_VLE_T(T_evp).p_v,T_ads)-X_ads)
                *self.fluidProp.calc_VLE_T(T_evp).h_v 
                + self.mcp_sor*(T_des-T_ads) 
                + self.m_flow_sor
                *(X_des*self.wp.calc_h_ads_xT(X_des,T_des)-X_ads*self.wp.calc_h_ads_xT(X_ads,T_ads)) 
                + self.mcp_HX*(T_des-T_ads + self.mcp_des/self.alphaA_ads_o*(self.T_des_in-T_des)*(1-np.exp(-self.NTU_des)) - self.mcp_ads/self.alphaA_ads_o*(self.T_ads_in-T_ads)*(1-np.exp(-self.NTU_ads)))
                + self.mcp_fl*(T_des-T_ads + 1/self.NTU_des*(self.T_des_in-T_des)*(1-np.exp(-self.NTU_des)) - 1/self.NTU_ads*(self.T_ads_in-T_ads)*(1-np.exp(-self.NTU_ads)))) #+ lgo.log_TP(self,var,"F[2]")
        
        # energy balance at desorber
        F[3] = (self.mcp_des*(self.T_des_in-T_des)*(1-np.exp(-self.NTU_des)) 
                - self.beta_LDF
                *(X_des-self.wp.calc_x_pT(self.fluidProp.calc_VLE_T(T_cond).p_v,T_des))
                *self.fluidProp.calc_fluidProp_pT(self.wp.calc_p_xT(X_des,T_des),T_des).h 
                + self.mcp_sor*(T_ads-T_des) 
                + self.m_flow_sor
                *(X_ads*self.wp.calc_h_ads_xT(X_ads,T_ads)-X_des*self.wp.calc_h_ads_xT(X_des,T_des))
                + self.mcp_HX*(T_ads-T_des + self.mcp_ads/self.alphaA_ads_o*(self.T_ads_in-T_ads)*(1-np.exp(-self.NTU_ads)) - self.mcp_des/self.alphaA_ads_o*(self.T_des_in-T_des)*(1-np.exp(-self.NTU_des))) 
                + self.mcp_fl*(T_ads-T_des + 1/self.NTU_ads*(self.T_ads_in-T_ads)*(1-np.exp(-self.NTU_ads)) - 1/self.NTU_des*(self.T_des_in-T_des)*(1-np.exp(-self.NTU_des)))) #+ lgo.log_TP(self,var,"F[3]")
        
        # mass balance at ad/desorber
        F[4] = (self.beta_LDF
                *(X_des-self.wp.calc_x_pT(self.fluidProp.calc_VLE_T(T_cond).p_v,T_des)) 
                + self.m_flow_sor*(X_des-X_ads)) #+ lgo.log_TP(self,var,"F[4]")

        # consistent of ad/desorption speed
        F[5] = (self.wp.calc_x_pT(self.fluidProp.calc_VLE_T(T_evp).p_v,T_ads) 
                + self.wp.calc_x_pT(self.fluidProp.calc_VLE_T(T_cond).p_v,T_des) 
                - X_ads - X_des) #+ lgo.log_TP(self,var,"F[5]")
        
        return F
        
    def solve(self,var_guess):
        self.__internalParameters()
        var = optimize.root(self.__EqSystem,var_guess)
        self.T_evp, self.T_cond, self.T_ads, self.T_des, self.X_ads, self.X_des = var.x
        self.__calcHeatFlows()
        return var
            
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

    