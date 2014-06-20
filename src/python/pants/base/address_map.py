# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)


class AddressMap(object):
  def __init__(self, build_file_parser):
    self._build_file_parser = build_file_parser
    self.address_to_addressable = {}

  def resolve(self, address):
    if address not in self.address_to_addressable:
      build_file = self._build_file_parser.build_file_from_address(address)
      self._build_file_parser.parse_build_file_family(build_file)
      address_map = self._build_file_parser.address_map_from_build_file(build_file)
      if address not in address_map:
        raise AddressError("Failed to resolve address {address} from BuildFile {build_file}"
                           .format(address=address, build_file=build_file))
      self.address_to_addressable.update(address_map)
    return self.address_to_addressable[address]

  def resolve_spec(self, spec):
    address = SyntheticAddress(spec)
    return self.resolve(address)
