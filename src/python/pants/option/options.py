# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from argparse import ArgumentParser
from collections import defaultdict
import sys

from pants.option.arg_splitter import ArgSplitter


class NoSuchOptionError(Exception):
  def __init__(self, scope, name=None):
    if name is None:
      msg = 'Unknown scope %s' % scope
    else:
      msg = 'Unknown option %s in scope %s' % (name, scope)
    super(NoSuchOptionError, self).__init__(msg)


class Options(object):
  def __init__(self, known_scopes, args=sys.argv):
    splitter = ArgSplitter(known_scopes)
    self._scope_to_flags, self._targets = splitter.split_args(args)
    self._argparser_by_scope = defaultdict(ArgumentParser)  # Registered args.
    self._args_by_scope = {}  # Arg values, parsed per-scope on demand.

  @property
  def targets(self):
    return self._targets

  def register_global(self, *args, **kwargs):
    self.register(ArgSplitter.GLOBAL, *args, **kwargs)

  def register(self, scope, *args, **kwargs):
    self._argparser_by_scope[scope].add_argument(*args, **kwargs)

  def for_global_scope(self):
    return self.for_scope(ArgSplitter.GLOBAL)

  def for_scope(self, scope):
    if not scope in self._args_by_scope:
      if not scope in self._argparser_by_scope:
        raise NoSuchOptionError(scope)
      argparser = self._argparser_by_scope[scope]

      flags_in_scope = self._scope_to_flags.get(scope, [])
      args = argparser.parse_args(flags_in_scope)
      self._args_by_scope[scope] = args
    else:
      args = self._args_by_scope[scope]
    return args

