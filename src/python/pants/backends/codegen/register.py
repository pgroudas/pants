# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from pants.goal import Goal as goal

from pants.backends.codegen.targets.java_antlr_library import JavaAntlrLibrary
from pants.backends.codegen.targets.java_protobuf_library import JavaProtobufLibrary
from pants.backends.codegen.targets.java_thrift_library import JavaThriftLibrary
from pants.backends.codegen.targets.python_antlr_library import PythonAntlrLibrary
from pants.backends.codegen.targets.python_thrift_library import PythonThriftLibrary
from pants.backends.codegen.tasks.antlr_gen import AntlrGen
from pants.backends.codegen.tasks.apache_thrift_gen import ApacheThriftGen
from pants.backends.codegen.tasks.protobuf_gen import ProtobufGen
from pants.backends.codegen.tasks.scrooge_gen import ScroogeGen


def target_aliases():
  return {
    'java_antlr_library': JavaAntlrLibrary,
    'java_protobuf_library': JavaProtobufLibrary,
    'java_thrift_library': JavaThriftLibrary,
    'python_antlr_library': PythonAntlrLibrary,
    'python_thrift_library': PythonThriftLibrary,
  }


def object_aliases():
  return {}


def partial_path_relative_util_aliases():
  return {}


def applicative_path_relative_util_aliases():
  return {}


def commands():
  pass


def goals():
  goal(name='thrift', action=ApacheThriftGen
  ).install('gen').with_description('Generate code.')

  goal(name='scrooge', dependencies=['bootstrap'], action=ScroogeGen
  ).install('gen')

  goal(name='protoc', action=ProtobufGen
  ).install('gen')

  goal(name='antlr', dependencies=['bootstrap'], action=AntlrGen
  ).install('gen')

