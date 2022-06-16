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
import functools

from federatedml.feature.hetero_time_series_feature_extraction.base_time_series_feature_extraction import BaseTimeSeriesFeatureExtraction
from federatedml.secureprotol import PaillierEncrypt
from federatedml.secureprotol.fate_paillier import PaillierEncryptedNumber
from federatedml.statistic import data_overview
from federatedml.statistic import statics
from federatedml.util import LOGGER
from federatedml.util import consts
import numpy as np
from random import randint

class HeteroTimeSeriesFeatureExtractionGuest(BaseTimeSeriesFeatureExtraction):
    @staticmethod
    def striptimestamp(data, idx_list):
        features = np.array(data.features,dtype=float)
        processed_features=[]
        for i in idx_list:
            value=int(features[i])
            processed_features.append(value)

        _data = copy.deepcopy(data)
        _data.features = copy.deepcopy(processed_features)
        return _data
    
    @staticmethod
    def convert_window_size(ws):
        return ws*86400 #convert time window size of days to seconds

    def function_val_calculation(self, encrypted_ts, ts_u, ts_l):
        a = randint(2,5)
        b = randint(1,10) * 86400
        y1 = a*ts_u + b
        y2 = a*ts_l + b
        e_y = encrypted_ts.__mul__(a)
        e_y = e_y.__add__(b)
        res = [y1,y2,e_y]
        return res

    def process_timestamp_list(self, timestamp_list):
        LOGGER.info("Process timestamp list")
        count = 0
        time_window = self.convert_window_size(self.model_param.window_size)
        for sample in timestamp_list:
            inst_id = sample[0]
            time_stamp = sample[1].features[0] + 100
            time_stamp_l = time_stamp - time_window
            count += 1
            LOGGER.info(count)
            LOGGER.info(inst_id)
            LOGGER.info(time_stamp)
            check=True
            self.transfer_variable.target_idx.remote(inst_id, role=consts.HOST,idx=-1)
            while(check):
                check_ts = self.transfer_variable.encrypted_time_stamp.get()[0]
                if check_ts == -1: #End of one sample check
                    check=False
                    break
                function_val =  self.function_val_calculation(check_ts, time_stamp, time_stamp_l)
                self.transfer_variable.function_val.remote(function_val, role=consts.HOST, idx=-1)
        stop = -1 #done with all data, exit
        self.transfer_variable.target_idx.remote(stop, role=consts.HOST, idx=-1)
        
    def fit(self, data_instances):
        self.read_schema(data_instances)
        self.data_output=self.process(data_instances)
        return self.data_output #data_instances

    def process(self, data_instances):
        data_instances = data_instances.mapValues(self.load_data)
        self.set_schema(data_instances)
        LOGGER.info(self.model_param.ts_idx)
        idx_list = [ self.model_param.ts_idx ]  
        f=functools.partial(HeteroTimeSeriesFeatureExtractionGuest.striptimestamp, idx_list = idx_list)
        time_stamps= data_instances.mapValues(f)
        timestamp_list= list(time_stamps.collect())

        self.process_timestamp_list(timestamp_list)
        self.data_output=data_instances
        return data_instances

    def transform(self, data_instances):
        out = self.fit(data_instances)
        return out
