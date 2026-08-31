# Ruby Implementation Notes

## Approach

Built from the spec (requirements.md + design.md). Core is the diamond
enumeration algorithm from design.md; the total neighborhood is the set-union of
every positive cell's neighborhood, so overlaps de-duplicate automatically
(Requirements 3.4 / 4.2 / 5.1).

## Design decisions

- **`Position` defines `==`, `eql?`, and `hash`.** Ruby's `Set` uses `eql?` +
  `hash` for membership, so value-based equality is required for the union to
  de-duplicate correctly.
- **`Set` for the union** (`require 'set'`), mirroring the other implementations.
- **Early-termination clamp (Requirement 8.3).** `enumerate_neighborhood` clamps
  the row and column delta ranges to the farthest reachable grid cell from the
  center. Applied from the start (the Rust version showed the naive full
  `[-N, N]` scan makes scenario 23, a 2x2 grid with N=100000, take minutes).
  Ruby has arbitrary-precision integers so there is no overflow risk, but the
  clamp is still needed for the suite to finish quickly — with it, the BDD run
  is ~7ms.

## Property-based testing

Ruby 2.7 on this machine (MinGW build) has no reliable offline PBT gem, so
`test/property_helper.rb` provides a small dependency-free harness: a seeded
`Random` loop of >= 100 usable cases per property. On failure it reports the
seed and the offending input so the case can be reproduced. Generators may
return `nil` to skip an input (not counted toward the 100).

## Testing

- 26 BDD scenarios in `test/bdd_scenarios_test.rb` (minitest), each asserting the
  canonical expected count and printing the standardized comparison line.
- 13 properties in `test/properties_test.rb`, 100 iterations each, tagged with
  the design-document property numbers.
- Both suites pass: 26 + 13.

## Toolchain note

Ruby 2.7.5 (x64-mingw32) and bundler 2.1.4 were already installed — no setup
needed. minitest is part of the standard library, so the tests run without
`bundle install`. The `Gemfile` / `Rakefile` are provided for convenience but
are not required to run the tests.
