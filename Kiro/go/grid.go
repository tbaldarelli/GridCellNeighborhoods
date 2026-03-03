package gridneighborhoods

// Grid represents a 2D grid with positive cell positions
type Grid struct {
	Height        int
	Width         int
	PositiveCells []Position
}

// NewGrid creates a new grid with validation
func NewGrid(height, width int, positiveCells []Position) (*Grid, error) {
	// Validate dimensions
	if height <= 0 || width <= 0 {
		return nil, &InvalidGridDimensionsError{Height: height, Width: width}
	}

	// Validate all positive cell positions are within bounds
	for _, pos := range positiveCells {
		if pos.Row < 0 || pos.Row >= height || pos.Column < 0 || pos.Column >= width {
			return nil, &PositionOutOfBoundsError{Position: pos, Height: height, Width: width}
		}
	}

	return &Grid{
		Height:        height,
		Width:         width,
		PositiveCells: positiveCells,
	}, nil
}

// IsValidPosition checks if a position is within grid boundaries
func (g *Grid) IsValidPosition(pos Position) bool {
	return pos.Row >= 0 && pos.Row < g.Height && pos.Column >= 0 && pos.Column < g.Width
}
