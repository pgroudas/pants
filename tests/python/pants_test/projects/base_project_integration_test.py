# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

import os

from pants_test.pants_run_integration_test import PantsRunIntegrationTest


class ProjectIntegrationTest(PantsRunIntegrationTest):
  @staticmethod
  def _android_flags():
    exclude_android = os.environ.get('SKIP_ANDROID') == "true" or not os.environ.get('ANDROID_HOME')
    return ['--exclude-target-regexp=.*android.*'] if exclude_android else []

  def pants_test(self, strategy, command):
    return self.run_pants([
      'test'
      '--compile-apt-strategy={}'.format(strategy),
      '--compile-java-strategy={}'.format(strategy),
      '--compile-scala-strategy={}'.format(strategy),
    ] + command + self._android_flags())
