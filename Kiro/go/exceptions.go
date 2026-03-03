package gridneighborhoods

import "fmt"

// InvalidGridDimensionsError represents an error when grid dimensions are invalid
type InvalidGridDimensionsError struct {
	Height int
	Width  int
}

func (e *InvalidGridDimensionsError) Error() string {
	return fmt.Sprintf("invalid grid dimensions: height=%d, width=%d (both must be > 0)", e.Height, e.Width)
}

// PositionOutOfBoundsError represents an error when a position is outside grid boundaries
type PositionOutOfBoundsError struct {
	Position Position
	Height   int
	Width    int
}

func (e *PositionOutOfBoundsError) Error() string {
	return fmt.Sprintf("position (%d,%d) is out of bounds for grid %dx%d", e.Position.Row, e.Position.Column, e.Height, e.Width)
}

// InvalidDistanceThresholdError represents an error when distance threshold is negative
type InvalidDistanceThresholdError struct {
	Threshold int
}

func (e *InvalidDistanceThresholdError) Error() string {
	return fmt.Sprintf("invalid distance threshold: %d (must be >= 0)", e.Threshold)
}
