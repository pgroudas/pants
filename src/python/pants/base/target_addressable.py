# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)


class TargetAddressable(object):
  def __init__(self, *args, **kwargs):
    build_file = kwargs.pop('build_file')
    target_type = self.target_type

    if 'name' not in kwargs:
      raise ValueError('name is a required parameter to all Target objects'
                       ' specified within a BUILD file.'
                       '  Target type was: {target_type}.'
                       '  Current BUILD file is: {build_file}.'
                       .format(target_type=target_type,
                               build_file=build_file))

    if args:
      raise ValueError('All arguments passed to Targets within BUILD files should'
                       ' use explicit keyword syntax.'
                       '  Target type was: {target_type}.'
                       '  Current BUILD file is: {build_file}.'
                       '  Arguments passed were: {args}'
                       .format(target_type=target_type,
                               build_file=build_file,
                               args=args))

    self.build_file = build_file
    self.kwargs = kwargs
    self.name = kwargs['name']
    self.address = BuildFileAddress(build_file, self.name)
    self.description = None

    self.dependencies = self.kwargs.pop('dependencies', [])
    # self._dependency_addresses = None
    for dep_spec in self.dependencies:
      if not isinstance(dep_spec, Compatibility.string):
        msg = ('dependencies passed to Target constructors must be strings.  {dep_spec} is not'
               ' a string.  Target type was: {target_type}.  Current BUILD file is: {build_file}.'
               .format(target_type=target_type, build_file=build_file, dep_spec=dep_spec))
        raise TargetDefinitionException(target=self, msg=msg)

  # @property
  # def dependency_addresses(self):
  #   def dep_address_iter():
  #     for dep_spec in self.dependencies:
  #       dep_spec_path, dep_target_name = parse_spec(dep_spec,
  #                                                   relative_to=self.build_file.spec_path)
  #       dep_build_file = BuildFileCache.spec_path_to_build_file(self.build_file.root_dir,
  #                                                               dep_spec_path)
  #       dep_address = BuildFileAddress(dep_build_file, dep_target_name)
  #       yield dep_address

  #   if self._dependency_addresses is None:
  #     self._dependency_addresses = list(dep_address_iter())
  #   return self._dependency_addresses

  def with_description(self, description):
    self.description = description

  def to_target(self, build_graph):
    try:
      return self.target_type(build_graph=build_graph,
                              address=self.address,
                              **self.kwargs).with_description(self.description)
    except Exception:
      traceback.print_exc()
      logger.exception('Failed to instantiate Target with type {target_type} with name "{name}"'
                       ' from {build_file}'
                       .format(target_type=self.target_type,
                               name=self.name,
                               build_file=self.build_file))
      raise

  def __str__(self):
    format_str = ('<TargetAddressable(target_type={target_type}, build_file={build_file})'
                  ' [name={name}, address={address}]>')
    return format_str.format(target_type=self.target_type,
                             build_file=self.build_file,
                             name=self.name,
                             address=self.address)

  def __repr__(self):
    format_str = ('TargetAddressable(target_type={target_type}, build_file={build_file}, '
                  'kwargs={kwargs})')
    return format_str.format(target_type=self.target_type,
                             build_file=self.build_file,
                             kwargs=self.kwargs)
