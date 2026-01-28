#ifndef POSITION_SET_H
#define POSITION_SET_H

#include "position.h"
#include <stdbool.h>
#include <stddef.h>

/**
 * A set data structure for storing unique positions.
 * Implemented as a dynamic array with uniqueness checking.
 */
typedef struct {
    Position* positions;
    size_t size;
    size_t capacity;
} PositionSet;

/**
 * Creates a new empty position set.
 */
PositionSet* position_set_create(void);

/**
 * Destroys a position set and frees memory.
 */
void position_set_destroy(PositionSet* set);

/**
 * Adds a position to the set (only if not already present).
 * Returns true if added, false if already present.
 */
bool position_set_add(PositionSet* set, Position pos);

/**
 * Checks if a position is in the set.
 */
bool position_set_contains(const PositionSet* set, Position pos);

/**
 * Returns the number of positions in the set.
 */
size_t position_set_size(const PositionSet* set);

/**
 * Clears all positions from the set.
 */
void position_set_clear(PositionSet* set);

#endif /* POSITION_SET_H */
