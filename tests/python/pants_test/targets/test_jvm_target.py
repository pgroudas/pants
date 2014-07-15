# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from textwrap import dedent

from pants.backend.core.targets.resources import Resources
from pants.backend.jvm.targets.jvm_target import JvmTarget
from pants.base.address import SyntheticAddress
from pants.base.build_file_aliases import BuildFileAliases
from pants_test.base_test import BaseTest


class JvmTargetTest(BaseTest):
  @property
  def alias_groups(self):
    return BuildFileAliases.create(
      targets={
        'jvm_target': JvmTarget,
        'fake_resources': Resources,
      })

  def test_resources(self):
    self.add_to_build_file('a', dedent('''
      jvm_target(name="jvm-target",
                 resources=[':res'])
      fake_resources(name='res',
                     sources=[])
    '''))
    jvm_lib = self.target('a:jvm-target')
    self.assertEquals(set(jvm_lib.resources), set([self.target('a:res')]))

  def test_resources_after_replacement(self):
    self.add_to_build_file('a', dedent('''
      jvm_target(name="jvm-target",
                 resources=[':res'])
      fake_resources(name='res',
                     sources=[])
    '''))
    resource = self.target('a:res')
    syn_address = SyntheticAddress.parse('a:sync')
    self.build_graph.inject_synthetic_target(address=syn_address,
                                             target_type=Resources,
                                             derived_from=resource)
    self.build_graph.replace_dependency(resource.address, syn_address)
    jvm_lib = self.target('a:jvm-target')
    self.assertEquals(set(jvm_lib.resources), set([self.target('a:res')]))
