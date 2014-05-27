# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import os

from pants.backends.codegen.targets.java_antlr_library import JavaAntlrLibrary
from pants.backends.codegen.targets.java_protobuf_library import JavaProtobufLibrary
from pants.backends.codegen.targets.java_thrift_library import JavaThriftLibrary
from pants.backends.codegen.targets.python_antlr_library import PythonAntlrLibrary
from pants.backends.codegen.targets.python_thrift_library import PythonThriftLibrary
from pants.backends.core.targets.doc import Page
from pants.backends.core.targets.resources import Resources
from pants.base.source_root import SourceRoot
from pants.jvm.targets.annotation_processor import AnnotationProcessor
from pants.jvm.targets.java_agent import JavaAgent
from pants.jvm.targets.java_library import JavaLibrary
from pants.jvm.targets.java_tests import JavaTests
from pants.jvm.targets.jvm_binary import JvmBinary
from pants.jvm.targets.scala_library import ScalaLibrary
from pants.jvm.targets.scala_tests import ScalaTests
from pants.python.targets.python_binary import PythonBinary
from pants.python.targets.python_library import PythonLibrary
from pants.python.targets.python_tests import PythonTests


def maven_layout(basedir='', rel_path=None):
  """Sets up typical maven project source roots for all built-in pants target types.

  Shortcut for ``source_root('src/main/java', *java targets*)``,
  ``source_root('src/main/python', *python targets*)``, ...

  :param string basedir: Instead of using this BUILD file's directory as
    the base of the source tree, use a subdirectory. E.g., instead of
    expecting to find java files in ``src/main/java``, expect them in
    ``**basedir**/src/main/java``.
  """

  def root(path, *types):
    SourceRoot.register(os.path.join(rel_path, basedir, path), *types)

  root('src/main/antlr', JavaAntlrLibrary, Page, PythonAntlrLibrary)
  root('src/main/java', AnnotationProcessor, JavaAgent, JavaLibrary, JvmBinary, Page)
  root('src/main/protobuf', JavaProtobufLibrary, Page)
  root('src/main/python', Page, PythonBinary, PythonLibrary)
  root('src/main/resources', Page, Resources)
  root('src/main/scala', JvmBinary, Page, ScalaLibrary)
  root('src/main/thrift', JavaThriftLibrary, Page, PythonThriftLibrary)

  root('src/test/java', JavaLibrary, JavaTests, Page)
  root('src/test/python', Page, PythonLibrary, PythonTests)
  root('src/test/resources', Page, Resources)
  root('src/test/scala', JavaTests, Page, ScalaLibrary, ScalaTests)

