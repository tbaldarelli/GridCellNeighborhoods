//! Neighborhood calculator: diamond enumeration + union.
//!
//! Implements the core algorithm from design.md:
//!   for delta_row in -N..=N:
//!       remaining = N - |delta_row|
//!       for delta_col in -remaining..=remaining:
//!           candidate = (center.row + delta_row, center.col + delta_col)
//!           if valid_position(candidate): add to neighborhood
//!
//! Requirements 3.x (single cell), 4.x (non-overlapping), 5.x (overlapping union),
//! 7.x (edge cases).

use crate::errors::GridError;
use crate::grid::Grid;
use crate::position::Position;
use std::collections::HashSet;

/// Enumerate the neighborhood of a single center within Manhattan distance `n`,
/// clipped to the grid boundaries.
///
/// Requirement 3.1: the center itself is included (delta_row = delta_col = 0).
/// Requirement 3.2: all in-bounds cells within N steps are included.
/// Requirement 3.3: out-of-bounds cells are excluded (no wraparound).
pub fn enumerate_neighborhood(grid: &Grid, center: &Position, n: i64) -> HashSet<Position> {
    let mut neighborhood = HashSet::new();

    // Requirement 8.3 / design "Early Termination": clamp the row delta range to the
    // grid so an N far larger than the grid does not drive a huge empty scan. A row
    // delta can never usefully exceed the distance to the farthest grid row.
    let max_row_reach = (center.row).max(grid.height() - 1 - center.row);
    let row_span = n.min(max_row_reach);

    let mut delta_row = -row_span;
    while delta_row <= row_span {
        let remaining = n - delta_row.abs();
        // Likewise clamp the column delta range to the grid width.
        let max_col_reach = (center.column).max(grid.width() - 1 - center.column);
        let col_span = remaining.min(max_col_reach);

        let mut delta_col = -col_span;
        while delta_col <= col_span {
            let candidate = Position::new(center.row + delta_row, center.column + delta_col);
            if grid.is_valid_position(&candidate) {
                neighborhood.insert(candidate);
            }
            delta_col += 1;
        }
        delta_row += 1;
    }
    neighborhood
}

/// The union of all positive-cell neighborhoods within distance `n`.
///
/// Requirement 3.4 / 4.2 / 5.1: each cell appears at most once (set semantics).
/// Requirement 5.2: computes the union of all neighborhoods.
/// Requirement 7.1: empty positive-cell set yields an empty result.
pub fn get_neighborhood_cells(
    grid: &Grid,
    distance_threshold: i64,
) -> Result<HashSet<Position>, GridError> {
    if distance_threshold < 0 {
        return Err(GridError::InvalidDistanceThreshold { threshold: distance_threshold });
    }

    let mut all_cells = HashSet::new();
    for center in grid.positive_cells() {
        let neighborhood = enumerate_neighborhood(grid, center, distance_threshold);
        all_cells.extend(neighborhood);
    }
    Ok(all_cells)
}

/// Count of unique cells across all positive-cell neighborhoods.
///
/// Requirement 7.2: N=0 counts only the positive cells themselves.
/// Requirement 7.3: N exceeding grid dimensions counts all reachable grid cells.
pub fn count_neighborhood_cells(grid: &Grid, distance_threshold: i64) -> Result<usize, GridError> {
    Ok(get_neighborhood_cells(grid, distance_threshold)?.len())
}
