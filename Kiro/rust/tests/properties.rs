//! Property-based tests — the 13 correctness properties from the spec.
//!
//! Uses proptest with a minimum of 100 cases per property.

use grid_neighborhoods::{
    boundary_handler, count_neighborhood_cells, enumerate_neighborhood, get_neighborhood_cells,
    Grid, GridError, Position,
};
use proptest::collection::vec as pvec;
use proptest::prelude::*;
use std::collections::HashSet;

proptest! {
    #![proptest_config(ProptestConfig::with_cases(100))]

    /// Feature: grid-neighborhoods, Property 1: Grid Validation
    /// Validates: Requirements 1.1, 1.2
    #[test]
    fn property_1_grid_validation(height in -100i64..1000, width in -100i64..1000) {
        let result = Grid::new(height, width, &[]);
        if height > 0 && width > 0 {
            let grid = result.expect("valid dimensions should succeed");
            prop_assert_eq!(grid.height(), height);
            prop_assert_eq!(grid.width(), width);
        } else {
            let is_invalid_dims = matches!(result, Err(GridError::InvalidGridDimensions { .. }));
            prop_assert!(is_invalid_dims);
        }
    }

    /// Feature: grid-neighborhoods, Property 2: Manhattan Distance Calculation
    /// Validates: Requirements 2.1, 2.2, 2.3
    #[test]
    fn property_2_manhattan_distance(
        r1 in 0i64..1000, c1 in 0i64..1000, r2 in 0i64..1000, c2 in 0i64..1000
    ) {
        let p1 = Position::new(r1, c1);
        let p2 = Position::new(r2, c2);
        let d = p1.manhattan_distance(&p2);

        prop_assert_eq!(d, (r1 - r2).abs() + (c1 - c2).abs());
        prop_assert!(d >= 0);
        if r1 == r2 && c1 == c2 {
            prop_assert_eq!(d, 0);
        }
        // symmetric
        prop_assert_eq!(d, p2.manhattan_distance(&p1));
    }

    /// Feature: grid-neighborhoods, Property 3: Coordinate System Consistency
    /// Validates: Requirements 1.3, 1.4
    #[test]
    fn property_3_coordinate_system(height in 1i64..50, width in 1i64..50) {
        let grid = Grid::new(height, width, &[]).unwrap();
        prop_assert!(grid.is_valid_position(&Position::new(0, 0)));
        prop_assert!(grid.is_valid_position(&Position::new(height - 1, width - 1)));
        prop_assert!(!grid.is_valid_position(&Position::new(height, 0)));
        prop_assert!(!grid.is_valid_position(&Position::new(0, width)));
    }

    /// Feature: grid-neighborhoods, Property 4: Self-Inclusion in Neighborhoods
    /// Validates: Requirements 3.1
    #[test]
    fn property_4_self_inclusion(
        height in 1i64..20, width in 1i64..20, n in 0i64..20
    ) {
        let row = height / 2;
        let col = width / 2;
        let center = Position::new(row, col);
        let grid = Grid::new(height, width, &[center]).unwrap();

        let neighborhood = get_neighborhood_cells(&grid, n).unwrap();
        prop_assert!(neighborhood.contains(&center));
        prop_assert!(count_neighborhood_cells(&grid, n).unwrap() >= 1);
    }

    /// Feature: grid-neighborhoods, Property 5: Complete Neighborhood Enumeration
    /// Validates: Requirements 3.2
    #[test]
    fn property_5_complete_enumeration(n in 1i64..10) {
        // Grid large enough that the full diamond fits with the center away from edges.
        let height = 2 * n + 3;
        let width = 2 * n + 3;
        let center = Position::new(n + 1, n + 1);
        let grid = Grid::new(height, width, &[center]).unwrap();

        let neighborhood = enumerate_neighborhood(&grid, &center, n);
        // Diamond size formula: (N+1)^2 + N^2
        let expected = ((n + 1) * (n + 1) + n * n) as usize;
        prop_assert_eq!(neighborhood.len(), expected);
    }

    /// Feature: grid-neighborhoods, Property 6: Boundary Constraint Enforcement
    /// Validates: Requirements 3.3, 6.1, 6.2, 6.3
    #[test]
    fn property_6_boundary_enforcement(
        height in 1i64..20, width in 1i64..20, n in 0i64..20
    ) {
        let center = Position::new(0, 0);
        let grid = Grid::new(height, width, &[center]).unwrap();
        let neighborhood = enumerate_neighborhood(&grid, &center, n);

        for cell in &neighborhood {
            prop_assert!(boundary_handler::is_within_bounds(cell, &grid));
            prop_assert!(cell.row >= 0 && cell.row < height);
            prop_assert!(cell.column >= 0 && cell.column < width);
        }
    }

    /// Feature: grid-neighborhoods, Property 7: Cell Uniqueness Guarantee
    /// Validates: Requirements 3.4, 4.2, 5.1
    #[test]
    fn property_7_cell_uniqueness(
        height in 1i64..30, width in 1i64..30, n in 0i64..20,
        raw in pvec((0i64..30, 0i64..30), 1..10)
    ) {
        let cells: Vec<Position> = raw.iter()
            .filter(|&&(r, c)| r < height && c < width)
            .map(|&(r, c)| Position::new(r, c))
            .collect();
        prop_assume!(!cells.is_empty());

        let grid = Grid::new(height, width, &cells).unwrap();
        let all_cells = get_neighborhood_cells(&grid, n).unwrap();
        let count = count_neighborhood_cells(&grid, n).unwrap();
        prop_assert_eq!(count, all_cells.len());

        // total <= sum of individual counts (overlaps only reduce)
        let sum_individual: usize = grid.positive_cells().iter()
            .map(|c| enumerate_neighborhood(&grid, c, n).len())
            .sum();
        prop_assert!(count <= sum_individual);
    }

    /// Feature: grid-neighborhoods, Property 8: Non-Overlapping Additivity
    /// Validates: Requirements 4.1, 4.3
    #[test]
    fn property_8_non_overlapping_additivity(n in 1i64..8) {
        let min_separation = 2 * n + 1;
        let height = min_separation + 2 * n + 2;
        let width = min_separation + 2 * n + 2;

        let p1 = Position::new(n, n);
        let p2 = Position::new(n + min_separation, n + min_separation);
        let grid = Grid::new(height, width, &[p1, p2]).unwrap();

        let nb1 = enumerate_neighborhood(&grid, &p1, n);
        let nb2 = enumerate_neighborhood(&grid, &p2, n);
        let overlap: HashSet<_> = nb1.intersection(&nb2).collect();
        prop_assert_eq!(overlap.len(), 0);

        let total = count_neighborhood_cells(&grid, n).unwrap();
        prop_assert_eq!(total, nb1.len() + nb2.len());
    }

    /// Feature: grid-neighborhoods, Property 9: Overlapping Union Behavior
    /// Validates: Requirements 5.2, 5.3
    #[test]
    fn property_9_overlapping_union(n in 2i64..8) {
        let height = 2 * n + 10;
        let width = 2 * n + 10;
        let p1 = Position::new(n + 1, n + 1);
        let p2 = Position::new(n + 2, n + 2); // close -> overlap
        let grid = Grid::new(height, width, &[p1, p2]).unwrap();

        let nb1 = enumerate_neighborhood(&grid, &p1, n);
        let nb2 = enumerate_neighborhood(&grid, &p2, n);
        let overlap: HashSet<_> = nb1.intersection(&nb2).collect();
        prop_assert!(overlap.len() > 0);

        let total = count_neighborhood_cells(&grid, n).unwrap();
        prop_assert!(total < nb1.len() + nb2.len());
    }

    /// Feature: grid-neighborhoods, Property 10: Zero Distance Threshold
    /// Validates: Requirements 7.2
    #[test]
    fn property_10_zero_distance(
        height in 1i64..20, width in 1i64..20,
        raw in pvec((0i64..20, 0i64..20), 1..20)
    ) {
        let cells: Vec<Position> = raw.iter()
            .filter(|&&(r, c)| r < height && c < width)
            .map(|&(r, c)| Position::new(r, c))
            .collect();
        prop_assume!(!cells.is_empty());

        let grid = Grid::new(height, width, &cells).unwrap();
        let count = count_neighborhood_cells(&grid, 0).unwrap();
        prop_assert_eq!(count, grid.positive_cells().len());
    }

    /// Feature: grid-neighborhoods, Property 11: Maximum Distance Threshold
    /// Validates: Requirements 7.3
    #[test]
    fn property_11_maximum_distance(
        height in 1i64..20, width in 1i64..20,
        raw in pvec((0i64..20, 0i64..20), 1..10)
    ) {
        let cells: Vec<Position> = raw.iter()
            .filter(|&&(r, c)| r < height && c < width)
            .map(|&(r, c)| Position::new(r, c))
            .collect();
        prop_assume!(!cells.is_empty());

        let grid = Grid::new(height, width, &cells).unwrap();
        let max_distance = (height - 1) + (width - 1);
        let count = count_neighborhood_cells(&grid, max_distance + 10).unwrap();
        prop_assert_eq!(count, (height * width) as usize);
    }

    /// Feature: grid-neighborhoods, Property 12: Degenerate Grid Handling
    /// Validates: Requirements 7.4
    #[test]
    fn property_12_degenerate_grid(
        grid_type in 0u8..3, dimension in 1i64..50, n in 0i64..20
    ) {
        let (height, width, center) = match grid_type {
            0 => (1, dimension, Position::new(0, dimension / 2)),
            1 => (dimension, 1, Position::new(dimension / 2, 0)),
            _ => (1, 1, Position::new(0, 0)),
        };
        let grid = Grid::new(height, width, &[center]).unwrap();
        let neighborhood = get_neighborhood_cells(&grid, n).unwrap();
        let count = count_neighborhood_cells(&grid, n).unwrap();

        prop_assert_eq!(neighborhood.len(), count);
        prop_assert!(neighborhood.contains(&center));
        // Every cell in the result is within Manhattan distance n of the center.
        for cell in &neighborhood {
            prop_assert!(center.manhattan_distance(cell) <= n);
        }
        if grid_type == 2 {
            prop_assert_eq!(count, 1);
        }
    }

    /// Feature: grid-neighborhoods, Property 13: Cross-Language Result Consistency
    /// Validates: Requirements 9.1, 9.3, 9.4
    ///
    /// Verifies determinism: the same input always yields the same count.
    /// True cross-language validation is done by comparing BDD scenario output.
    #[test]
    fn property_13_deterministic(
        height in 1i64..30, width in 1i64..30, n in 0i64..15,
        raw in pvec((0i64..30, 0i64..30), 1..5)
    ) {
        let cells: Vec<Position> = raw.iter()
            .filter(|&&(r, c)| r < height && c < width)
            .map(|&(r, c)| Position::new(r, c))
            .collect();
        prop_assume!(!cells.is_empty());

        let grid = Grid::new(height, width, &cells).unwrap();
        let count1 = count_neighborhood_cells(&grid, n).unwrap();
        let count2 = count_neighborhood_cells(&grid, n).unwrap();
        prop_assert_eq!(count1, count2);
    }
}
