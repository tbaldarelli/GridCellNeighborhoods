package gridneighborhoods

// NeighborhoodCalculator calculates neighborhood cells for positive cells in a grid
type NeighborhoodCalculator struct {
	distanceCalculator *DistanceCalculator
	boundaryHandler    *BoundaryHandler
}

// NewNeighborhoodCalculator creates a new neighborhood calculator
func NewNeighborhoodCalculator() *NeighborhoodCalculator {
	return &NeighborhoodCalculator{
		distanceCalculator: NewDistanceCalculator(),
		boundaryHandler:    NewBoundaryHandler(),
	}
}

// CountNeighborhoodCells counts the total unique cells in all neighborhoods
func (nc *NeighborhoodCalculator) CountNeighborhoodCells(grid *Grid, distanceThreshold int) (int, error) {
	// Validate distance threshold
	if distanceThreshold < 0 {
		return 0, &InvalidDistanceThresholdError{Threshold: distanceThreshold}
	}

	// Get all neighborhood cells
	cells := nc.GetNeighborhoodCells(grid, distanceThreshold)
	return len(cells), nil
}

// GetNeighborhoodCells returns the set of all unique cells in neighborhoods
func (nc *NeighborhoodCalculator) GetNeighborhoodCells(grid *Grid, distanceThreshold int) map[Position]bool {
	allCells := make(map[Position]bool)

	// Handle empty positive cells case
	if len(grid.PositiveCells) == 0 {
		return allCells
	}

	// For each positive cell, enumerate its neighborhood and add to union
	for _, positiveCell := range grid.PositiveCells {
		neighborhood := nc.enumerateNeighborhood(grid, positiveCell, distanceThreshold)
		// Union operation
		for pos := range neighborhood {
			allCells[pos] = true
		}
	}

	return allCells
}

// enumerateNeighborhood enumerates all cells within Manhattan distance N from center
func (nc *NeighborhoodCalculator) enumerateNeighborhood(grid *Grid, center Position, distanceThreshold int) map[Position]bool {
	neighborhood := make(map[Position]bool)

	// Iterate through the diamond shape
	for deltaRow := -distanceThreshold; deltaRow <= distanceThreshold; deltaRow++ {
		remainingDistance := distanceThreshold - Abs(deltaRow)
		for deltaCol := -remainingDistance; deltaCol <= remainingDistance; deltaCol++ {
			candidateRow := center.Row + deltaRow
			candidateCol := center.Column + deltaCol
			candidate := Position{Row: candidateRow, Column: candidateCol}

			// Only add if within grid boundaries
			if grid.IsValidPosition(candidate) {
				neighborhood[candidate] = true
			}
		}
	}

	return neighborhood
}

// EnumerateNeighborhood is the exported version for testing
func (nc *NeighborhoodCalculator) EnumerateNeighborhood(grid *Grid, center Position, distanceThreshold int) map[Position]bool {
	return nc.enumerateNeighborhood(grid, center, distanceThreshold)
}
