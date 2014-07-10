# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from argparse import ArgumentParser
from collections import defaultdict


class OptionRegistry(object):
  def __init__(self):
    self._argparser_by_scope = defaultdict(ArgumentParser)

  def register(self, scope, *args, **kwargs):
    self._argparser_by_scope[scope].add_argument(*args, **kwargs)

  def get_argparser_for_scope(self, scope):
    return self._argparser_by_scope.get(scope) or ArgumentParser()
