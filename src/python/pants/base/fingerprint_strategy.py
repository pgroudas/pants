# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)


class FingerprintStrategy(object):
  @classmethod
  def name(cls):
    raise NotImplemented

  def compute_fingerprint(self, target):
    raise NotImplemented

  def fingerprint_target(self, target):
    return '{fingerprint}-{name}'.format(fingerprint=self.compute_fingerprint(target),
                                         name=self.name())


class DefaultFingerprintStrategy(FingerprintStrategy):
  @classmethod
  def name(cls):
    return 'default'

  def compute_fingerprint(self, target):
    return target.payload.invalidation_hash()
