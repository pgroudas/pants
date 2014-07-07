# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import argparse
import sys


class CommandLineParser(object):
  def __init__(self, option_registry):
    self._option_registry = option_registry
    self._args = []  # The args to parse, in reverse order.

  def parse(self, args=None):
    self._args = list(reversed(sys.argv if args is None else args))

  def _consume_arg(self):
    return self._args.pop()

  def _consume_flag(self):
    flag = self._consume_arg()
    if flag.startswith('--'):
      name, _, val = flag[2:].partition('=')
      option = self._option_registry.get(name)
    elif flag.startswith('-'):
      name = flag[1:]
      option = self._option_registry.get(name)
      val = None
