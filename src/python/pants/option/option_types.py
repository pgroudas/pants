# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)


from pants.option.option_error import OptionError


class Enum(object):
  def __init__(self, *args):
    self._allowed_values = list(*args)

  def __call__(self, val):
    if val not in self._allowed_values:
      raise OptionError('%s not one of [%s]' % (val, ', '.join(self._allowed_values)))

enum = Enum




# TODO(benjy): Are argv entries are indeed str (not unicode) in python2?
VALID_TYPES = (str, int, float, enum)

def validate_type(typ):
  if type not in VALID_TYPES:
    raise OptionError('Invalid option type: %s' % typ)