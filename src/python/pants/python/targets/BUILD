
python_library(
  name = 'python',
  sources = [
    'python_antlr_library.py',
    'python_binary.py',
    'python_library.py',
    'python_requirement_library.py',
    'python_target.py',
    'python_tests.py',
    'python_thrift_library.py',
  ],
  dependencies = [
    pants('3rdparty/python/twitter/commons:twitter.common.collections'),
    pants('3rdparty/python/twitter/commons:twitter.common.lang'),
    pants('3rdparty/python/twitter/commons:twitter.common.python'),
    pants('3rdparty/python/twitter/commons:twitter.common.quantity'),
    pants('3rdparty/python:setuptools'),
    pants('src/python/pants/base:build_manual'),
    pants('src/python/pants/base:target'),
    pants('src/python/pants/targets:common'),
  ],
)