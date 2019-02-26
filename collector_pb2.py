# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: collector.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='collector.proto',
  package='drago.services.collector',
  syntax='proto3',
  serialized_pb=_b('\n\x0f\x63ollector.proto\x12\x18\x64rago.services.collector\"\"\n\x06\x45ntity\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\"\x1b\n\x03Geo\x12\x14\n\x0c\x62ounding_box\x18\x01 \x03(\x01\"\xa0\x01\n\x04Rule\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x04term\x18\xe8\x07 \x01(\tH\x00\x12\x0e\n\x03url\x18\xe9\x07 \x01(\tH\x00\x12\x33\n\x06\x65ntity\x18\xea\x07 \x01(\x0b\x32 .drago.services.collector.EntityH\x00\x12-\n\x03geo\x18\xeb\x07 \x01(\x0b\x32\x1d.drago.services.collector.GeoH\x00\x42\x07\n\x05value\"6\n\x05Rules\x12-\n\x05rules\x18\x01 \x03(\x0b\x32\x1e.drago.services.collector.Rule\"\xf9\x01\n\x0cTaskResponse\x12,\n\x04rule\x18\x01 \x01(\x0b\x32\x1e.drago.services.collector.Rule\x12<\n\x05\x65rror\x18\xe8\x07 \x01(\x0e\x32,.drago.services.collector.TaskResponse.Error\"}\n\x05\x45rror\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x08\n\x04NONE\x10\x01\x12\x14\n\x0fINVALID_REQUEST\x10\xe8\x07\x12\x12\n\rINVALID_VALUE\x10\xe9\x07\x12\x16\n\x11RULE_ID_NOT_FOUND\x10\xea\x07\x12\x1b\n\x16RULE_COLLECTION_FAILED\x10\xd0\x0f\"J\n\rTaskResponses\x12\x39\n\tresponses\x18\x01 \x03(\x0b\x32&.drago.services.collector.TaskResponse2\x96\x04\n\tCollector\x12V\n\x0cValidateRule\x12\x1e.drago.services.collector.Rule\x1a&.drago.services.collector.TaskResponse\x12S\n\tStartRule\x12\x1e.drago.services.collector.Rule\x1a&.drago.services.collector.TaskResponse\x12R\n\x08StopRule\x12\x1e.drago.services.collector.Rule\x1a&.drago.services.collector.TaskResponse\x12Y\n\rValidateRules\x12\x1f.drago.services.collector.Rules\x1a\'.drago.services.collector.TaskResponses\x12V\n\nStartRules\x12\x1f.drago.services.collector.Rules\x1a\'.drago.services.collector.TaskResponses\x12U\n\tStopRules\x12\x1f.drago.services.collector.Rules\x1a\'.drago.services.collector.TaskResponsesBj\n\"com.qntfy.drago.services.collectorB\x13\x44GOCollectorServiceH\x01P\x01Z%gitlab.qntfy.com/qcr/drago/collection\xa2\x02\x03\x44GOb\x06proto3')
)



_TASKRESPONSE_ERROR = _descriptor.EnumDescriptor(
  name='Error',
  full_name='drago.services.collector.TaskResponse.Error',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NONE', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_REQUEST', index=2, number=1000,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_VALUE', index=3, number=1001,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RULE_ID_NOT_FOUND', index=4, number=1002,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RULE_COLLECTION_FAILED', index=5, number=2000,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=454,
  serialized_end=579,
)
_sym_db.RegisterEnumDescriptor(_TASKRESPONSE_ERROR)


_ENTITY = _descriptor.Descriptor(
  name='Entity',
  full_name='drago.services.collector.Entity',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='drago.services.collector.Entity.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='drago.services.collector.Entity.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=45,
  serialized_end=79,
)


_GEO = _descriptor.Descriptor(
  name='Geo',
  full_name='drago.services.collector.Geo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='bounding_box', full_name='drago.services.collector.Geo.bounding_box', index=0,
      number=1, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=81,
  serialized_end=108,
)


_RULE = _descriptor.Descriptor(
  name='Rule',
  full_name='drago.services.collector.Rule',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='drago.services.collector.Rule.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='term', full_name='drago.services.collector.Rule.term', index=1,
      number=1000, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='url', full_name='drago.services.collector.Rule.url', index=2,
      number=1001, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='entity', full_name='drago.services.collector.Rule.entity', index=3,
      number=1002, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='geo', full_name='drago.services.collector.Rule.geo', index=4,
      number=1003, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='value', full_name='drago.services.collector.Rule.value',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=111,
  serialized_end=271,
)


_RULES = _descriptor.Descriptor(
  name='Rules',
  full_name='drago.services.collector.Rules',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='rules', full_name='drago.services.collector.Rules.rules', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=273,
  serialized_end=327,
)


_TASKRESPONSE = _descriptor.Descriptor(
  name='TaskResponse',
  full_name='drago.services.collector.TaskResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='rule', full_name='drago.services.collector.TaskResponse.rule', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='error', full_name='drago.services.collector.TaskResponse.error', index=1,
      number=1000, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _TASKRESPONSE_ERROR,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=330,
  serialized_end=579,
)


_TASKRESPONSES = _descriptor.Descriptor(
  name='TaskResponses',
  full_name='drago.services.collector.TaskResponses',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='responses', full_name='drago.services.collector.TaskResponses.responses', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=581,
  serialized_end=655,
)

_RULE.fields_by_name['entity'].message_type = _ENTITY
_RULE.fields_by_name['geo'].message_type = _GEO
_RULE.oneofs_by_name['value'].fields.append(
  _RULE.fields_by_name['term'])
_RULE.fields_by_name['term'].containing_oneof = _RULE.oneofs_by_name['value']
_RULE.oneofs_by_name['value'].fields.append(
  _RULE.fields_by_name['url'])
_RULE.fields_by_name['url'].containing_oneof = _RULE.oneofs_by_name['value']
_RULE.oneofs_by_name['value'].fields.append(
  _RULE.fields_by_name['entity'])
_RULE.fields_by_name['entity'].containing_oneof = _RULE.oneofs_by_name['value']
_RULE.oneofs_by_name['value'].fields.append(
  _RULE.fields_by_name['geo'])
_RULE.fields_by_name['geo'].containing_oneof = _RULE.oneofs_by_name['value']
_RULES.fields_by_name['rules'].message_type = _RULE
_TASKRESPONSE.fields_by_name['rule'].message_type = _RULE
_TASKRESPONSE.fields_by_name['error'].enum_type = _TASKRESPONSE_ERROR
_TASKRESPONSE_ERROR.containing_type = _TASKRESPONSE
_TASKRESPONSES.fields_by_name['responses'].message_type = _TASKRESPONSE
DESCRIPTOR.message_types_by_name['Entity'] = _ENTITY
DESCRIPTOR.message_types_by_name['Geo'] = _GEO
DESCRIPTOR.message_types_by_name['Rule'] = _RULE
DESCRIPTOR.message_types_by_name['Rules'] = _RULES
DESCRIPTOR.message_types_by_name['TaskResponse'] = _TASKRESPONSE
DESCRIPTOR.message_types_by_name['TaskResponses'] = _TASKRESPONSES
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Entity = _reflection.GeneratedProtocolMessageType('Entity', (_message.Message,), dict(
  DESCRIPTOR = _ENTITY,
  __module__ = 'collector_pb2'
  # @@protoc_insertion_point(class_scope:drago.services.collector.Entity)
  ))
_sym_db.RegisterMessage(Entity)

Geo = _reflection.GeneratedProtocolMessageType('Geo', (_message.Message,), dict(
  DESCRIPTOR = _GEO,
  __module__ = 'collector_pb2'
  # @@protoc_insertion_point(class_scope:drago.services.collector.Geo)
  ))
_sym_db.RegisterMessage(Geo)

Rule = _reflection.GeneratedProtocolMessageType('Rule', (_message.Message,), dict(
  DESCRIPTOR = _RULE,
  __module__ = 'collector_pb2'
  # @@protoc_insertion_point(class_scope:drago.services.collector.Rule)
  ))
_sym_db.RegisterMessage(Rule)

Rules = _reflection.GeneratedProtocolMessageType('Rules', (_message.Message,), dict(
  DESCRIPTOR = _RULES,
  __module__ = 'collector_pb2'
  # @@protoc_insertion_point(class_scope:drago.services.collector.Rules)
  ))
_sym_db.RegisterMessage(Rules)

TaskResponse = _reflection.GeneratedProtocolMessageType('TaskResponse', (_message.Message,), dict(
  DESCRIPTOR = _TASKRESPONSE,
  __module__ = 'collector_pb2'
  # @@protoc_insertion_point(class_scope:drago.services.collector.TaskResponse)
  ))
_sym_db.RegisterMessage(TaskResponse)

TaskResponses = _reflection.GeneratedProtocolMessageType('TaskResponses', (_message.Message,), dict(
  DESCRIPTOR = _TASKRESPONSES,
  __module__ = 'collector_pb2'
  # @@protoc_insertion_point(class_scope:drago.services.collector.TaskResponses)
  ))
_sym_db.RegisterMessage(TaskResponses)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\"com.qntfy.drago.services.collectorB\023DGOCollectorServiceH\001P\001Z%gitlab.qntfy.com/qcr/drago/collection\242\002\003DGO'))

_COLLECTOR = _descriptor.ServiceDescriptor(
  name='Collector',
  full_name='drago.services.collector.Collector',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=658,
  serialized_end=1192,
  methods=[
  _descriptor.MethodDescriptor(
    name='ValidateRule',
    full_name='drago.services.collector.Collector.ValidateRule',
    index=0,
    containing_service=None,
    input_type=_RULE,
    output_type=_TASKRESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='StartRule',
    full_name='drago.services.collector.Collector.StartRule',
    index=1,
    containing_service=None,
    input_type=_RULE,
    output_type=_TASKRESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='StopRule',
    full_name='drago.services.collector.Collector.StopRule',
    index=2,
    containing_service=None,
    input_type=_RULE,
    output_type=_TASKRESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='ValidateRules',
    full_name='drago.services.collector.Collector.ValidateRules',
    index=3,
    containing_service=None,
    input_type=_RULES,
    output_type=_TASKRESPONSES,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='StartRules',
    full_name='drago.services.collector.Collector.StartRules',
    index=4,
    containing_service=None,
    input_type=_RULES,
    output_type=_TASKRESPONSES,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='StopRules',
    full_name='drago.services.collector.Collector.StopRules',
    index=5,
    containing_service=None,
    input_type=_RULES,
    output_type=_TASKRESPONSES,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_COLLECTOR)

DESCRIPTOR.services_by_name['Collector'] = _COLLECTOR

# @@protoc_insertion_point(module_scope)