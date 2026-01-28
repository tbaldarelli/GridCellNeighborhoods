/**
 * Property-based tests for grid neighborhoods core components.
 * 
 * This file implements property-based testing using the Check framework
 * with custom property test helpers that run multiple iterations.
 */

#include <check.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>
#include "../include/grid.h"
#include "../include/position.h"
#include "../include/neighborhood_calculator.h"
#include "../include/boundary_handler.h"
#include "../include/distance_calculator.h"
#include "../include/exceptions.h"

#define PROPERTY_TEST_ITERATIONS 100
#define MAX_GRID_SIZE 20
#define MAX_DISTANCE 20

/* Random number generation helpers */
static int rand_range(int min, int max) {
    return min + rand() % (max - min + 1);
}

/* Property 2: Manhattan Distance Calculation */
START_TEST(test_manhattan_distance_calculation) {
    /* For any two positions in a coordinate system, the Manhattan distance should 
     * equal |row1 - row2| + |column1 - column2|, always return a non-negative 
     * integer, and return 0 when both positions are identical.
     * 
     * Feature: grid-neighborhoods, Property 2: Manhattan Distance Calculation
     * Validates: Requirements 2.1, 2.2, 2.3
     */
    
    for (int i = 0; i < PROPERTY_TEST_ITERATIONS; i++) {
        int row1 = rand_range(0, 1000);
        int col1 = rand_range(0, 1000);
        int row2 = rand_range(0, 1000);
        int col2 = rand_range(0, 1000);
        
        Position pos1 = position_create(row1, col1);
        Position pos2 = position_create(row2, col2);
        
        int distance = position_manhattan_distance(pos1, pos2);
        int expected_distance = abs(row1 - row2) + abs(col1 - col2);
        
        /* Distance should equal the Manhattan formula */
        ck_assert_int_eq(distance, expected_distance);
        
        /* Distance should always be non-negative */
        ck_assert_int_ge(distance, 0);
        
        /* Distance should be 0 when positions are identical */
        if (row1 == row2 && col1 == col2) {
            ck_assert_int_eq(distance, 0);
        }
        
        /* Distance should be symmetric */
        ck_assert_int_eq(position_manhattan_distance(pos1, pos2), 
                        position_manhattan_distance(pos2, pos1));
    }
}
END_TEST

/* Property 1: Grid Validation */
START_TEST(test_grid_validation) {
    /* For any height and width values, grid creation should succeed if and only if 
     * both height > 0 and width > 0, and all specified positive cell positions 
     * should be within the resulting grid boundaries.
     * 
     * Feature: grid-neighborhoods, Property 1: Grid Validation
     * Validates: Requirements 1.1, 1.2
     */
    
    for (int i = 0; i < PROPERTY_TEST_ITERATIONS; i++) {
        int height = rand_range(-100, 1000);
        int width = rand_range(-100, 1000);
        
        Grid* grid = grid_create(height, width, NULL, 0);
        
        if (height > 0 && width > 0) {
            /* Valid dimensions should create a grid successfully */
            ck_assert_ptr_nonnull(grid);
            ck_assert_int_eq(grid->height, height);
            ck_assert_int_eq(grid->width, width);
            grid_destroy(grid);
        } else {
            /* Invalid dimensions should return NULL */
            ck_assert_ptr_null(grid);
        }
    }
}
END_TEST

/* Property 3: Coordinate System Consistency */
START_TEST(test_coordinate_system_consistency) {
    /* For any grid dimensions, position (0,0) should consistently represent the 
     * bottom-left corner, and stored positive cell positions should be retrievable 
     * for neighborhood calculations.
     * 
     * Feature: grid-neighborhoods, Property 3: Coordinate System Consistency
     * Validates: Requirements 1.3, 1.4
     */
    
    for (int i = 0; i < PROPERTY_TEST_ITERATIONS; i++) {
        int height = rand_range(1, 20);
        int width = rand_range(1, 20);
        int num_positive = rand_range(0, 10);
        
        Position* positive_cells = malloc(num_positive * sizeof(Position));
        if (!positive_cells && num_positive > 0) continue;
        
        int valid_count = 0;
        
        /* Generate random positive cell positions within bounds */
        for (int j = 0; j < num_positive; j++) {
            int row = rand_range(0, height - 1);
            int col = rand_range(0, width - 1);
            positive_cells[valid_count++] = position_create(row, col);
        }
        
        Grid* grid = grid_create(height, width, positive_cells, valid_count);
        if (!grid) {
            free(positive_cells);
            continue;
        }
        
        /* Position (0,0) should be valid for any grid */
        Position bottom_left = position_create(0, 0);
        ck_assert(grid_is_valid_position(grid, bottom_left));
        
        /* Position (height-1, width-1) should be valid (top-right corner) */
        Position top_right = position_create(height - 1, width - 1);
        ck_assert(grid_is_valid_position(grid, top_right));
        
        /* Positions outside bounds should be invalid */
        Position out_of_bounds = position_create(height, 0);
        ck_assert(!grid_is_valid_position(grid, out_of_bounds));
        
        out_of_bounds = position_create(0, width);
        ck_assert(!grid_is_valid_position(grid, out_of_bounds));
        
        /* All positive cells should be retrievable */
        ck_assert_int_eq(grid->positive_cell_count, valid_count);
        
        grid_destroy(grid);
        free(positive_cells);
    }
}
END_TEST

/* Property 6: Boundary Constraint Enforcement */
START_TEST(test_boundary_constraint_enforcement) {
    /* For any positive cell and distance threshold, the neighborhood count should 
     * exclude all cells that would fall outside the grid boundaries, with no 
     * wraparound behavior.
     * 
     * Feature: grid-neighborhoods, Property 6: Boundary Constraint Enforcement
     * Validates: Requirements 3.3, 6.1, 6.2, 6.3
     */
    
    for (int i = 0; i < PROPERTY_TEST_ITERATIONS; i++) {
        int height = rand_range(1, 20);
        int width = rand_range(1, 20);
        
        Grid* grid = grid_create(height, width, NULL, 0);
        if (!grid) continue;
        
        /* Test boundary validation for various positions */
        for (int j = 0; j < 10; j++) {
            int row = rand_range(-10, height + 10);
            int col = rand_range(-10, width + 10);
            
            if (row < 0 || col < 0) continue; /* Position struct uses unsigned, skip negative */
            
            Position pos = position_create(row, col);
            bool is_valid = boundary_handler_is_within_bounds(pos, grid);
            bool expected_valid = (row >= 0 && row < height && col >= 0 && col < width);
            
            ck_assert_int_eq(is_valid, expected_valid);
            ck_assert_int_eq(is_valid, grid_is_valid_position(grid, pos));
        }
        
        grid_destroy(grid);
    }
}
END_TEST

/* Property 4: Self-Inclusion in Neighborhoods */
START_TEST(test_self_inclusion_in_neighborhoods) {
    /* For any positive cell at any valid position, that cell should always be 
     * included in its own neighborhood count regardless of distance threshold 
     * (when N >= 0).
     * 
     * Feature: grid-neighborhoods, Property 4: Self-Inclusion in Neighborhoods
     * Validates: Requirements 3.1
     */
    
    for (int i = 0; i < PROPERTY_TEST_ITERATIONS; i++) {
        int height = rand_range(1, MAX_GRID_SIZE);
        int width = rand_range(1, MAX_GRID_SIZE);
        int positive_row = rand_range(0, height - 1);
        int positive_col = rand_range(0, width - 1);
        int distance_threshold = rand_range(0, MAX_DISTANCE);
        
        Position positive_pos = position_create(positive_row, positive_col);
        Grid* grid = grid_create(height, width, &positive_pos, 1);
        ck_assert_ptr_nonnull(grid);
        
        ErrorCode error_code = ERROR_NONE;
        PositionSet* neighborhood = neighborhood_calculator_get_cells(grid, distance_threshold, &error_code);
        
        ck_assert_int_eq(error_code, ERROR_NONE);
        ck_assert_ptr_nonnull(neighborhood);
        
        /* The positive cell should always be included in its own neighborhood */
        ck_assert(position_set_contains(neighborhood, positive_pos));
        
        /* Count should be at least 1 */
        int count = neighborhood_calculator_count(grid, distance_threshold, &error_code);
        ck_assert_int_ge(count, 1);
        
        position_set_destroy(neighborhood);
        grid_destroy(grid);
    }
}
END_TEST

/* Property 5: Complete Neighborhood Enumeration */
START_TEST(test_complete_neighborhood_enumeration) {
    /* For any positive cell positioned away from grid boundaries, the neighborhood 
     * should include all cells within N Manhattan steps when the full diamond 
     * fits within the grid.
     * 
     * Feature: grid-neighborhoods, Property 5: Complete Neighborhood Enumeration
     * Validates: Requirements 3.2
     */
    
    for (int i = 0; i < PROPERTY_TEST_ITERATIONS; i++) {
        int distance_threshold = rand_range(1, 10);
        int height = rand_range(2 * distance_threshold + 3, 50);
        int width = rand_range(2 * distance_threshold + 3, 50);
        
        /* Place positive cell away from boundaries so full diamond fits */
        int center_row = distance_threshold + 1;
        int center_col = distance_threshold + 1;
        
        /* Ensure the full diamond fits within the grid */
        if (center_row + distance_threshold >= height || 
            center_col + distance_threshold >= width) {
            continue;
        }
        
        Position center_pos = position_create(center_row, center_col);
        Grid* grid = grid_create(height, width, &center_pos, 1);
        ck_assert_ptr_nonnull(grid);
        
        ErrorCode error_code = ERROR_NONE;
        PositionSet* neighborhood = neighborhood_calculator_get_cells(grid, distance_threshold, &error_code);
        
        ck_assert_int_eq(error_code, ERROR_NONE);
        ck_assert_ptr_nonnull(neighborhood);
        
        /* Calculate expected neighborhood size for a complete diamond */
        /* Diamond size formula: (N+1)^2 + N^2 */
        int expected_size = (distance_threshold + 1) * (distance_threshold + 1) + 
                           distance_threshold * distance_threshold;
        /* Verify we got the expected complete diamond */
        ck_assert_int_eq(position_set_size(neighborhood), expected_size);
        /* Verify all cells in the diamond are present */
        for (int delta_row = -distance_threshold; delta_row <= distance_threshold; delta_row++) {
            int remaining_distance = distance_threshold - abs(delta_row);
            for (int delta_col = -remaining_distance; delta_col <= remaining_distance; delta_col++) {
                Position expected_pos = position_create(center_row + delta_row, center_col + delta_col);
                ck_assert(position_set_contains(neighborhood, expected_pos));
            }
        }
        
        position_set_destroy(neighborhood);
        grid_destroy(grid);
    }
}
END_TEST

/* Property 7: Cell Uniqueness Guarantee */
START_TEST(test_cell_uniqueness_guarantee) {
    /* For any grid configuration with positive cells, each cell should be counted 
     * at most once in the total neighborhood count, regardless of how many positive 
     * cell neighborhoods it falls within.
     * 
     * Feature: grid-neighborhoods, Property 7: Cell Uniqueness Guarantee
     * Validates: Requirements 3.4, 4.2, 5.1
     */
    
    for (int i = 0; i < PROPERTY_TEST_ITERATIONS; i++) {
        int height = rand_range(1, 30);
        int width = rand_range(1, 30);
        int num_positive = rand_range(1, 10);
        int distance_threshold = rand_range(0, 20);
        
        Position* positive_cells = malloc(num_positive * sizeof(Position));
        int valid_count = 0;
        
        /* Generate unique positive cell positions */
        for (int j = 0; j < num_positive; j++) {
            int row = rand_range(0, height - 1);
            int col = rand_range(0, width - 1);
            Position pos = position_create(row, col);
            
            /* Check for duplicates */
            bool duplicate = false;
            for (int k = 0; k < valid_count; k++) {
                if (position_equals(positive_cells[k], pos)) {
                    duplicate = true;
                    break;
                }
            }
            
            if (!duplicate) {
                positive_cells[valid_count++] = pos;
            }
        }
        
        if (valid_count == 0) {
            free(positive_cells);
            continue;
        }
        
        Grid* grid = grid_create(height, width, positive_cells, valid_count);
        ck_assert_ptr_nonnull(grid);
        
        ErrorCode error_code = ERROR_NONE;
        PositionSet* all_neighborhood_cells = neighborhood_calculator_get_cells(grid, distance_threshold, &error_code);
        int total_count = neighborhood_calculator_count(grid, distance_threshold, &error_code);
        
        ck_assert_int_eq(error_code, ERROR_NONE);
        ck_assert_ptr_nonnull(all_neighborhood_cells);
        
        /* The count should equal the size of the set (no duplicates) */
        ck_assert_int_eq(total_count, position_set_size(all_neighborhood_cells));
        
        /* Each cell in the result should be unique (verified by set implementation) */
        /* Total count should be <= sum of individual counts (due to potential overlaps) */
        
        position_set_destroy(all_neighborhood_cells);
        grid_destroy(grid);
        free(positive_cells);
    }
}
END_TEST

/* Property 8: Non-Overlapping Additivity */
START_TEST(test_non_overlapping_additivity) {
    /* For any set of positive cells whose neighborhoods do not overlap, the total 
     * neighborhood count should equal the sum of individual neighborhood counts.
     * 
     * Feature: grid-neighborhoods, Property 8: Non-Overlapping Additivity
     * Validates: Requirements 4.1, 4.3
     */
    
    for (int i = 0; i < PROPERTY_TEST_ITERATIONS; i++) {
        int distance_threshold = rand_range(1, 10);
        int min_separation = 2 * distance_threshold + 1;
        
        int height = rand_range(min_separation + 2 * distance_threshold, 50);
        int width = rand_range(min_separation + 2 * distance_threshold, 50);
        
        /* Place first positive cell */
        int pos1_row = distance_threshold;
        int pos1_col = distance_threshold;
        
        /* Place second positive cell far enough away to ensure no overlap */
        int pos2_row = pos1_row + min_separation;
        int pos2_col = pos1_col + min_separation;
        
        /* Ensure second position is within bounds */
        if (pos2_row >= height - distance_threshold || pos2_col >= width - distance_threshold) {
            continue;
        }
        
        Position positive_cells[2];
        positive_cells[0] = position_create(pos1_row, pos1_col);
        positive_cells[1] = position_create(pos2_row, pos2_col);
        
        Grid* grid = grid_create(height, width, positive_cells, 2);
        ck_assert_ptr_nonnull(grid);
        
        ErrorCode error_code = ERROR_NONE;
        
        /* Calculate individual neighborhoods */
        Grid* grid1 = grid_create(height, width, &positive_cells[0], 1);
        Grid* grid2 = grid_create(height, width, &positive_cells[1], 1);
        
        int count1 = neighborhood_calculator_count(grid1, distance_threshold, &error_code);
        int count2 = neighborhood_calculator_count(grid2, distance_threshold, &error_code);
        
        /* Calculate total neighborhood count */
        int total_count = neighborhood_calculator_count(grid, distance_threshold, &error_code);
        
        /* For non-overlapping neighborhoods, total should equal sum of individual counts */
        int expected_count = count1 + count2;
        ck_assert_int_eq(total_count, expected_count);
        
        grid_destroy(grid);
        grid_destroy(grid1);
        grid_destroy(grid2);
    }
}
END_TEST

/* Property 9: Overlapping Union Behavior */
START_TEST(test_overlapping_union_behavior) {
    /* For any set of positive cells with overlapping neighborhoods, the total count 
     * should equal the size of the union of all neighborhoods and be less than or 
     * equal to the sum of individual neighborhood counts.
     * 
     * Feature: grid-neighborhoods, Property 9: Overlapping Union Behavior
     * Validates: Requirements 5.2, 5.3
     */
    
    for (int i = 0; i < PROPERTY_TEST_ITERATIONS; i++) {
        int distance_threshold = rand_range(2, 8);
        int overlap_distance = distance_threshold - 1;
        
        int height = rand_range(2 * distance_threshold + overlap_distance + 2, 50);
        int width = rand_range(2 * distance_threshold + overlap_distance + 2, 50);
        
        /* Place first positive cell with enough border space */
        int pos1_row = distance_threshold + 1;
        int pos1_col = distance_threshold + 1;
        
        /* Place second positive cell close enough to create overlap */
        int pos2_row = pos1_row + overlap_distance;
        int pos2_col = pos1_col + overlap_distance;
        
        /* Ensure second position is within bounds and has enough space */
        if (pos2_row >= height - distance_threshold - 1 || 
            pos2_col >= width - distance_threshold - 1) {
            continue;
        }
        
        Position positive_cells[2];
        positive_cells[0] = position_create(pos1_row, pos1_col);
        positive_cells[1] = position_create(pos2_row, pos2_col);
        
        Grid* grid = grid_create(height, width, positive_cells, 2);
        ck_assert_ptr_nonnull(grid);
        
        ErrorCode error_code = ERROR_NONE;
        
        /* Calculate individual neighborhoods */
        Grid* grid1 = grid_create(height, width, &positive_cells[0], 1);
        Grid* grid2 = grid_create(height, width, &positive_cells[1], 1);
        
        int count1 = neighborhood_calculator_count(grid1, distance_threshold, &error_code);
        int count2 = neighborhood_calculator_count(grid2, distance_threshold, &error_code);
        
        /* Calculate total neighborhood count */
        int total_count = neighborhood_calculator_count(grid, distance_threshold, &error_code);
        
        /* For overlapping neighborhoods, total should be less than sum of individual counts */
        int sum_of_individual = count1 + count2;
        ck_assert_int_lt(total_count, sum_of_individual);
        
        grid_destroy(grid);
        grid_destroy(grid1);
        grid_destroy(grid2);
    }
}
END_TEST

/* Property 10: Zero Distance Threshold */
START_TEST(test_zero_distance_threshold) {
    /* For any grid with positive cells, when distance threshold N = 0, the 
     * neighborhood count should equal exactly the number of positive cells.
     * 
     * Feature: grid-neighborhoods, Property 10: Zero Distance Threshold
     * Validates: Requirements 7.2
     */
    
    for (int i = 0; i < PROPERTY_TEST_ITERATIONS; i++) {
        int height = rand_range(1, MAX_GRID_SIZE);
        int width = rand_range(1, MAX_GRID_SIZE);
        int num_positive = rand_range(1, 20);
        
        Position* positive_cells = malloc(num_positive * sizeof(Position));
        int valid_count = 0;
        
        /* Generate unique positive cell positions */
        for (int j = 0; j < num_positive; j++) {
            int row = rand_range(0, height - 1);
            int col = rand_range(0, width - 1);
            Position pos = position_create(row, col);
            
            /* Check for duplicates */
            bool duplicate = false;
            for (int k = 0; k < valid_count; k++) {
                if (position_equals(positive_cells[k], pos)) {
                    duplicate = true;
                    break;
                }
            }
            
            if (!duplicate) {
                positive_cells[valid_count++] = pos;
            }
        }
        
        if (valid_count == 0) {
            free(positive_cells);
            continue;
        }
        
        Grid* grid = grid_create(height, width, positive_cells, valid_count);
        ck_assert_ptr_nonnull(grid);
        
        ErrorCode error_code = ERROR_NONE;
        
        /* With distance threshold 0, only positive cells themselves should be counted */
        int distance_threshold = 0;
        int total_count = neighborhood_calculator_count(grid, distance_threshold, &error_code);
        
        /* Count should equal exactly the number of positive cells */
        ck_assert_int_eq(total_count, valid_count);
        
        grid_destroy(grid);
        free(positive_cells);
    }
}
END_TEST

/* Property 11: Maximum Distance Threshold */
START_TEST(test_maximum_distance_threshold) {
    /* For any grid and distance threshold N that exceeds the grid's maximum 
     * possible Manhattan distance, the neighborhood count should equal the total 
     * number of grid cells when positive cells exist.
     * 
     * Feature: grid-neighborhoods, Property 11: Maximum Distance Threshold
     * Validates: Requirements 7.3
     */
    
    for (int i = 0; i < PROPERTY_TEST_ITERATIONS; i++) {
        int height = rand_range(1, 20);
        int width = rand_range(1, 20);
        int num_positive = rand_range(1, 10);
        
        Position* positive_cells = malloc(num_positive * sizeof(Position));
        int valid_count = 0;
        
        /* Generate unique positive cell positions */
        for (int j = 0; j < num_positive; j++) {
            int row = rand_range(0, height - 1);
            int col = rand_range(0, width - 1);
            Position pos = position_create(row, col);
            
            /* Check for duplicates */
            bool duplicate = false;
            for (int k = 0; k < valid_count; k++) {
                if (position_equals(positive_cells[k], pos)) {
                    duplicate = true;
                    break;
                }
            }
            
            if (!duplicate) {
                positive_cells[valid_count++] = pos;
            }
        }
        
        if (valid_count == 0) {
            free(positive_cells);
            continue;
        }
        
        Grid* grid = grid_create(height, width, positive_cells, valid_count);
        ck_assert_ptr_nonnull(grid);
        
        ErrorCode error_code = ERROR_NONE;
        
        /* Calculate maximum possible Manhattan distance in the grid */
        int max_possible_distance = (height - 1) + (width - 1);
        
        /* Use a distance threshold that exceeds the maximum possible distance */
        int excessive_distance_threshold = max_possible_distance + 10;
        
        int total_count = neighborhood_calculator_count(grid, excessive_distance_threshold, &error_code);
        
        /* When distance threshold exceeds grid dimensions, all grid cells should be counted */
        int expected_count = height * width;
        ck_assert_int_eq(total_count, expected_count);
        
        grid_destroy(grid);
        free(positive_cells);
    }
}
END_TEST

/* Property 12: Degenerate Grid Handling */
START_TEST(test_degenerate_grid_handling) {
    /* For any grid with unusual dimensions (1×N, N×1, 1×1), neighborhood 
     * calculations should produce mathematically correct results consistent 
     * with the Manhattan distance definition.
     * 
     * Feature: grid-neighborhoods, Property 12: Degenerate Grid Handling
     * Validates: Requirements 7.4
     */
    
    for (int i = 0; i < PROPERTY_TEST_ITERATIONS; i++) {
        int grid_type = rand_range(0, 2); /* 0=1xN, 1=Nx1, 2=1x1 */
        int dimension = rand_range(1, 50);
        int distance_threshold = rand_range(0, 20);
        
        int height, width, positive_row, positive_col;
        
        if (grid_type == 0) { /* 1xN */
            height = 1;
            width = dimension;
            positive_row = 0;
            positive_col = rand_range(0, width - 1);
        } else if (grid_type == 1) { /* Nx1 */
            height = dimension;
            width = 1;
            positive_row = rand_range(0, height - 1);
            positive_col = 0;
        } else { /* 1x1 */
            height = 1;
            width = 1;
            positive_row = 0;
            positive_col = 0;
        }
        
        Position positive_pos = position_create(positive_row, positive_col);
        Grid* grid = grid_create(height, width, &positive_pos, 1);
        ck_assert_ptr_nonnull(grid);
        
        ErrorCode error_code = ERROR_NONE;
        PositionSet* neighborhood = neighborhood_calculator_get_cells(grid, distance_threshold, &error_code);
        int total_count = neighborhood_calculator_count(grid, distance_threshold, &error_code);
        
        ck_assert_int_eq(error_code, ERROR_NONE);
        ck_assert_ptr_nonnull(neighborhood);
        
        /* Verify basic properties */
        ck_assert_int_eq(position_set_size(neighborhood), total_count);
        ck_assert(position_set_contains(neighborhood, positive_pos)); /* Self-inclusion */
        
        /* For degenerate grids, verify Manhattan distance calculation is correct */
        /* All cells in neighborhood should be within distance threshold */
        for (size_t j = 0; j < position_set_size(neighborhood); j++) {
            Position cell = neighborhood->positions[j];
            int manhattan_dist = position_manhattan_distance(positive_pos, cell);
            ck_assert_int_le(manhattan_dist, distance_threshold);
        }
        
        /* Special case verification for 1x1 grid */
        if (grid_type == 2) {
            if (distance_threshold >= 0) {
                ck_assert_int_eq(total_count, 1);
            }
        }
        
        position_set_destroy(neighborhood);
        grid_destroy(grid);
    }
}
END_TEST

/* Property 13: Cross-Language Result Consistency */
START_TEST(test_cross_language_result_consistency) {
    /* For any identical grid configuration, positive cell positions, and distance 
     * threshold, all programming language implementations should produce identical 
     * neighborhood counts.
     * 
     * Feature: grid-neighborhoods, Property 13: Cross-Language Result Consistency
     * Validates: Requirements 9.1, 9.3, 9.4
     * 
     * Note: This test verifies internal consistency. Cross-language validation
     * requires running the same test scenarios across different implementations
     * and comparing outputs.
     */
    
    for (int i = 0; i < PROPERTY_TEST_ITERATIONS; i++) {
        int height = rand_range(1, 30);
        int width = rand_range(1, 30);
        int num_positive = rand_range(1, 5);
        int distance_threshold = rand_range(0, 15);
        
        Position* positive_cells = malloc(num_positive * sizeof(Position));
        int valid_count = 0;
        
        for (int j = 0; j < num_positive; j++) {
            int row = rand_range(0, height - 1);
            int col = rand_range(0, width - 1);
            Position pos = position_create(row, col);
            
            bool duplicate = false;
            for (int k = 0; k < valid_count; k++) {
                if (position_equals(positive_cells[k], pos)) {
                    duplicate = true;
                    break;
                }
            }
            
            if (!duplicate) {
                positive_cells[valid_count++] = pos;
            }
        }
        
        if (valid_count == 0) {
            free(positive_cells);
            continue;
        }
        
        Grid* grid = grid_create(height, width, positive_cells, valid_count);
        ck_assert_ptr_nonnull(grid);
        
        ErrorCode error_code = ERROR_NONE;
        
        /* Run the calculation multiple times - should get consistent results */
        int count1 = neighborhood_calculator_count(grid, distance_threshold, &error_code);
        ck_assert_int_eq(error_code, ERROR_NONE);
        
        int count2 = neighborhood_calculator_count(grid, distance_threshold, &error_code);
        ck_assert_int_eq(error_code, ERROR_NONE);
        
        /* Results should be deterministic and consistent */
        ck_assert_int_eq(count1, count2);
        
        grid_destroy(grid);
        free(positive_cells);
    }
}
END_TEST

/* Test suite setup */
Suite* properties_suite(void) {
    Suite* s = suite_create("Property Tests");
    
    TCase* tc_position = tcase_create("Position Properties");
    tcase_add_test(tc_position, test_manhattan_distance_calculation);
    suite_add_tcase(s, tc_position);
    
    TCase* tc_grid = tcase_create("Grid Properties");
    tcase_add_test(tc_grid, test_grid_validation);
    tcase_add_test(tc_grid, test_coordinate_system_consistency);
    suite_add_tcase(s, tc_grid);
    
    TCase* tc_boundary = tcase_create("Boundary Properties");
    tcase_add_test(tc_boundary, test_boundary_constraint_enforcement);
    suite_add_tcase(s, tc_boundary);
    
    TCase* tc_neighborhood = tcase_create("Neighborhood Properties");
    tcase_add_test(tc_neighborhood, test_self_inclusion_in_neighborhoods);
    tcase_add_test(tc_neighborhood, test_complete_neighborhood_enumeration);
    tcase_add_test(tc_neighborhood, test_cell_uniqueness_guarantee);
    tcase_add_test(tc_neighborhood, test_non_overlapping_additivity);
    tcase_add_test(tc_neighborhood, test_overlapping_union_behavior);
    tcase_add_test(tc_neighborhood, test_zero_distance_threshold);
    tcase_add_test(tc_neighborhood, test_maximum_distance_threshold);
    tcase_add_test(tc_neighborhood, test_degenerate_grid_handling);
    tcase_add_test(tc_neighborhood, test_cross_language_result_consistency);
    suite_add_tcase(s, tc_neighborhood);
    
    return s;
}

int main(void) {
    /* Seed random number generator */
    srand(time(NULL));
    
    int number_failed;
    Suite* s = properties_suite();
    SRunner* sr = srunner_create(s);
    
    srunner_run_all(sr, CK_VERBOSE);
    number_failed = srunner_ntests_failed(sr);
    srunner_free(sr);
    
    return (number_failed == 0) ? 0 : 1;
}
