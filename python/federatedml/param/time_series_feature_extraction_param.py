#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright 2019 The FATE Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
import copy

from federatedml.param.base_param import BaseParam
from federatedml.param.encrypt_param import EncryptParam
from federatedml.util import consts


class TimeSeriesFeatureExtractionParam(BaseParam):
    """
    Define the feature binning method

    Parameters
    ----------
    need_run: bool, default True
        Indicate if this module needed to be run
    """

    def __init__(self, method=None,
                 need_run=True, skip_static=False, window_size=None, ts_idx=None, tsf_cols=None, target_cols=None):
        super(TimeSeriesFeatureExtractionParam, self).__init__()
        self.method = method
        self.need_run = need_run
        self.skip_static = skip_static
        self.window_size = window_size
        self.tsf_cols = tsf_cols
        self.ts_idx = ts_idx
        self.target_cols = target_cols

    def check(self):
        descr = "Time Series Feature Extraction param's"

        self.check_defined_type(self.method, descr, ['list', "NoneType"])
        self.check_boolean(self.need_run, descr)
        self.check_boolean(self.skip_static, descr)
        self.check_integer(self.window_size, descr)
        self.check_integer(self.ts_idx, descr)
        self.check_defined_type(self.tsf_cols, descr, ['list', "NoneType"])
        self.check_defined_type(self.target_cols, descr, ['list', "NoneType"])

        #self.check_decimal_float(self.error, descr)
        #self.check_positive_integer(self.bin_num, descr)
        #self.check_open_unit_interval(self.adjustment_factor, descr)


class HeteroTimeSeriesFeatureExtractionParam(TimeSeriesFeatureExtractionParam):
    def __init__(self, method=[consts.TS_COUNT],
                 need_run=True, skip_static=False, window_size=0, ts_idx=0, tsf_cols=None, target_cols=None):
        super(HeteroTimeSeriesFeatureExtractionParam, self).__init__(method=method, 
                                                        need_run=need_run, 
                                                        skip_static=skip_static, window_size=window_size, ts_idx=ts_idx, tsf_cols=tsf_cols, target_cols=target_cols)
    def check(self):
        descr = "Hetero Time Series Feature Extraction param's"
        super(HeteroTimeSeriesFeatureExtractionParam, self).check()
        
        for m in self.method:
            m = m.lower()
            self.check_string(m, descr)
            self.check_valid_value(m, descr, [consts.TS_DCOUNT, consts.TS_MEAN, consts.TS_SUM, consts.TS_MAX, consts.TS_MIN, consts.TS_COUNT])

