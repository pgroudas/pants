# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from collections import defaultdict

from pants.option.option import Option
from pants.option.option_error import OptionError


class OptionRegistry(object):
  def __init__(self):
    self._registry_by_scope = defaultdict(dict)

  def register(self,
               scope,
               name,
               type,
               default=None,
               config_section='DEFAULT',
               help=''):
    options_for_scope = self._registry_by_scope[scope]
    if name in options_for_scope:
      raise OptionError('Option %s already registered in scope %s' % (name, scope))
    options_for_scope[name] = Option(name, type, default, config_section, help)

  def get(self, scope, name):
    options_for_scope = self._registry_by_scope[scope]
    if name not in options_for_scope:
      raise OptionError('No such option in scope %s: %s' % (scope, name))
    return options_for_scope[name]