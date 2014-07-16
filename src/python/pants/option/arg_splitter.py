# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import sys


class ArgSplitterError(Exception):
  pass


class ArgSplitter(object):
  def __init__(self, known_scopes):
    self._known_scopes = known_scopes
    self._unconsumed_args = []  # In reverse order, for efficient consumption from the end.

  def split_args(self, args=None):
    scope_to_flags = {}
    targets = []

    self._unconsumed_args = list(reversed(sys.argv if args is None else args))[:-1]
    if self._unconsumed_args and self._unconsumed_args[-1] == 'goal':
      print("WARNING: The word 'goal' is superfluous and deprecated.")
      self._unconsumed_args.pop()

    global_flags = self._consume_flags()
    scope_to_flags[''] = global_flags
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
    if target.startswith(b'-'):  # Special-case check for what may be a common error.
      raise ArgSplitterError('Invalid target name: %s. Flags cannot appear here.' % target)
    return target

  def _at_flag(self):
    return (self._unconsumed_args and
            self._unconsumed_args[-1].startswith(b'-') and
            not self._at_double_dash())

  def _at_scope(self):
    return self._unconsumed_args and self._unconsumed_args[-1] in self._known_scopes

  def _at_double_dash(self):
    return self._unconsumed_args and self._unconsumed_args[-1] == b'--'
