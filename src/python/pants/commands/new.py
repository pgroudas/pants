# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from contextlib import contextmanager
import inspect
import os
import sys
import traceback

from twitter.common import log
from twitter.common.dirutil import safe_mkdir
from twitter.common.lang import Compatibility
from twitter.common.log.options import LogOptions

from pants.backend.core.tasks.console_task import ConsoleTask
from pants.backend.jvm.tasks.nailgun_task import NailgunTask  # XXX(pl)
from pants.base.config import Config
from pants.base.cmd_line_spec_parser import CmdLineSpecParser
from pants.base.workunit import WorkUnit
from pants.commands.command import Command
from pants.engine.round_engine import RoundEngine
from pants.goal import Context, GoalError, Phase
from pants.goal.initialize_reporting import update_reporting
from pants.option.options import Options


StringIO = Compatibility.StringIO


class New(Command):
  """Lists installed goals or else executes a named goal."""

  class IntermixedArgumentsError(GoalError):
    pass

  __command__ = 'new'
  output = None

  @classmethod
  def register_global_options(cls, options):
    options.register_boolean('-e', '--explain', action='store_true', default=False,
                             help='Explain goal execution instead of actually executing them.'),
    options.register('-l', '--level', dest='log_level', choices=['debug', 'info', 'warn'],
                     default='info', help='Set the logging level.'),
    options.register_boolean('--color', action='store_true', default=True,
                             help='Colorize log messages.'),
    options.register_boolean('-x', '--time', action='store_true', default=False,
                             help='Print a timing report.'),
    options.register_boolean('-q', '--quiet', action='store_true', default=False,
                             help='Squelches all non-error console output.'),

# TODO(John Sirois): revisit wholesale locking when we move py support into pants new
  @classmethod
  def serialized(cls):
    # Goal serialization is now handled in goal execution during group processing.
    # The goal command doesn't need to hold the serialization lock; individual goals will
    # acquire the lock if they need to be serialized.
    return False

  def __init__(self, *args, **kwargs):
    super(New, self).__init__(*args, **kwargs)
    self.config = None
    self.options = None

  def init(self):
    known_scopes = ['']
    for phase, goals in Phase.all():
      known_scopes.append(phase.name)
      for goal in goals:
        known_scopes.append('%s.%s' % (phase.name, goal.name))

    self.config = Config.load()
    self.options = Options(env=os.environ, config=self.config,
                           known_scopes=known_scopes, args=sys.argv)

  def register_options(self):
    self.register_global_options(self.options.get_global_parser())
    for phase, goals in Phase.all():
      phase.register_options(self.options.get_parser(phase.name))
      for goal in goals:
        goal.task_type.register_options(self.options.get_parser('%s.%s' % (phase.name, goal.name)))

  def parse_target_specs(self):
    targets = []
    with self.run_tracker.new_workunit(name='setup', labels=[WorkUnit.SETUP]):
      # Bootstrap user goals by loading any BUILD files implied by targets.
      spec_parser = CmdLineSpecParser(self.root_dir, self.build_file_parser)
      with self.run_tracker.new_workunit(name='parse', labels=[WorkUnit.SETUP]):
        for address in spec_parser.parse_addresses(self.options.target_specs):
          self.build_file_parser.inject_spec_closure_into_build_graph(address.spec,
                                                                      self.build_graph)
          targets.append(self.build_graph.get_target(address))
    return targets

  @contextmanager
  def check_errors(self, banner):
    errors = {}
    def error(key, include_traceback=False):
      exc_type, exc_value, _ = sys.exc_info()
      msg = StringIO()
      if include_traceback:
        frame = inspect.trace()[-2]
        filename = frame[1]
        lineno = frame[2]
        funcname = frame[3]
        code = ''.join(frame[4]) if frame[4] else None
        traceback.print_list([(filename, lineno, funcname, code)], file=msg)
      if exc_type:
        msg.write(''.join(traceback.format_exception_only(exc_type, exc_value)))
      errors[key] = msg.getvalue()
      sys.exc_clear()

    yield error

    if errors:
      msg = StringIO()
      msg.write(banner)
      invalid_keys = [key for key, exc in errors.items() if not exc]
      if invalid_keys:
        msg.write('\n  %s' % '\n  '.join(invalid_keys))
      for key, exc in errors.items():
        if exc:
          msg.write('\n  %s =>\n    %s' % (key, '\n      '.join(exc.splitlines())))
      # The help message for goal is extremely verbose, and will obscure the
      # actual error message, so we don't show it in this case.
      self.error(msg.getvalue(), show_help=False)

  def run(self, lock):
    self.init()
    self.register_options()

    phases = [Phase(goal) for goal in self.options.goals]
    targets = self.parse_target_specs()
    global_options = self.options.for_global_scope()

    # TODO(John Sirois): Consider moving to straight python logging.  The divide between the
    # context/work-unit logging and standard python logging doesn't buy us anything.

    # Enable standard python logging for code with no handle to a context/workunit.
    LogOptions.set_stderr_log_level((global_options.log_level or 'info').upper())
    logdir = os.path.join(self.config.getdefault('pants_workdir'), 'log')
    safe_mkdir(logdir)
    LogOptions.set_log_dir(logdir)
    log.init('pants')

    # Update the reporting settings, now that we have flags etc.
    def is_console_task():
      for phase in phases:
        for g in phase.goals():
          if issubclass(g.task_type, ConsoleTask):
            return True
      return False

    update_reporting(global_options, is_console_task() or global_options.explain, self.run_tracker,
                     logdir)

    context = Context(
      self.config,
      self.options,
      self.run_tracker,
      targets,
      requested_goals=self.options.goals,
      build_graph=self.build_graph,
      build_file_parser=self.build_file_parser,
      lock=lock)

    unknown = []
    for phase in phases:
      if not phase.goals():
        unknown.append(phase)

    if unknown:
      context.log.error('Unknown goal(s): %s\n' % ' '.join(phase.name for phase in unknown))
      return 1

    engine = RoundEngine()
    return engine.execute(context, phases)

  def cleanup(self):
    # TODO: This is JVM-specific and really doesn't belong here.
    # TODO: Make this more selective? Only kill nailguns that affect state? E.g., checkstyle
    # may not need to be killed.
    NailgunTask.killall(log.info)
    sys.exit(1)
