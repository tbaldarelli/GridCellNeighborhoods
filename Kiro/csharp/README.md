# Grid Cell Neighborhoods — C#

C# / .NET 8 implementation of the Grid Cell Neighborhoods algorithm: counts the
total number of unique grid cells within Manhattan distance `N` of any
positive-valued cell in a 2D grid.

Implemented directly from the spec in `../.kiro/specs/grid-neighborhoods/`
(requirements.md + design.md), not migrated from the other language versions.

## Layout

```
csharp/
  GridNeighborhoods.sln
  src/
    GridNeighborhoods.csproj
    Position.cs                 # Position record + Manhattan distance
    Grid.cs                     # Grid model + validation
    Exceptions.cs               # exception hierarchy
    BoundaryHandler.cs          # bounds checks / filtering
    NeighborhoodCalculator.cs   # diamond enumeration + union
  tests/
    GridNeighborhoods.Tests.csproj
    BddScenarioTests.cs         # 26 canonical BDD scenarios (xUnit)
    PropertyTests.cs            # 13 correctness properties (CsCheck)
```

## Build & test

```
dotnet test                         # run all tests
dotnet test -l "console;verbosity=detailed"   # show BDD scenario output lines
```

## Cross-language output

Each BDD scenario writes:

```
Scenario {N}: Expected={expected}, Grid={H}x{W}, N={threshold}, Pos=[{positions}], Got={actual}
```

matching the format used by the C, Go, Java, and Rust implementations.
