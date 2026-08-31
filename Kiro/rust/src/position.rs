//! Position within the grid.
//!
//! Requirements 2.1-2.3: Manhattan distance calculation.
//! A position uses (row, column) coordinates where (0,0) is the bottom-left corner.

/// A cell position in the grid, identified by (row, column).
///
/// Coordinates are non-negative. `(0,0)` represents the bottom-left corner
/// per the coordinate system defined in the spec glossary.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct Position {
    pub row: i64,
    pub column: i64,
}

impl Position {
    /// Create a new position.
    pub fn new(row: i64, column: i64) -> Self {
        Position { row, column }
    }

    /// Manhattan distance to another position: `|r1 - r2| + |c1 - c2|`.
    ///
    /// Requirement 2.1: computes |row1 - row2| + |column1 - column2|.
    /// Requirement 2.2: always returns a non-negative integer.
    /// Requirement 2.3: returns 0 when positions are identical.
    pub fn manhattan_distance(&self, other: &Position) -> i64 {
        (self.row - other.row).abs() + (self.column - other.column).abs()
    }
}
