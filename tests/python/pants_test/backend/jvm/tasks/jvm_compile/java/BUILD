# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

target(
  name='java',
  dependencies=[
    ':jmake_analysis'
  ],
)

python_tests(
  name='jmake_analysis',
  sources=['test_jmake_analysis.py'],
  dependencies=[
    'src/python/pants/backend/jvm/tasks/jvm_compile:java',
    'src/python/pants/util:contextutil',
  ]
)

python_tests(
  name='apt_compile_integration',
  sources=['test_apt_compile_integration.py'],
  dependencies=[
    'tests/python/pants_test/backend/jvm/tasks/jvm_compile:base_compile_integration_test',
  ]
)

python_tests(
  name='java_zinc_compile_integration',
  sources=['test_java_zinc_compile_integration.py'],
  dependencies=[
    'tests/python/pants_test/backend/jvm/tasks/jvm_compile:base_compile_integration_test',
  ]
)

python_tests(
  name='java_compile_integration',
  sources=['test_java_compile_integration.py'],
  dependencies=[
    'src/python/pants/backend/jvm/tasks/jvm_compile:java',
    'src/python/pants/fs',
    'src/python/pants/util:contextutil',
    'src/python/pants/util:dirutil',
    'tests/python/pants_test:int-test',
  ]
)
