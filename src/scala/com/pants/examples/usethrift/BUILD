# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

# This doesn't test much. It shows Pants-ly using Thrift from Java, though.

scala_library(name='usethrift',
  sources=['UseThrift.scala',],
  dependencies=[
    pants('src/thrift/com/pants/examples/distance:distance-scala'),
    pants('src/thrift/com/pants/examples/precipitation:precipitation-scala'),
  ],
)


