# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from twitter.common.lang import AbstractClass


class AddressableCallProxy(object):
  def __init__(self, addressable_type, build_file, registration_callback):
    self._addressable_type = addressable_type
    self._build_file = build_file
    self._registration_callback = registration_callback

  def __call__(self, *args, **kwargs):
    kwargs['build_file'] = self._build_file
    addressable = self._addressable_type(*args, **kwargs)
    if 'name' in kwargs:
      self._registration_callback.add(kwargs['name'], addressable)
    return addressable


class Addressable(AbstractClass):
  pass
