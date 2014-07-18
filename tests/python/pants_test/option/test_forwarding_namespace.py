# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import unittest

from pants.option.forwarding_namespace import ForwardingNamespace


class ForwardingNamespaceTest(unittest.TestCase):
  def test_indirection(self):
    ns = ForwardingNamespace()
    ns.add_forwardings({'foo': 'bar'})
    ns.bar = 1
    self.assertEqual(1, ns.foo)
    ns.bar = 2
    self.assertEqual(2, ns.foo)

    ns.add_forwardings({'baz': 'qux'})
    ns.qux = 3
    self.assertEqual(2, ns.foo)
    self.assertEqual(3, ns.baz)

    # Direct setting overrides forwarding.
    ns.foo = 4
    self.assertEqual(4, ns.foo)