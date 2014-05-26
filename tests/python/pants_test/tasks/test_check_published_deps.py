# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from textwrap import dedent

from pants.jvm.tasks.check_published_deps import CheckPublishedDeps
from pants_test.tasks.test_base import ConsoleTaskTest


class CheckPublishedDepsTest(ConsoleTaskTest):

  @classmethod
  def task_type(cls):
    return CheckPublishedDeps

  def setUp(self):
    super(CheckPublishedDepsTest, self).setUp()

    self.create_file('repo/pushdb/publish.properties', dedent('''
        revision.major.org.name%lib1=2
        revision.minor.org.name%lib1=0
        revision.patch.org.name%lib1=0
        revision.sha.org.name%lib1=12345
        revision.major.org.name%lib2=2
        revision.minor.org.name%lib2=0
        revision.patch.org.name%lib2=0
        revision.sha.org.name%lib2=12345
        '''))
    self.add_to_build_file('repo/BUILD', dedent('''
        import os
        repo(name='repo',
             url='http://www.www.com',
             push_db=os.path.join(os.path.dirname(__file__), 'pushdb', 'publish.properties'))
        '''))

    self.add_to_build_file('provider/BUILD', dedent('''
        java_library(name='lib1',
          provides=artifact(
            org='org.name',
            name='lib1',
            repo=pants('repo')),
          sources=[])
        java_library(name='lib2',
          provides=artifact(
            org='org.name',
            name='lib2',
            repo=pants('repo')),
          sources=[])
        '''))
    self.add_to_build_file('outdated/BUILD', dedent('''
        jar_library(name='outdated',
          jars=[jar(org='org.name', name='lib1', rev='1.0.0')]
        )
        '''))
    self.add_to_build_file('uptodate/BUILD', dedent('''
        jar_library(name='uptodate',
          jars=[jar(org='org.name', name='lib2', rev='2.0.0')]
        )
        '''))
    self.add_to_build_file('both/BUILD', dedent('''
        dependencies(name='both',
          dependencies=[
            pants('outdated'),
            pants('uptodate'),
          ]
        )
        '''))

  def test_all_up_to_date(self):
    self.assert_console_output(
      targets=[self.target('uptodate')]
    )

  def test_print_up_to_date_and_outdated(self):
    self.assert_console_output(
      'outdated org.name#lib1 1.0.0 latest 2.0.0',
      'up-to-date org.name#lib2 2.0.0',
      targets=[self.target('both')],
      args=['--test-print-uptodate']
    )

  def test_outdated(self):
    self.assert_console_output(
      'outdated org.name#lib1 1.0.0 latest 2.0.0',
      targets=[self.target('outdated')]
    )
