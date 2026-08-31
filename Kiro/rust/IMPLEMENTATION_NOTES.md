# Rust Implementation Notes

## Approach

Built from the spec (requirements.md + design.md). The core is the diamond
enumeration algorithm from design.md:

```
for delta_row in -N..=N:
    remaining = N - |delta_row|
    for delta_col in -remaining..=remaining:
        candidate = (center.row + delta_row, center.column + delta_col)
        if valid_position(candidate): add to set
```

The total neighborhood is the set-union of every positive cell's neighborhood,
so overlaps are de-duplicated automatically (Requirements 3.4 / 4.2 / 5.1).

## Design decisions

- **`i64` coordinates.** The spec allows a distance threshold as large as
  100000 (scenario 23) and requires validating negative dimensions
  (Property 1 draws down to -100). Using a signed 64-bit type keeps
  `center + delta` arithmetic safe without overflow across all tested inputs.
- **`Position` is `Copy + Hash + Eq`.** Cheap to store in a `HashSet`, which is
  the natural structure for the union.
- **Early-termination clamp (Requirement 8.3).** The raw algorithm loops
  `delta_row` over the full `[-N, N]` range. For scenario 23 (2x2 grid, N=100000)
  that is ~40 billion iterations that all get discarded by the bounds check —
  the naive version took ~237s. `enumerate_neighborhood` clamps the row and
  column delta ranges to the farthest reachable grid cell from the center, which
  makes the work proportional to the grid rather than to N. Results are
  unchanged (clamped cells were out of bounds anyway); the suite now runs in
  well under a second.

## Toolchain note (Windows)

The default Rust target on Windows is `x86_64-pc-windows-msvc`, which needs the
Visual Studio C++ build tools' `link.exe`. Those were not installed on this
machine, and an MSYS2 `link.exe` (a GNU coreutil) was shadowing the linker on
PATH, causing `link: extra operand` errors.

Rather than pull in the multi-GB Visual Studio build tools for a self-contained
exercise, this project uses the GNU toolchain
(`stable-x86_64-pc-windows-gnu`), which ships its own linker. A directory-level
`rustup override` is set so `cargo` in `rust/` uses it automatically.

## Testing

- 26 BDD scenarios in `tests/bdd_scenarios.rs`, each asserting the canonical
  expected count and printing the standardized comparison line.
- 13 properties in `tests/properties.rs` using `proptest`, 100 cases each,
  tagged with the design-document property numbers.
- `cargo test`: 26 + 13 pass.
