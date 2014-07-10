# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import sys

class OptionParser(object):
  def __init__(self, known_scopes):
    self._known_scopes = known_scopes
    self._unconsumed_args = []  # In reverse order, for efficient consumption from the end.
    self._error = None

  def parse(self, args=None):
    scope_to_flags = {}
    targets = []

    self._unconsumed_args = list(sys.argv[1:] if args is None else args).reverse()
    if self._unconsumed_args[-1] == 'goal':
      print("WARNING: The word 'goal' is superfluous and deprecated.")
      self._unconsumed_args.pop()

    scope_to_flags[''] = self._consume_flags()  # Global scope.
    scope, flags = self._consume_scope()
    while scope:
      scope_to_flags[scope] = flags
      scope, flags = self._consume_scope()

    if self._at_double_dash():
      self._unconsumed_args.pop()

    target = self._consume_target()
    while target:
      targets.append(target)
      target = self._consume_target()

    return scope_to_flags, targets

  def _consume_scope(self):
    if not self._at_scope():
      return None, []
    scope = self._unconsumed_args.pop()
    flags = self._consume_flags()
    return scope, flags

  def _consume_flags(self):
    flags = []
    while self._at_flag():
      flags.append(self._unconsumed_args.pop())
    return flags

  def _consume_target(self):
    if not self._unconsumed_args:
      return None
    target = self._unconsumed_args.pop()
    if target.startswith('-'):  # Special-case check for what may be a common error.
      self._error = 'Invalid target name: %s. Flags cannot appear here.' % target
      return None
    return target

  def _at_flag(self):
    return (self._unconsumed_args and
            self._unconsumed_args[-1].startswith('-') and
            not self._at_double_dash())

  def _at_scope(self):
    return self._unconsumed_args and self._unconsumed_args[-1] in self._known_scopes

  def _at_double_dash(self):
    return self._unconsumed_args and self._unconsumed_args[-1] == '--'
