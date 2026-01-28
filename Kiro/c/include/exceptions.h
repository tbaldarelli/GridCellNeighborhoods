#ifndef EXCEPTIONS_H
#define EXCEPTIONS_H

/**
 * Error codes for grid neighborhood calculations.
 */
typedef enum {
    ERROR_NONE = 0,
    ERROR_INVALID_GRID_DIMENSIONS,
    ERROR_POSITION_OUT_OF_BOUNDS,
    ERROR_INVALID_DISTANCE_THRESHOLD,
    ERROR_MEMORY_ALLOCATION
} ErrorCode;

/**
 * Returns a human-readable error message for the given error code.
 */
const char* error_message(ErrorCode code);

#endif /* EXCEPTIONS_H */
