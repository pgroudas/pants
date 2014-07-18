# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import shlex
import unittest

from twitter.common.lang import Compatibility

from pants.option.options import Options


class OptionsTest(unittest.TestCase):
  _known_scopes = ['compile', 'compile.java', 'compile.scala', 'test', 'test.junit']

  def _register(self, options):
    options.register_global_boolean('-v', '--verbose', action='store_true', help='Verbose output.')
    options.register_global_boolean('-x', '--xlong', action='store_true')
    # Override -x with a different type.
    options.register('test', '--xlong', type=int)

  def _parse(self, args):
    if isinstance(args, Compatibility.string):
      args = shlex.split(str(args))
    options = Options(OptionsTest._known_scopes, args)
    self._register(options)
    return options

  def test_arg_scoping(self):
    # Some basic smoke tests.
    options = self._parse('./pants --verbose')
    self.assertEqual(True, options.for_global_scope().verbose)
    self.assertEqual(True, options.for_global_scope().v)
    options = self._parse('./pants -v compile tgt')
    self.assertEqual(['tgt'], options.targets)
    self.assertEqual(True, options.for_global_scope().verbose)
    self.assertEqual(True, options.for_global_scope().v)

    # Scoping of different values of the same option.
    options = self._parse('./pants --verbose compile --no-verbose compile.java -v')
    self.assertEqual(True, options.for_global_scope().verbose)
    self.assertEqual(False, options.for_scope('compile').verbose)
    self.assertEqual(True, options.for_scope('compile.java').verbose)

    # Proper shadowing of a re-registered flag.  The flag's alias retains its old meaning.
    options = self._parse('./pants --no-xlong test --xlong=100 -x')
    self.assertEqual(False, options.for_global_scope().xlong)
    self.assertEqual(False, options.for_global_scope().x)
    self.assertEqual(100, options.for_scope('test').xlong)
    self.assertEqual(True, options.for_scope('test').x)
