"""
Created on Tue 01 Feb

@author: Hibiki Kimura
"""
class params:
    def __init__(self):
        self.Silica123_water = {
              'm_flow_evp':0.191, 
              'm_flow_cond':0.111,
              'm_flow_ads':0.166,
              'm_flow_des':0.166,
              'm_sor':2.236,
              'r_particle':0.00045,
              'cp_HX':379,
              'cp_sor':1000,
              'cp_W':4184,
              'm_HX':6.2,

              # working pair
              'sorbent':'Silicagel123_water',
              'fluid':'water',

              # 85 27 18
              'T_evp_in':291.15,
              'T_cond_in':300.15,
              'T_ads_in':300.15,
              'T_des_in':358.15,
              't_cycle':1000,

              'alphaA_evp_o':1.07899936e+02,
              'alphaA_cond_o':3.30200086e+03,
              'alphaA_ads_o': 3.16025449e+02 ,
              'alphaA_evp_i':1.07899936e+02,
              'alphaA_cond_i':3.30200086e+03,
              'alphaA_ads_i': 3.16025449e+02 ,
              'D_eff':3.72926712e-10,
              'corr_sor_c': 6.33222288e-01 ,
              'corr_HX_c':3.73305009e-01,
              'corr_sor_t': 7.37539599e-04,
              'corr_HX_t':5.59730376e-02
              }

        self.Silica123_water_one_temp = {
              'm_flow_evp':0.191, 
              'm_flow_cond':0.111,
              'm_flow_ads':0.166,
              'm_flow_des':0.166,
              'm_sor':2.236,
              'r_particle':0.00045,
              'cp_HX':379,
              'cp_sor':1000,
              'cp_W':4184,
              'm_HX':6.2,

              # working pair
              'sorbent':'Silicagel123_water',
              'fluid':'water',

              # 85 27 18
              'T_evp_in':291.15,
              'T_cond_in':300.15,
              'T_ads_in':300.15,
              'T_des_in':358.15,
              't_cycle':1000,

              'alphaA_evp_o': 69.24,
              'alphaA_cond_o': 2854.02,
              'alphaA_ads_o': 424.69,
              'alphaA_evp_i': 69.24,
              'alphaA_cond_i': 2854.02,
              'alphaA_ads_i': 424.69,
              'D_eff': 6.550e-10,
              'corr_sor_c': 0.597,
              'corr_HX_c': 0.285,
              'corr_sor_t': 3.15e-03 ,
              'corr_HX_t': 5.54e-02
              }

        self.AQSOAZ02_water = {
              'm_flow_evp':0.191, 
              'm_flow_cond':0.111,
              'm_flow_ads':0.166,
              'm_flow_des':0.166,
              'm_sor':2.236,
              'r_particle':0.00045,
              'cp_HX':379,
              'cp_sor':1000,
              'cp_W':4184,
              'm_HX':6.2,

              # working pair
              'sorbent':'AqsoaZ02_water',
              'fluid':'water',

              # 85 27 18
              'T_evp_in':291.15,
              'T_cond_in':300.15,
              'T_ads_in':300.15,
              'T_des_in':358.15,
              't_cycle':1000,

              'alphaA_evp_o': 142,
              'alphaA_cond_o': 3218.59,
              'alphaA_ads_o': 257.48,
              'alphaA_evp_i': 142,
              'alphaA_cond_i': 3218.59,
              'alphaA_ads_i': 257.48,
              'D_eff': 1.85e-10,
              'corr_sor_c': 0.222,
              'corr_HX_c': 0.242,
              'corr_sor_t': 9.38e-03 ,
              'corr_HX_t': 6.02e-02
              }

        self.Silica123_water_without_dt = {
              'm_flow_evp':0.191, 
              'm_flow_cond':0.111,
              'm_flow_ads':0.166,
              'm_flow_des':0.166,
              'm_sor':2.236,
              'r_particle':0.00045,
              'cp_HX':379,
              'cp_sor':1000,
              'cp_W':4184,
              'm_HX':6.2,

              # working pair
              'sorbent':'AqsoaZ02_water',
              'fluid':'water',

              # 85 27 18
              'T_evp_in':291.15,
              'T_cond_in':300.15,
              'T_ads_in':300.15,
              'T_des_in':358.15,
              't_cycle':1000,

              'alphaA_evp_o': 110,
              'alphaA_cond_o': 5146.47,
              'alphaA_ads_o': 322.47,
              'alphaA_evp_i': 110,
              'alphaA_cond_i': 5146.47,
              'alphaA_ads_i': 322.47,
              'D_eff': 5.347e-10,
              'corr_sor_c': 0.623,
              'corr_HX_c': 2.066,
              'corr_sor_t': 0, # dt coefficients are excluded from the system
              'corr_HX_t': 0
              }

        self.Silica123_water_case1 = {
              'm_flow_evp':0.191, 
              'm_flow_cond':0.111,
              'm_flow_ads':0.166,
              'm_flow_des':0.166,
              'm_sor':2.236,
              'r_particle':0.00045,
              'cp_HX':379,
              'cp_sor':1000,
              'cp_W':4184,
              'm_HX':6.2,

              # working pair
              'sorbent':'Silicagel123_water',
              'fluid':'water',

              # 85 27 18
              'T_evp_in':291.15,
              'T_cond_in':300.15,
              'T_ads_in':300.15,
              'T_des_in':358.15,
              't_cycle':1000,

              'alphaA_evp_o':176,
              'alphaA_cond_o':3174,
              'alphaA_ads_o':151,
              'alphaA_evp_i':176,
              'alphaA_cond_i':3174,
              'alphaA_ads_i':151,
              'D_eff':1.8e-10,
              'corr_sor_c': 6.84359359e-01,
              'corr_sor_t': 0,
              'corr_HX_c': 1.07286827e+00,
              'corr_HX_t':0
              }
