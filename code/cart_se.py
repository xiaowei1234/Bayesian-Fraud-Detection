#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 16:32:53 2019

@author: xiaowei
"""

import pandas as pd
import constants as c
import numpy as np

#%%
df = pd.read_csv(c.cart_sql_data)

df['cnts'] = df.groupby(['channel', 'location_id'])['cart_rate'].transform('count').values


se_df = df.loc[df.cnts > 1].groupby(['channel', 'location_id']).agg({'cart_rate': 'std', 'cnts': 'max'})

se_df['se'] = se_df.cart_rate / np.sqrt(se_df.cnts - 1)

mse_df = se_df.groupby('channel')[['se']].mean()


import scipy.stats as stats

pnorm = np.vectorize(stats.norm.ppf, excluded=[0, 1])

mse_df['p60'] = pnorm(0.6, 0, mse_df.se)

mse_df