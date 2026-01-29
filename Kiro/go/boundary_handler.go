package gridneighborhoods

// BoundaryHandler handles grid boundary validation
type BoundaryHandler struct{}

// NewBoundaryHandler creates a new boundary handler
func NewBoundaryHandler() *BoundaryHandler {
	return &BoundaryHandler{}
}

// IsWithinBounds checks if a position is within grid boundaries
func (bh *BoundaryHandler) IsWithinBounds(pos Position, grid *Grid) bool {
	return grid.IsValidPosition(pos)
}

// FilterValidPositions filters a set of positions to only include those within grid bounds
func (bh *BoundaryHandler) FilterValidPositions(positions map[Position]bool, grid *Grid) map[Position]bool {
	result := make(map[Position]bool)
	for pos := range positions {
		if grid.IsValidPosition(pos) {
			result[pos] = true
		}
	}
	return result
}
