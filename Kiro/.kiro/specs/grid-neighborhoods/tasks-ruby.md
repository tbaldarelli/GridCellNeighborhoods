# Implementation Plan: Grid Cell Neighborhoods — Ruby

Implemented from the spec (`requirements.md`, `design.md`), NOT migrated from another
language. The 26 BDD scenarios and 13 correctness properties are the oracle.

- Toolchain: ruby 2.7.5, bundler 2.1.4
- Test framework: minitest for unit/BDD; self-contained PBT harness for property-based tests
- Directory: `/ruby/`

## Status: COMPLETE — 26 BDD + 13 properties pass (minitest)

Note: switched PBT from `rantly` to a small self-contained seeded-random harness
(`test/property_helper.rb`) — no reliable offline PBT gem for Ruby 2.7 MinGW.

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

- [x] Rb1. Set up Ruby project structure (lib/, test/, Gemfile, Rakefile)
- [x] Rb2. Implement `Position` (row, column, manhattan_distance) — Requirements 2.1-2.3
- [x] Rb3. Implement `Grid` (height, width, positive cells, validation, valid_position?) — Requirements 1.1-1.4
- [x] Rb4. Implement error classes (InvalidGridDimensions, PositionOutOfBounds, InvalidDistanceThreshold) — Requirements 8.x
- [x] Rb5. Implement boundary handler (within_bounds?, filter_valid_positions) — Requirements 6.1-6.3
- [x] Rb6. Implement neighborhood calculator (diamond enumeration + union) — Requirements 3.x, 4.x, 5.x
- [x] Rb7. Implement edge-case handling (N=0, N>max w/ early-termination clamp, empty grid, degenerate) — Requirements 7.x, 8.3
- [x] Rb8. Write 26 BDD scenario tests with standardized output — All requirements
- [x] Rb9. Write property tests (Properties 1-13), min 100 cases — Requirements 9.x
- [x] Rb10. Verify tests pass; add README + IMPLEMENTATION_NOTES
