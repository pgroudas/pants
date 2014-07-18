# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import copy
import sys

from pants.option.arg_splitter import ArgSplitter
from pants.option.forwarding_namespace import ForwardingNamespace
from pants.option.parser_hierarchy import ParserHierarchy


class OptionError(Exception):
  pass


class Options(object):
  def __init__(self, known_scopes, args=sys.argv):
    splitter = ArgSplitter(known_scopes)
    self._scope_to_flags, self._targets = splitter.split_args(args)
    self._parser_hierarchy = ParserHierarchy(known_scopes)
    self._values_by_scope = {}  # Arg values, parsed per-scope on demand.

  @property
  def targets(self):
    return self._targets

  def register_global(self, *args, **kwargs):
    self.register('', *args, **kwargs)

  def register_global_boolean(self, *args, **kwargs):
    self.register_boolean('', *args, **kwargs)

  def register(self, scope, *args, **kwargs):
    self._parser_hierarchy.get_parser_by_scope(scope).register(*args, **kwargs)

  def register_boolean(self, scope, *args, **kwargs):
    self._parser_hierarchy.get_parser_by_scope(scope).register_boolean(*args, **kwargs)

  def for_global_scope(self):
    return self.for_scope('')

  def for_scope(self, scope):
    # Short-circuit, if already computed.
    if scope in self._values_by_scope:
      return self._values_by_scope[scope]

    # First get enclosing scope's option values, if any.
    if scope == '':
      values = ForwardingNamespace()
    else:
      values = copy.deepcopy(self.for_scope(scope.rpartition('.')[0]))

    # Now add our values.
    flags_in_scope = self._scope_to_flags.get(scope, [])
    self._parser_hierarchy.get_parser_by_scope(scope).parse_args(flags_in_scope, values)
    self._values_by_scope[scope] = values
    return values
