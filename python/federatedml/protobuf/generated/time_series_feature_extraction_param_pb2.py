# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: time-series-feature-extraction-param.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='time-series-feature-extraction-param.proto',
  package='com.webank.ai.fate.core.mlmodel.buffer',
  syntax='proto3',
  serialized_options=_b('B%TimeSeriesFeatureExtractionParamProto'),
  serialized_pb=_b('\n*time-series-feature-extraction-param.proto\x12&com.webank.ai.fate.core.mlmodel.buffer\"~\n TimeSeriesFeatureExtractionParam\x12\r\n\x05test1\x18\x01 \x01(\t\x12\r\n\x05test2\x18\x02 \x01(\t\x12\x0e\n\x06header\x18\x03 \x03(\t\x12\x18\n\x10header_anonymous\x18\x04 \x03(\t\x12\x12\n\nmodel_name\x18\x05 \x01(\tB\'B%TimeSeriesFeatureExtractionParamProtob\x06proto3')
)




_TIMESERIESFEATUREEXTRACTIONPARAM = _descriptor.Descriptor(
  name='TimeSeriesFeatureExtractionParam',
  full_name='com.webank.ai.fate.core.mlmodel.buffer.TimeSeriesFeatureExtractionParam',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='test1', full_name='com.webank.ai.fate.core.mlmodel.buffer.TimeSeriesFeatureExtractionParam.test1', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='test2', full_name='com.webank.ai.fate.core.mlmodel.buffer.TimeSeriesFeatureExtractionParam.test2', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='header', full_name='com.webank.ai.fate.core.mlmodel.buffer.TimeSeriesFeatureExtractionParam.header', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='header_anonymous', full_name='com.webank.ai.fate.core.mlmodel.buffer.TimeSeriesFeatureExtractionParam.header_anonymous', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='model_name', full_name='com.webank.ai.fate.core.mlmodel.buffer.TimeSeriesFeatureExtractionParam.model_name', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=86,
  serialized_end=212,
)

DESCRIPTOR.message_types_by_name['TimeSeriesFeatureExtractionParam'] = _TIMESERIESFEATUREEXTRACTIONPARAM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TimeSeriesFeatureExtractionParam = _reflection.GeneratedProtocolMessageType('TimeSeriesFeatureExtractionParam', (_message.Message,), {
  'DESCRIPTOR' : _TIMESERIESFEATUREEXTRACTIONPARAM,
  '__module__' : 'time_series_feature_extraction_param_pb2'
  # @@protoc_insertion_point(class_scope:com.webank.ai.fate.core.mlmodel.buffer.TimeSeriesFeatureExtractionParam)
  })
_sym_db.RegisterMessage(TimeSeriesFeatureExtractionParam)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
