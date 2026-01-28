#include "boundary_handler.h"

bool boundary_handler_is_within_bounds(Position pos, const Grid* grid) {
    return grid_is_valid_position(grid, pos);
}
