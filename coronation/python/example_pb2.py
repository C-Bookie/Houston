# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: example.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rexample.proto\"~\n\x0eReceiveRequest\x12\x0c\n\x04size\x18\x01 \x01(\x05\x12)\n\x04type\x18\x02 \x01(\x0e\x32\x1b.ReceiveRequest.RequestType\"3\n\x0bRequestType\x12\x12\n\x0eReceiveRequest\x10\x00\x12\x10\n\x0cLightRequest\x10\x02\"4\n\x08RGBValue\x12\x0b\n\x03red\x18\x01 \x01(\x05\x12\r\n\x05green\x18\x02 \x01(\x05\x12\x0c\n\x04\x62lue\x18\x03 \x01(\x05\"N\n\x0cLightRequest\x12\x0e\n\x06lights\x18\x01 \x01(\x05\x12\x0e\n\x06offset\x18\x02 \x01(\x05\x12\x1e\n\x0bvalue_array\x18\x03 \x03(\x0b\x32\t.RGBValue\"\x1b\n\x0cSensorReport\x12\x0b\n\x03pot\x18\x01 \x01(\x05\"\r\n\x0b\x41\x63knowledgeb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'example_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _RECEIVEREQUEST._serialized_start=17
  _RECEIVEREQUEST._serialized_end=143
  _RECEIVEREQUEST_REQUESTTYPE._serialized_start=92
  _RECEIVEREQUEST_REQUESTTYPE._serialized_end=143
  _RGBVALUE._serialized_start=145
  _RGBVALUE._serialized_end=197
  _LIGHTREQUEST._serialized_start=199
  _LIGHTREQUEST._serialized_end=277
  _SENSORREPORT._serialized_start=279
  _SENSORREPORT._serialized_end=306
  _ACKNOWLEDGE._serialized_start=308
  _ACKNOWLEDGE._serialized_end=321
# @@protoc_insertion_point(module_scope)