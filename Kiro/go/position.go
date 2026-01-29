package gridneighborhoods

// Position represents a cell position in the grid with (0,0) at bottom-left
type Position struct {
	Row    int
	Column int
}

// ManhattanDistance calculates the Manhattan distance between two positions
func (p Position) ManhattanDistance(other Position) int {
	rowDiff := p.Row - other.Row
	if rowDiff < 0 {
		rowDiff = -rowDiff
	}
	colDiff := p.Column - other.Column
	if colDiff < 0 {
		colDiff = -colDiff
	}
	return rowDiff + colDiff
}

// Abs returns the absolute value of an integer
func Abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}
