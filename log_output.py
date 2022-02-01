"""
Created on Tue 01 Feb

@author: Hibiki Kimura
"""

import logging
import numpy as np
import pickle 


""" 
The results or Logger can be summarized in Log/ folder
Each Logging can be turned off by 'lg.setlevel(logging.WARN)'
"""

class Log:
        """ Define the Logging settings, log file, format, Log on/off
        """
        def __init__(self):
                # 'Temperature and Pressure log for each iteration
                lg = logging.getLogger('TP')
                handler_TP = logging.FileHandler(filename = "Log/log_TP.log",mode = 'a')
                handler_TP.setFormatter(logging.Formatter("%(message)s"))
                #lg.setLevel(logging.DEBUG) # log on
                lg.setLevel(logging.WARN)   # log off
                lg.addHandler(handler_TP)

                # output of final results
                lg =  logging.getLogger('EQ')
                handler_eq = logging.FileHandler(filename = "Log/log_eq.log",mode = 'a')
                handler_eq.setFormatter(logging.Formatter("%(message)s"))
                #lg.setLevel(logging.INFO)  # log on 
                lg.setLevel(logging.WARN) # log off
                lg.addHandler(handler_eq)

                # output of key parameter
                lg =  logging.getLogger('excel')
                handler_excel = logging.FileHandler(filename = "Log/log_parameter.csv",mode = 'a')
                handler_excel.setFormatter(logging.Formatter("%(message)s"))
                #lg.setLevel(logging.INFO)  # log on 
                lg.setLevel(logging.WARN) # log off
                lg.addHandler(handler_excel)

                # output for validation
                lg =  logging.getLogger('validation')
                handler_excel2 = logging.FileHandler(filename = "Log/validate.csv",mode = 'a')
                handler_excel2.setFormatter(logging.Formatter("%(message)s"))
                lg.setLevel(logging.INFO)  # log on 
                #lg.setLevel(logging.WARN) # log off
                lg.addHandler(handler_excel2)

                Log.__instance = self     


        def log_TePr(self,msg):
                log = logging.getLogger('TP')
                log.debug(msg)

        def log_eq(self,msg):
                log = logging.getLogger('EQ')
                log.info(msg)

        def log_excel(self,msg):
                log = logging.getLogger('excel')
                log.info(msg)

        def log_validate(self,msg):
                log = logging.getLogger('validation')
                log.info(msg)



""" creating instance of Logger """
l = Log()


""" make a log at each time that the equation in a AKM.solve is called """
def log_TP(AKM,var,eq_name):
        T_evp=var[0]
        T_cond=var[1]
        T_ads=var[2]
        T_des=var[3]
        X_ads=var[4]
        X_des=var[5]
        l.log_TePr("\neq {} is called".format(eq_name))

        evp = AKM.fluidProp.calc_VLE_T(T_evp)
        evp_l = AKM.fluidProp.calc_VLE_liquid_T(T_evp)
        l.log_TePr(" evaporator // T = {}, P = {}, h_v = {}, h_l = {}, X_ads = {}, X_des = {}"\
                .format(T_evp, evp.p_v, evp.h_v, evp_l.h_l,X_ads,X_des, evp_l.d_l,evp_l.arfa))

        cond = AKM.fluidProp.calc_VLE_T(T_cond)
        h_dry = AKM.fluidProp.calc_fluidProp_pT(AKM.wp.calc_p_xT(X_des,T_des),T_des).h
        l.log_TePr(" condenser // T = {}, P = {}, h_v = {}, h_l = {}, h_dry = {}, X_ads = {}, X_des = {}"\
                .format(T_cond, cond.p_v, cond.h_v, AKM.fluidProp.calc_VLE_liquid_T(T_cond).h_l,h_dry,X_ads,X_des))

        ads = AKM.fluidProp.calc_VLE_T(T_ads)
        l.log_TePr(" adsorber // T = {}, P = {}, h_v = {}, h_l = {}, X_ads = {}, X_des = {}"\
                .format(T_ads, ads.p_v, ads.h_v, AKM.fluidProp.calc_VLE_liquid_T(T_ads).h_l,X_ads,X_des))

        des = AKM.fluidProp.calc_VLE_T(T_des)
        l.log_TePr(" desorber // T = {}, P = {}, h_v = {}, h_l = {}, X_ads = {}, X_des = {}"\
                .format(T_des, des.p_v, des.h_v, AKM.fluidProp.calc_VLE_liquid_T(T_des).h_l,X_ads,X_des))

        mv_ads = AKM.mv_ads()
        mv_des = AKM.mv_des()
        X_eq_ads = AKM.wp.calc_x_pT(AKM.fluidProp.calc_VLE_T(T_evp).p_v,T_ads)
        X_eq_des = AKM.wp.calc_x_pT(AKM.fluidProp.calc_VLE_T(T_cond).p_v,T_des)
        l.log_TePr(" mv(ads) = {}, mv(des) = {}, X_eq_ads = {}, X_eq_des = {}"\
                .format(mv_ads,  mv_des, X_eq_ads, X_eq_des))
        return 0



""" output any message to "Log/validate.csv" file """
def log_excel_msg(msg):
        l.log_validate(msg)
        return 0



""" output detail results to "Log/log_parameter.csv" file """
def log_output_excel(AKM):
        # cycle time
        t = AKM.t_cycle

        # variables for each configuration
        T_evp = AKM.T_evp
        T_cond = AKM.T_cond
        T_ads = AKM.T_ads
        T_des = AKM.T_des
        X_ads = AKM.X_ads
        X_des = AKM.X_des

        #mass balance
        mv = AKM.mv_ads()

        # heat balance term (inner cycle between ad/de)
        h_sor = AKM.HX_sor()
        h_ad_water = AKM.HX_fluids()
        h_hx = AKM.HX_heatExchanger()

        h_v_from_evp = AKM.mv_ads()*AKM.fluidProp.calc_VLE_T(AKM.T_evp).h_v
        h_v_to_cond = AKM.mv_des()*AKM.fluidProp.calc_fluidProp_pT(AKM.wp.calc_p_xT(AKM.X_des,AKM.T_des),AKM.T_des).h

        # temperature difference of heat recovery
        Diff_T_sor = T_des - T_ads
        T_high_HX = AKM.T_des + AKM.mcp_des/AKM.alphaA_ads_o*(AKM.T_des_in-AKM.T_des)*(1-np.exp(-AKM.NTU_des))
        T_low_HX = AKM.T_ads  + AKM.mcp_ads/AKM.alphaA_ads_o*(AKM.T_ads_in-AKM.T_ads)*(1-np.exp(-AKM.NTU_ads))
        #Diff_T_HTF = T_des-T_ads + 1/AKM.NTU_des*(AKM.T_des_in-T_des)*(1-np.exp(-AKM.NTU_des)) - 1/AKM.NTU_ads*(AKM.T_ads_in-T_ads)*(1-np.exp(-AKM.NTU_ads))

        l.log_excel("{},  {},{},{},{},{},{},  {},  {},{},{}, {},{}, {},{},{}"\
                .format(t,  T_evp,T_cond,T_ads,T_des,X_ads,X_des,  mv,  h_sor,h_ad_water,h_hx,  h_v_from_evp,h_v_to_cond, Diff_T_sor,T_high_HX,T_low_HX))
        return 0