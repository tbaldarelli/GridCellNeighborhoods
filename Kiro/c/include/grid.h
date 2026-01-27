#ifndef GRID_H
#define GRID_H

#include "position.h"
#include <stdbool.h>

/**
 * Represents a 2D grid with height, width, and positive cell positions.
 */
typedef struct {
    int height;
    int width;
    Position* positive_cells;
    int positive_cell_count;
} Grid;

/**
 * Creates a new grid with specified dimensions and positive cells.
 * Returns NULL if dimensions are invalid (height <= 0 or width <= 0).
 * Caller is responsible for freeing the grid with grid_destroy().
 */
Grid* grid_create(int height, int width, Position* positive_cells, int positive_cell_count);

/**
 * Destroys a grid and frees associated memory.
 */
void grid_destroy(Grid* grid);

/**
 * Checks if a position is within grid boundaries.
 */
bool grid_is_valid_position(const Grid* grid, Position pos);

/**
 * Validates that all positive cells are within grid boundaries.
 * Returns true if all positions are valid, false otherwise.
 */
bool grid_validate_positions(const Grid* grid);

#endif /* GRID_H */
