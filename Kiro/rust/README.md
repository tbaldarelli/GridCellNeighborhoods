# Grid Cell Neighborhoods — Rust

Rust implementation of the Grid Cell Neighborhoods algorithm: counts the total
number of unique grid cells within Manhattan distance `N` of any positive-valued
cell in a 2D grid.

Implemented directly from the spec in `../.kiro/specs/grid-neighborhoods/`
(requirements.md + design.md), not migrated from the other language versions.

## Layout

```
rust/
  Cargo.toml
  src/
    lib.rs                      # crate root, re-exports
    position.rs                 # Position + Manhattan distance
    grid.rs                     # Grid model + validation
    errors.rs                   # GridError variants
    boundary_handler.rs         # bounds checks / filtering
    neighborhood_calculator.rs  # diamond enumeration + union
  tests/
    bdd_scenarios.rs            # 26 canonical BDD scenarios
    properties.rs               # 13 correctness properties (proptest)
```

## Build & test

This project uses the GNU toolchain (`stable-x86_64-pc-windows-gnu`) — see
IMPLEMENTATION_NOTES.md for why. A `rustup override` is already set for this
directory.

```
cargo test                 # run all tests
cargo test -- --nocapture  # show the standardized BDD scenario output lines
```

## Cross-language output

Each BDD scenario prints:

```
Scenario {N}: Expected={expected}, Grid={H}x{W}, N={threshold}, Pos=[{positions}], Got={actual}
```

which matches the format used by the C, Go, and Java implementations for
side-by-side comparison.
