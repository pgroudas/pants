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

  def _do_parse(self, args):
    parser = OptionParser(OptionParserTest._known_scopes)
    if isinstance(args, Compatibility.string):
      args = shlex.split(args)
    parser.parse(args)

  def test_parser(self):
    self._do_parse('./pants goal')


