# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from contextlib import contextmanager
import tempfile
from textwrap import dedent
import unittest

import pytest

from pants.base.build_file import BuildFile
from pants.base.build_file_manipulator import (BuildFileManipulator,
                                               BuildTargetParseError,
                                               DependencySpec)


class MockBuildFile(object):
  def __init__(self, full_path):
    self.full_path = full_path

  def __repr__(self):
    return 'MockBuildFile({full_path})'.format(full_path=self.full_path)


@contextmanager
def mock_build_file(content):
  with tempfile.NamedTemporaryFile() as f:
    f.write(content)
    f.flush()
    yield MockBuildFile(f.name)


class BuildFileManipulatorTest(unittest.TestCase):
  def test_malformed_targets(self):
    bad_targets = dedent(
      """
      target_type(name='name_on_line')

      target_type(
        name=
        'dangling_kwarg_value'
      )

      # TODO(pl):  Split this out.  Right now it fails
      # the test for all of the targets and masks other
      # expected failures
      # target_type(
      #   name=str('non_str_literal')
      # )

      target_type(
        name='end_paren_not_on_own_line')

      target_type(
        object(),
        name='has_non_kwarg'
      )

      target_type(
        name='non_list_deps',
        dependencies=object(),
      )

      target_type(
        name='deps_not_on_own_lines1',
        dependencies=['some_dep'],
      )

      target_type(
        name='deps_not_on_own_lines2',
        dependencies=[
          'some_dep', 'some_other_dep'],
      )

      target_type(
        name = 'sentinal',
      )
      """
    )

    bad_target_names = [
      'name_on_line',
      'dangling_kwarg_value',
      'non_str_literal',
      'end_paren_not_on_own_line',
      'name_not_in_build_file',
      'has_non_kwarg',
      'non_list_deps',
    ]
    with mock_build_file(bad_targets) as build_file:
      # Make sure this exception isn't just being thrown no matter what.
      # Probably these exceptions should be more granular.
      BuildFileManipulator.load(build_file, 'sentinal', set(['target_type']))
      for bad_target in bad_target_names:
        with pytest.raises(BuildTargetParseError):
          BuildFileManipulator.load(build_file, bad_target, set(['target_type']))
  
  def test_simple_targets(self):
    simple_targets = dedent(
      """
      target_type(
        name = 'no_deps',
      )

      target_type(
        name = 'empty_deps',
        dependencies = [
        ]
      )

      target_type(
        name = 'empty_deps_inline',
        dependencies = []
      )
      """
    )

    with mock_build_file(simple_targets) as build_file:
      for no_deps_name in ['no_deps', 'empty_deps', 'empty_deps_inline']:
        no_deps = BuildFileManipulator.load(build_file, no_deps_name, set(['target_type']))
        self.assertEqual(tuple(no_deps.dependency_lines()), tuple())
        no_deps._dependencies.append(DependencySpec(':fake_dep'))
        self.assertEqual(tuple(no_deps.dependency_lines()),
                         tuple(['  dependencies = [',
                                "    ':fake_dep',",
                                '  ],']))
        no_deps._dependencies.append(DependencySpec(':b_fake_dep'))
        no_deps._dependencies.append(DependencySpec(':a_fake_dep'))
        self.assertEqual(tuple(no_deps.dependency_lines()),
                         tuple(['  dependencies = [',
                                "    ':a_fake_dep',",
                                "    ':b_fake_dep',",
                                "    ':fake_dep',",
                                '  ],']))
        self.assertEqual(tuple(no_deps.target_lines()),
                         tuple(['target_type(',
                                "  name = '{0}',".format(no_deps_name),
                                '  dependencies = [',
                                "    ':a_fake_dep',",
                                "    ':b_fake_dep',",
                                "    ':fake_dep',",
                                '  ],',
                                ')']))

  def test_comment_rules(self):
    complicated_dep_comments = dedent(
      """\
      target_type(
        # This comment should be okay
        name = 'no_bg_no_cry',  # Side comments here will stay
        # This comment should be okay
        dependencies = [
          # nbgbc_above1
          # nbgnc_above2
          'really/need/this:dep', #nobgnc_side

          ':whitespace_above',
          ':only_side',#only_side
          #only_above
          ':only_above'
        ],
        # This comment is also fine
        thing = object()
        # And finally this comment survives
      )"""
    )

    expected_target_str = dedent(
      """\
      target_type(
        # This comment should be okay
        name = 'no_bg_no_cry',  # Side comments here will stay
        # This comment should be okay
        dependencies = [
          # only_above
          ':only_above',
          ':only_side',  # only_side

          ':whitespace_above',
          # nbgbc_above1
          # nbgnc_above2
          'really/need/this:dep',  # nobgnc_side
        ],
        # This comment is also fine
        thing = object()
        # And finally this comment survives
      )"""
    )

    with mock_build_file(complicated_dep_comments) as build_file:
      no_deps = BuildFileManipulator.load(build_file, 'no_bg_no_cry', set(['target_type']))
      target_str = '\n'.join(no_deps.target_lines())
      print(target_str)
      print(expected_target_str)
      self.assertEqual(target_str, expected_target_str)


