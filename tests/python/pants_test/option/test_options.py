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
    options.register_global('-e', '--explain', action='store_true', help='Explain goal execution.')
    options.register('compile', '-n', '--no-cache', action='store_true', help="Don't use artifact cache.")

  def _parse(self, args):
    if isinstance(args, Compatibility.string):
      args = shlex.split(str(args))
    options = Options(OptionsTest._known_scopes, args)
    self._register(options)
    return options

  def test_arg_splitting(self):
    options = self._parse('./pants -e compile src/java/com/pants/example')
    self.assertEqual(['src/java/com/pants/example'], options.targets)
    self.assertEqual(True, options.for_global_scope().explain)

    options = self._parse('./pants --explain compile src/java/com/pants/example')
    self.assertEqual(['src/java/com/pants/example'], options.targets)
    self.assertEqual(True, options.for_global_scope().explain)

