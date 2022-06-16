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

import functools
import operator

from federatedml.cipher_compressor import compressor
from federatedml.feature.hetero_time_series_feature_extraction.base_time_series_feature_extraction import BaseTimeSeriesFeatureExtraction
from federatedml.secureprotol import PaillierEncrypt
from federatedml.secureprotol.fate_paillier import PaillierEncryptedNumber
from federatedml.util import LOGGER
from federatedml.util import consts
from fate_arch.session import computing_session
from federatedml.feature.instance import Instance
import numpy as np
import time

class HeteroTimeSeriesFeatureExtractionHost(BaseTimeSeriesFeatureExtraction):
    def fit(self, data_instances):
        self.read_schema(data_instances)
        out=self.process(data_instances)
        self.data_output= out 
        self.set_schema(out)
        return out 

    def check_ts_range(self, msg, cipher):
        x1 = msg[0]
        x2 = msg[1]
        x3 = cipher.decrypt(msg[2])

        if(x1 < x3 and x3 > x2) or (x1 > x3 and x3 > x2):
            return True
        return False

    @staticmethod
    def agg_mean(mat):
        return mat.mean(axis=0)
    
    @staticmethod
    def agg_max(mat):
        return mat.max(axis=0)
     
    @staticmethod
    def agg_min(mat):
        return mat.min(axis=0)
     
    @staticmethod
    def agg_count(mat):
        return len(mat)

    @staticmethod
    def agg_sum(mat):
        return mat.sum(axis=0)

    @staticmethod 
    def agg_unique_count(mat):
        num_features = len(mat[0])
        res = []
        for i in range(num_features):
            unique_count = len(np.unique(mat[:,i]))
            res.append(unique_count)
        return res

    def aggregation(self, target_id, data_id, data_features, static_features):
        num_samples = len(data_features)
        LOGGER.info(num_samples)
        method =self.model_param.method
        if num_samples == 0:
            new_features = [0] * (self.num_new_features)
            feature_array = np.array(new_features)
        else:
            ts_features = data_features[0][1].features[self.model_param.tsf_cols].reshape(1,-1)
            for i in range(num_samples-1):
                f_i = data_features[i+1][1].features[self.model_param.tsf_cols].reshape(1, -1)
                ts_features = np.concatenate((ts_features, f_i), axis=0)
            for m in method:
                if m == consts.TS_DCOUNT:
                    new_features = self.agg_unique_count(ts_features)
                elif m == consts.TS_MEAN:
                    new_features = self.agg_mean(ts_features)
                elif m == consts.TS_SUM:
                    new_features = self.agg_sum(ts_features)
                elif m == consts.TS_MAX:
                    new_features = self.agg_max(ts_features)
                elif m == consts.TS_MIN:
                    new_features = self.agg_min(ts_features)
                elif m == consts.TS_COUNT:
                    new_features = self.agg_count(ts_features)
                else:
                    LOGGER.error("Unsupported method")
                
                try:    feature_array = np.append(feature_array, np.array(new_features))
                except: feature_array = np.array(new_features)

        feature_array = np.append(static_features, feature_array)
        instance = Instance(inst_id=data_id, features=feature_array)
        return (target_id, instance)

    def process_header(self):
        method = self.model_param.method 
        headers = self.header
        new_header = []
        for i in self.static_features_col: #non-time series target columns
            new_header.append(headers[i])
        for m in method:
            if m == consts.TS_COUNT:
                new_header.append(m) #only 1 feature for all features
                continue
            for i in self.model_param.tsf_cols:
                header = headers[i]
                header = str(header) + "_" + m #'_unique_count'
                new_header.append(header)
        self.header = new_header 
        self.num_new_features = len(new_header) - len(self.static_features_col)

    def process(self, data_instances):
        data_instances = data_instances.mapValues(self.load_data)
        self.static_features_col = list(set(self.model_param.target_cols)-set(self.model_param.tsf_cols))
        self.process_header()
        run = True
        end = -1 #end signal for GUEST side
        cipher = PaillierEncrypt()
        cipher.generate_key(1024)
        start = time.time()
        ts_idx = self.model_param.ts_idx
        while run:
            receive_idx = self.transfer_variable.target_idx.get(idx=-1)[0]
            LOGGER.info(receive_idx)
            yes_range = [0,0]
            no_ts = []
            if receive_idx == -1:  #check stop condition
                run = False
                break
            target_idx = receive_idx.split("_")[0]
            filtered_samples = data_instances.filter(lambda k,v: k.split("_")[0]==target_idx)
            filtered_list  = list(filtered_samples.collect())
            test_res = []
            calculation_list = []
            if len(filtered_list) == 0:
                static_features = [0] * len(self.static_features_col)
            else:
                static_features = np.array(filtered_list[0][1].features[self.static_features_col].reshape(1, -1)) #static features
            for i in filtered_list:
                ts = int(i[1].features[ts_idx])
                bigger=False
                check=True
                if ts in no_ts:
                    res=False
                    check=False
                if ts > yes_range[0]:
                    bigger=True
                    if ts < yes_range[1]:
                        res=True
                        check=False
                if check:
                    encrypted_ts = cipher.encrypt(ts)
                    self.transfer_variable.encrypted_time_stamp.remote(encrypted_ts, role=consts.GUEST, idx=-1)
                    msg=self.transfer_variable.function_val.get(idx=-1)
                    res = self.check_ts_range(msg[0], cipher)
                    if res:
                        if yes_range[0] == 0:
                            yes_range = [ts-100, ts+100]
                        if bigger:
                            yes_range[1] = ts+100  #reduce multiple checks
                        else:
                            yes_range[0] = ts-100
                    else:
                        no_ts.append(ts)
                test_res.append(res)
                if res: 
                    calculation_list.append(i)

            new_entry = self.aggregation(receive_idx, target_idx, calculation_list, static_features)
            self.new_data.append(new_entry)
            self.transfer_variable.encrypted_time_stamp.remote(end, role=consts.GUEST, idx=-1)
            bottom=time.time()
            LOGGER.info(bottom - start)
        return computing_session.parallelize(self.new_data, include_key=True, partition=2)


    def transform(self, data_instances):
        self.fit(data_instances)
