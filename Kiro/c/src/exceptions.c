#include "exceptions.h"

const char* error_message(ErrorCode code) {
    switch (code) {
        case ERROR_NONE:
            return "No error";
        case ERROR_INVALID_GRID_DIMENSIONS:
            return "Invalid grid dimensions: height and width must be greater than 0";
        case ERROR_POSITION_OUT_OF_BOUNDS:
            return "Position out of bounds: position exceeds grid boundaries";
        case ERROR_INVALID_DISTANCE_THRESHOLD:
            return "Invalid distance threshold: threshold must be non-negative";
        case ERROR_MEMORY_ALLOCATION:
            return "Memory allocation failed";
        default:
            return "Unknown error";
    }
}
