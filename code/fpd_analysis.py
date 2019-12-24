#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 10:56:38 2019

@author: xiaowei
"""

import numpy as np
import pandas as pd
import logging
import sys
import constants as c
import stats
#%%
logging.basicConfig(stream=sys.stdout, level=logging.WARNING
                    , format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
                    , datefmt='%m-%d %H:%M')

logger = logging.getLogger(__name__)

#%%
def good_locations(df):
    """
    filter df to only return locations with fpd < X and at least Y num matured leases prespecified in constants file
    """
    good_locs = (df['2mp'] <= c.good_store_cutoff) & (df.num_matured >= c.good_matured_cutoff)
    if np.sum(good_locs) == 0:
        logger.warning('zero locations meet good location cutoff criteria of <={0} fpd and at least {1} matured leases'\
            .format(c.good_store_cutoff, c.good_matured_cutoff))
    return df.loc[good_locs, :]


def remove_no_zero_score(df):
    """
    remove locations without prime score
    """
    not_zeros = df.avg_score > 0.0001
    return df.loc[pd.notnull(df.avg_score) & not_zeros, :]


def create_channel_debias(df_debias):
    """
    debias against the fact that model prediction is 2MP60 whereas we are using 2MP7. Also the model will naturally over/under predict over time
    """
    df_debias['weighted_score'] = df_debias.avg_score * df_debias.num_matured
    g_df = df_debias.groupby('channel', as_index=False)[['fpd', 'weighted_score', 'num_matured']].sum()
    g_df['weighted_score'] = g_df['weighted_score'] / g_df.num_matured
    g_df['fpd_ratio'] = np.maximum(g_df.fpd / g_df.num_matured, 0.01)
    g_df['debias_factor'] = (g_df.fpd_ratio / g_df.weighted_score)
    return g_df


def create_expectations(df):
    """
    expectation is the expected FPD rate given what the model predicts for each location within each channel
    """
    df_debias = good_locations(df)
    g_df = create_channel_debias(df_debias)
    debias_df = df.merge(g_df[['channel', 'debias_factor']], on='channel', how='left')
    null_debias = debias_df.loc[pd.isnull(debias_df.debias_factor), 'channel']
    if null_debias.size > 0:
        channels = ', '.join(set(null_debias.values))
        logger.warning('Channels: {}\
            do not contain any good locations that fit the criteria to create debias factor. Custom fpd score may be inaccurate for these channels'.format(channels))
    debias_df['debias_factor'] = debias_df.debias_factor.fillna(1.0)
    debias_df['expected'] = debias_df.avg_score * debias_df.debias_factor
    return debias_df


def create_fpd_variances(df):
    """
    variance of fpd across locations within each channel
    """
    variance_df = (good_locations(df)[['channel', '2mp']]
                    .groupby('channel', as_index=False).var()
                    .rename(columns={'2mp': 'variance'}))
    not_zero = variance_df.variance > 0
    low = variance_df.loc[not_zero, 'variance'].min()
    variance_df.loc[~not_zero, 'variance'] = low
    df2 = variance_df.merge(df, how='right', on='channel')
    df2['variance'] = df2.variance.fillna(low)
    return df2


def main_fpd_pipes(csv_path):
    if isinstance(csv_path, pd.DataFrame):
        df = csv_path
    else:
        df = pd.read_csv(csv_path)
    df['2mp'] = df.fpd / df.num_matured
    clean_df = df.pipe(remove_no_zero_score)
    if clean_df.shape[0] < 2:
        return pd.DataFrame({'location_id': [], 'fpd_score': []})
    beta_df = (clean_df.pipe(create_expectations)
                .pipe(create_fpd_variances)
                .pipe(stats.create_beta_priors)
                .pipe(stats.create_beta_posteriors)
                .pipe(stats.beta_quantiles)
                .pipe(stats.round_scores, 'fpd_score'))
    return beta_df


#%%
if __name__ == '__main__':
    df = main_fpd_pipes(c.fpd_sql_data)
    df[['location_id', 'fpd_score']].to_csv(c.fpd_output, index=False)
