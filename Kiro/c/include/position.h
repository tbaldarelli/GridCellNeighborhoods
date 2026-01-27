#ifndef POSITION_H
#define POSITION_H

#include <stddef.h>
#include <stdbool.h>

/**
 * Represents a position in the grid with row and column coordinates.
 * (0,0) is the bottom-left corner.
 */
typedef struct {
    int row;
    int column;
} Position;

/**
 * Creates a new position.
 */
Position position_create(int row, int column);

/**
 * Calculates Manhattan distance between two positions.
 * Returns |row1 - row2| + |column1 - column2|
 */
int position_manhattan_distance(Position pos1, Position pos2);

/**
 * Checks if two positions are equal.
 */
bool position_equals(Position pos1, Position pos2);

/**
 * Hash function for positions (for use in hash sets).
 */
size_t position_hash(Position pos);

#endif /* POSITION_H */
