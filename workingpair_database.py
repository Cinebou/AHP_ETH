# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 09:21:29 2020

@author: gibelhaus
"""
import pandas as pd

wp_db=pd.DataFrame(columns=['func','coeff', 'heatCap'])
wp_db.loc['Silicagel123_water']=['arctan',[5.072313e-1 * 1e-3 , 1.305531e2 * 1e3 , -8.492403e1 * 1e3 , 4.128962e-3 * 1e-3], 1000]
wp_db.loc['Silicagel125_water']=['arctan',[4.527805e-4,1.229005e5,-8.847167e4,6.034706e-7], 1000]
wp_db.loc['AqsoaZ02_water']=['arctan',[3.466e-4,3.094e5,-9.765e4,7.312e-7], 1000]

wp_db=wp_db.T