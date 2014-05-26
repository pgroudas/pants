# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from pants.goal import Goal as goal, Group as group

from pants.tasks.build_lint import BuildLint
from pants.tasks.builddictionary import BuildBuildDictionary
from pants.tasks.check_exclusives import CheckExclusives
from pants.tasks.clean import Invalidator, Cleaner, AsyncCleaner
from pants.tasks.dependees import ReverseDepmap
from pants.tasks.dependencies import Dependencies
from pants.tasks.depmap import Depmap
from pants.tasks.filedeps import FileDeps
from pants.tasks.filemap import Filemap
from pants.tasks.filter import Filter
from pants.tasks.list_goals import ListGoals
from pants.tasks.listtargets import ListTargets
from pants.tasks.markdown_to_html import MarkdownToHtml
from pants.tasks.minimal_cover import MinimalCover
from pants.tasks.pathdeps import PathDeps
from pants.tasks.paths import Path, Paths
from pants.tasks.prepare_resources import PrepareResources
from pants.tasks.reporting_server import RunServer, KillServer
from pants.tasks.roots import ListRoots
from pants.tasks.sorttargets import SortTargets
from pants.tasks.targets_help import TargetsHelp


# Getting help.

goal(name='goals', action=ListGoals
).install().with_description('List all documented goals.')

goal(name='targets', action=TargetsHelp
).install().with_description('List all target types.')

goal(name='builddict', action=BuildBuildDictionary
).install()


# Cleaning.

goal(name='invalidate', action=Invalidator, dependencies=['ng-killall']
).install().with_description('Invalidate all targets.')

goal(name='clean-all', action=Cleaner, dependencies=['invalidate']
).install().with_description('Clean all build output.')

goal(name='clean-all-async', action=AsyncCleaner, dependencies=['invalidate']
).install().with_description('Clean all build output in a background process.')


# Reporting.

goal(name='server', action=RunServer, serialize=False
).install().with_description('Run the pants reporting server.')

goal(name='killserver', action=KillServer, serialize=False
).install().with_description('Kill the reporting server.')


# Bootstrapping.
goal(name='prepare', action=PrepareResources
).install('resources')

goal(name='markdown', action=MarkdownToHtml
).install('markdown').with_description('Generate html from markdown docs.')


# Linting.

goal(name='check-exclusives', dependencies=['gen'], action=CheckExclusives
).install('check-exclusives').with_description('Check for exclusivity violations.')

goal(name='buildlint', action=BuildLint, dependencies=['compile']
).install()


goal(name='filedeps', action=FileDeps
).install('filedeps').with_description('Print out the source and BUILD files the target depends on.')

goal(name='pathdeps', action=PathDeps).install('pathdeps').with_description(
  'Print out all paths containing BUILD files the target depends on.')

goal(name='list', action=ListTargets
).install('list').with_description('List available BUILD targets.')


# Build graph information.

goal(name='path', action=Path
).install().with_description('Find a dependency path from one target to another.')

goal(name='paths', action=Paths
).install().with_description('Find all dependency paths from one target to another.')

goal(name='dependees', action=ReverseDepmap
).install().with_description("Print the target's dependees.")

goal(name='depmap', action=Depmap
).install().with_description("Depict the target's dependencies.")

goal(name='dependencies', action=Dependencies
).install().with_description("Print the target's dependencies.")

goal(name='filemap', action=Filemap
).install().with_description('Outputs a mapping from source file to owning target.')

goal(name='minimize', action=MinimalCover
).install().with_description('Print the minimal cover of the given targets.')

goal(name='filter', action=Filter
).install().with_description('Filter the input targets based on various criteria.')

goal(name='sort', action=SortTargets
).install().with_description("Topologically sort the targets.")

goal(name='roots', action=ListRoots
).install('roots').with_description("Print the workspace's source roots and associated target types.")
