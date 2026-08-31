//! Boundary handling.
//!
//! Requirements 6.1-6.3: exclude out-of-bounds cells, no wraparound.

use crate::grid::Grid;
use crate::position::Position;
use std::collections::HashSet;

/// Whether a position is within the grid boundaries.
///
/// Requirement 6.2: no wraparound at grid edges.
pub fn is_within_bounds(pos: &Position, grid: &Grid) -> bool {
    grid.is_valid_position(pos)
}

/// Retain only positions that fall within the grid boundaries.
///
/// Requirement 6.1 / 6.3: out-of-bounds cells are excluded.
pub fn filter_valid_positions(positions: &HashSet<Position>, grid: &Grid) -> HashSet<Position> {
    positions
        .iter()
        .copied()
        .filter(|p| grid.is_valid_position(p))
        .collect()
}
