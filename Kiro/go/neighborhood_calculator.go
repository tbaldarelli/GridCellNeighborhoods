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

	// Handle empty positive cells case
	if len(grid.PositiveCells) == 0 {
		return 0, nil
	}

	// Optimization 1: Early termination - if distance threshold exceeds grid dimensions,
	// all grid cells will be included (when at least one positive cell exists)
	maxPossibleDistance := (grid.Height - 1) + (grid.Width - 1)
	if distanceThreshold >= maxPossibleDistance {
		return grid.Height * grid.Width, nil
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

	// Optimization 1: Early termination - if distance threshold exceeds grid dimensions,
	// return all grid cells
	maxPossibleDistance := (grid.Height - 1) + (grid.Width - 1)
	if distanceThreshold >= maxPossibleDistance {
		for row := 0; row < grid.Height; row++ {
			for col := 0; col < grid.Width; col++ {
				allCells[Position{Row: row, Column: col}] = true
			}
		}
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

	// Optimization 2: Calculate actual row range considering grid boundaries
	minRow := max(0, center.Row-distanceThreshold)
	maxRow := min(grid.Height-1, center.Row+distanceThreshold)

	// Iterate through the diamond shape
	for row := minRow; row <= maxRow; row++ {
		deltaRow := row - center.Row
		remainingDistance := distanceThreshold - Abs(deltaRow)

		// Optimization 2: Calculate actual column range considering grid boundaries
		minCol := max(0, center.Column-remainingDistance)
		maxCol := min(grid.Width-1, center.Column+remainingDistance)

		for col := minCol; col <= maxCol; col++ {
			neighborhood[Position{Row: row, Column: col}] = true
		}
	}

	return neighborhood
}

// EnumerateNeighborhood is the exported version for testing
func (nc *NeighborhoodCalculator) EnumerateNeighborhood(grid *Grid, center Position, distanceThreshold int) map[Position]bool {
	return nc.enumerateNeighborhood(grid, center, distanceThreshold)
}

// Helper functions for min/max
func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}
