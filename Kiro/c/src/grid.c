#include "grid.h"
#include <stdlib.h>
#include <string.h>

Grid* grid_create(int height, int width, Position* positive_cells, int positive_cell_count) {
    // Validate dimensions
    if (height <= 0 || width <= 0) {
        return NULL;
    }
    
    Grid* grid = (Grid*)malloc(sizeof(Grid));
    if (!grid) return NULL;
    
    grid->height = height;
    grid->width = width;
    grid->positive_cell_count = positive_cell_count;
    
    // Copy positive cells
    if (positive_cell_count > 0 && positive_cells) {
        grid->positive_cells = (Position*)malloc(positive_cell_count * sizeof(Position));
        if (!grid->positive_cells) {
            free(grid);
            return NULL;
        }
        memcpy(grid->positive_cells, positive_cells, positive_cell_count * sizeof(Position));
    } else {
        grid->positive_cells = NULL;
    }
    
    return grid;
}

void grid_destroy(Grid* grid) {
    if (grid) {
        free(grid->positive_cells);
        free(grid);
    }
}

bool grid_is_valid_position(const Grid* grid, Position pos) {
    if (!grid) return false;
    return pos.row >= 0 && pos.row < grid->height &&
           pos.column >= 0 && pos.column < grid->width;
}

bool grid_validate_positions(const Grid* grid) {
    if (!grid) return false;
    
    for (int i = 0; i < grid->positive_cell_count; i++) {
        if (!grid_is_valid_position(grid, grid->positive_cells[i])) {
            return false;
        }
    }
    return true;
}
