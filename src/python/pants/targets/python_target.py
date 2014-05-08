# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from collections import defaultdict

from twitter.common.collections import maybe_list, OrderedSet
from twitter.common.python.interpreter import PythonIdentity

from pants.base.payload import PythonPayload
from pants.base.target import Target
from pants.base.exceptions import TargetDefinitionException
from pants.targets.python_artifact import PythonArtifact


class PythonTarget(Target):
  """Base class for all Python targets."""

  def __init__(self,
               address=None,
               sources=None,
               resources=None,
               provides=None,
               compatibility=None,
               **kwargs):
    payload = PythonPayload(sources_rel_path=address.spec_path,
                            sources=sources or [],
                            resources=resources)
    super(PythonTarget, self).__init__(address=address, payload=payload, **kwargs)
    self.add_labels('python')

    if provides and not isinstance(provides, PythonArtifact):
      raise TargetDefinitionException(self,
        "Target must provide a valid pants setup_py object. Received a '%s' object instead." %
          provides.__class__.__name__)

    self.provides = provides

    self.compatibility = maybe_list(compatibility or ())
    for req in self.compatibility:
      try:
        PythonIdentity.parse_requirement(req)
      except ValueError as e:
        raise TargetDefinitionException(self, str(e))

  @property
  def resources(self):
    return self.payload.resources

  def _walk(self, walked, work, predicate=None):
    super(PythonTarget, self)._walk(walked, work, predicate)
    if self.provides and self.provides.binaries:
      for binary in self.provides.binaries.values():
        binary._walk(walked, work, predicate)

  def _propagate_exclusives(self):
    self.exclusives = defaultdict(set)
    for k in self.declared_exclusives:
      self.exclusives[k] = self.declared_exclusives[k]
    for t in self.dependencies:
      if isinstance(t, Target):
        t._propagate_exclusives()
        self.add_to_exclusives(t.exclusives)
      elif hasattr(t, "declared_exclusives"):
        self.add_to_exclusives(t.declared_exclusives)
