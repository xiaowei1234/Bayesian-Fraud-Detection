#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 15:09:20 2019

@author: xiaowei
"""

import numpy as np
import pandas as pd
import unittest
from test_stats import float_equals
from fpd_analysis import create_expectations, create_fpd_variances, remove_no_zero_score, create_channel_debias



class TestFpdAnalysis(unittest.TestCase):
    """
    """
    def setUp(self):
        self.zeros_df = pd.DataFrame({'avg_score': [0, 1.1, .000001, None, np.nan]})
        df = pd.DataFrame({'channel': ['m', 'm', 'm', 'm', 'm', 's', 's', 's', 's', 'o', 'n']
                                , 'fpd': [0, 2, 4, 0, 1, 2, 2, 2, 2, 0, 5]
                                , 'num_matured': [2, 14, 12, 2, 4, 12, 32, 5, 23, 2, 6]
                                , 'avg_score': [0.1, 0.13, 0.41, 0.04, 0.05, 0.12, 0.15, 0.07, 0.19, 0.4, 0.3]
                                })
        df['2mp'] = df.fpd / df.num_matured
        self.df = df

    def test_remove_no_score(self):
        df = remove_no_zero_score(self.zeros_df)
        assert df.shape[0] == 1

    def test_create_debias_min_fpd_ratio(self):
        df = create_channel_debias(self.df)
        fpd_ratio_val = df.loc[df.channel=='o', 'fpd_ratio'].values[0]
        assert fpd_ratio_val == 0.01

    def test_debias_calculation(self):
        """
        """
        input_df = self.df.loc[self.df.channel == 'm', :]
        df = create_channel_debias(input_df)
        weighted_scores = np.average(input_df.avg_score, weights=input_df.num_matured)
        self.assertTrue(float_equals(df.weighted_score.values[0], weighted_scores))
    
    def test_expectations(self):
        expected_df = create_expectations(self.df)
        nafill = expected_df.loc[expected_df.channel == 'n', 'debias_factor'].values[0]
        self.assertTrue(float_equals(1.0, nafill))
        
    def test_variances(self):
        input_df = self.df.loc[self.df.channel.isin(['s', 'o', 'n']), :]
        df = create_fpd_variances(input_df)
        self.assertTrue(float_equals(np.mean(df.variance), df.variance.values[0]))