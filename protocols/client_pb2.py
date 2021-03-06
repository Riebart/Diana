# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: client.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='client.proto',
  package='client',
  serialized_pb='\n\x0c\x63lient.proto\x12\x06\x63lient\"\xcf\x02\n\x0eMessageWrapper\x12\x37\n\x0bmessageType\x18\x01 \x02(\x0e\x32\".client.MessageWrapper.MessageType\x12$\n\tthrustMsg\x18\n \x01(\x0b\x32\x11.client.ThrustMsg\x12(\n\x0bvelocityMsg\x18\x0b \x01(\x0b\x32\x13.client.VelocityMsg\x12 \n\x07jumpMsg\x18\x0c \x01(\x0b\x32\x0f.client.JumpMsg\x12 \n\x07infoMsg\x18\r \x01(\x0b\x32\x0f.client.InfoMsg\x12&\n\nrequestMsg\x18\x0e \x01(\x0b\x32\x12.client.RequestMsg\"H\n\x0bMessageType\x12\n\n\x06THRUST\x10\n\x12\x0c\n\x08VELOCITY\x10\x0b\x12\x08\n\x04JUMP\x10\x0c\x12\x08\n\x04INFO\x10\r\x12\x0b\n\x07REQUEST\x10\x0e\",\n\tVectorMsg\x12\t\n\x01x\x18\x01 \x02(\x01\x12\t\n\x01y\x18\x02 \x02(\x01\x12\t\n\x01z\x18\x03 \x02(\x01\"D\n\tThrustMsg\x12\x14\n\x04name\x18\x01 \x01(\t:\x06THRUST\x12!\n\x06thrust\x18\x02 \x02(\x0b\x32\x11.client.VectorMsg\"J\n\x0bVelocityMsg\x12\x16\n\x04name\x18\x01 \x01(\t:\x08VELOCITY\x12#\n\x08velocity\x18\x02 \x02(\x0b\x32\x11.client.VectorMsg\"F\n\x07JumpMsg\x12\x12\n\x04name\x18\x01 \x01(\t:\x04JUMP\x12\'\n\x0cnew_position\x18\x02 \x02(\x0b\x32\x11.client.VectorMsg\"=\n\x07InfoMsg\x12\x12\n\x04name\x18\x01 \x01(\t:\x04INFO\x12\x10\n\x08infoType\x18\x02 \x02(\t\x12\x0c\n\x04\x64\x61ta\x18\x03 \x02(\t\"L\n\nRequestMsg\x12\x15\n\x04name\x18\x01 \x01(\t:\x07REQUEST\x12\x12\n\ncontinuous\x18\x02 \x02(\x05\x12\x13\n\x0brequestType\x18\x03 \x02(\t')



_MESSAGEWRAPPER_MESSAGETYPE = _descriptor.EnumDescriptor(
  name='MessageType',
  full_name='client.MessageWrapper.MessageType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='THRUST', index=0, number=10,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VELOCITY', index=1, number=11,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='JUMP', index=2, number=12,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INFO', index=3, number=13,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REQUEST', index=4, number=14,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=288,
  serialized_end=360,
)


_MESSAGEWRAPPER = _descriptor.Descriptor(
  name='MessageWrapper',
  full_name='client.MessageWrapper',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='messageType', full_name='client.MessageWrapper.messageType', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=10,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='thrustMsg', full_name='client.MessageWrapper.thrustMsg', index=1,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='velocityMsg', full_name='client.MessageWrapper.velocityMsg', index=2,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='jumpMsg', full_name='client.MessageWrapper.jumpMsg', index=3,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='infoMsg', full_name='client.MessageWrapper.infoMsg', index=4,
      number=13, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='requestMsg', full_name='client.MessageWrapper.requestMsg', index=5,
      number=14, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _MESSAGEWRAPPER_MESSAGETYPE,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=25,
  serialized_end=360,
)


_VECTORMSG = _descriptor.Descriptor(
  name='VectorMsg',
  full_name='client.VectorMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='client.VectorMsg.x', index=0,
      number=1, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='y', full_name='client.VectorMsg.y', index=1,
      number=2, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='z', full_name='client.VectorMsg.z', index=2,
      number=3, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=362,
  serialized_end=406,
)


_THRUSTMSG = _descriptor.Descriptor(
  name='ThrustMsg',
  full_name='client.ThrustMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='client.ThrustMsg.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=unicode("THRUST", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='thrust', full_name='client.ThrustMsg.thrust', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=408,
  serialized_end=476,
)


_VELOCITYMSG = _descriptor.Descriptor(
  name='VelocityMsg',
  full_name='client.VelocityMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='client.VelocityMsg.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=unicode("VELOCITY", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='velocity', full_name='client.VelocityMsg.velocity', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=478,
  serialized_end=552,
)


_JUMPMSG = _descriptor.Descriptor(
  name='JumpMsg',
  full_name='client.JumpMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='client.JumpMsg.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=unicode("JUMP", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='new_position', full_name='client.JumpMsg.new_position', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=554,
  serialized_end=624,
)


_INFOMSG = _descriptor.Descriptor(
  name='InfoMsg',
  full_name='client.InfoMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='client.InfoMsg.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=unicode("INFO", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='infoType', full_name='client.InfoMsg.infoType', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data', full_name='client.InfoMsg.data', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=626,
  serialized_end=687,
)


_REQUESTMSG = _descriptor.Descriptor(
  name='RequestMsg',
  full_name='client.RequestMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='client.RequestMsg.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=unicode("REQUEST", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='continuous', full_name='client.RequestMsg.continuous', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='requestType', full_name='client.RequestMsg.requestType', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=689,
  serialized_end=765,
)

_MESSAGEWRAPPER.fields_by_name['messageType'].enum_type = _MESSAGEWRAPPER_MESSAGETYPE
_MESSAGEWRAPPER.fields_by_name['thrustMsg'].message_type = _THRUSTMSG
_MESSAGEWRAPPER.fields_by_name['velocityMsg'].message_type = _VELOCITYMSG
_MESSAGEWRAPPER.fields_by_name['jumpMsg'].message_type = _JUMPMSG
_MESSAGEWRAPPER.fields_by_name['infoMsg'].message_type = _INFOMSG
_MESSAGEWRAPPER.fields_by_name['requestMsg'].message_type = _REQUESTMSG
_MESSAGEWRAPPER_MESSAGETYPE.containing_type = _MESSAGEWRAPPER;
_THRUSTMSG.fields_by_name['thrust'].message_type = _VECTORMSG
_VELOCITYMSG.fields_by_name['velocity'].message_type = _VECTORMSG
_JUMPMSG.fields_by_name['new_position'].message_type = _VECTORMSG
DESCRIPTOR.message_types_by_name['MessageWrapper'] = _MESSAGEWRAPPER
DESCRIPTOR.message_types_by_name['VectorMsg'] = _VECTORMSG
DESCRIPTOR.message_types_by_name['ThrustMsg'] = _THRUSTMSG
DESCRIPTOR.message_types_by_name['VelocityMsg'] = _VELOCITYMSG
DESCRIPTOR.message_types_by_name['JumpMsg'] = _JUMPMSG
DESCRIPTOR.message_types_by_name['InfoMsg'] = _INFOMSG
DESCRIPTOR.message_types_by_name['RequestMsg'] = _REQUESTMSG

class MessageWrapper(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _MESSAGEWRAPPER

  # @@protoc_insertion_point(class_scope:client.MessageWrapper)

class VectorMsg(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _VECTORMSG

  # @@protoc_insertion_point(class_scope:client.VectorMsg)

class ThrustMsg(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _THRUSTMSG

  # @@protoc_insertion_point(class_scope:client.ThrustMsg)

class VelocityMsg(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _VELOCITYMSG

  # @@protoc_insertion_point(class_scope:client.VelocityMsg)

class JumpMsg(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _JUMPMSG

  # @@protoc_insertion_point(class_scope:client.JumpMsg)

class InfoMsg(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _INFOMSG

  # @@protoc_insertion_point(class_scope:client.InfoMsg)

class RequestMsg(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _REQUESTMSG

  # @@protoc_insertion_point(class_scope:client.RequestMsg)


# @@protoc_insertion_point(module_scope)
