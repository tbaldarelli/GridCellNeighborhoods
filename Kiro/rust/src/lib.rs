//! Grid Cell Neighborhoods — Rust implementation.
//!
//! Counts the total number of unique grid cells that fall within Manhattan
//! distance neighborhoods of positive-valued cells in a 2D grid.
//!
//! Implemented from the spec in `.kiro/specs/grid-neighborhoods/`
//! (requirements.md + design.md), not migrated from another language.

pub mod boundary_handler;
pub mod errors;
pub mod grid;
pub mod neighborhood_calculator;
pub mod position;

pub use errors::GridError;
pub use grid::Grid;
pub use neighborhood_calculator::{
    count_neighborhood_cells, enumerate_neighborhood, get_neighborhood_cells,
};
pub use position::Position;
