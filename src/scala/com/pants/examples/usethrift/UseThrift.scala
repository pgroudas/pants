// Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
// Licensed under the Apache License, Version 2.0 (see LICENSE).

// Illustrate using Thrift-generated code from Scala.

package com.pants.examples.usethrift

import com.pants.examples.{distance, precipitation}

case class Distance(number: Int, unit: Option[String])
case class Precipitation(distance: Option[Distance])

object Precipitation {
  def toThrift(precip: Precipitation): precipitation.thriftscala.Precipitation = {
    precipitation.thriftscala.Precipitation(
      distance = precip.distance map { dist: Distance =>
        distance.thriftscala.Distance(number = dist.number, unit = dist.unit)
      }      
    )
  }
}

