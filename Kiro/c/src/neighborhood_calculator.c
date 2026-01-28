#include "neighborhood_calculator.h"
#include "boundary_handler.h"
#include "distance_calculator.h"
#include <stdlib.h>

static PositionSet* enumerate_neighborhood(Position center, int distance_threshold, const Grid* grid) {
    PositionSet* neighborhood = position_set_create();
    if (!neighborhood) return NULL;
    
    for (int delta_row = -distance_threshold; delta_row <= distance_threshold; delta_row++) {
        int remaining_distance = distance_threshold - abs(delta_row);
        
        for (int delta_col = -remaining_distance; delta_col <= remaining_distance; delta_col++) {
            Position candidate = position_create(
                center.row + delta_row,
                center.column + delta_col
            );
            
            if (boundary_handler_is_within_bounds(candidate, grid)) {
                position_set_add(neighborhood, candidate);
            }
        }
    }
    
    return neighborhood;
}

int neighborhood_calculator_count(const Grid* grid, int distance_threshold, ErrorCode* error_code) {
    PositionSet* cells = neighborhood_calculator_get_cells(grid, distance_threshold, error_code);
    if (!cells) {
        return -1;
    }
    
    int count = (int)position_set_size(cells);
    position_set_destroy(cells);
    return count;
}

PositionSet* neighborhood_calculator_get_cells(const Grid* grid, int distance_threshold, ErrorCode* error_code) {
    *error_code = ERROR_NONE;
    
    // Validate inputs
    if (!grid || grid->height <= 0 || grid->width <= 0) {
        *error_code = ERROR_INVALID_GRID_DIMENSIONS;
        return NULL;
    }
    
    if (distance_threshold < 0) {
        *error_code = ERROR_INVALID_DISTANCE_THRESHOLD;
        return NULL;
    }
    
    if (!grid_validate_positions(grid)) {
        *error_code = ERROR_POSITION_OUT_OF_BOUNDS;
        return NULL;
    }
    
    // Create result set
    PositionSet* all_cells = position_set_create();
    if (!all_cells) {
        *error_code = ERROR_MEMORY_ALLOCATION;
        return NULL;
    }
    
    // Handle empty grid case
    if (grid->positive_cell_count == 0) {
        return all_cells;
    }
    
    // Optimization: If distance threshold exceeds maximum possible distance,
    // return all grid cells (early termination)
    int max_possible_distance = (grid->height - 1) + (grid->width - 1);
    if (distance_threshold >= max_possible_distance) {
        for (int row = 0; row < grid->height; row++) {
            for (int col = 0; col < grid->width; col++) {
                position_set_add(all_cells, position_create(row, col));
            }
        }
        return all_cells;
    }
    
    // Enumerate neighborhoods for each positive cell
    for (int i = 0; i < grid->positive_cell_count; i++) {
        PositionSet* neighborhood = enumerate_neighborhood(
            grid->positive_cells[i],
            distance_threshold,
            grid
        );
        
        if (!neighborhood) {
            position_set_destroy(all_cells);
            *error_code = ERROR_MEMORY_ALLOCATION;
            return NULL;
        }
        
        // Add all cells from this neighborhood to the union
        for (size_t j = 0; j < position_set_size(neighborhood); j++) {
            position_set_add(all_cells, neighborhood->positions[j]);
        }
        
        position_set_destroy(neighborhood);
    }
    
    return all_cells;
}
