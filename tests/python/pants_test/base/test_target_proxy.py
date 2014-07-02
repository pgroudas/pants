# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from pants.backend.jvm.targets.java_library import JavaLibrary
from pants.backend.python.targets.python_library import PythonLibrary
from pants.base.build_file import BuildFile
from pants.base.build_file_parser import TargetProxy

from pants_test.base_test import BaseTest


class TargetProxyTest(BaseTest):

  def test_target_proxy_init_python_target(self):

    kwargs = {'name': 'foo',
              'resources': ['a.txt'],
              }
    with self.workspace('./BUILD') as root_dir:
      target_proxy = TargetProxy(PythonLibrary,
                                 BuildFile(root_dir, 'BUILD'),
                                 [],
                                 kwargs)
      self.assertEqual(target_proxy.resources, [])

      kwargs['resource_targets'] = [':foo']
      target_proxy = TargetProxy(PythonLibrary,
                                 BuildFile(root_dir, 'BUILD'),
                                 [],
                                 kwargs)
      self.assertEqual(target_proxy.resources, [':foo'])

  def test_target_proxy_init_jvm_target(self):
    kwargs = {'name': 'foo',
              'resources': [':foo'],
              }
    with self.workspace('./BUILD') as root_dir:
      target_proxy = TargetProxy(JavaLibrary,
                                 BuildFile(root_dir, 'BUILD'),
                                 [],
                                 kwargs)
      self.assertEqual(target_proxy.resources, [':foo'])
