# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

dependencies(
  name = 'common',
  dependencies = [
    'src/python/pants/tasks:task',
  ],
)

python_library(
  name = 'benchmark_run',
  sources = ['benchmark_run.py'],
  dependencies = [
    pants(':common'),
    pants(':jvm_task'),
    pants('src/python/pants/java:util'),
    pants('src/python/pants/jvm/tasks:jvm_tool_task_mixin'),
  ],
)

python_library(
  name = 'binary_create',
  sources = ['binary_create.py'],
  dependencies = [
    pants(':common'),
    pants(':jvm_binary_task'),
    pants('3rdparty/python/twitter/commons:twitter.common.contextutil'),
    pants('3rdparty/python/twitter/commons:twitter.common.dirutil'),
    pants('src/python/pants/base:build_environment'),
    pants('src/python/pants/fs'),
    pants('src/python/pants/java:jar'),
  ],
)

python_library(
  name = 'bootstrap_jvm_tools',
  sources = ['bootstrap_jvm_tools.py'],
  dependencies = [
    pants('src/python/pants/base:workunit'),
    pants('src/python/pants/base:exceptions'),
    pants('src/python/pants/jvm/tasks:ivy_task_mixin'),
    pants('src/python/pants/tasks:task'),
  ],
)

python_library(
  name = 'bundle_create',
  sources = ['bundle_create.py'],
  dependencies = [
    pants(':common'),
    pants(':jvm_binary_task'),
    pants('3rdparty/python/twitter/commons:twitter.common.collections'),
    pants('3rdparty/python/twitter/commons:twitter.common.contextutil'),
    pants('3rdparty/python/twitter/commons:twitter.common.dirutil'),
    pants('src/python/pants/base:build_environment'),
    pants('src/python/pants/fs'),
    pants('src/python/pants/java:jar'),
    pants('src/python/pants/jvm/targets:jvm'),
  ],
)

python_library(
  name = 'check_published_deps',
  sources = ['check_published_deps.py'],
  dependencies = [
    pants(':common'),
    pants('src/python/pants/tasks:console_task'),
    pants(':jar_publish'),
    pants('src/python/pants/base:build_environment'),
    pants('src/python/pants/base:build_file'),
    pants('src/python/pants/base:target'),
    pants('src/python/pants/jvm/targets:jvm'),
  ],
)

python_library(
  name = 'checkstyle',
  sources = ['checkstyle.py'],
  dependencies = [
    pants(':common'),
    pants('3rdparty/python/twitter/commons:twitter.common.dirutil'),
    pants('src/python/pants/jvm/tasks:jvm_tool_task_mixin'),
    pants('src/python/pants/jvm/tasks:nailgun_task'),
    pants('src/python/pants/process'),
  ],
)

python_library(
  name = 'detect_duplicates',
  sources = ['detect_duplicates.py'],
  dependencies = [
    pants(':common'),
    pants(':jvm_binary_task'),
    pants('src/python/pants/java:jar'),
  ],
)

python_library(
  name = 'eclipse_gen',
  sources = ['eclipse_gen.py'],
  resources = globs('templates/eclipse/*.mustache'),
  dependencies = [
    pants(':common'),
    pants(':ide_gen'),
    pants('3rdparty/python/twitter/commons:twitter.common.collections'),
    pants('3rdparty/python/twitter/commons:twitter.common.dirutil'),
    pants('src/python/pants/base:build_environment'),
    pants('src/python/pants/base:generator'),
  ],
)

python_library(
  name = 'ide_gen',
  sources = ['ide_gen.py'],
  dependencies = [
    pants(':checkstyle'),
    pants(':common'),
    pants(':jvm_binary_task'),
    pants('3rdparty/python/twitter/commons:twitter.common.collections'),
    pants('3rdparty/python/twitter/commons:twitter.common.dirutil'),
    pants('src/python/pants/base:build_environment'),
    pants('src/python/pants/base:target'),
    pants('src/python/pants/goal:phase'), # XXX?
    pants('src/python/pants/jvm/tasks:jvm_tool_task_mixin'),
    pants('src/python/pants/jvm/targets:jvm'),
    pants('src/python/pants:binary_util'),
  ],
)

python_library(
  name = 'idea_gen',
  sources = ['idea_gen.py'],
  resources = globs('templates/idea/*.mustache'),
  dependencies = [
    pants(':common'),
    pants(':ide_gen'),
    pants('3rdparty/python/twitter/commons:twitter.common.dirutil'),
    pants('src/python/pants/base:build_environment'),
    pants('src/python/pants/base:generator'),
    pants('src/python/pants/targets:common'),
    pants('src/python/pants/jvm/targets:java'),
    pants('src/python/pants/jvm/targets:scala'),
  ],
)

python_library(
  name = 'ivy_resolve',
  sources = ['ivy_resolve.py'],
  dependencies = [
    pants('src/python/pants/jvm:ivy_utils'),
    pants(':nailgun_task'),
    pants('3rdparty/python/twitter/commons:twitter.common.dirutil'),
    pants('src/python/pants:binary_util'),
    pants('src/python/pants/base:cache_manager'),
    pants('src/python/pants/ivy'),
    pants('src/python/pants/jvm/tasks:ivy_task_mixin'),
    pants('src/python/pants/jvm/tasks:jvm_tool_task_mixin'),
  ],
)

python_library(
  name = 'ivy_task_mixin',
  sources = ['ivy_task_mixin.py'],
  dependencies = [
    pants('src/python/pants/jvm:ivy_utils'),
    pants('src/python/pants/base:cache_manager'),
    pants('src/python/pants/ivy'),
  ],
)

python_library(
  name = 'jar_create',
  sources = ['jar_create.py'],
  dependencies = [
    pants(':common'),
    pants(':javadoc_gen'),
    pants(':scaladoc_gen'),
    pants('3rdparty/python/twitter/commons:twitter.common.dirutil'),
    pants('src/python/pants/base:build_environment'),
    pants('src/python/pants/fs'),
    pants('src/python/pants/java:jar'),
    pants('src/python/pants/jvm/targets:jvm'),
  ],
)

python_library(
  name = 'jar_publish',
  sources = ['jar_publish.py'],
  resources = globs('templates/jar_publish/*.mustache') +
              globs('templates/ivy_resolve/*.mustache'),
  dependencies = [
    pants(':common'),
    pants('src/python/pants/tasks:scm_publish'),
    pants('3rdparty/python/twitter/commons:twitter.common.collections'),
    pants('3rdparty/python/twitter/commons:twitter.common.config'),
    pants('3rdparty/python/twitter/commons:twitter.common.dirutil'),
    pants('3rdparty/python/twitter/commons:twitter.common.log'),
    pants('src/python/pants/base:address'),
    pants('src/python/pants/base:build_environment'),
    pants('src/python/pants/base:generator'),
    pants('src/python/pants/base:target'),
    pants('src/python/pants/ivy'),
    pants('src/python/pants/targets:common'),
  ],
)

python_library(
  name = 'javadoc_gen',
  sources = ['javadoc_gen.py'],
  dependencies = [
    pants(':jvmdoc_gen'),
  ],
)

python_library(
  name = 'junit_run',
  sources = ['junit_run.py'],
  dependencies = [
    pants(':common'),
    pants(':jvm_task'),
    pants('3rdparty/python/twitter/commons:twitter.common.dirutil'),
    pants('src/python/pants:binary_util'),
    pants('src/python/pants/base:build_environment'),
    pants('src/python/pants/base:workunit'),
    pants('src/python/pants/java:util'),
    pants('src/python/pants/jvm/tasks:jvm_tool_task_mixin'),
    pants('src/python/pants/jvm/targets:java'),
  ],
)

python_library(
  name = 'jvm_binary_task',
  sources = ['jvm_binary_task.py'],
  dependencies = [
    pants(':common'),
    pants('3rdparty/python/twitter/commons:twitter.common.collections'),
    pants('src/python/pants/jvm/targets:jvm'),
  ],
)

python_library(
  name = 'jvm_run',
  sources = ['jvm_run.py'],
  dependencies = [
    pants(':common'),
    pants(':jvm_task'),
    pants('3rdparty/python/twitter/commons:twitter.common.dirutil'),
    pants('src/python/pants/base:workunit'),
    pants('src/python/pants/java:executor'),
    pants('src/python/pants/java:util'),
    pants('src/python/pants/jvm/targets:jvm'),
  ],
)

python_library(
  name = 'jvm_task',
  sources = ['jvm_task.py'],
  dependencies = [
    pants(':common'),
    pants('src/python/pants/base:build_environment'),
  ],
)

python_library(
  name = 'jvm_tool_task_mixin',
  sources = ['jvm_tool_task_mixin.py'],
  dependencies = [
    pants('src/python/pants/jvm:jvm_tool_bootstrapper'),
  ],
)

python_library(
  name = 'jvmdoc_gen',
  sources = ['jvmdoc_gen.py'],
  dependencies = [
    pants(':common'),
    pants('3rdparty/python/twitter/commons:twitter.common.dirutil'),
    pants('src/python/pants:binary_util'),
  ],
)

python_library(
  name = 'nailgun_task',
  sources = ['nailgun_task.py'],
  dependencies = [
    pants('src/python/pants/base:exceptions'),
    pants('src/python/pants/java:executor'),
    pants('src/python/pants/java:nailgun_executor'),
    pants('src/python/pants/java:distribution'),
    pants('src/python/pants/java:util'),
    pants('src/python/pants/jvm/tasks:jvm_tool_task_mixin'),
    pants('src/python/pants/tasks:task'),
    pants('src/python/pants/tasks:console_task'),
  ],
)

python_library(
  name = 'provides',
  sources = ['provides.py'],
  dependencies = [
    pants(':common'),
    pants('3rdparty/python/twitter/commons:twitter.common.collections'),
    pants('3rdparty/python/twitter/commons:twitter.common.contextutil'),
    pants('src/python/pants/jvm:ivy_utils'),
    pants('src/python/pants/jvm/targets:jvm'),
  ],
)

python_library(
  name = 'scala_repl',
  sources = ['scala_repl.py'],
  dependencies = [
    pants(':common'),
    pants(':jvm_task'),
    pants('src/python/pants/base:workunit'),
    pants('src/python/pants/java:util'),
    pants('src/python/pants/jvm/tasks:jvm_tool_task_mixin'),
  ],
)

python_library(
  name = 'scaladoc_gen',
  sources = ['scaladoc_gen.py'],
  dependencies = [
    pants(':jvmdoc_gen'),
  ],
)

python_library(
  name = 'scalastyle',
  sources = ['scalastyle.py'],
  dependencies = [
    pants(':common'),
    pants('src/python/pants/base:config'),
    pants('src/python/pants/jvm/tasks:jvm_tool_task_mixin'),
    pants('src/python/pants/jvm/tasks:nailgun_task'),
    pants('src/python/pants/base:target'),
    pants('src/python/pants/process'),
  ],
)

python_library(
  name = 'specs_run',
  sources = ['specs_run.py'],
  dependencies = [
    pants(':common'),
    pants(':jvm_task'),
    pants('3rdparty/python/twitter/commons:twitter.common.collections'),
    pants('src/python/pants/base:workunit'),
    pants('src/python/pants:binary_util'),
    pants('src/python/pants/java:util'),
    pants('src/python/pants/jvm/tasks:jvm_tool_task_mixin'),
  ],
)

