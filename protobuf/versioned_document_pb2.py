# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protobuf/versioned-document.proto
# Protobuf Python Version: 5.27.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    3,
    '',
    'protobuf/versioned-document.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!protobuf/versioned-document.proto\x12\x12versioned_document\"V\n\x08\x44ocument\x12\x1c\n\x14serializationVersion\x18\x01 \x01(\r\x12,\n\x07version\x18\x02 \x03(\x0b\x32\x1b.versioned_document.Version\"V\n\x07Version\x12\x1c\n\x14serializationVersion\x18\x01 \x01(\r\x12\x1f\n\x17minimumSupportedVersion\x18\x02 \x01(\r\x12\x0c\n\x04\x64\x61ta\x18\x03 \x01(\x0c\x42\x02H\x03')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protobuf.versioned_document_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'H\003'
  _globals['_DOCUMENT']._serialized_start=57
  _globals['_DOCUMENT']._serialized_end=143
  _globals['_VERSION']._serialized_start=145
  _globals['_VERSION']._serialized_end=231
# @@protoc_insertion_point(module_scope)
