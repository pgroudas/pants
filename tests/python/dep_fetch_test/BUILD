
python_requirement_library(
  name = 'toro',
  requirements = [
    python_requirement('toro', '0.5'),
  ],
)

python_binary(
  name = 'dep_fetch_test',
  source = 'empty.py',
  dependencies = [
    ':toro',
  ],
  compatibility = ('CPython>=2.7,<3',),
  platforms = ('macosx-10.9-x86_64', 'linux-x86_64'),
)
