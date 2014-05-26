# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

python_library(
  name = 'common',
  sources = ['__init__.py'],
  dependencies = [
    'src/python/pants/tasks:task',
    'src/python/pants/base:exceptions',
  ]
)

python_library(
  name = 'apache_thrift_gen',
  sources = ['apache_thrift_gen.py'],
  dependencies = [
    pants('3rdparty/python/twitter/commons:twitter.common.collections'),
    pants('3rdparty/python/twitter/commons:twitter.common.dirutil'),
    pants('3rdparty/python/twitter/commons:twitter.common.log'),
    pants(':code_gen'),
    pants(':common'),
    pants('src/python/pants/base:build_environment'),
    pants('src/python/pants/jvm/targets:java'),
    pants('src/python/pants/targets:common'),
    pants('src/python/pants/targets:python'),
    pants('src/python/pants:thrift_util'),
  ],
)

python_library(
  name = 'antlr_gen',
  sources = ['antlr_gen.py'],
  dependencies = [
    pants('3rdparty/python/twitter/commons:twitter.common.collections'),
    pants('3rdparty/python/twitter/commons:twitter.common.dirutil'),
    pants(':code_gen'),
    pants(':common'),
    pants('src/python/pants/jvm/targets:java'),
    pants('src/python/pants/jvm/tasks:jvm_tool_task_mixin'),
    pants('src/python/pants/jvm/tasks:nailgun_task'),
  ],
)

python_library(
  name = 'code_gen',
  sources = ['code_gen.py'],
  dependencies = [
    pants(':common'),
    pants('src/python/pants/base:build_environment'),
  ],
)


python_library(
  name = 'protobuf_gen',
  sources = ['protobuf_gen.py'],
  dependencies = [
    pants('3rdparty/python/twitter/commons:twitter.common.collections'),
    pants('3rdparty/python/twitter/commons:twitter.common.dirutil'),
    pants('3rdparty/python/twitter/commons:twitter.common.log'),
    pants(':code_gen'),
    pants(':common'),
    pants('src/python/pants/jvm/targets:java'),
    pants('src/python/pants/targets:python'),
    pants('src/python/pants:binary_util'),
  ],
)

python_library(
  name = 'scrooge_gen',
  sources = ['scrooge_gen.py'],
  dependencies = [
    pants('3rdparty/python/twitter/commons:twitter.common.collections'),
    pants('3rdparty/python/twitter/commons:twitter.common.dirutil'),
    pants(':common'),
    pants('src/python/pants/base:build_environment'),
    pants('src/python/pants/jvm/targets:java'),
    pants('src/python/pants/jvm/targets:scala'),
    pants('src/python/pants/jvm/tasks:jvm_tool_task_mixin'),
    pants('src/python/pants/jvm/tasks:nailgun_task'),
    pants('src/python/pants/targets:common'),
    pants('src/python/pants:thrift_util'),
  ],
)
