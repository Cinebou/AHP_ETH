
class params:
    def __init__(self):
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

        self.Silica123_water_fit = {
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

              'alphaA_evp_o':9.49999929e+01,
              'alphaA_cond_o':3.87600000e+03,
              'alphaA_ads_o':2.96999988e+02,
              'alphaA_evp_i':9.49999929e+01,
              'alphaA_cond_i':3.87600000e+03,
              'alphaA_ads_i':2.96999988e+02,
              'D_eff':6.07052737e-10,
              'corr_sor_c':  6.99997583e-01,
              'corr_sor_t': 1.68411995e-03,
              'corr_HX_c': 4.60999771e-01,
              'corr_HX_t':5.09992928e-02
              }

        self.Silica123_water_notime = {
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

              'alphaA_evp_o':1.36041482e+02,
              'alphaA_cond_o':3.17402235e+03,
              'alphaA_ads_o':2.08242143e+02 ,
              'alphaA_evp_i':1.36041482e+02,
              'alphaA_cond_i':3.17402235e+03,
              'alphaA_ads_i':2.08242143e+02 ,
              'D_eff':9.70896677e-10,
              'corr_sor_c': 9.21710287e-01,
              'corr_sor_t': 0,
              'corr_HX_c': 2.03851340e+00,
              'corr_HX_t':0
              }
              
        self.Silica123_water_1_temp = {
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

              'alphaA_evp_o':1.00537394e+02,
              'alphaA_cond_o':3.42943168e+03,
              'alphaA_ads_o':5.05362201e+02,
              'alphaA_evp_i':1.00537394e+02,
              'alphaA_cond_i':3.42943168e+03,
              'alphaA_ads_i':5.05362201e+02,
              'D_eff':2.39364061e-10,
              'corr_sor_c':2.56628646e-01,
              'corr_sor_t': 8.22035411e-03,
              'corr_HX_c':5.37264184e-01,
              'corr_HX_t':5.17084931e-02
              }

        self.AQSOA_water_fit = {
              'm_flow_evp':0.191, 
              'm_flow_cond':0.111,
              'm_flow_ads':0.166,
              'm_flow_des':0.166,
              'm_sor':2.236,
              'r_particle':0.00045,
              'cp_HX':379,
              'cp_sor':778,
              'cp_W':4184,
              'm_HX':6.2,

              # working pair
              'sorbent':'AqsoaZ02_water',
              'fluid':'water',

              'alphaA_evp_o':1.31595818e+02,
              'alphaA_cond_o':3.17406677e+03,
              'alphaA_ads_o':2.15319994e+02,
              'alphaA_evp_i':1.31595818e+02,
              'alphaA_cond_i':3.17406677e+03,
              'alphaA_ads_i':2.15319994e+02,
              'D_eff':5.42081251e-10,
              'corr_sor_c':7.05277721e-01,
              'corr_sor_t': 4.32197372e-04,
              'corr_HX_c': 3.18101008e-01,
              'corr_HX_t':5.91826141e-02
              }
"""
    def set_t_cycle_param(self):
        param = self.Silica123_water_case1
        return param
"""
