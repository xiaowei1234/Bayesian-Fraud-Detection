#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 12:39:39 2019

@author: xiaowei
"""

fpd_sql_file = 'fpd_eval_query.sql'
cart_sql_file = 'cart_eval_query.sql'

data_path = '../data/'
fpd_sql_data = data_path + 'fpd_eval_data.csv'
cart_sql_data = data_path + 'cart_eval_data.csv'


fpd_eval_periods = [dict(pull=1, dt1='2019-02-01', eval1='2019-04-01')
                    , dict(pull=2, dt1='2019-02-08', eval1='2019-04-01')
                    , dict(pull=3, dt1='2019-02-15', eval1='2019-04-01')
                    , dict(pull=11, dt1='2019-04-01', eval1='2019-06-01')
                    , dict(pull=12, dt1='2019-04-08', eval1='2019-06-01')
                    , dict(pull=13, dt1='2019-04-15', eval1='2019-06-01')
                    , dict(pull=4, dt1='2019-03-01', eval1='2019-05-01')
                    ]


cart_eval_periods = [dict(pull=1, dt1='2019-03-18', eval1='2019-04-01')
                    , dict(pull=11, dt1='2019-05-18', eval1='2019-06-01')
                    , dict(pull=4, dt1='2019-04-17', eval1='2019-05-01')
                    ]


eval_fpd_output = data_path + 'fpd_eval_forR.csv'
eval_cart_output = data_path + 'cart_eval_forR.csv'