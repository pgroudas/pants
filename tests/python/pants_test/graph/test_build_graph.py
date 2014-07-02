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
from pants.backend.jvm.targets.jvm_target import JvmTarget
from pants.base.address import SyntheticAddress
from pants.base.build_file_parser import BuildFileParser
from pants.base.build_graph import BuildGraph
from pants.base.build_root import BuildRoot
from pants.base.target import Target


class BuildGraphTest(unittest.TestCase):
  @contextmanager
  def workspace(self, *buildfiles):
    with temporary_dir() as root_dir:
      with BuildRoot().temporary(root_dir):
        with pushd(root_dir):
          for buildfile in buildfiles:
            touch(os.path.join(root_dir, buildfile))
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

      parser = BuildFileParser(root_dir=root_dir)
      parser.register_target_alias('fake', Target)
      build_graph = BuildGraph()
      parser.inject_spec_closure_into_build_graph(':foo', build_graph)
      self.assertEqual(len(build_graph.dependencies_of(SyntheticAddress.parse(':foo'))), 1)

  def test_resources_of(self):
    with self.workspace('a/BUILD') as root_dir:

      with open(os.path.join(root_dir, 'a/BUILD'), 'w') as build:
        build.write(dedent('''
          fake(name="a",
               resources=['a:foo-res'],
               )
          fake_resources(name='foo-res',
                         sources=[]
                         )
        '''))
      parser = BuildFileParser(root_dir=root_dir)
      parser.register_target_alias('fake', JvmTarget)
      parser.register_target_alias('fake_resources', Resources)
      build_graph = BuildGraph()
      parser.inject_spec_closure_into_build_graph('a', build_graph)
      self.assertEquals(build_graph.resources_for(SyntheticAddress.parse('a:a')),
                        set([SyntheticAddress.parse('a:foo-res')]))

  def test_add_resources(self):
    with self.workspace('a/BUILD') as root_dir:

      with open(os.path.join(root_dir, 'a/BUILD'), 'w') as build:
        build.write(dedent('''
          fake(name="a",
               resources=['a:foo-res'],
               )
          fake_resources(name='foo-res',
                         sources=[]
                         )
        '''))
      parser = BuildFileParser(root_dir=root_dir)
      parser.register_target_alias('fake', JvmTarget)
      parser.register_target_alias('fake_resources', Resources)
      build_graph = BuildGraph()
      parser.inject_spec_closure_into_build_graph('a', build_graph)

      resource_tgt = build_graph.get_target(SyntheticAddress.parse('a:foo-res'))
      build_graph.inject_synthetic_target(address=SyntheticAddress.parse('a:syn-res'),
                                          target_type=Resources,
                                          derived_from=resource_tgt)
      build_graph.add_resource(SyntheticAddress.parse('a'),
                               SyntheticAddress.parse('a:syn-res'))

      self.assertEquals(build_graph.resources_for(SyntheticAddress.parse('a:a')),
                        set([SyntheticAddress.parse('a:syn-res')]))

      syn_resources = Resources(name='syn-res',
                               address=SyntheticAddress.parse('a:syn-res'),
                               build_graph=build_graph,
                               sources=[])
      build_graph.inject_synthetic_target(address=SyntheticAddress.parse('a:syn-syn-res'),
                                          target_type=Resources,
                                          derived_from=syn_resources)
      build_graph.add_resource(SyntheticAddress.parse('a'),
                               SyntheticAddress.parse('a:syn-syn-res'))
      self.assertEquals(build_graph.resources_for(SyntheticAddress.parse('a:a')),
                        set([SyntheticAddress.parse('a:syn-syn-res')]))
