//! Error types for grid neighborhood operations.
//!
//! Requirements 8.1-8.3: input validation errors.

use crate::position::Position;
use std::fmt;

/// Errors produced during grid construction and neighborhood calculation.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum GridError {
    /// Grid created with height <= 0 or width <= 0.
    InvalidGridDimensions { height: i64, width: i64 },
    /// A positive cell position falls outside the grid boundaries.
    PositionOutOfBounds { position: Position, height: i64, width: i64 },
    /// Distance threshold N < 0.
    InvalidDistanceThreshold { threshold: i64 },
}

impl fmt::Display for GridError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            GridError::InvalidGridDimensions { height, width } => write!(
                f,
                "invalid grid dimensions: height={} width={} (both must be > 0)",
                height, width
            ),
            GridError::PositionOutOfBounds { position, height, width } => write!(
                f,
                "position ({}, {}) is out of bounds for a {}x{} grid",
                position.row, position.column, height, width
            ),
            GridError::InvalidDistanceThreshold { threshold } => write!(
                f,
                "invalid distance threshold: {} (must be >= 0)",
                threshold
            ),
        }
    }
}

impl std::error::Error for GridError {}
