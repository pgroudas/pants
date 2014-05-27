python_library(
  name = 'python',
  sources = globs('*.py'),
  dependencies = [
    pants('3rdparty/python/twitter/commons:twitter.common.collections'),
    pants('src/python/pants/base:target'),
    pants('src/python/pants/python:interpreter_cache'),
    pants('src/python/pants/python/targets:python'),
    pants('src/python/pants/backends/core/tasks:common'),
  ]
)
