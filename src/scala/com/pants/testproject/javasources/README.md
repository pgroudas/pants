This is testing if a scala_library that has java_sources triggers the
"Missing BUILD dependency" warning. It should not.

We also test that if a java_library depends on a scala_library that
has the java_library as java_sources, it should not complain about
a missing dependency from java->scala.