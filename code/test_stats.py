#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 13:59:07 2019

@author: xiaowei
"""

import numpy as np
import pandas as pd
import unittest
from scipy.stats import ttest_ind
import constants as c
from stats import create_beta_priors, ttest
#%%


def float_equals(a, b):
    equals = abs(a - b) < 0.00001
    if not equals:
        print (a, b)
    return equals


array_equals = np.vectorize(float_equals)


class TestStats(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({'location_id': [1,2,3,4,5,6]
                                , 'channel':['m', 'm', 'm', 's', 's', 's']
                                , 'avg_score': [0, 0.01, 0.5, 1, 1.2, 1.3]
                                , 'variance': [0.001, 0.1, 0.2, 0.4, 0.5, 1]
                                , 'expected': [0.001, 0.0001, 0.1, 0.4, 1, 1.2]
                                , 'num_matured': [1, 2, 3, 5, 10, 100]
                                , 'fpd': [0, 2, 0, 1, 8, 4]
                                })
        self.cart_array1 = np.asarray([0.5])
        self.cart_array2 = np.asarray([0.5, 1.2, 1.0])
        self.cart_array3 = np.asarray([0.5, 0.5 - c.cart_p60, 0.5])
        self.cart_array4 = np.asarray([0.8])
    
    def test_create_beta_priors(self):
        def inverse_beta_var(v, e):
            return max([e**2 * (1 - e) / v - e, 0.1])
        def calc_beta(a, e):
            return a/e - a
        make_alpha = np.vectorize(inverse_beta_var)
        make_beta = np.vectorize(calc_beta)
        stats_df = create_beta_priors(self.df)
        test_alphas = make_alpha(self.df.variance.values, self.df.expected.values)
        test_betas = make_beta(test_alphas, self.df.expected.values)
        assert np.sum(array_equals(stats_df.alpha, test_alphas)) == test_alphas.size
        assert np.sum(array_equals(stats_df.beta, test_betas)) == test_betas.size

    def test_ttest_less(self):
        less = ttest(self.cart_array1, self.cart_array2)
        self.assertTrue(float_equals(c.low_score, less))

    def test_ttest_short1(self):
        short = ttest(self.cart_array4, self.cart_array1)
        self.assertTrue(float_equals(c.single_item_cart_max, short))
        
    def test_ttest_short2(self):
        short2 = ttest(self.cart_array4, self.cart_array3)
        self.assertTrue(float_equals(c.single_item_cart_max, short2))

    def test_ttest_norm(self):
        norm = ttest(self.cart_array2, self.cart_array3)
        test_result = 1 - ttest_ind(self.cart_array2, self.cart_array3, equal_var=False).pvalue
        self.assertTrue(float_equals(norm, test_result))