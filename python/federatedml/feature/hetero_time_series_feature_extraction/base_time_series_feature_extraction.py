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

import copy

import numpy as np

from federatedml.feature.fate_element_type import NoneType
from federatedml.feature.sparse_vector import SparseVector
from federatedml.model_base import ModelBase
from federatedml.param.time_series_feature_extraction_param import HeteroTimeSeriesFeatureExtractionParam as TimeSeriesFeatureExtractionParam
from federatedml.transfer_variable.transfer_class.hetero_time_series_feature_extraction_transfer_variable import \
    HeteroTimeSeriesFeatureExtractionTransferVariable
from federatedml.protobuf.generated import time_series_feature_extraction_meta_pb2,  time_series_feature_extraction_param_pb2
from federatedml.statistic.data_overview import get_header
from federatedml.statistic import data_overview
from federatedml.util import LOGGER
from federatedml.util import abnormal_detection
from federatedml.util import consts
from federatedml.util.io_check import assert_io_num_rows_equal
from federatedml.util.schema_check import assert_schema_consistent

MODEL_PARAM_NAME = 'TimeSeriesFeatureExtractionParam'
MODEL_META_NAME = 'TimeSeriesFeatureExtractionMeta'


class BaseTimeSeriesFeatureExtraction(ModelBase):
    """
    Time Series Feature Extraction function

    """

    def __init__(self):
        super(BaseTimeSeriesFeatureExtraction, self).__init__()
        self.transfer_variable = HeteroTimeSeriesFeatureExtractionTransferVariable()
        self.header = None
        #self.header_anonymous = None
        self.schema = None
        #self.host_results = []
        self.data_shape = None
        self.model_param = TimeSeriesFeatureExtractionParam()
        self.num_features = None
        self.new_data = []
        self.key = None

    def _init_model(self, params): #: TimeSeriesFeatureExtractionParam):
        self.model_param = params
        #self.transform_type = self.model_param.transform_param.transform_type

        #if self.model_param.method == consts.QUANTILE:
        #    self.binning_obj = QuantileBinning(self.model_param)
        #elif self.model_param.method == consts.BUCKET:
        #    self.binning_obj = BucketBinning(self.model_param)
        #elif self.model_param.method == consts.OPTIMAL:
        #    if self.role == consts.HOST:
        #        self.model_param.bin_num = self.model_param.optimal_binning_param.init_bin_nums
        #        self.binning_obj = QuantileBinning(self.model_param)
        #    else:
        #        self.binning_obj = OptimalBinning(self.model_param)
        #else:
            # self.binning_obj = QuantileBinning(self.bin_param)
        #    raise ValueError("Binning method: {} is not supported yet".format(self.model_param.method))
        #LOGGER.debug("in _init_model, role: {}, local_partyid: {}".format(self.role, self.component_properties))
        #self.binning_obj.set_role_party(self.role, self.component_properties.local_partyid)


    def _get_meta(self):
        #pass
        # col_list = [str(x) for x in self.cols]

        #transform_param = feature_binning_meta_pb2.TransformMeta(
        #    transform_cols=self.bin_inner_param.transform_bin_indexes,
            #transform_type=self.model_param.transform_param.transform_type
        #)

        meta_protobuf_obj = time_series_feature_extraction_meta_pb2.TimeSeriesFeatureExtractionMeta(
            method=self.model_param.method,
        #    compress_thres=self.model_param.compress_thres,
        #    head_size=self.model_param.head_size,
        #    error=self.model_param.error,
        #    bin_num=self.model_param.bin_num,
        #    cols=self.bin_inner_param.bin_names,
        #    adjustment_factor=self.model_param.adjustment_factor,
        #    local_only=self.model_param.local_only,
            need_run=self.need_run,
        #    transform_param=transform_param,
            skip_static=self.model_param.skip_static,
            ts_col=self.model_param.ts_col,
            window_size=self.model_param.window_size
        )
        return meta_protobuf_obj

    def _get_param(self):
        pass

        #binning_result_obj = self.binning_obj.bin_results.generated_pb()
        # binning_result_obj = self.bin_results.generated_pb()
        #host_results = [x.bin_results.generated_pb() for x in self.host_results]
        #result_obj = feature_binning_param_pb2. \
        #    FeatureBinningParam(binning_result=binning_result_obj,
        #                        host_results=host_results,
        #                        header=self.header,
        #                        header_anonymous=self.header_anonymous,
        #                        model_name=consts.BINNING_MODEL)

        return result_obj

    def load_model(self, model_dict):
        #pass

        model_param = list(model_dict.get('model').values())[0].get(MODEL_PARAM_NAME)
        model_meta = list(model_dict.get('model').values())[0].get(MODEL_META_NAME)

        #self.bin_inner_param = BinInnerParam()

        assert isinstance(model_meta, time_series_feature_extraction_meta_pb2.TimeSeriesFeatureExtractionMeta)
        assert isinstance(model_param, time_series_feature_extraction_param_pb2.TimeSeriesFeatureExtractionParam)

        #self.header = list(model_param.header)
        #self.bin_inner_param.set_header(self.header)

        #self.bin_inner_param.add_transform_bin_indexes(list(model_meta.transform_param.transform_cols))
        #self.bin_inner_param.add_bin_names(list(model_meta.cols))
        #self.transform_type = model_meta.transform_param.transform_type

        #bin_method = str(model_meta.method)
        #if bin_method == consts.QUANTILE:
        #    self.binning_obj = QuantileBinning(params=model_meta)
        #else:
        #    self.binning_obj = BucketBinning(params=model_meta)

        #self.binning_obj.set_role_party(self.role, self.component_properties.local_partyid)
        #self.binning_obj.set_bin_inner_param(self.bin_inner_param)
        #self.binning_obj.bin_results.reconstruct(model_param.binning_result)

        #self.host_results = []
        #for host_pb in model_param.host_results:
        #    host_bin_obj = BaseBinning()
        #    host_bin_obj.bin_results.reconstruct(host_pb)
        #    self.host_results.append(host_bin_obj)

    def export_model(self):
        pass

        #if self.model_output is not None:
        #    return self.model_output

        #meta_obj = self._get_meta()
        #param_obj = self._get_param()
        #result = {
        #    MODEL_META_NAME: meta_obj,
        #    MODEL_PARAM_NAME: param_obj
        #}
        #self.model_output = result
        #return result

    def save_data(self):
        return self.data_output

    def read_schema(self, data_instance):
        self.schema = data_instance.schema
        self.header = self.schema['header']
        LOGGER.debug("After time series feature extraction, when setting schema, schema is : {}".format(data_instance.schema))

    def set_schema(self, data_instance):
        self.schema['header'] = self.header
        data_instance.schema = self.schema
        LOGGER.debug("After time series feature extraction, when setting schema, schema is : {}".format(data_instance.schema))

    def _abnormal_detection(self, data_instances):
        """
        Make sure input data_instances is valid.
        """
        abnormal_detection.empty_table_detection(data_instances)
        abnormal_detection.empty_feature_detection(data_instances)
        self.check_schema_content(data_instances.schema)

    def load_data(self,data_instance):
        data_instance = copy.deepcopy(data_instance)
        #LOGGER.info("Load data")
        #LOGGER.info(data_instance)
        # Here suppose this is a binary question and the event label is 1
        if data_instance.label != 1:
            data_instance.label = 0
        return data_instance

    def _get_data_shape(self, data_instances):
        if not self.data_shape:
            self.data_shape = data_overview.get_features_shape(data_instances)

    def _get_time_stamp_column_idx(self, data_instances):
        data_shape = self._get_data_shape(data_instances)
        header = get_header(data_instances)
        time_stamp_name = "time_stamp"
        names = set(header).intersection(set(time_stamp_names))
        idx_from_name = list(map(lambda n: header.index(n), names))
        return idx_from_name 

    @staticmethod
    def encrypt(x, cipher):
        f = np.array(x.features,dtype=int)
        res = []
        for i in f:
            res.append(cipher.encrypt(int(f)))
        return res
        return cipher.encrypt(f)
