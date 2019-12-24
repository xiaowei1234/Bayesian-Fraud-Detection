#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 16:10:28 2019

@author: xiaowei
"""

import pandas as pd
import unittest
from cart_analysis import main_cart_pipes


class TestFpdAnalysis(unittest.TestCase):
    """
    """
    def setUp(self):
        self.empty_df = pd.DataFrame({'channel': [], 'location_id': [], 'cart_rate': []})
    
    def test_empty(self):
        returned_df = main_cart_pipes(self.empty_df)
        assert returned_df.shape[0] == 0