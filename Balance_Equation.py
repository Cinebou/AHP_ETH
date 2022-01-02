"""
@author: Hibiki Kimura
"""
from SteadyStateAKM import adsorptionChiller_steadyState
import numpy as np



class Balance_equation(adsorptionChiller_steadyState):
    def __init__(self, var):
        self.T_evp=var[0]
        self.T_cond=var[1]
        self.T_ads=var[2]
        self.T_des=var[3]
        self.X_ads=var[4]
        self.X_des=var[5]

    """ term calculation """
    def mv_ads(self):
        p_evp = self.fluidProp.calc_VLE_T(self.T_evp).p_v
        X_ads_eq = self.wp.calc_x_pT(p_evp,self.T_ads)
        mv = self.beta_LDF * (X_ads_eq - self.X_ads)
        return mv


    def mv_des(self):
        p_cond = self.fluidProp.calc_VLE_T(self.T_cond).p_v
        X_des_eq = self.wp.calc_x_pT(p_cond, self.T_des)
        mv = self.beta_LDF * (self.X_des - X_des_eq)
        return mv


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
        Desorber : negative -
    """
    def HX_sor(self):
        heatX = self.mcp_sor*(self.T_des-self.T_ads) 
        return heatX

    
    def HX_fluids(self):
        h_des = self.wp.calc_h_ads_xT(self.X_des,self.T_des)
        h_ads = self.wp.calc_h_ads_xT(self.X_ads,self.T_ads)
        heatX = self.m_flow_sor * (self.X_des*h_des - self.X_ads*h_ads) 
        return heatX


    def HX_heatExchanger(self):
        T_HX_des = self.T_des + self.mcp_des/self.alphaA_ads_o*(self.T_des_in-self.T_des)*(1-np.exp(-self.NTU_des))
        T_HX_ads = self.T_ads + self.mcp_ads/self.alphaA_ads_o*(self.T_ads_in-self.T_ads)*(1-np.exp(-self.NTU_ads))
        heatX = self.mcp_HX*(T_HX_des - T_HX_ads)
        return heatX

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


    """ 6 balance equations"""
    def energy_evp(self):
        # enthalpy of in and out
        h_in = self.fluidProp.calc_VLE_liquid_T(self.T_cond).h_l
        h_out = self.fluidProp.calc_VLE_T(self.T_evp).h_v

        # energy balance 
        eq = self.HTF_energy('evp') + self.mv_ads() * (h_in - h_out)
        return eq

    
    def energy_cond(self):
        # enthalpy of in and out
        p_des = self.wp.calc_p_xT(self.X_des,self.T_des)
        h_in = self.fluidProp.calc_fluidProp_pT(p_des,self.T_des).h
        h_out = self.fluidProp.calc_VLE_liquid_T(self.T_cond).h_l

        # energy balance 
        eq = self.HTF_energy('cond') + self.mv_des() * (h_in - h_out)
        return eq


    def energy_ads(self):
        #enthalpy from evaporator
        h_in = self.fluidProp.calc_VLE_T(self.T_evp).h_v

        # energy balance 
        eq = self.HTF_energy('ads') + self.mv_ads()*h_in + self.HX_sor() + self.HX_fluids() + self.HX_heatExchanger()
        return eq


    def energy_des(self):
        # enthalpy to desorber
        h_out = self.fluidProp.calc_fluidProp_pT(self.wp.calc_p_xT(self.X_des,self.T_des),self.T_des).h

        # energy balance 
        eq = self.HTF_energy('des') - self.mv_des()*h_out - self.HX_sor() - self.HX_fluids() - self.HX_heatExchanger()
        return eq


    def mass_in_bed(self):
        # mass balance
        eq = self.mv_des + self.m_flow_sor * (self.X_des - self.X_ads)
        return eq


    def two_mv_speed(self):
        eq = self.mv_ads() - self.mv_des()
        return eq