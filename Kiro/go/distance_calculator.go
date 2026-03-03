package gridneighborhoods

// DistanceCalculator provides Manhattan distance calculation
type DistanceCalculator struct{}

// NewDistanceCalculator creates a new distance calculator
func NewDistanceCalculator() *DistanceCalculator {
	return &DistanceCalculator{}
}

// CalculateManhattanDistance computes the Manhattan distance between two positions
func (dc *DistanceCalculator) CalculateManhattanDistance(pos1, pos2 Position) int {
	return pos1.ManhattanDistance(pos2)
}
