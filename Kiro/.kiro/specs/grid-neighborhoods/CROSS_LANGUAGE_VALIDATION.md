# Cross-Language Validation — Rust / C# / Ruby

Validates Requirement 9 (Multi-Language Implementation Consistency): all
implementations produce identical neighborhood counts for identical inputs.

## Method

Each implementation runs the same 26 canonical BDD scenarios and prints the
standardized line:

```
Scenario {N}: Expected={expected}, Grid={H}x{W}, N={threshold}, Pos=[{positions}], Got={actual}
```

The `Got` values were compared across all three new implementations and against
the canonical expected values (the C / Go / Java oracle).

## Result

All 26 scenarios: **identical across Rust, C#, and Ruby**, and every `Got`
equals its `Expected`.

| # | Grid | N | Positive cells | Expected | Rust | C# | Ruby |
|---|------|---|----------------|----------|------|----|----|
| 1 | 11x11 | 3 | (5,5) | 25 | 25 | 25 | 25 |
| 2 | 11x11 | 3 | (5,1) | 21 | 21 | 21 | 21 |
| 3 | 11x11 | 2 | (3,3),(7,7) | 26 | 26 | 26 | 26 |
| 4 | 11x11 | 2 | (3,3),(4,5) | 22 | 22 | 22 | 22 |
| 5 | 11x11 | 2 | (3,0),(4,2) | 18 | 18 | 18 | 18 |
| 6 | 11x11 | 2 | (0,0),(1,2) | 14 | 14 | 14 | 14 |
| 7 | 11x11 | 2 | (0,3),(1,5) | 17 | 17 | 17 | 17 |
| 8 | 11x11 | 2 | (3,8),(4,10) | 18 | 18 | 18 | 18 |
| 9 | 11x11 | 2 | (9,3),(10,5) | 17 | 17 | 17 | 17 |
| 10 | 11x11 | 2 | (3,3),(4,4) | 18 | 18 | 18 | 18 |
| 11 | 11x11 | 2 | (3,3),(3,4) | 18 | 18 | 18 | 18 |
| 12 | 11x11 | 2 | (3,4),(4,4) | 18 | 18 | 18 | 18 |
| 13 | 11x11 | 3 | (0,0),(10,10) | 20 | 20 | 20 | 20 |
| 14 | 11x11 | 3 | (10,9),(9,10),(10,10) | 15 | 15 | 15 | 15 |
| 15 | 1x21 | 3 | (0,9) | 7 | 7 | 7 | 7 |
| 16 | 21x1 | 3 | (10,0) | 7 | 7 | 7 | 7 |
| 17 | 1x1 | 0 | (0,0) | 1 | 1 | 1 | 1 |
| 18 | 20x20 | 0 | (0,0) | 1 | 1 | 1 | 1 |
| 19 | 2x2 | 2 | (0,1) | 4 | 4 | 4 | 4 |
| 20 | 21x3 | 5 | (10,2) | 27 | 27 | 27 | 27 |
| 21 | 4x15 | 5 | (2,9) | 36 | 36 | 36 | 36 |
| 22 | 2x2 | 3 | (0,1) | 4 | 4 | 4 | 4 |
| 23 | 2x2 | 100000 | (0,1) | 4 | 4 | 4 | 4 |
| 24 | 11x11 | 12 | (0,0) | 85 | 85 | 85 | 85 |
| 25 | 11x11 | 12 | (5,5) | 121 | 121 | 121 | 121 |
| 26 | 10x10 | 3 | (none) | 0 | 0 | 0 | 0 |

Property-based tests (13 correctness properties, >= 100 cases each) also pass in
all three implementations.

## How to reproduce

```
# Rust
cd rust  && cargo test --test bdd_scenarios -- --nocapture

# C#
cd csharp && dotnet test --logger "console;verbosity=detailed"

# Ruby
cd ruby  && ruby -Ilib -Itest test/bdd_scenarios_test.rb
```
