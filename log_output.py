import logging
import numpy as np
import pickle 

class Log:
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
                #handler_excel.setFormatter(logging.Formatter("%(message)s"))
                lg.setLevel(logging.INFO)  # log on 
                #lg.setLevel(logging.WARN) # log off
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

def ARE(COP_dyn_852718,Qflow_chill_dyn_852718,COP_stat_852718,Qflow_chill_stat_852718,COP_dyn_903010,Qflow_chill_dyn_903010,COP_stat_903010,Qflow_chill_stat_903010):
    RE = abs(COP_dyn_852718 - COP_stat_852718)/COP_dyn_852718 + abs(Qflow_chill_dyn_852718 - Qflow_chill_stat_852718)/Qflow_chill_dyn_852718 + abs(COP_dyn_903010 - COP_stat_903010)/COP_dyn_903010 + abs(Qflow_chill_dyn_903010 - Qflow_chill_stat_903010)/Qflow_chill_dyn_903010
    return sum(RE)/len(RE)

def read_pickle(file):
        with open(file, 'rb') as f:
                results = pickle.load(f)
        t_cycle = results['t_Cycle']
        Qflow = results['Q_flow_cool_avg']
        COP = results['COP']
        return t_cycle, Qflow, COP

l = Log()
# make a log at each time that the equation in a AKM.solve is called
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
        l.log_TePr(" evaporator // T = {}, P = {}, h_v = {}, h_l = {}, X_ads = {}, X_des = {}".format(T_evp, evp.p_v, evp.h_v, evp_l.h_l,X_ads,X_des, evp_l.d_l,evp_l.arfa))

        cond = AKM.fluidProp.calc_VLE_T(T_cond)
        h_dry = AKM.fluidProp.calc_fluidProp_pT(AKM.wp.calc_p_xT(X_des,T_des),T_des).h
        l.log_TePr(" condenser // T = {}, P = {}, h_v = {}, h_l = {}, h_dry = {}, X_ads = {}, X_des = {}".format(T_cond, cond.p_v, cond.h_v, AKM.fluidProp.calc_VLE_liquid_T(T_cond).h_l,h_dry,X_ads,X_des))

        ads = AKM.fluidProp.calc_VLE_T(T_ads)
        l.log_TePr(" adsorber // T = {}, P = {}, h_v = {}, h_l = {}, X_ads = {}, X_des = {}".format(T_ads, ads.p_v, ads.h_v, AKM.fluidProp.calc_VLE_liquid_T(T_ads).h_l,X_ads,X_des))

        des = AKM.fluidProp.calc_VLE_T(T_des)
        l.log_TePr(" desorber // T = {}, P = {}, h_v = {}, h_l = {}, X_ads = {}, X_des = {}".format(T_des, des.p_v, des.h_v, AKM.fluidProp.calc_VLE_liquid_T(T_des).h_l,X_ads,X_des))

        mv_ads = AKM.beta_LDF*(AKM.wp.calc_x_pT(AKM.fluidProp.calc_VLE_T(T_evp).p_v,T_ads)-X_ads)
        mv_des = AKM.beta_LDF*(X_des - AKM.wp.calc_x_pT(AKM.fluidProp.calc_VLE_T(T_cond).p_v,T_des))
        X_eq_ads = AKM.wp.calc_x_pT(AKM.fluidProp.calc_VLE_T(T_evp).p_v,T_ads)
        X_eq_des = AKM.wp.calc_x_pT(AKM.fluidProp.calc_VLE_T(T_cond).p_v,T_des)
        l.log_TePr(" mv(ads) = {}, mv(des) = {}, X_eq_ads = {}, X_eq_des = {}".format(mv_ads,  mv_des, X_eq_ads, X_eq_des))
        return 0

def log_excel_msg(msg):
        l.log_validate(msg)
        return 0

def log_output_excel(AKM,init = False):
        
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
        mv = AKM.beta_LDF*(AKM.wp.calc_x_pT(AKM.fluidProp.calc_VLE_T(AKM.T_evp).p_v,AKM.T_ads) - AKM.X_ads)

        # heat balance term (inner cycle between ad/de)
        h_sor = AKM.mcp_sor*(AKM.T_des-AKM.T_ads)
        h_ad_water = AKM.m_flow_sor * (AKM.X_des*AKM.wp.calc_h_ads_xT(AKM.X_des,AKM.T_des)-AKM.X_ads*AKM.wp.calc_h_ads_xT(AKM.X_ads,AKM.T_ads))
        h_hx = AKM.mcp_HX*(AKM.T_des-AKM.T_ads + AKM.mcp_des/AKM.alphaA_ads_o*(AKM.T_des_in-AKM.T_des)*(1-np.exp(-AKM.NTU_des)) - AKM.mcp_ads/AKM.alphaA_ads_o*(AKM.T_ads_in-AKM.T_ads)*(1-np.exp(-AKM.NTU_ads)))

        h_v_from_evp = AKM.beta_LDF*(AKM.wp.calc_x_pT(AKM.fluidProp.calc_VLE_T(AKM.T_evp).p_v,AKM.T_ads)-AKM.X_ads)*AKM.fluidProp.calc_VLE_T(AKM.T_evp).h_v
        h_v_to_cond = AKM.beta_LDF*(AKM.X_des-AKM.wp.calc_x_pT(AKM.fluidProp.calc_VLE_T(AKM.T_cond).p_v,AKM.T_des))*AKM.fluidProp.calc_fluidProp_pT(AKM.wp.calc_p_xT(AKM.X_des,AKM.T_des),AKM.T_des).h

        # temperature difference of heat recovery
        Diff_T_sor = T_des - T_ads
        T_high_HX = AKM.T_des + AKM.mcp_des/AKM.alphaA_ads_o*(AKM.T_des_in-AKM.T_des)*(1-np.exp(-AKM.NTU_des))
        T_low_HX = AKM.T_ads  + AKM.mcp_ads/AKM.alphaA_ads_o*(AKM.T_ads_in-AKM.T_ads)*(1-np.exp(-AKM.NTU_ads))
        #Diff_T_HTF = T_des-T_ads + 1/AKM.NTU_des*(AKM.T_des_in-T_des)*(1-np.exp(-AKM.NTU_des)) - 1/AKM.NTU_ads*(AKM.T_ads_in-T_ads)*(1-np.exp(-AKM.NTU_ads))

        #l.log_excel("t,  T_evp,T_cond,T_ads,T_des,X_ads,X_des,  mv,  h_sor,h_ad_water,h_hx,  h_v_from_evp,h_v_to_cond")
        l.log_excel("{},  {},{},{},{},{},{},  {},  {},{},{}, {},{}, {},{},{}"\
                .format(t,  T_evp,T_cond,T_ads,T_des,X_ads,X_des,  mv,  h_sor,h_ad_water,h_hx,  h_v_from_evp,h_v_to_cond, Diff_T_sor,T_high_HX,T_low_HX))
        return 0


def log_output_eq(AKM):
        l.log_eq("Cycle time = {}".format(AKM.t_cycle))
        # evaporator
        mv_evp = AKM.beta_LDF*(AKM.wp.calc_x_pT(AKM.fluidProp.calc_VLE_T(AKM.T_evp).p_v,AKM.T_ads) - AKM.X_ads)
        hl_T_cond = AKM.fluidProp.calc_VLE_liquid_T(AKM.T_cond).h_l
        hv_T_evp = AKM.fluidProp.calc_VLE_T(AKM.T_evp).h_v
        l.log_eq('\nenergy balance at evaporator\n\
                  cooling power for HTF = mcp/ {} * (T_chill/ {} - T_evp_out\ {})\n\
                  latent heat of evaporation = mv/ {} * (h_l/ {} - h_v/ {})'
                .format(AKM.mcp_evp,AKM.T_evp_in,AKM.T_evp_out,mv_evp,hl_T_cond,hv_T_evp))
        l.log_eq('F[0] = {}'.format(AKM.mcp_evp*(AKM.T_evp_in-AKM.T_evp)*(1-np.exp(-AKM.NTU_evp))
                + AKM.beta_LDF*(AKM.wp.calc_x_pT(AKM.fluidProp.calc_VLE_T(AKM.T_evp).p_v,AKM.T_ads) - AKM.X_ads)
                *(AKM.fluidProp.calc_VLE_liquid_T(AKM.T_cond).h_l-AKM.fluidProp.calc_VLE_T(AKM.T_evp).h_v)))

        # condenser
        mv_cond = AKM.beta_LDF*(AKM.X_des - AKM.wp.calc_x_pT(AKM.fluidProp.calc_VLE_T(AKM.T_cond).p_v,AKM.T_des))
        h_T_des = AKM.fluidProp.calc_fluidProp_pT(AKM.wp.calc_p_xT(AKM.X_des,AKM.T_des),AKM.T_des).h
        hl_T_cond = AKM.fluidProp.calc_VLE_liquid_T(AKM.T_cond).h_l
        l.log_eq('\nenergy balance at condenser\n\
                  cooled by HTF = mcp/ {} * (T_cool/ {} - T_cond_out\ {})\n\
                  latent heat of condensation = mv/ {} * (h_v_dry/ {} - h_l/ {})'
                .format(AKM.mcp_cond,AKM.T_cond_in,AKM.T_cond_out,mv_cond,h_T_des,hl_T_cond))
        l.log_eq('F[1] = {}'.format((AKM.mcp_cond*(AKM.T_cond_in-AKM.T_cond)*(1-np.exp(-AKM.NTU_cond)) 
                + AKM.beta_LDF*(AKM.X_des-AKM.wp.calc_x_pT(AKM.fluidProp.calc_VLE_T(AKM.T_cond).p_v,AKM.T_des))
                *(AKM.fluidProp.calc_fluidProp_pT(AKM.wp.calc_p_xT(AKM.X_des,AKM.T_des),AKM.T_des).h-AKM.fluidProp.calc_VLE_liquid_T(AKM.T_cond).h_l))))

        # adsorber
        cooled_by_HTF = AKM.mcp_ads*(AKM.T_ads_in-AKM.T_ads)*(1-np.exp(-AKM.NTU_ads))
        h_v_from_evp = AKM.beta_LDF*(AKM.wp.calc_x_pT(AKM.fluidProp.calc_VLE_T(AKM.T_evp).p_v,AKM.T_ads)-AKM.X_ads)*AKM.fluidProp.calc_VLE_T(AKM.T_evp).h_v 
        heat_back_s = AKM.mcp_sor*(AKM.T_des-AKM.T_ads)
        heat_back_w = AKM.m_flow_sor * (AKM.X_des*AKM.wp.calc_h_ads_xT(AKM.X_des,AKM.T_des)-AKM.X_ads*AKM.wp.calc_h_ads_xT(AKM.X_ads,AKM.T_ads))
        heat_back_hx = AKM.mcp_HX*(AKM.T_des-AKM.T_ads + AKM.mcp_des/AKM.alphaA_ads_o*(AKM.T_des_in-AKM.T_des)*(1-np.exp(-AKM.NTU_des)) - AKM.mcp_ads/AKM.alphaA_ads_o*(AKM.T_ads_in-AKM.T_ads)*(1-np.exp(-AKM.NTU_ads)))
        heat_back_HTF = AKM.mcp_fl*(AKM.T_des-AKM.T_ads + 1/AKM.NTU_des*(AKM.T_des_in-AKM.T_des)*(1-np.exp(-AKM.NTU_des)) - 1/AKM.NTU_ads*(AKM.T_ads_in-AKM.T_ads)*(1-np.exp(-AKM.NTU_ads)))
        l.log_eq('\nenergy balance at adsorber\n\
                  cooled by HTF = {}\n\
                  enthalpy of working fluid vapor = {}\n\
                  heat back from sorbent = {}\n\
                  heat back from water in adsorbent = {}\n\
                  heat back from heat exchanger = {}\n\
                  heat back from HFT = {}'
                .format(cooled_by_HTF,h_v_from_evp,heat_back_s, heat_back_w, heat_back_hx, heat_back_HTF))

        l.log_eq("cooled by HTF = mcp/ {} * (T_cool/ {} - T_ads_out/ {})".format(AKM.mcp_ads, AKM.T_ads_in, AKM.T_ads_out))
        l.log_eq("heat back from water = m_flow_sor/ {} * (X_des/ {} * h_des/ {} - X_ads/ {} * h_ads/ {}) "\
                .format(AKM.m_flow_sor, AKM.X_des, AKM.wp.calc_h_ads_xT(AKM.X_des,AKM.T_des), AKM.X_ads, AKM.wp.calc_h_ads_xT(AKM.X_ads,AKM.T_ads)))

        l.log_eq('F[2] = {}'.format((AKM.mcp_ads*(AKM.T_ads_in-AKM.T_ads)*(1-np.exp(-AKM.NTU_ads)) 
                + AKM.beta_LDF
                *(AKM.wp.calc_x_pT(AKM.fluidProp.calc_VLE_T(AKM.T_evp).p_v,AKM.T_ads)-AKM.X_ads)
                *AKM.fluidProp.calc_VLE_T(AKM.T_evp).h_v 
                + AKM.mcp_sor*(AKM.T_des-AKM.T_ads) 
                + AKM.m_flow_sor
                *(AKM.X_des*AKM.wp.calc_h_ads_xT(AKM.X_des,AKM.T_des)-AKM.X_ads*AKM.wp.calc_h_ads_xT(AKM.X_ads,AKM.T_ads)) 
                + AKM.mcp_HX*(AKM.T_des-AKM.T_ads + AKM.mcp_des/AKM.alphaA_ads_o*(AKM.T_des_in-AKM.T_des)*(1-np.exp(-AKM.NTU_des)) - AKM.mcp_ads/AKM.alphaA_ads_o*(AKM.T_ads_in-AKM.T_ads)*(1-np.exp(-AKM.NTU_ads)))
                + AKM.mcp_fl*(AKM.T_des-AKM.T_ads + 1/AKM.NTU_des*(AKM.T_des_in-AKM.T_des)*(1-np.exp(-AKM.NTU_des)) - 1/AKM.NTU_ads*(AKM.T_ads_in-AKM.T_ads)*(1-np.exp(-AKM.NTU_ads))))))

        # desorber 
        heated_by_HTF = AKM.mcp_des*(AKM.T_des_in-AKM.T_des)*(1-np.exp(-AKM.NTU_des))
        h_v_to_cond = AKM.beta_LDF*(AKM.X_des-AKM.wp.calc_x_pT(AKM.fluidProp.calc_VLE_T(AKM.T_cond).p_v,AKM.T_des))*AKM.fluidProp.calc_fluidProp_pT(AKM.wp.calc_p_xT(AKM.X_des,AKM.T_des),AKM.T_des).h 
        heat_back_s = AKM.mcp_sor*(AKM.T_ads-AKM.T_des) 
        heat_back_w = AKM.m_flow_sor*(AKM.X_ads*AKM.wp.calc_h_ads_xT(AKM.X_ads,AKM.T_ads)-AKM.X_des*AKM.wp.calc_h_ads_xT(AKM.X_des,AKM.T_des))
        heat_back_hx = AKM.mcp_HX*(AKM.T_ads-AKM.T_des + AKM.mcp_ads/AKM.alphaA_ads_o*(AKM.T_ads_in-AKM.T_ads)*(1-np.exp(-AKM.NTU_ads)) - AKM.mcp_des/AKM.alphaA_ads_o*(AKM.T_des_in-AKM.T_des)*(1-np.exp(-AKM.NTU_des))) 
        heat_back_HTF = AKM.mcp_fl*(AKM.T_ads-AKM.T_des + 1/AKM.NTU_ads*(AKM.T_ads_in-AKM.T_ads)*(1-np.exp(-AKM.NTU_ads)) - 1/AKM.NTU_des*(AKM.T_des_in-AKM.T_des)*(1-np.exp(-AKM.NTU_des)))
        l.log_eq('\nenergy balance at desorber\n\
                  heated by HTF = {}\n\
                  enthalpy of working fluid vapor out = {}\n\
                  heat back from sorbent = {}\n\
                  heat back from water in adsorbent = {}\n\
                  heat back from heat exchanger = {}\n\
                  heat back from HFT = {}'
                .format(heated_by_HTF,h_v_to_cond,heat_back_s, heat_back_w, heat_back_hx, heat_back_HTF))

        l.log_eq('F[3] = {}'.format((AKM.mcp_des*(AKM.T_des_in-AKM.T_des)*(1-np.exp(-AKM.NTU_des)) 
                - AKM.beta_LDF
                *(AKM.X_des-AKM.wp.calc_x_pT(AKM.fluidProp.calc_VLE_T(AKM.T_cond).p_v,AKM.T_des))
                *AKM.fluidProp.calc_fluidProp_pT(AKM.wp.calc_p_xT(AKM.X_des,AKM.T_des),AKM.T_des).h 
                + AKM.mcp_sor*(AKM.T_ads-AKM.T_des) 
                + AKM.m_flow_sor*(AKM.X_ads*AKM.wp.calc_h_ads_xT(AKM.X_ads,AKM.T_ads)-AKM.X_des*AKM.wp.calc_h_ads_xT(AKM.X_des,AKM.T_des))
                + AKM.mcp_HX*(AKM.T_ads-AKM.T_des + AKM.mcp_ads/AKM.alphaA_ads_o*(AKM.T_ads_in-AKM.T_ads)*(1-np.exp(-AKM.NTU_ads)) - AKM.mcp_des/AKM.alphaA_ads_o*(AKM.T_des_in-AKM.T_des)*(1-np.exp(-AKM.NTU_des))) 
                + AKM.mcp_fl*(AKM.T_ads-AKM.T_des + 1/AKM.NTU_ads*(AKM.T_ads_in-AKM.T_ads)*(1-np.exp(-AKM.NTU_ads)) - 1/AKM.NTU_des*(AKM.T_des_in-AKM.T_des)*(1-np.exp(-AKM.NTU_des))))))

        #mass balance at ad/desorber
        mv = AKM.beta_LDF*(AKM.X_des-AKM.wp.calc_x_pT(AKM.fluidProp.calc_VLE_T(AKM.T_cond).p_v,AKM.T_des))
        m_ads_des = AKM.m_flow_sor*(AKM.X_des-AKM.X_ads)
        l.log_eq("\nmass balance at ad/desorber\n\
                mv = {}\n\
                m_flow_sor * (X_des - X_ads) = {}".format(mv, m_ads_des))
        l.log_eq('F[4] = {}'.format((AKM.beta_LDF*(AKM.X_des-AKM.wp.calc_x_pT(AKM.fluidProp.calc_VLE_T(AKM.T_cond).p_v,AKM.T_des)) \
                + AKM.m_flow_sor*(AKM.X_des-AKM.X_ads))))

        #consistent of ad/desorption speed
        X_ads_eq = AKM.wp.calc_x_pT(AKM.fluidProp.calc_VLE_T(AKM.T_evp).p_v,AKM.T_ads)
        X_des_eq = AKM.wp.calc_x_pT(AKM.fluidProp.calc_VLE_T(AKM.T_cond).p_v,AKM.T_des)
        l.log_eq('\nconsistent of ad/desorption speed\n\
                X_ads_eq = {}\n\
                X_des_eq = {}\n\
                X_ads = {}\n\
                X_des = {}\n'.format(X_ads_eq,X_des_eq,AKM.X_ads,AKM.X_des))
        l.log_eq("F[5] = {}".format((AKM.wp.calc_x_pT(AKM.fluidProp.calc_VLE_T(AKM.T_evp).p_v,AKM.T_ads) 
                + AKM.wp.calc_x_pT(AKM.fluidProp.calc_VLE_T(AKM.T_cond).p_v,AKM.T_des) 
                - AKM.X_ads - AKM.X_des)))

        # optimised temperature
        l.log_eq("optimised temperature parameters  \n\
                T_evp_in: {}      T_evp: {}   T_evp_out: {}\n\
                T_cond_in:{}      T_cond:{}   T_cond_out:{}\n\
                T_ads_in: {}      T_ads: {}   T_ads_out: {}\n\
                T_des_in: {}      T_des: {}   T_des_out: {}\n"\
                .format(AKM.T_evp_in, AKM.T_evp,AKM.T_evp_out,AKM.T_cond_in,AKM.T_cond,AKM.T_cond_out,AKM.T_ads_in,AKM.T_ads,AKM.T_ads_out,AKM.T_des_in,AKM.T_des,AKM.T_des_out))
        l.log_eq('\n\n\n\n')
