# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import shlex
import unittest

from twitter.common.lang import Compatibility

from pants.option.option_parser import OptionParser


class OptionParserTest(unittest.TestCase):
  _known_scopes = ['foo', 'foo.bar', 'baz.bar', 'qux.quux']

  def _do_parse(self, args, expected_scope_to_flags, expected_targets):
    parser = OptionParser(OptionParserTest._known_scopes)
    if isinstance(args, Compatibility.string):
      args = shlex.split(args)
    scope_to_flags, targets = parser.parse(args)
    self.assertEquals(expected_scope_to_flags, scope_to_flags)
    self.assertEquals(expected_targets, targets)

  def test_parser(self):
    self._do_parse('./pants', {}, [])
    self._do_parse('./pants goal', {}, [])
    self._do_parse('./pants -f', {'': ['-f']}, [])
    self._do_parse('./pants goal -f', {'': ['-f']}, [])


