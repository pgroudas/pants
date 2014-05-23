// Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
// Licensed under the Apache License, Version 2.0 (see LICENSE).

// Illustrate using Thrift-generated code from Scala.

package com.pants.examples.usethrift

import org.junit.Test
import org.junit.Assert.assertEquals

import com.pants.examples.{distance, precipitation}

/* Not testing behavior; we're happy if this compiles. */
class UseThriftTest {
  @Test
  def makeItRain() {
    val notMuch = distance.thriftscala.Distance(number = 8, unit = Some("mm"))
    val sprinkle = precipitation.thriftscala.Precipitation(
      distance = Some(notMuch)
    )
    assertEquals(sprinkle, Precipitation.toThrift(Precipitation(Some(Distance(8, Some("mm"))))))
  }
}

