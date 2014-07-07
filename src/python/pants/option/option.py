# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from pants.option.option_types import validate_type


class Option(object):
  def __init__(self,
               name,
               type=str,
               default=None,
               config_section='DEFAULT',
               help=''):
    validate_type(type)
    self._name = name
    self._type = type
    self._default = default
    self._config_section = config_section
    self._help = help

