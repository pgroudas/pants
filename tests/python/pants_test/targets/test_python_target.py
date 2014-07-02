# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import os
from textwrap import dedent

import pytest

from pants.backend.core.targets.resources import Resources
from pants.backend.jvm.targets.artifact import Artifact
from pants.backend.jvm.targets.repository import Repository
from pants.backend.python.python_artifact import PythonArtifact
from pants.backend.python.targets.python_library import PythonLibrary
from pants.backend.python.targets.python_target import PythonTarget
from pants.base.address import SyntheticAddress
from pants.base.exceptions import TargetDefinitionException
from pants.base.source_root import SourceRoot
from pants_test.base_test import BaseTest


class PythonTargetTest(BaseTest):

  def setUp(self):
    super(PythonTargetTest, self).setUp()
    SourceRoot.register(os.path.realpath(os.path.join(self.build_root, 'test_python_target')),
                        PythonTarget)

    self.add_to_build_file('test_thrift_replacement', dedent('''
      python_thrift_library(name='one',
        sources=['thrift/keyword.thrift']
      )
    '''))

  def test_validation(self):

    self.make_target(spec=':internal',
                     target_type=Repository,
                     url=None,
                     push_db=None,
                     exclusives=None)
    # Adding a JVM Artifact as a provides on a PythonTarget doesn't make a lot of sense.
    # This test sets up that very scenario, and verifies that pants throws a
    # TargetDefinitionException.
    with pytest.raises(TargetDefinitionException):
      self.make_target(target_type=PythonTarget,
                       spec=":one",
                       provides=Artifact(org='com.twitter', name='one-jar', repo=':internal'))

    spec = ":test-with-PythonArtifact"
    pa = PythonArtifact(name='foo', version='1.0', description='foo')

    # This test verifies that adding a 'setup_py' provides to a PythonTarget is okay.
    pt_with_artifact = self.make_target(spec=spec,
                                        target_type=PythonTarget,
                                        provides=pa)
    self.assertEquals(pt_with_artifact.address.spec, spec)

    spec = ":test-with-none"
    # This test verifies that having no provides is okay.
    pt_no_artifact = self.make_target(spec=spec,
                                      target_type=PythonTarget,
                                      provides=None)
    self.assertEquals(pt_no_artifact.address.spec, spec)

  def test_resources(self):
    self.add_to_build_file('a', dedent('''
      python_library(name="py-lib",
                     resource_targets=[':py-res'],
                     resources=['a.txt'],
                    )
      fake_resources(name='py-res',
                     sources=[]
                    )
    '''))

    self.build_file_parser.register_target_alias('python_library', PythonLibrary)
    self.build_file_parser.register_target_alias('fake_resources', Resources)
    py_lib = self.target('a:py-lib')

    synthetic_resources = Resources(name='py-lib_synthetic_resources',
                                    address=SyntheticAddress.parse('a:py-lib_synthetic_resources'),
                                    build_graph=self.build_graph,
                                    sources=['a.txt'])
    self.assertEquals(set(py_lib.resources), set([self.target('a:py-res'), synthetic_resources]))
