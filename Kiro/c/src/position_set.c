#include "position_set.h"
#include <stdlib.h>
#include <string.h>

#define INITIAL_CAPACITY 16

PositionSet* position_set_create(void) {
    PositionSet* set = (PositionSet*)malloc(sizeof(PositionSet));
    if (!set) return NULL;
    
    set->positions = (Position*)malloc(INITIAL_CAPACITY * sizeof(Position));
    if (!set->positions) {
        free(set);
        return NULL;
    }
    
    set->size = 0;
    set->capacity = INITIAL_CAPACITY;
    return set;
}

void position_set_destroy(PositionSet* set) {
    if (set) {
        free(set->positions);
        free(set);
    }
}

bool position_set_add(PositionSet* set, Position pos) {
    if (!set) return false;
    
    // Check if already present
    if (position_set_contains(set, pos)) {
        return false;
    }
    
    // Resize if needed
    if (set->size >= set->capacity) {
        size_t new_capacity = set->capacity * 2;
        Position* new_positions = (Position*)realloc(set->positions, new_capacity * sizeof(Position));
        if (!new_positions) return false;
        
        set->positions = new_positions;
        set->capacity = new_capacity;
    }
    
    set->positions[set->size++] = pos;
    return true;
}

bool position_set_contains(const PositionSet* set, Position pos) {
    if (!set) return false;
    
    for (size_t i = 0; i < set->size; i++) {
        if (position_equals(set->positions[i], pos)) {
            return true;
        }
    }
    return false;
}

size_t position_set_size(const PositionSet* set) {
    return set ? set->size : 0;
}

void position_set_clear(PositionSet* set) {
    if (set) {
        set->size = 0;
    }
}
