# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import pytest
import shlex
import unittest

from twitter.common.lang import Compatibility

from pants.option.option_parser import OptionParser, OptionParserError


class OptionParserTest(unittest.TestCase):
  _known_scopes = ['compile', 'compile.java', 'compile.scala', 'test', 'test.junit']

  def _do_parse(self, args, expected_scope_to_flags, expected_targets):
    parser = OptionParser(OptionParserTest._known_scopes)
    if isinstance(args, Compatibility.string):
      args = shlex.split(str(args))
    scope_to_flags, targets = parser.parse(args)
    self.assertEquals(expected_scope_to_flags, scope_to_flags)
    self.assertEquals(expected_targets, targets)

  def _do_error_parse(self, args):
    parser = OptionParser(OptionParserTest._known_scopes)
    if isinstance(args, Compatibility.string):
      args = shlex.split(str(args))
    with pytest.raises(OptionParserError):
      parser.parse(args)

  def test_parser(self):
    # Various flag combos.
    self._do_parse('./pants', {'': []}, [])
    self._do_parse('./pants goal', {'': []}, [])
    self._do_parse('./pants -f', {'': ['-f']}, [])
    self._do_parse('./pants goal -f', {'': ['-f']}, [])
    self._do_parse('./pants -f compile -g compile.java -h test.junit -i '
                   'src/java/com/pants/foo src/java/com/pants/bar:baz',
                   {'': ['-f'], 'compile': ['-g'], 'compile.java': ['-h'], 'test.junit': ['-i']},
                   ['src/java/com/pants/foo', 'src/java/com/pants/bar:baz'])
    self._do_parse('./pants -farg --fff=arg compile --gg-gg=arg-arg -g test.junit --iii '
                   'src/java/com/pants/foo src/java/com/pants/bar:baz',
                   {'': ['-farg', '--fff=arg'], 'compile': ['--gg-gg=arg-arg', '-g'], 'test.junit': ['--iii']},
                   ['src/java/com/pants/foo', 'src/java/com/pants/bar:baz'])

    # Distinguishing goals and targets.
    self._do_parse('./pants compile test foo', {'': [], 'compile': [], 'test': []}, ['foo'])
    self._do_parse('./pants compile test -- foo', {'': [], 'compile': [], 'test': []}, ['foo'])
    self._do_parse('./pants compile -- test', {'': [], 'compile': []}, ['test'])
    self._do_parse('./pants test -- test', {'': [], 'test': []}, ['test'])

    self._do_error_parse('./pants compile -- -f')
    self._do_error_parse('./pants compile -- foo/bar --flag')


