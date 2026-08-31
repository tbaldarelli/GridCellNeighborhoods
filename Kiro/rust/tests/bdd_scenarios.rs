//! BDD scenario tests — the 26 canonical scenarios from the spec.
//!
//! Each test prints the standardized cross-language output line:
//!   Scenario {N}: Expected={expected}, Grid={H}x{W}, N={threshold}, Pos=[{positions}], Got={actual}
//! Run with `cargo test -- --nocapture` to see the output.

use grid_neighborhoods::{count_neighborhood_cells, Grid, Position};

fn run_scenario(
    scenario: u32,
    expected: usize,
    height: i64,
    width: i64,
    n: i64,
    positions: &[(i64, i64)],
) {
    let cells: Vec<Position> = positions.iter().map(|&(r, c)| Position::new(r, c)).collect();
    let grid = Grid::new(height, width, &cells).expect("grid should be valid");
    let got = count_neighborhood_cells(&grid, n).expect("count should succeed");

    let pos_str: Vec<String> = positions.iter().map(|&(r, c)| format!("({},{})", r, c)).collect();
    println!(
        "Scenario {}: Expected={}, Grid={}x{}, N={}, Pos=[{}], Got={}",
        scenario,
        expected,
        height,
        width,
        n,
        pos_str.join(","),
        got
    );
    assert_eq!(got, expected, "scenario {} mismatch", scenario);
}

#[test]
fn scenario_1_single_cell_fully_contained() {
    run_scenario(1, 25, 11, 11, 3, &[(5, 5)]);
}

#[test]
fn scenario_2_single_cell_near_edge() {
    run_scenario(2, 21, 11, 11, 3, &[(5, 1)]);
}

#[test]
fn scenario_3_non_overlapping() {
    run_scenario(3, 26, 11, 11, 2, &[(3, 3), (7, 7)]);
}

#[test]
fn scenario_4_overlapping() {
    run_scenario(4, 22, 11, 11, 2, &[(3, 3), (4, 5)]);
}

#[test]
fn scenario_5_overlapping_oob_left() {
    run_scenario(5, 18, 11, 11, 2, &[(3, 0), (4, 2)]);
}

#[test]
fn scenario_6_overlapping_oob_bottom_left() {
    run_scenario(6, 14, 11, 11, 2, &[(0, 0), (1, 2)]);
}

#[test]
fn scenario_7_overlapping_oob_bottom() {
    run_scenario(7, 17, 11, 11, 2, &[(0, 3), (1, 5)]);
}

#[test]
fn scenario_8_overlapping_oob_right() {
    run_scenario(8, 18, 11, 11, 2, &[(3, 8), (4, 10)]);
}

#[test]
fn scenario_9_overlapping_oob_top() {
    run_scenario(9, 17, 11, 11, 2, &[(9, 3), (10, 5)]);
}

#[test]
fn scenario_10_diagonally_adjacent() {
    run_scenario(10, 18, 11, 11, 2, &[(3, 3), (4, 4)]);
}

#[test]
fn scenario_11_same_row_adjacent() {
    run_scenario(11, 18, 11, 11, 2, &[(3, 3), (3, 4)]);
}

#[test]
fn scenario_12_same_column_adjacent() {
    run_scenario(12, 18, 11, 11, 2, &[(3, 4), (4, 4)]);
}

#[test]
fn scenario_13_opposite_corners() {
    run_scenario(13, 20, 11, 11, 3, &[(0, 0), (10, 10)]);
}

#[test]
fn scenario_14_three_in_one_corner() {
    run_scenario(14, 15, 11, 11, 3, &[(10, 9), (9, 10), (10, 10)]);
}

#[test]
fn scenario_15_1x21_grid() {
    run_scenario(15, 7, 1, 21, 3, &[(0, 9)]);
}

#[test]
fn scenario_16_21x1_grid() {
    run_scenario(16, 7, 21, 1, 3, &[(10, 0)]);
}

#[test]
fn scenario_17_1x1_grid() {
    run_scenario(17, 1, 1, 1, 0, &[(0, 0)]);
}

#[test]
fn scenario_18_20x20_threshold_zero() {
    run_scenario(18, 1, 20, 20, 0, &[(0, 0)]);
}

#[test]
fn scenario_19_2x2_grid() {
    run_scenario(19, 4, 2, 2, 2, &[(0, 1)]);
}

#[test]
fn scenario_20_21x3_n_greater_than_w() {
    run_scenario(20, 27, 21, 3, 5, &[(10, 2)]);
}

#[test]
fn scenario_21_4x15_n_greater_than_h() {
    run_scenario(21, 36, 4, 15, 5, &[(2, 9)]);
}

#[test]
fn scenario_22_2x2_n_greater_than_both() {
    run_scenario(22, 4, 2, 2, 3, &[(0, 1)]);
}

#[test]
fn scenario_23_2x2_n_much_greater() {
    run_scenario(23, 4, 2, 2, 100000, &[(0, 1)]);
}

#[test]
fn scenario_24_11x11_corner_large_n() {
    run_scenario(24, 85, 11, 11, 12, &[(0, 0)]);
}

#[test]
fn scenario_25_11x11_center_large_n() {
    run_scenario(25, 121, 11, 11, 12, &[(5, 5)]);
}

#[test]
fn scenario_26_no_positive_cells() {
    run_scenario(26, 0, 10, 10, 3, &[]);
}
