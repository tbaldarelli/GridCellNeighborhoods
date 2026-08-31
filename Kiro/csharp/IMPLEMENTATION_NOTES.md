# C# Implementation Notes

## Approach

Built from the spec (requirements.md + design.md). Core is the diamond
enumeration algorithm from design.md; the total neighborhood is the set-union of
every positive cell's neighborhood, so overlaps de-duplicate automatically
(Requirements 3.4 / 4.2 / 5.1).

## Design decisions

- **`Position` is a `readonly record struct`.** Value semantics give correct
  `Equals`/`GetHashCode` for free, which is what `HashSet<Position>` relies on
  for the union.
- **`long` coordinates.** Scenario 23 uses N=100000 and Property 1 draws
  dimensions down to -100; signed 64-bit keeps `center + delta` arithmetic and
  the validation comparisons safe.
- **Early-termination clamp (Requirement 8.3).** `EnumerateNeighborhood` clamps
  the row and column delta ranges to the farthest reachable grid cell from the
  center. Applied from the start (the Rust version showed that the naive full
  `[-N, N]` scan makes scenario 23 take minutes). Work is proportional to the
  grid, not to N.
- **Exception hierarchy.** `InvalidGridDimensionsException`,
  `PositionOutOfBoundsException`, and `InvalidDistanceThresholdException` all
  derive from `GridNeighborhoodsException` (Requirements 8.1-8.3).

## Testing

- 26 BDD scenarios in `tests/BddScenarioTests.cs` (xUnit), each asserting the
  canonical expected count and writing the standardized comparison line via
  `ITestOutputHelper`.
- 13 properties in `tests/PropertyTests.cs` using CsCheck, 100 iterations each
  (`iter: 100`), tagged with the design-document property numbers.
- `dotnet test`: 39 tests pass (26 + 13).

## Toolchain note

.NET SDK 8.0.424 (installed via winget). No special configuration needed —
unlike the Rust setup, the .NET toolchain is self-contained on Windows and had
no linker conflicts. NuGet restored xUnit, Microsoft.NET.Test.Sdk, and CsCheck
with floating version ranges.
