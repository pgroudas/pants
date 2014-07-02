# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from textwrap import dedent

from pants.backend.core.targets.resources import Resources
from pants.backend.jvm.targets.jvm_target import JvmTarget
from pants_test.base_test import BaseTest


class JvmTargetTest(BaseTest):
  def test_resources(self):
    self.add_to_build_file('a', dedent('''
      jvm_target(name="jvm-target",
                 resources=[':res'],
                    )
      fake_resources(name='res',
                     sources=[]
                    )
    '''))

    self.build_file_parser.register_target_alias('jvm_target', JvmTarget)
    self.build_file_parser.register_target_alias('fake_resources', Resources)
    jvm_lib = self.target('a:jvm-target')
    self.assertEquals(set(jvm_lib.resources), set([self.target('a:res')]))
