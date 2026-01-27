#ifndef BOUNDARY_HANDLER_H
#define BOUNDARY_HANDLER_H

#include "grid.h"
#include "position.h"
#include <stdbool.h>

/**
 * Checks if a position is within grid boundaries.
 */
bool boundary_handler_is_within_bounds(Position pos, const Grid* grid);

#endif /* BOUNDARY_HANDLER_H */
