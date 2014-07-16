# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from argparse import ArgumentParser
import copy

class RegistrationError(Exception):
  pass


class Parser(object):
  """A parser in a scoped hierarchy.

  Options registered on a parser are also registered on all the parsers in enclosed scopes.
  Registration must be in outside-in order: we forbid registering options on an outer scope if
  we've already registered an option on one of its inner scopes. This is to ensure that
  re-registering the same option name on an inner scope correctly replaces the option inherited
  from the outer scope.
  """
  def __init__(self, scope, parent_parser):
    self._scope = scope
    self._locked = False
    self._argparser = ArgumentParser(conflict_handler='resolve')
    self._parent_parser = parent_parser  # A Parser instance, or None for the global scope parser.
    self._child_parsers = []  # List of Parser instances.
    if self._parent_parser:
      self._parent_parser._child_parsers.append(self)

  def parse_args(self, args, namespace):
    return self._argparser.parse_args(args, namespace)

  def register(self, *args, **kwargs):
    if self._locked:
      raise RegistrationError('Cannot register option %s in scope %s after registering options '
                              'in any of its inner scopes.' % (args[0], self._scope))
    # We no longer allow registration in enclosing scopes.
    if self._parent_parser:
      self._parent_parser._lock()
    self._register(*args, **kwargs)

  def register_boolean(self, *args, **kwargs):
    if self._locked:
      raise RegistrationError('Cannot register option %s in scope %s after registering options '
                              'in any of its inner scopes.' % (args[0], self._scope))
    # We no longer allow registration in enclosing scopes.
    if self._parent_parser:
      self._parent_parser._lock()

    action = kwargs.get('action')
    if action not in ('store_false', 'store_true'):
      raise RegistrationError('Invalid action for boolean flag: %s' % action)
    inverse_action = 'store_true' if action == 'store_false' else 'store_false'

    inverse_args = []
    for flag in args:
      if flag.startswith('--'):
        inverse_args.append('--no-' + flag[2:])

    if inverse_args:
      inverse_kwargs = copy.copy(kwargs)
      inverse_kwargs['action'] = inverse_action
      self._register_boolean(args, kwargs, inverse_args, inverse_kwargs)
    else:
      self._register(*args, **kwargs)

  def _register(self, *args, **kwargs):
    self._argparser.add_argument(*args, **kwargs)
    # Propagate registration down to inner scopes.
    for child_parser in self._child_parsers:
      child_parser._register(*args, **kwargs)

  def _register_boolean(self, args, kwargs, inverse_args, inverse_kwargs):
    group = self._argparser.add_mutually_exclusive_group()
    action = group.add_argument(*args, **kwargs)
    # Ensure the synthetic inverse flag has the same dest (with the opposite action).
    if 'dest' not in inverse_kwargs:
      inverse_kwargs['dest'] = action.dest
    group.add_argument(*inverse_args, **inverse_kwargs)

    # Propagate registration down to inner scopes.
    for child_parser in self._child_parsers:
      child_parser._register_boolean(args, kwargs, inverse_args, inverse_kwargs)

  def _lock(self):
    if not self._locked:
      self._locked = True
      if self._parent_parser:
        self._parent_parser._lock()

  def __str__(self):
    return 'Parser(%s)' % self._scope


class ParserHierarchy(object):
  def __init__(self, all_scopes):
    # Sorting ensures that ancestors preceed descendants.
    all_scopes = sorted(set(list(all_scopes) + ['']))
    self._parser_by_scope = {}
    for scope in all_scopes:
      parent_parser = None if scope == '' else self._parser_by_scope[scope.rpartition('.')[0]]
      self._parser_by_scope[scope] = Parser(scope, parent_parser)

  def get_parser_by_scope(self, scope):
    return self._parser_by_scope[scope]
