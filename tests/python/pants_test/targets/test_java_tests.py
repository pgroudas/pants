# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import pytest

from pants.backend.jvm.targets.java_tests import JavaTests
from pants_test.base_test import BaseTest


class JavaTestsTest(BaseTest):
  @property
  def alias_groups(self):
    return {
      'target_aliases': {
        'junit_tests': JavaTests,
      },
    }

  def test_none(self):
    self.add_to_build_file('default', '''junit_tests(name='default', sources=None)''')
    with pytest.raises(ValueError):
      self.build_file_parser.scan(self.build_root)

  def test_empty(self):
    self.add_to_build_file('default', '''junit_tests(name='default', sources=[])''')
    with pytest.raises(ValueError):
      self.build_file_parser.scan(self.build_root)
