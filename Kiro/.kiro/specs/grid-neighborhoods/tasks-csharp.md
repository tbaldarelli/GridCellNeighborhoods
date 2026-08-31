# Implementation Plan: Grid Cell Neighborhoods — C#

Implemented from the spec (`requirements.md`, `design.md`), NOT migrated from another
language. The 26 BDD scenarios and 13 correctness properties are the oracle.

- Toolchain: .NET SDK 8.0.424
- Test framework: xUnit for unit/BDD; CsCheck for property-based tests
- Directory: `/csharp/`

## Status: COMPLETE — `dotnet test` = 39 tests (26 BDD + 13 properties) pass

## Canonical BDD Scenarios (oracle — expected counts)

| # | Grid | N | Positive cells | Expected |
|---|------|---|----------------|----------|
| 1 | 11x11 | 3 | (5,5) | 25 |
| 2 | 11x11 | 3 | (5,1) | 21 |
| 3 | 11x11 | 2 | (3,3),(7,7) | 26 |
| 4 | 11x11 | 2 | (3,3),(4,5) | 22 |
| 5 | 11x11 | 2 | (3,0),(4,2) | 18 |
| 6 | 11x11 | 2 | (0,0),(1,2) | 14 |
| 7 | 11x11 | 2 | (0,3),(1,5) | 17 |
| 8 | 11x11 | 2 | (3,8),(4,10) | 18 |
| 9 | 11x11 | 2 | (9,3),(10,5) | 17 |
| 10 | 11x11 | 2 | (3,3),(4,4) | 18 |
| 11 | 11x11 | 2 | (3,3),(3,4) | 18 |
| 12 | 11x11 | 2 | (3,4),(4,4) | 18 |
| 13 | 11x11 | 3 | (0,0),(10,10) | 20 |
| 14 | 11x11 | 3 | (10,9),(9,10),(10,10) | 15 |
| 15 | 1x21 | 3 | (0,9) | 7 |
| 16 | 21x1 | 3 | (10,0) | 7 |
| 17 | 1x1 | 0 | (0,0) | 1 |
| 18 | 20x20 | 0 | (0,0) | 1 |
| 19 | 2x2 | 2 | (0,1) | 4 |
| 20 | 21x3 | 5 | (10,2) | 27 |
| 21 | 4x15 | 5 | (2,9) | 36 |
| 22 | 2x2 | 3 | (0,1) | 4 |
| 23 | 2x2 | 100000 | (0,1) | 4 |
| 24 | 11x11 | 12 | (0,0) | 85 |
| 25 | 11x11 | 12 | (5,5) | 121 |
| 26 | 10x10 | 3 | (none) | 0 |

## Tasks

- [x] C1. Set up C# solution: `GridNeighborhoods` class lib + `GridNeighborhoods.Tests` xUnit project
- [x] C2. Implement `Position` (Row, Column, ManhattanDistance) — Requirements 2.1-2.3
- [x] C3. Implement `Grid` (Height, Width, positive cells, validation, IsValidPosition) — Requirements 1.1-1.4
- [x] C4. Implement exception types (InvalidGridDimensions, PositionOutOfBounds, InvalidDistanceThreshold) — Requirements 8.x
- [x] C5. Implement boundary handler (IsWithinBounds, FilterValidPositions) — Requirements 6.1-6.3
- [x] C6. Implement neighborhood calculator (diamond enumeration + union) — Requirements 3.x, 4.x, 5.x
- [x] C7. Implement edge-case handling (N=0, N>max w/ early-termination clamp, empty grid, degenerate) — Requirements 7.x, 8.3
- [x] C8. Write 26 BDD scenario tests with standardized output — All requirements
- [x] C9. Write property tests (Properties 1-13) using CsCheck, min 100 cases — Requirements 9.x
- [x] C10. Verify `dotnet test` passes; add README + IMPLEMENTATION_NOTES
