# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protobuf/topotext.proto
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
    'protobuf/topotext.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x17protobuf/topotext.proto\x12\x08topotext\"\xc6\x01\n\x06String\x12\x0e\n\x06string\x18\x02 \x01(\t\x12&\n\tsubstring\x18\x03 \x03(\x0b\x32\x13.topotext.Substring\x12,\n\ttimestamp\x18\x04 \x01(\x0b\x32\x19.topotext.VectorTimestamp\x12,\n\x0c\x61ttributeRun\x18\x05 \x03(\x0b\x32\x16.topotext.AttributeRun\x12(\n\nattachment\x18\x06 \x03(\x0b\x32\x14.topotext.Attachment\"\xd5\x01\n\x0fVectorTimestamp\x12.\n\x05\x63lock\x18\x01 \x03(\x0b\x32\x1f.topotext.VectorTimestamp.Clock\x1a\x91\x01\n\x05\x43lock\x12\x13\n\x0breplicaUUID\x18\x01 \x01(\x0c\x12\x42\n\x0creplicaClock\x18\x02 \x03(\x0b\x32,.topotext.VectorTimestamp.Clock.ReplicaClock\x1a/\n\x0cReplicaClock\x12\r\n\x05\x63lock\x18\x01 \x01(\r\x12\x10\n\x08subclock\x18\x02 \x01(\r\"*\n\x06\x43harID\x12\x11\n\treplicaID\x18\x01 \x01(\r\x12\r\n\x05\x63lock\x18\x02 \x01(\r\"\x84\x01\n\tSubstring\x12 \n\x06\x63harID\x18\x01 \x01(\x0b\x32\x10.topotext.CharID\x12\x0e\n\x06length\x18\x02 \x01(\r\x12#\n\ttimestamp\x18\x03 \x01(\x0b\x32\x10.topotext.CharID\x12\x11\n\ttombstone\x18\x04 \x01(\x08\x12\r\n\x05\x63hild\x18\x05 \x03(\r\"\xf0\x01\n\tSelection\x12\x13\n\x0breplicaUUID\x18\x01 \x03(\x0c\x12(\n\x05range\x18\x02 \x03(\x0b\x32\x19.topotext.Selection.Range\x12.\n\x08\x61\x66\x66inity\x18\x03 \x01(\x0e\x32\x1c.topotext.Selection.Affinity\x1aM\n\x05Range\x12\"\n\x08\x66romChar\x18\x01 \x01(\x0b\x32\x10.topotext.CharID\x12 \n\x06toChar\x18\x02 \x01(\x0b\x32\x10.topotext.CharID\"%\n\x08\x41\x66\x66inity\x12\x0c\n\x08\x42\x61\x63kward\x10\x00\x12\x0b\n\x07\x46orward\x10\x01\"\xf4\x03\n\x0c\x41ttributeRun\x12\x0e\n\x06length\x18\x01 \x01(\r\x12\x30\n\x0eparagraphStyle\x18\x02 \x01(\x0b\x32\x18.topotext.ParagraphStyle\x12\x1c\n\x04\x66ont\x18\x03 \x01(\x0b\x32\x0e.topotext.Font\x12\x11\n\tfontHints\x18\x05 \x01(\r\x12\x11\n\tunderline\x18\x06 \x01(\r\x12\x15\n\rstrikethrough\x18\x07 \x01(\r\x12\x13\n\x0bsuperscript\x18\x08 \x01(\x05\x12\x0c\n\x04link\x18\t \x01(\t\x12\x1e\n\x05\x63olor\x18\n \x01(\x0b\x32\x0f.topotext.Color\x12\x41\n\x10writingDirection\x18\x0b \x01(\x0e\x32\'.topotext.AttributeRun.WritingDirection\x12\x30\n\x0e\x61ttachmentInfo\x18\x0c \x01(\x0b\x32\x18.topotext.AttachmentInfo\x12\x11\n\ttimestamp\x18\r \x01(\x04\"|\n\x10WritingDirection\x12\x14\n\x10NaturalDirection\x10\x00\x12\x0f\n\x0bLeftToRight\x10\x01\x12\x0f\n\x0bRightToLeft\x10\x02\x12\x17\n\x13LeftToRightOverride\x10\x03\x12\x17\n\x13RightToLeftOverride\x10\x04\":\n\x04\x46ont\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\tpointSize\x18\x02 \x01(\x02\x12\x11\n\tfontHints\x18\x03 \x01(\r\"\xc9\x02\n\x0eParagraphStyle\x12\r\n\x05style\x18\x01 \x01(\r\x12\x35\n\talignment\x18\x02 \x01(\x0e\x32\".topotext.ParagraphStyle.Alignment\x12\x41\n\x10writingDirection\x18\x03 \x01(\x0e\x32\'.topotext.AttributeRun.WritingDirection\x12\x0e\n\x06indent\x18\x04 \x01(\x05\x12\x1c\n\x04todo\x18\x05 \x01(\x0b\x32\x0e.topotext.Todo\x12\x16\n\x0eparagraphHints\x18\x06 \x01(\r\x12\x1e\n\x16startingListItemNumber\x18\x07 \x01(\r\"H\n\tAlignment\x12\x08\n\x04Left\x10\x00\x12\n\n\x06\x43\x65nter\x10\x01\x12\t\n\x05Right\x10\x02\x12\r\n\tJustified\x10\x03\x12\x0b\n\x07Natural\x10\x04\"?\n\x0e\x41ttachmentInfo\x12\x1c\n\x14\x61ttachmentIdentifier\x18\x01 \x01(\t\x12\x0f\n\x07typeUTI\x18\x02 \x01(\t\"\x9d\x07\n\nAttachment\x12\x12\n\nidentifier\x18\x02 \x01(\t\x12\x15\n\rmergeableData\x18\x03 \x01(\x0c\x12\x12\n\nsizeHeight\x18\x04 \x01(\x02\x12\x11\n\tsizeWidth\x18\x05 \x01(\x02\x12\x0f\n\x07summary\x18\x06 \x01(\t\x12\r\n\x05title\x18\x07 \x01(\t\x12\x0f\n\x07typeUTI\x18\x08 \x01(\t\x12\x11\n\turlString\x18\t \x01(\t\x12$\n\x08location\x18\n \x01(\x0b\x32\x12.topotext.Location\x12\x1e\n\x05media\x18\x0b \x01(\x0b\x32\x0f.topotext.Media\x12\'\n\x07preview\x18\x0c \x03(\x0b\x32\x16.topotext.PreviewImage\x12\x0f\n\x07originX\x18\r \x01(\x02\x12\x0f\n\x07originY\x18\x0e \x01(\x02\x12\x13\n\x0borientation\x18\x0f \x01(\x05\x12\x19\n\x11previewUpdateDate\x18\x10 \x01(\x01\x12\x18\n\x10modificationDate\x18\x11 \x01(\x01\x12\x15\n\rremoteFileURL\x18\x12 \x01(\t\x12\x1a\n\x12\x63heckedForLocation\x18\x13 \x01(\x08\x12\x10\n\x08\x66ileSize\x18\x14 \x01(\x03\x12\x10\n\x08\x64uration\x18\x15 \x01(\x01\x12\x17\n\x0fimageFilterType\x18\x16 \x01(\x05\x12\x17\n\x0fmarkupModelData\x18\x17 \x01(\x0c\x12+\n\rsubAttachment\x18\x18 \x03(\x0b\x32\x14.topotext.Attachment\x12$\n\x1cminimumSupportedNotesVersion\x18\x19 \x01(\x03\x12\x1f\n\x17\x63roppingQuadBottomLeftX\x18\x1a \x01(\x01\x12\x1f\n\x17\x63roppingQuadBottomLeftY\x18\x1b \x01(\x01\x12 \n\x18\x63roppingQuadBottomRightX\x18\x1c \x01(\x01\x12 \n\x18\x63roppingQuadBottomRightY\x18\x1d \x01(\x01\x12\x1c\n\x14\x63roppingQuadTopLeftX\x18\x1e \x01(\x01\x12\x1c\n\x14\x63roppingQuadTopLeftY\x18\x1f \x01(\x01\x12\x1d\n\x15\x63roppingQuadTopRightX\x18  \x01(\x01\x12\x1d\n\x15\x63roppingQuadTopRightY\x18! \x01(\x01\x12\x14\n\x0cmetadataData\x18\" \x01(\x0c\x12\x11\n\tuserTitle\x18# \x01(\t\x12\x19\n\x11\x66\x61llbackImageData\x18$ \x01(\x0c\"X\n\x08Location\x12\x10\n\x08latitude\x18\x01 \x01(\x01\x12\x11\n\tlongitude\x18\x02 \x01(\x01\x12\x11\n\tplacemark\x18\x03 \x01(\x0c\x12\x14\n\x0cplaceUpdated\x18\x04 \x01(\x08\"|\n\x05Media\x12\x12\n\nidentifier\x18\x01 \x01(\t\x12\x19\n\x11\x66ilenameExtension\x18\x02 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x03 \x01(\x0c\x12\x10\n\x08\x66ilename\x18\x04 \x01(\t\x12$\n\x1cminimumSupportedNotesVersion\x18\x05 \x01(\x03\"\xa8\x01\n\x0cPreviewImage\x12\r\n\x05scale\x18\x01 \x01(\x02\x12\x18\n\x10scaleWhenDrawing\x18\x02 \x01(\x08\x12\x0c\n\x04\x64\x61ta\x18\x03 \x01(\x0c\x12\x10\n\x08metadata\x18\x04 \x01(\x0c\x12\x0f\n\x07version\x18\x05 \x01(\x05\x12\x18\n\x10versionOutOfDate\x18\x06 \x01(\x08\x12$\n\x1cminimumSupportedNotesVersion\x18\x07 \x01(\x03\"&\n\x04Todo\x12\x10\n\x08todoUUID\x18\x01 \x01(\x0c\x12\x0c\n\x04\x64one\x18\x02 \x01(\x08\"@\n\x05\x43olor\x12\x0b\n\x03red\x18\x01 \x01(\x02\x12\r\n\x05green\x18\x02 \x01(\x02\x12\x0c\n\x04\x62lue\x18\x03 \x01(\x02\x12\r\n\x05\x61lpha\x18\x04 \x01(\x02\x42\x02H\x03')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protobuf.topotext_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'H\003'
  _globals['_STRING']._serialized_start=38
  _globals['_STRING']._serialized_end=236
  _globals['_VECTORTIMESTAMP']._serialized_start=239
  _globals['_VECTORTIMESTAMP']._serialized_end=452
  _globals['_VECTORTIMESTAMP_CLOCK']._serialized_start=307
  _globals['_VECTORTIMESTAMP_CLOCK']._serialized_end=452
  _globals['_VECTORTIMESTAMP_CLOCK_REPLICACLOCK']._serialized_start=405
  _globals['_VECTORTIMESTAMP_CLOCK_REPLICACLOCK']._serialized_end=452
  _globals['_CHARID']._serialized_start=454
  _globals['_CHARID']._serialized_end=496
  _globals['_SUBSTRING']._serialized_start=499
  _globals['_SUBSTRING']._serialized_end=631
  _globals['_SELECTION']._serialized_start=634
  _globals['_SELECTION']._serialized_end=874
  _globals['_SELECTION_RANGE']._serialized_start=758
  _globals['_SELECTION_RANGE']._serialized_end=835
  _globals['_SELECTION_AFFINITY']._serialized_start=837
  _globals['_SELECTION_AFFINITY']._serialized_end=874
  _globals['_ATTRIBUTERUN']._serialized_start=877
  _globals['_ATTRIBUTERUN']._serialized_end=1377
  _globals['_ATTRIBUTERUN_WRITINGDIRECTION']._serialized_start=1253
  _globals['_ATTRIBUTERUN_WRITINGDIRECTION']._serialized_end=1377
  _globals['_FONT']._serialized_start=1379
  _globals['_FONT']._serialized_end=1437
  _globals['_PARAGRAPHSTYLE']._serialized_start=1440
  _globals['_PARAGRAPHSTYLE']._serialized_end=1769
  _globals['_PARAGRAPHSTYLE_ALIGNMENT']._serialized_start=1697
  _globals['_PARAGRAPHSTYLE_ALIGNMENT']._serialized_end=1769
  _globals['_ATTACHMENTINFO']._serialized_start=1771
  _globals['_ATTACHMENTINFO']._serialized_end=1834
  _globals['_ATTACHMENT']._serialized_start=1837
  _globals['_ATTACHMENT']._serialized_end=2762
  _globals['_LOCATION']._serialized_start=2764
  _globals['_LOCATION']._serialized_end=2852
  _globals['_MEDIA']._serialized_start=2854
  _globals['_MEDIA']._serialized_end=2978
  _globals['_PREVIEWIMAGE']._serialized_start=2981
  _globals['_PREVIEWIMAGE']._serialized_end=3149
  _globals['_TODO']._serialized_start=3151
  _globals['_TODO']._serialized_end=3189
  _globals['_COLOR']._serialized_start=3191
  _globals['_COLOR']._serialized_end=3255
# @@protoc_insertion_point(module_scope)
