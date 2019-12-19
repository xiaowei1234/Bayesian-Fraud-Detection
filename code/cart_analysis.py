#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 10:56:38 2019

@author: xiaowei
"""
import numpy as np
import pandas as pd
import constants as c
import stats
#%%

def ttest_location(channel, location, df):
    channel_array = np.ravel(df.loc[channel])
    location_array = np.ravel(df.loc[location])
    return stats.ttest(location_array, channel_array)


make_all_ttests = stats.vectorize(ttest_location, [2])


def run_ttests(df):
    locations = df.index.drop_duplicates()
    channels = locations.get_level_values(0)
    pvals = make_all_ttests(channels, locations, df)
    p_df = pd.DataFrame({'location_id': [t[1] for t in locations.values], 'cart_score': pvals})
    return p_df.dropna()


def main_cart_pipes(csv_path):
    if isinstance(csv_path, pd.DataFrame):
        df = csv_path
    else:
        df = pd.read_csv(csv_path)
    p_df = (df.set_index(['channel', 'location_id']).sort_index()
            .pipe(run_ttests).pipe(stats.round_scores, 'cart_score'))
    return p_df
#%%

if __name__ == '__main__':
    p_df = main_cart_pipes(c.cart_sql_data)
    p_df[['location_id', 'cart_score']].to_csv(c.cart_output, index=False)
