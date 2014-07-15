# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import os
import unittest
from contextlib import contextmanager
from textwrap import dedent

from twitter.common.contextutil import pushd, temporary_dir
from twitter.common.dirutil import touch

from pants.backend.core.targets.resources import Resources
from pants.backend.jvm.targets.java_library import JavaLibrary
from pants.base.address import SyntheticAddress
from pants.base.build_configuration import BuildConfiguration
from pants.base.build_file_parser import BuildFileParser
from pants.base.build_graph import BuildGraph
from pants.base.build_root import BuildRoot


class BuildGraphTest(unittest.TestCase):
  @contextmanager
  def workspace(self, *buildfiles):
    with temporary_dir() as root_dir:
      with BuildRoot().temporary(root_dir):
        with pushd(root_dir):
          for buildfile in buildfiles:
            touch(os.path.join(root_dir, buildfile))
          build_configuration = BuildConfiguration()
          build_configuration.register_target_alias('fake', JavaLibrary)
          build_configuration.register_target_alias('resources', Resources)
          self.parser = BuildFileParser(build_configuration, root_dir=root_dir)
          self.build_graph = BuildGraph()
          yield os.path.realpath(root_dir)

  def test_transitive_closure_spec(self):
    with self.workspace('./BUILD', 'a/BUILD', 'a/b/BUILD') as root_dir:
      with open(os.path.join(root_dir, './BUILD'), 'w') as build:
        build.write(dedent('''
          fake(name="foo",
               dependencies=[
                 'a',
               ])
        '''))

      with open(os.path.join(root_dir, 'a/BUILD'), 'w') as build:
        build.write(dedent('''
          fake(name="a",
               dependencies=[
                 'a/b:bat',
               ])
        '''))

      with open(os.path.join(root_dir, 'a/b/BUILD'), 'w') as build:
        build.write(dedent('''
          fake(name="bat")
        '''))
      self.parser.inject_spec_closure_into_build_graph(':foo', self.build_graph)
      self.assertEqual(len(self.build_graph.dependencies_of(SyntheticAddress.parse(':foo'))), 1)

  def test_build_graph_res_dependencies(self):
    with self.workspace('./BUILD') as root_dir:
      with open(os.path.join(root_dir, './BUILD'), 'w') as build:
        build.write(dedent('''
          fake(name="foo",
               dependencies=[],
               resources=[
                 ':res',
               ])
          resources(name="res",
                    sources=[])
        '''))

      self.parser.inject_spec_closure_into_build_graph(':foo', self.build_graph)
      self.assertEqual(self.build_graph.dependencies_of(SyntheticAddress.parse(':foo')),
                       set([SyntheticAddress.parse(':res')]))

  def test_build_graph_replace_dependency(self):
    with self.workspace('./BUILD') as root_dir:
      with open(os.path.join(root_dir, './BUILD'), 'w') as build:
        build.write(dedent('''
          fake(name="foo",
               dependencies=[],
               resources=[
                 ':res',
               ])
          resources(name="res",
                    sources=[])
        '''))
      self.parser.inject_spec_closure_into_build_graph(':foo', self.build_graph)
      resource = self.build_graph.get_target(SyntheticAddress.parse(':res'))
      syn_address = SyntheticAddress.parse(':sync')
      self.build_graph.inject_synthetic_target(address=syn_address,
                                               target_type=Resources,
                                               derived_from=resource)
      self.build_graph.replace_dependency(resource.address, syn_address)
      self.assertEqual(self.build_graph.dependencies_of(SyntheticAddress.parse(':foo')),
                       set([SyntheticAddress.parse(':sync')]))
