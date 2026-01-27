/**
 * BDD scenario tests for grid neighborhoods.
 * 
 * This test suite implements the 26 BDD scenarios from grid-neighborhoods.feature.md
 * Each scenario validates the system against concrete examples with specific expected counts.
 * 
 * All scenarios use an 11x11 grid unless otherwise specified.
 */

#include <check.h>
#include <stdio.h>
#include "../include/grid.h"
#include "../include/position.h"
#include "../include/neighborhood_calculator.h"
#include "../include/exceptions.h"

/* Helper function to print scenario results */
static void print_scenario(int scenario_num, int expected, int height, int width, 
                          int distance_threshold, Position* positions, int num_positions, int got) {
    printf("Scenario %d: Expected=%d, Grid=%dx%d, N=%d, Pos=[", 
           scenario_num, expected, height, width, distance_threshold);
    for (int i = 0; i < num_positions; i++) {
        printf("(%d,%d)", positions[i].row, positions[i].column);
        if (i < num_positions - 1) printf(",");
    }
    printf("], Got=%d\n", got);
}

/* Scenario 1: Single positive cell fully contained */
START_TEST(test_scenario_1_single_positive_cell_fully_contained) {
    Position pos = position_create(5, 5);
    Grid* grid = grid_create(11, 11, &pos, 1);
    
    ErrorCode error_code = ERROR_NONE;
    int count = neighborhood_calculator_count(grid, 3, &error_code);
    
    print_scenario(1, 25, 11, 11, 3, &pos, 1, count);
    ck_assert_int_eq(count, 25);
    
    grid_destroy(grid);
}
END_TEST

/* Scenario 2: Single positive cell near a grid edge */
START_TEST(test_scenario_2_single_positive_cell_near_edge) {
    Position pos = position_create(5, 1);
    Grid* grid = grid_create(11, 11, &pos, 1);
    
    ErrorCode error_code = ERROR_NONE;
    int count = neighborhood_calculator_count(grid, 3, &error_code);
    
    print_scenario(2, 21, 11, 11, 3, &pos, 1, count);
    ck_assert_int_eq(count, 21);
    
    grid_destroy(grid);
}
END_TEST

/* Scenario 3: Multiple positive cells with non-overlapping neighborhoods */
START_TEST(test_scenario_3_non_overlapping_neighborhoods) {
    Position positions[2] = {
        position_create(3, 3),
        position_create(7, 7)
    };
    Grid* grid = grid_create(11, 11, positions, 2);
    
    ErrorCode error_code = ERROR_NONE;
    int count = neighborhood_calculator_count(grid, 2, &error_code);
    
    print_scenario(3, 26, 11, 11, 2, positions, 2, count);
    ck_assert_int_eq(count, 26);
    
    grid_destroy(grid);
}
END_TEST

/* Scenario 4: Multiple positive cells with overlapping neighborhoods */
START_TEST(test_scenario_4_overlapping_neighborhoods) {
    Position positions[2] = {
        position_create(3, 3),
        position_create(4, 5)
    };
    Grid* grid = grid_create(11, 11, positions, 2);
    
    ErrorCode error_code = ERROR_NONE;
    int count = neighborhood_calculator_count(grid, 2, &error_code);
    
    print_scenario(4, 22, 11, 11, 2, positions, 2, count);
    ck_assert_int_eq(count, 22);
    
    grid_destroy(grid);
}
END_TEST

/* Scenario 5: Overlapping neighborhoods, out of bounds on left */
START_TEST(test_scenario_5_overlapping_out_of_bounds_left) {
    Position positions[2] = {
        position_create(3, 0),
        position_create(4, 2)
    };
    Grid* grid = grid_create(11, 11, positions, 2);
    
    ErrorCode error_code = ERROR_NONE;
    int count = neighborhood_calculator_count(grid, 2, &error_code);
    
    print_scenario(5, 18, 11, 11, 2, positions, 2, count);
    ck_assert_int_eq(count, 18);
    
    grid_destroy(grid);
}
END_TEST

/* Scenario 6: Overlapping neighborhoods, out of bounds on bottom left */
START_TEST(test_scenario_6_overlapping_out_of_bounds_bottom_left) {
    Position positions[2] = {
        position_create(0, 0),
        position_create(1, 2)
    };
    Grid* grid = grid_create(11, 11, positions, 2);
    
    ErrorCode error_code = ERROR_NONE;
    int count = neighborhood_calculator_count(grid, 2, &error_code);
    
    print_scenario(6, 14, 11, 11, 2, positions, 2, count);
    ck_assert_int_eq(count, 14);
    
    grid_destroy(grid);
}
END_TEST

/* Scenario 7: Overlapping neighborhoods, out of bounds on bottom */
START_TEST(test_scenario_7_overlapping_out_of_bounds_bottom) {
    Position positions[2] = {
        position_create(0, 3),
        position_create(1, 5)
    };
    Grid* grid = grid_create(11, 11, positions, 2);
    
    ErrorCode error_code = ERROR_NONE;
    int count = neighborhood_calculator_count(grid, 2, &error_code);
    
    print_scenario(7, 17, 11, 11, 2, positions, 2, count);
    ck_assert_int_eq(count, 17);
    
    grid_destroy(grid);
}
END_TEST

/* Scenario 8: Overlapping neighborhoods, out of bounds right */
START_TEST(test_scenario_8_overlapping_out_of_bounds_right) {
    Position positions[2] = {
        position_create(3, 8),
        position_create(4, 10)
    };
    Grid* grid = grid_create(11, 11, positions, 2);
    
    ErrorCode error_code = ERROR_NONE;
    int count = neighborhood_calculator_count(grid, 2, &error_code);
    
    print_scenario(8, 18, 11, 11, 2, positions, 2, count);
    ck_assert_int_eq(count, 18);
    
    grid_destroy(grid);
}
END_TEST

/* Scenario 9: Overlapping neighborhoods, out of bounds top */
START_TEST(test_scenario_9_overlapping_out_of_bounds_top) {
    Position positions[2] = {
        position_create(9, 3),
        position_create(10, 5)
    };
    Grid* grid = grid_create(11, 11, positions, 2);
    
    ErrorCode error_code = ERROR_NONE;
    int count = neighborhood_calculator_count(grid, 2, &error_code);
    
    print_scenario(9, 17, 11, 11, 2, positions, 2, count);
    ck_assert_int_eq(count, 17);
    
    grid_destroy(grid);
}
END_TEST

/* Scenario 10: Overlapping neighborhoods, diagonally adjacent */
START_TEST(test_scenario_10_overlapping_diagonally_adjacent) {
    Position positions[2] = {
        position_create(3, 3),
        position_create(4, 4)
    };
    Grid* grid = grid_create(11, 11, positions, 2);
    
    ErrorCode error_code = ERROR_NONE;
    int count = neighborhood_calculator_count(grid, 2, &error_code);
    
    print_scenario(10, 18, 11, 11, 2, positions, 2, count);
    ck_assert_int_eq(count, 18);
    
    grid_destroy(grid);
}
END_TEST

/* Scenario 11: Overlapping neighborhoods, same row adjacent */
START_TEST(test_scenario_11_overlapping_same_row_adjacent) {
    Position positions[2] = {
        position_create(3, 3),
        position_create(3, 4)
    };
    Grid* grid = grid_create(11, 11, positions, 2);
    
    ErrorCode error_code = ERROR_NONE;
    int count = neighborhood_calculator_count(grid, 2, &error_code);
    
    print_scenario(11, 18, 11, 11, 2, positions, 2, count);
    ck_assert_int_eq(count, 18);
    
    grid_destroy(grid);
}
END_TEST

/* Scenario 12: Overlapping neighborhoods, same column adjacent */
START_TEST(test_scenario_12_overlapping_same_column_adjacent) {
    Position positions[2] = {
        position_create(3, 4),
        position_create(4, 4)
    };
    Grid* grid = grid_create(11, 11, positions, 2);
    
    ErrorCode error_code = ERROR_NONE;
    int count = neighborhood_calculator_count(grid, 2, &error_code);
    
    print_scenario(12, 18, 11, 11, 2, positions, 2, count);
    ck_assert_int_eq(count, 18);
    
    grid_destroy(grid);
}
END_TEST

/* Scenario 13: Multiple positive cells, opposite corners */
START_TEST(test_scenario_13_opposite_corners) {
    Position positions[2] = {
        position_create(0, 0),
        position_create(10, 10)
    };
    Grid* grid = grid_create(11, 11, positions, 2);
    
    ErrorCode error_code = ERROR_NONE;
    int count = neighborhood_calculator_count(grid, 3, &error_code);
    
    print_scenario(13, 20, 11, 11, 3, positions, 2, count);
    ck_assert_int_eq(count, 20);
    
    grid_destroy(grid);
}
END_TEST

/* Scenario 14: Multiple positive cells, 3 in one corner */
START_TEST(test_scenario_14_three_in_one_corner) {
    Position positions[3] = {
        position_create(10, 9),
        position_create(9, 10),
        position_create(10, 10)
    };
    Grid* grid = grid_create(11, 11, positions, 3);
    
    ErrorCode error_code = ERROR_NONE;
    int count = neighborhood_calculator_count(grid, 3, &error_code);
    
    print_scenario(14, 15, 11, 11, 3, positions, 3, count);
    ck_assert_int_eq(count, 15);
    
    grid_destroy(grid);
}
END_TEST

/* Scenario 15: One positive cell, 1x21 grid */
START_TEST(test_scenario_15_1x21_grid) {
    Position pos = position_create(0, 9);
    Grid* grid = grid_create(1, 21, &pos, 1);
    
    ErrorCode error_code = ERROR_NONE;
    int count = neighborhood_calculator_count(grid, 3, &error_code);
    
    print_scenario(15, 7, 1, 21, 3, &pos, 1, count);
    ck_assert_int_eq(count, 7);
    
    grid_destroy(grid);
}
END_TEST

/* Scenario 16: One positive cell, 21x1 grid */
START_TEST(test_scenario_16_21x1_grid) {
    Position pos = position_create(10, 0);
    Grid* grid = grid_create(21, 1, &pos, 1);
    
    ErrorCode error_code = ERROR_NONE;
    int count = neighborhood_calculator_count(grid, 3, &error_code);
    
    print_scenario(16, 7, 21, 1, 3, &pos, 1, count);
    ck_assert_int_eq(count, 7);
    
    grid_destroy(grid);
}
END_TEST

/* Scenario 17: One positive cell, 1x1 grid */
START_TEST(test_scenario_17_1x1_grid) {
    Position pos = position_create(0, 0);
    Grid* grid = grid_create(1, 1, &pos, 1);
    
    ErrorCode error_code = ERROR_NONE;
    int count = neighborhood_calculator_count(grid, 0, &error_code);
    
    print_scenario(17, 1, 1, 1, 0, &pos, 1, count);
    ck_assert_int_eq(count, 1);
    
    grid_destroy(grid);
}
END_TEST

/* Scenario 18: One positive cell, 20x20 grid, threshold zero */
START_TEST(test_scenario_18_20x20_grid_threshold_zero) {
    Position pos = position_create(0, 0);
    Grid* grid = grid_create(20, 20, &pos, 1);
    
    ErrorCode error_code = ERROR_NONE;
    int count = neighborhood_calculator_count(grid, 0, &error_code);
    
    print_scenario(18, 1, 20, 20, 0, &pos, 1, count);
    ck_assert_int_eq(count, 1);
    
    grid_destroy(grid);
}
END_TEST

/* Scenario 19: One positive cell, 2x2 grid */
START_TEST(test_scenario_19_2x2_grid) {
    Position pos = position_create(0, 1);
    Grid* grid = grid_create(2, 2, &pos, 1);
    
    ErrorCode error_code = ERROR_NONE;
    int count = neighborhood_calculator_count(grid, 2, &error_code);
    
    print_scenario(19, 4, 2, 2, 2, &pos, 1, count);
    ck_assert_int_eq(count, 4);
    
    grid_destroy(grid);
}
END_TEST

/* Scenario 20: One positive cell, 21x3 grid, N > W */
START_TEST(test_scenario_20_21x3_grid_n_greater_than_w) {
    Position pos = position_create(10, 2);
    Grid* grid = grid_create(21, 3, &pos, 1);
    
    ErrorCode error_code = ERROR_NONE;
    int count = neighborhood_calculator_count(grid, 5, &error_code);
    
    print_scenario(20, 27, 21, 3, 5, &pos, 1, count);
    ck_assert_int_eq(count, 27);
    
    grid_destroy(grid);
}
END_TEST

/* Scenario 21: One positive cell, 4x15 grid, N > H */
START_TEST(test_scenario_21_4x15_grid_n_greater_than_h) {
    Position pos = position_create(2, 9);
    Grid* grid = grid_create(4, 15, &pos, 1);
    
    ErrorCode error_code = ERROR_NONE;
    int count = neighborhood_calculator_count(grid, 5, &error_code);
    
    print_scenario(21, 36, 4, 15, 5, &pos, 1, count);
    ck_assert_int_eq(count, 36);
    
    grid_destroy(grid);
}
END_TEST

/* Scenario 22: One positive cell, 2x2 grid, N > H and W */
START_TEST(test_scenario_22_2x2_grid_n_greater_than_both) {
    Position pos = position_create(0, 1);
    Grid* grid = grid_create(2, 2, &pos, 1);
    
    ErrorCode error_code = ERROR_NONE;
    int count = neighborhood_calculator_count(grid, 3, &error_code);
    
    print_scenario(22, 4, 2, 2, 3, &pos, 1, count);
    ck_assert_int_eq(count, 4);
    
    grid_destroy(grid);
}
END_TEST

/* Scenario 23: One positive cell, 2x2 grid, N much > H and W */
START_TEST(test_scenario_23_2x2_grid_n_much_greater) {
    Position pos = position_create(0, 1);
    Grid* grid = grid_create(2, 2, &pos, 1);
    
    ErrorCode error_code = ERROR_NONE;
    int count = neighborhood_calculator_count(grid, 100000, &error_code);
    
    print_scenario(23, 4, 2, 2, 100000, &pos, 1, count);
    ck_assert_int_eq(count, 4);
    
    grid_destroy(grid);
}
END_TEST

/* Scenario 24: One positive cell at (0,0), 11x11 grid, N > H and W */
START_TEST(test_scenario_24_11x11_grid_corner_large_n) {
    Position pos = position_create(0, 0);
    Grid* grid = grid_create(11, 11, &pos, 1);
    
    ErrorCode error_code = ERROR_NONE;
    int count = neighborhood_calculator_count(grid, 12, &error_code);
    
    print_scenario(24, 85, 11, 11, 12, &pos, 1, count);
    ck_assert_int_eq(count, 85);
    
    grid_destroy(grid);
}
END_TEST

/* Scenario 25: One positive cell at (5,5), 11x11 grid, N > H and W */
START_TEST(test_scenario_25_11x11_grid_center_large_n) {
    Position pos = position_create(5, 5);
    Grid* grid = grid_create(11, 11, &pos, 1);
    
    ErrorCode error_code = ERROR_NONE;
    int count = neighborhood_calculator_count(grid, 12, &error_code);
    
    print_scenario(25, 121, 11, 11, 12, &pos, 1, count);
    ck_assert_int_eq(count, 121);
    
    grid_destroy(grid);
}
END_TEST

/* Scenario 26: No positive cells */
START_TEST(test_scenario_26_no_positive_cells) {
    Grid* grid = grid_create(10, 10, NULL, 0);
    
    ErrorCode error_code = ERROR_NONE;
    int count = neighborhood_calculator_count(grid, 3, &error_code);
    
    Position empty_positions[1]; /* Just for print function */
    print_scenario(26, 0, 10, 10, 3, empty_positions, 0, count);
    ck_assert_int_eq(count, 0);
    
    grid_destroy(grid);
}
END_TEST

/* Test suite setup */
Suite* bdd_scenarios_suite(void) {
    Suite* s = suite_create("BDD Scenarios");
    
    TCase* tc_single = tcase_create("Single Positive Cell");
    tcase_add_test(tc_single, test_scenario_1_single_positive_cell_fully_contained);
    tcase_add_test(tc_single, test_scenario_2_single_positive_cell_near_edge);
    suite_add_tcase(s, tc_single);
    
    TCase* tc_non_overlapping = tcase_create("Non-Overlapping Neighborhoods");
    tcase_add_test(tc_non_overlapping, test_scenario_3_non_overlapping_neighborhoods);
    suite_add_tcase(s, tc_non_overlapping);
    
    TCase* tc_overlapping = tcase_create("Overlapping Neighborhoods");
    tcase_add_test(tc_overlapping, test_scenario_4_overlapping_neighborhoods);
    tcase_add_test(tc_overlapping, test_scenario_5_overlapping_out_of_bounds_left);
    tcase_add_test(tc_overlapping, test_scenario_6_overlapping_out_of_bounds_bottom_left);
    tcase_add_test(tc_overlapping, test_scenario_7_overlapping_out_of_bounds_bottom);
    tcase_add_test(tc_overlapping, test_scenario_8_overlapping_out_of_bounds_right);
    tcase_add_test(tc_overlapping, test_scenario_9_overlapping_out_of_bounds_top);
    tcase_add_test(tc_overlapping, test_scenario_10_overlapping_diagonally_adjacent);
    tcase_add_test(tc_overlapping, test_scenario_11_overlapping_same_row_adjacent);
    tcase_add_test(tc_overlapping, test_scenario_12_overlapping_same_column_adjacent);
    tcase_add_test(tc_overlapping, test_scenario_13_opposite_corners);
    tcase_add_test(tc_overlapping, test_scenario_14_three_in_one_corner);
    suite_add_tcase(s, tc_overlapping);
    
    TCase* tc_degenerate = tcase_create("Degenerate Grids");
    tcase_add_test(tc_degenerate, test_scenario_15_1x21_grid);
    tcase_add_test(tc_degenerate, test_scenario_16_21x1_grid);
    tcase_add_test(tc_degenerate, test_scenario_17_1x1_grid);
    tcase_add_test(tc_degenerate, test_scenario_18_20x20_grid_threshold_zero);
    tcase_add_test(tc_degenerate, test_scenario_19_2x2_grid);
    tcase_add_test(tc_degenerate, test_scenario_20_21x3_grid_n_greater_than_w);
    tcase_add_test(tc_degenerate, test_scenario_21_4x15_grid_n_greater_than_h);
    tcase_add_test(tc_degenerate, test_scenario_22_2x2_grid_n_greater_than_both);
    tcase_add_test(tc_degenerate, test_scenario_23_2x2_grid_n_much_greater);
    tcase_add_test(tc_degenerate, test_scenario_24_11x11_grid_corner_large_n);
    tcase_add_test(tc_degenerate, test_scenario_25_11x11_grid_center_large_n);
    suite_add_tcase(s, tc_degenerate);
    
    TCase* tc_empty = tcase_create("No Positive Cells");
    tcase_add_test(tc_empty, test_scenario_26_no_positive_cells);
    suite_add_tcase(s, tc_empty);
    
    return s;
}

int main(void) {
    int number_failed;
    Suite* s = bdd_scenarios_suite();
    SRunner* sr = srunner_create(s);
    
    srunner_run_all(sr, CK_NORMAL);
    number_failed = srunner_ntests_failed(sr);
    srunner_free(sr);
    
    return (number_failed == 0) ? 0 : 1;
}
