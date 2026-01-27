#ifndef NEIGHBORHOOD_CALCULATOR_H
#define NEIGHBORHOOD_CALCULATOR_H

#include "grid.h"
#include "position_set.h"
#include "exceptions.h"

/**
 * Calculates the total number of unique cells within Manhattan distance
 * neighborhoods of all positive cells in the grid.
 * 
 * Returns the count of unique cells, or -1 on error.
 * Sets error_code to indicate any errors that occurred.
 */
int neighborhood_calculator_count(const Grid* grid, int distance_threshold, ErrorCode* error_code);

/**
 * Gets all unique cells within Manhattan distance neighborhoods.
 * Returns a PositionSet containing all neighborhood cells.
 * Caller is responsible for freeing the set with position_set_destroy().
 * Sets error_code to indicate any errors that occurred.
 */
PositionSet* neighborhood_calculator_get_cells(const Grid* grid, int distance_threshold, ErrorCode* error_code);

#endif /* NEIGHBORHOOD_CALCULATOR_H */
