# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import re

import pytest

from mock import Mock

from pants.tasks.jar_publish import JarPublish
from pants.tasks.task_error import TaskError
from pants_test.base_build_root_test import BaseBuildRootTest
from pants_test.tasks.test_base import prepare_task


class JarPublishTest(BaseBuildRootTest):

  @classmethod
  def setUpClass(cls):
    super(JarPublishTest, cls).setUpClass()

  def test_smoke_publish(self):
    task = prepare_task(JarPublish, args=['--test-local=/tmp'])
    task.scm = Mock(return_value={'branch2': 'dummy'})
    task.execute([])

  def test_publish_local_only(self):
    with pytest.raises(TaskError) as exc:
      prepare_task(JarPublish)
    assert re.search('This repo is not yet set for publishing to the world',
                       exc.value.message)
