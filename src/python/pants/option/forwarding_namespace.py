# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)


class ForwardingNamespace(object):
  """An object that optionally forwards attribute access to another attribute.

  An attribute can be registered as forwarding to another attribute, and attempts
  to read that attribute's value will be forwarded to the other attribute. All
  other attributes will be read directly, as usual.

  Note that if the forwarding attribute is also set directly, the direct value overrides.
  """
  def __init__(self):
    self._forwardings = {}

  def add_forwardings(self, forwardings):
    self._forwardings.update(forwardings)

  def __getattr__(self, key):
    """Called only if regular attribute lookup fails"""
    if key not in self._forwardings:
      raise AttributeError('No such forwarded attribute: %s' % key)
    return getattr(self, self._forwardings[key])