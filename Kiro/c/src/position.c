#include "position.h"
#include <stdlib.h>

Position position_create(int row, int column) {
    Position pos;
    pos.row = row;
    pos.column = column;
    return pos;
}

int position_manhattan_distance(Position pos1, Position pos2) {
    int row_diff = abs(pos1.row - pos2.row);
    int col_diff = abs(pos1.column - pos2.column);
    return row_diff + col_diff;
}

bool position_equals(Position pos1, Position pos2) {
    return pos1.row == pos2.row && pos1.column == pos2.column;
}

size_t position_hash(Position pos) {
    // Simple hash function combining row and column
    return (size_t)(pos.row * 31 + pos.column);
}
