# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

python_library(
  name = 'all',
  dependencies = [
    pants(':common'),
    pants(':python'),
  ],
)

python_library(
  name = 'common',
  sources = [
    'anonymous.py',
    'dependencies.py',
    'doc.py',
    'resources.py',
  ],
  dependencies = [
    pants('3rdparty/python/twitter/commons:twitter.common.collections'),
    pants('3rdparty/python/twitter/commons:twitter.common.lang'),
    pants('src/python/pants/base:address'),
    pants('src/python/pants/base:build_environment'),
    pants('src/python/pants/base:build_manual'),
    pants('src/python/pants/base:payload'),
    pants('src/python/pants/base:target'),
  ],
)

python_library(
  name = 'python',
  sources = [
    'python_antlr_library.py',
    'python_artifact.py',
    'python_binary.py',
    'python_egg.py',
    'python_library.py',
    'python_requirement.py',
    'python_requirements.py',
    'python_target.py',
    'python_tests.py',
    'python_thrift_library.py',
    'python_requirement_library.py',
  ],
  dependencies = [
    pants('3rdparty/python:setuptools'),
    pants(':common'),
    pants('3rdparty/python/twitter/commons:twitter.common.collections'),
    pants('3rdparty/python/twitter/commons:twitter.common.lang'),
    pants('3rdparty/python/twitter/commons:twitter.common.python'),
    pants('3rdparty/python/twitter/commons:twitter.common.quantity'),
    pants('src/python/pants/base:build_manual'),
    pants('src/python/pants/base:target'),
  ],
)
