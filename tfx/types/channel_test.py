# Lint as: python2, python3
# Copyright 2019 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for tfx.utils.channel."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# Standard Imports

import tensorflow as tf
from tfx.types.artifact import Artifact
from tfx.types.artifact import Property
from tfx.types.artifact import PropertyType
from tfx.types.channel import Channel


class _MyType(Artifact):
  TYPE_NAME = 'MyTypeName'
  PROPERTIES = {
      'string_value': Property(PropertyType.STRING),
  }


class _AnotherType(Artifact):
  TYPE_NAME = 'AnotherTypeName'


class ChannelTest(tf.test.TestCase):

  def testValidChannel(self):
    instance_a = _MyType()
    instance_b = _MyType()
    chnl = Channel(_MyType, artifacts=[instance_a, instance_b])
    self.assertEqual(chnl.type_name, 'MyTypeName')
    self.assertCountEqual(chnl.get(), [instance_a, instance_b])

  def testInvalidChannelType(self):
    instance_a = _MyType()
    instance_b = _MyType()
    with self.assertRaises(ValueError):
      Channel(_AnotherType, artifacts=[instance_a, instance_b])

  def testStringTypeNameNotAllowed(self):
    with self.assertRaises(ValueError):
      Channel('StringTypeName')

  def testJsonRoundTrip(self):
    channel = Channel(type=_MyType, artifacts=[_MyType()])
    serialized = channel.to_json_dict()
    rehydrated = Channel.from_json_dict(serialized)
    self.assertEqual(channel.mlmd_artifact_type, rehydrated.mlmd_artifact_type)
    self.assertEqual(channel.type_name, rehydrated.type_name)

  def testJsonRoundTripUnknownArtifactClass(self):
    channel = Channel(type=_MyType)

    serialized = channel.to_json_dict()
    serialized['artifact_type']['name'] = 'UnknownTypeName'

    rehydrated = Channel.from_json_dict(serialized)
    self.assertEqual(channel.mlmd_artifact_type.properties,
                     rehydrated.mlmd_artifact_type.properties)
    self.assertEqual('UnknownTypeName', rehydrated.type_name)


if __name__ == '__main__':
  tf.test.main()
