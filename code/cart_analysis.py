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
    """
    t test single location and compare against its channel
    """
    channel_array = np.ravel(df.loc[channel])
    location_array = np.ravel(df.loc[location])
    return stats.ttest(location_array, channel_array)


# vectorize ttest_location
make_all_ttests = stats.vectorize(ttest_location, [2])


def run_ttests(df):
    """
    get arrays of cart utilization rates for each distinct channel and location and then run t tests
    """
    if df.shape[0] == 0:
        return pd.DataFrame({'location_id': [], 'cart_score': []})
    locations = df.index.drop_duplicates()
    channels = locations.get_level_values(0)
    pvals = make_all_ttests(channels, locations, df)
    p_df = pd.DataFrame({'location_id': [t[1] for t in locations.values], 'cart_score': pvals})
    return p_df.dropna()


def main_cart_pipes(csv_path):
    """
    coordinate pipes
    """
    if isinstance(csv_path, pd.DataFrame):
        df = csv_path
    else:
        df = pd.read_csv(csv_path)
    p_df = (df.set_index(['channel', 'location_id']).sort_index()
            .pipe(run_ttests).pipe(stats.round_scores, 'cart_score'))
    return p_df
#%%

def main(input_data, output_path):
    p_df = main_cart_pipes(input_data)
    p_df[['location_id', 'cart_score']].to_csv(output_path, index=False)


if __name__ == '__main__':
    main(c.cart_sql_data, c.cart_output)