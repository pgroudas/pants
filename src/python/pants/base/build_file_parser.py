# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import logging
import traceback
from collections import defaultdict
from functools import partial

from twitter.common.lang import Compatibility

from pants.base.address import BuildFileAddress, parse_spec, SyntheticAddress
from pants.base.addressable import AddressableCallProxy
from pants.base.build_environment import get_buildroot
from pants.base.build_file import BuildFile
from pants.base.build_graph import BuildGraph
from pants.base.exceptions import TargetDefinitionException


logger = logging.getLogger(__name__)


class TargetCallProxy(object):
  def __init__(self, target_type, build_file, registered_target_proxies):
    self._target_type = target_type
    self._build_file = build_file
    self._registered_target_proxies = registered_target_proxies

  def __call__(self, *args, **kwargs):
    addressable = TargetProxy(self._target_type, self._build_file, args, kwargs)
    self._registered_target_proxies.add(addressable)
    return addressable

  def __repr__(self):
    return ('<TargetCallProxy(target_type={target_type}, build_file={build_file},'
            ' registered_target_proxies=<dict with id: {registered_target_proxies_id}>)>'
            .format(target_type=self._target_type,
                    build_file=self._build_file,
                    registered_target_proxies_id=id(self._registered_target_proxies)))


class BuildFileParser(object):

  class TargetConflictException(Exception):
    """Thrown if the same target is redefined in a BUILD file"""

  class SiblingConflictException(Exception):
    """Thrown if the same target is redefined in another BUILD file in the same directory"""

  class InvalidTargetException(Exception):
    """Thrown if the user called for a target not present in a BUILD file."""

  class EmptyBuildFileException(Exception):
    """Thrown if the user called for a target when none are present in a BUILD file."""

  def clear_registered_context(self):
    self._addressable_alias_map = {}
    self._exposed_objects = {}
    self._partial_path_relative_utils = {}
    self._applicative_path_relative_utils = {}
    self._target_creation_utils = {}

  def report_registered_context(self):
    """Return dict of syms defined in BUILD files, useful for docs/help.

    This dict isn't so useful for actually parsing BUILD files.
    It's useful for generating things like
    http://pantsbuild.github.io/build_dictionary.html
    """
    retval = {}
    retval.update(self._exposed_objects)
    retval.update(self._partial_path_relative_utils)
    retval.update(self._applicative_path_relative_utils)
    retval.update(self._addressable_alias_map)
    return retval

  def report_addressable_aliases(self):
    return self._addressable_alias_map.copy()

  def register_alias_groups(self, alias_map):
    for alias, obj in alias_map.get('exposed_objects', {}).items():
      self.register_exposed_object(alias, obj)

    for alias, obj in alias_map.get('applicative_path_relative_utils', {}).items():
      self.register_applicative_path_relative_util(alias, obj)

    for alias, obj in alias_map.get('partial_path_relative_utils', {}).items():
      self.register_partial_path_relative_util(alias, obj)

    for alias, obj in alias_map.get('target_aliases', {}).items():
      self.register_target_alias(alias, obj)

    for alias, func in alias_map.get('target_creation_utils', {}).items():
      self.register_target_creation_utils(alias, func)

  # TODO(pl): For the next four methods, provide detailed documentation.  Especially for the middle
  # two, the semantics are slightly tricky.
  def register_exposed_object(self, alias, obj):
    if alias in self._exposed_objects:
      logger.warn('Object alias {alias} has already been registered.  Overwriting!'
                  .format(alias=alias))
    self._exposed_objects[alias] = obj

  def register_applicative_path_relative_util(self, alias, obj):
    if alias in self._applicative_path_relative_utils:
      logger.warn('Applicative path relative util alias {alias} has already been registered.'
                  '  Overwriting!'
                  .format(alias=alias))
    self._applicative_path_relative_utils[alias] = obj

  def register_partial_path_relative_util(self, alias, obj):
    if alias in self._partial_path_relative_utils:
      logger.warn('Partial path relative util alias {alias} has already been registered.'
                  '  Overwriting!'
                  .format(alias=alias))
    self._partial_path_relative_utils[alias] = obj

  def register_addressable_alias(self, alias, obj):
    if alias in self._addressable_alias_map:
      logger.warn('Addressable alias {alias} has already been registered.  Overwriting!'
                  .format(alias=alias))
    self._addressable_alias_map[alias] = obj

  def register_target_alias(self, alias, target):
    self.register_addressable_alias(alias, target.get_addressable_type())

  def register_target_creation_utils(self, alias, func):
    if alias in self._target_creation_utils:
      logger.warn('Target Creation alias {alias} has already been registered.  Overwriting!'
                  .format(alias=alias))
    self._target_creation_utils[alias] = func

  def __init__(self, root_dir, run_tracker=None):
    self._root_dir = root_dir
    self.run_tracker = run_tracker
    self.clear_registered_context()

  def _raise_incorrect_target_error(self, wrong_target, targets):
    """Search through the list of targets and return those which originate from the same folder
    which wrong_target resides in.

    :raises: A helpful error message listing possible correct target addresses.
    """
    def path_parts(build): # Gets a tuple of directory, filename.
        build = str(build)
        slash = build.rfind('/')
        if slash < 0:
          return '', build
        return build[:slash], build[slash+1:]

    def are_siblings(a, b): # Are the targets in the same directory?
      return path_parts(a)[0] == path_parts(b)[0]

    valid_specs = []
    all_same = True
    # Iterate through all addresses, saving those which are similar to the wrong address.
    for target in targets:
      if are_siblings(target.build_file, wrong_target.build_file):
        possibility = (path_parts(target.build_file)[1], target.spec[target.spec.rfind(':'):])
        # Keep track of whether there are multiple BUILD files or just one.
        if all_same and valid_specs and possibility[0] != valid_specs[0][0]:
          all_same = False
        valid_specs.append(possibility)

    # Trim out BUILD extensions if there's only one anyway; no need to be redundant.
    if all_same:
      valid_specs = [('', tail) for head, tail in valid_specs]
    # Might be neat to sort by edit distance or something, but for now alphabetical is fine.
    valid_specs = [''.join(pair) for pair in sorted(valid_specs)]

    # Give different error messages depending on whether BUILD file was empty.
    if valid_specs:
      one_of = ' one of' if len(valid_specs) > 1 else '' # Handle plurality, just for UX.
      raise self.InvalidTargetException((
          ':{address} from spec {spec} was not found in BUILD file {build_file}. Perhaps you '
          'meant{one_of}: \n  {specs}').format(address=wrong_target.target_name,
                                               spec=wrong_target.spec,
                                               build_file=wrong_target.build_file,
                                               one_of=one_of,
                                               specs='\n  '.join(valid_specs)))
    # There were no targets in the BUILD file.
    raise self.EmptyBuildFileException((
        ':{address} from spec {spec} was not found in BUILD file {build_file}, because that '
        'BUILD file contains no targets.').format(address=wrong_target.target_name,
                                                  spec=wrong_target.spec,
                                                  build_file=wrong_target.build_file))

  def address_map_from_spec_path(self, spec_path, extra_parse_context=None):
    build_file = BuildFile.from_cache(self._root_dir, spec_path)
    family_address_map_by_build_file = self.parse_build_file_family(build_file)
    address_map = {}
    for build_file, sibling_address_map in family_address_map_by_build_file.items():
      address_map.update(sibling_address_map)
    return address_map

  def parse_build_file_family(self, build_file, extra_parse_context=None):
    family_address_map_by_build_file = {}  # {build_file: {addressable: address}}
    for bf in build_file.family():
      bf_address_map = self.parse_build_file(bf, extra_parse_context=extra_parse_context)
      for address, addressable in bf_address_map.items():
        for sibling_build_file, sibling_address_map in family_address_map_by_build_file.items():
          if address in sibling_address_map:
            raise BuildFileParser.SiblingConflictException(
              "Both {conflicting_file} and {addressable_file} define the same address"
              "'{target_name}'"
              .format(conflicting_file=sibling_build_file,
                      addressable_file=address.build_file,
                      target_name=address.target_name))
      family_address_map_by_build_file[bf] = bf_address_map
    return family_address_map_by_build_file

  def parse_build_file(self, build_file, extra_parse_context=None):
    """Capture Addressable instances from parsing `build_file`.
    Prepare a context for parsing, read a BUILD file from the filesystem, and return the
    Addressable instances generated by executing the code.
    """

    logger.debug("Parsing BUILD file {build_file}."
                 .format(build_file=build_file))

    parse_context = {}

    # TODO(pl): Don't inject __file__ into the context.  BUILD files should not be aware
    # of their location on the filesystem.
    parse_context['__file__'] = build_file.full_path

    parse_context.update(self._exposed_objects)
    parse_context.update(
      (key, partial(util, rel_path=build_file.spec_path)) for
      key, util in self._partial_path_relative_utils.items()
    )
    parse_context.update(
      (key, util(rel_path=build_file.spec_path)) for
      key, util in self._applicative_path_relative_utils.items()
    )

    registered_addressable_instances = []
    def registration_callback(address, addressable):
      registered_addressable_instances.append((address, addressable))

    parse_context.update(
      (alias, AddressableCallProxy(addressable_type=addressable_type,
                                   build_file=build_file,
                                   registration_callback=registration_callback)) for
      alias, addressable_type in self._addressable_alias_map.items()
    )

    for key, func in self._target_creation_utils.items():
      parse_context.update({key: partial(func, alias_map=parse_context)})

    parse_context.update(extra_parse_context or {})

    try:
      build_file_code = build_file.code()
    except Exception:
      logger.exception("Error parsing {build_file}."
                       .format(build_file=build_file))
      traceback.print_exc()
      raise

    try:
      Compatibility.exec_function(build_file_code, parse_context)
    except Exception:
      logger.exception("Error running {build_file}."
                       .format(build_file=build_file))
      traceback.print_exc()
      raise

    address_map = {}
    for address, addressable in registered_addressable_instances:
      logger.debug('Adding {addressable} to the BuildFileParser address map with {address}'
                   .format(addressable=addressable,
                           address=address))
      if address in address_map:
        conflicting_addressable = address_map[address]

        raise BuildFileParser.TargetConflictException(
          "File {conflicting_file} defines address '{target_name}' more than once."
          .format(conflicting_file=address.build_file,
                  target_name=address.target_name))

      address_map[address] = addressable

    logger.debug("{build_file} produced the following Addressables:"
                 .format(build_file=build_file))
    for address, addressable in address_map.items():
      logger.debug("  * {address}: {addressable}"
                   .format(address=address,
                           addressable=addressable))
    return address_map

  def scan(self, root=None):
    """Scans and parses all BUILD files found under ``root``.

    Only BUILD files found under ``root`` are parsed as roots in the graph, but any dependencies of
    targets parsed in the root tree's BUILD files will be followed and this may lead to BUILD files
    outside of ``root`` being parsed and included in the returned build graph.

    :param string root: The path to scan; by default, the build root.
    :returns: A new build graph encapsulating the targets found.
    """
    build_graph = BuildGraph()
    for build_file in BuildFile.scan_buildfiles(root or get_buildroot()):
      self.parse_build_file(build_file)
      for address in self.addresses_by_build_file[build_file]:
        self.inject_address_closure_into_build_graph(address, build_graph)
    return build_graph
