//! Grid model.
//!
//! Requirements 1.1-1.4: grid initialization and validation.

use crate::errors::GridError;
use crate::position::Position;
use std::collections::HashSet;

/// A 2D grid of height x width with a set of positive-valued cells.
///
/// Invariants: `height > 0`, `width > 0`. All stored positive cells lie within
/// the grid boundaries.
#[derive(Debug, Clone)]
pub struct Grid {
    height: i64,
    width: i64,
    positive_cells: HashSet<Position>,
}

impl Grid {
    /// Create a grid with the given dimensions and positive cell positions.
    ///
    /// Requirement 1.1: validates height > 0 and width > 0.
    /// Requirement 1.2: validates all positive cell positions are in bounds.
    /// Requirement 1.4: stores positive cell positions.
    pub fn new(height: i64, width: i64, positive_cells: &[Position]) -> Result<Self, GridError> {
        if height <= 0 || width <= 0 {
            return Err(GridError::InvalidGridDimensions { height, width });
        }

        let mut cells = HashSet::new();
        for &pos in positive_cells {
            if pos.row < 0 || pos.row >= height || pos.column < 0 || pos.column >= width {
                return Err(GridError::PositionOutOfBounds { position: pos, height, width });
            }
            cells.insert(pos);
        }

        Ok(Grid { height, width, positive_cells: cells })
    }

    pub fn height(&self) -> i64 {
        self.height
    }

    pub fn width(&self) -> i64 {
        self.width
    }

    /// The stored positive cell positions.
    ///
    /// Requirement 1.4.
    pub fn positive_cells(&self) -> &HashSet<Position> {
        &self.positive_cells
    }

    /// Whether the position lies within the grid boundaries.
    ///
    /// Requirement 1.3 / 6.x: (0,0) .. (height-1, width-1) inclusive; no wraparound.
    pub fn is_valid_position(&self, pos: &Position) -> bool {
        pos.row >= 0 && pos.row < self.height && pos.column >= 0 && pos.column < self.width
    }
}
