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
    self._locked = False  # If True, no more registration is allowed on this parser.
    self._argparser = ArgumentParser(conflict_handler='resolve')
    self._dest_forwardings = {}  # arg to dest.
    self._parent_parser = parent_parser  # A Parser instance, or None for the global scope parser.
    self._child_parsers = []  # List of Parser instances.
    if self._parent_parser:
      self._parent_parser._child_parsers.append(self)

  def parse_args(self, args, namespace):
    namespace.add_forwardings(self._dest_forwardings)
    return self._argparser.parse_args(args, namespace)

  def register(self, *args, **kwargs):
    if self._locked:
      raise RegistrationError('Cannot register option %s in scope %s after registering options '
                              'in any of its inner scopes.' % (args[0], self._scope))
    # Prevent further registration in enclosing scopes.
    if self._parent_parser:
      self._parent_parser._lock()
    self._set_dest(args, kwargs)
    self._register(args, kwargs)

  def register_boolean(self, *args, **kwargs):
    if self._locked:
      raise RegistrationError('Cannot register option %s in scope %s after registering options '
                              'in any of its inner scopes.' % (args[0], self._scope))
    # Prevent further registration in enclosing scopes.
    if self._parent_parser:
      self._parent_parser._lock()
    self._set_dest(args, kwargs)

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
      self._register(args, kwargs)

  def _register(self, args, kwargs):
    self._argparser.add_argument(*args, **kwargs)
    # Propagate registration down to inner scopes.
    for child_parser in self._child_parsers:
      child_parser._register(args, kwargs)

  def _register_boolean(self, args, kwargs, inverse_args, inverse_kwargs):
    group = self._argparser.add_mutually_exclusive_group()
    group.add_argument(*args, **kwargs)
    group.add_argument(*inverse_args, **inverse_kwargs)

    # Propagate registration down to inner scopes.
    for child_parser in self._child_parsers:
      child_parser._register_boolean(args, kwargs, inverse_args, inverse_kwargs)

  def _set_dest(self, args, kwargs):
    """Maps the externally-used dest to a scoped one only seen internally.

    If an option is re-registered in an inner scope, it'll shadow the external dest but will
    use a different internal one. This is important in the case that an option is registered
    with two names (say -x, --xlong) and we only re-register one of them, say --xlong, in an
    inner scope. In this case we no longer want them to write to the same dest, so that
    we can use both (now with different meanings) in the inner scope.
    """
    dest = kwargs.get('dest')
    if dest is None:
      # Replicated from the dest inference logic in argparse:
      # '--foo-bar' -> 'foo_bar' and '-x' -> 'x'.
      arg = next((a for a in args if a.startswith('--')), args[0])
      dest = arg.lstrip('-').replace('-', '_')
    scoped_dest = '_%s_%s__' % (self._scope, dest)
    kwargs['dest'] = scoped_dest
    self._dest_forwardings[dest] = scoped_dest
    # Also forward all option aliases, so there's still a way to reference -x (as options.x)
    # in the example above.
    for arg in args:
      self._dest_forwardings[arg.lstrip('-').replace('-', '_')] = scoped_dest

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
