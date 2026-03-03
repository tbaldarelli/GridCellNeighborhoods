package gridneighborhoods_test

import (
	"testing"

	. "gridneighborhoods"

	"pgregory.net/rapid"
)

// Property 1: Grid Validation
func TestProperty1GridValidation(t *testing.T) {
	rapid.Check(t, func(t *rapid.T) {
		height := rapid.IntRange(-100, 1000).Draw(t, "height")
		width := rapid.IntRange(-100, 1000).Draw(t, "width")

		grid, err := NewGrid(height, width, []Position{})

		if height > 0 && width > 0 {
			// Valid dimensions should create a grid successfully
			if err != nil {
				t.Fatalf("Expected no error for valid dimensions %dx%d, got %v", height, width, err)
			}
			if grid.Height != height || grid.Width != width {
				t.Fatalf("Grid dimensions mismatch: expected %dx%d, got %dx%d", height, width, grid.Height, grid.Width)
			}
		} else {
			// Invalid dimensions should return error
			if err == nil {
				t.Fatalf("Expected error for invalid dimensions %dx%d", height, width)
			}
		}
	})
}

// Property 2: Manhattan Distance Calculation
func TestProperty2ManhattanDistanceCalculation(t *testing.T) {
	rapid.Check(t, func(t *rapid.T) {
		row1 := rapid.IntRange(0, 1000).Draw(t, "row1")
		col1 := rapid.IntRange(0, 1000).Draw(t, "col1")
		row2 := rapid.IntRange(0, 1000).Draw(t, "row2")
		col2 := rapid.IntRange(0, 1000).Draw(t, "col2")

		pos1 := Position{Row: row1, Column: col1}
		pos2 := Position{Row: row2, Column: col2}

		distance := pos1.ManhattanDistance(pos2)
		expectedDistance := Abs(row1-row2) + Abs(col1-col2)

		// Distance should equal the Manhattan formula
		if distance != expectedDistance {
			t.Fatalf("Expected distance %d, got %d", expectedDistance, distance)
		}

		// Distance should always be non-negative
		if distance < 0 {
			t.Fatalf("Distance should be non-negative, got %d", distance)
		}

		// Distance should be 0 when positions are identical
		if row1 == row2 && col1 == col2 {
			if distance != 0 {
				t.Fatalf("Distance should be 0 for identical positions, got %d", distance)
			}
		}

		// Distance should be symmetric
		reverseDistance := pos2.ManhattanDistance(pos1)
		if distance != reverseDistance {
			t.Fatalf("Distance should be symmetric: %d != %d", distance, reverseDistance)
		}
	})
}

// Property 3: Coordinate System Consistency
func TestProperty3CoordinateSystemConsistency(t *testing.T) {
	rapid.Check(t, func(t *rapid.T) {
		height := rapid.IntRange(1, 100).Draw(t, "height")
		width := rapid.IntRange(1, 100).Draw(t, "width")

		// Generate valid positions within bounds
		numPositions := rapid.IntRange(0, 20).Draw(t, "numPositions")
		positions := make([]Position, 0, numPositions)
		posSet := make(map[Position]bool)

		for i := 0; i < numPositions; i++ {
			row := rapid.IntRange(0, height-1).Draw(t, "pos_row")
			col := rapid.IntRange(0, width-1).Draw(t, "pos_col")
			pos := Position{Row: row, Column: col}
			if !posSet[pos] {
				positions = append(positions, pos)
				posSet[pos] = true
			}
		}

		grid, err := NewGrid(height, width, positions)
		if err != nil {
			t.Fatalf("Failed to create grid: %v", err)
		}

		// Position (0,0) should be valid for any grid
		bottomLeft := Position{Row: 0, Column: 0}
		if !grid.IsValidPosition(bottomLeft) {
			t.Fatal("Position (0,0) should be valid")
		}

		// Position (height-1, width-1) should be valid (top-right corner)
		topRight := Position{Row: height - 1, Column: width - 1}
		if !grid.IsValidPosition(topRight) {
			t.Fatal("Top-right corner should be valid")
		}

		// Positions outside bounds should be invalid
		if height < 1000 {
			outOfBounds := Position{Row: height, Column: 0}
			if grid.IsValidPosition(outOfBounds) {
				t.Fatal("Position outside bounds should be invalid")
			}
		}

		if width < 1000 {
			outOfBounds := Position{Row: 0, Column: width}
			if grid.IsValidPosition(outOfBounds) {
				t.Fatal("Position outside bounds should be invalid")
			}
		}
	})
}

// Property 4: Self-Inclusion in Neighborhoods
func TestProperty4SelfInclusionInNeighborhoods(t *testing.T) {
	rapid.Check(t, func(t *rapid.T) {
		height := rapid.IntRange(1, 50).Draw(t, "height")
		width := rapid.IntRange(1, 50).Draw(t, "width")
		positiveRow := rapid.IntRange(0, height-1).Draw(t, "positiveRow")
		positiveCol := rapid.IntRange(0, width-1).Draw(t, "positiveCol")
		distanceThreshold := rapid.IntRange(0, 100).Draw(t, "distanceThreshold")

		positivePos := Position{Row: positiveRow, Column: positiveCol}
		grid, _ := NewGrid(height, width, []Position{positivePos})

		calculator := NewNeighborhoodCalculator()
		neighborhood := calculator.GetNeighborhoodCells(grid, distanceThreshold)

		// The positive cell should always be included in its own neighborhood
		if !neighborhood[positivePos] {
			t.Fatal("Positive cell should be included in its own neighborhood")
		}

		count, _ := calculator.CountNeighborhoodCells(grid, distanceThreshold)
		if count < 1 {
			t.Fatalf("Count should be at least 1, got %d", count)
		}
	})
}

// Property 7: Cell Uniqueness Guarantee
func TestProperty7CellUniquenessGuarantee(t *testing.T) {
	rapid.Check(t, func(t *rapid.T) {
		height := rapid.IntRange(1, 30).Draw(t, "height")
		width := rapid.IntRange(1, 30).Draw(t, "width")
		distanceThreshold := rapid.IntRange(0, 20).Draw(t, "distanceThreshold")

		// Generate 1-10 unique positive positions
		numPositions := rapid.IntRange(1, 10).Draw(t, "numPositions")
		positions := make([]Position, 0, numPositions)
		posSet := make(map[Position]bool)

		for i := 0; i < numPositions; i++ {
			row := rapid.IntRange(0, height-1).Draw(t, "pos_row")
			col := rapid.IntRange(0, width-1).Draw(t, "pos_col")
			pos := Position{Row: row, Column: col}
			if !posSet[pos] {
				positions = append(positions, pos)
				posSet[pos] = true
			}
		}

		if len(positions) == 0 {
			t.Skip("No valid positions generated")
		}

		grid, _ := NewGrid(height, width, positions)
		calculator := NewNeighborhoodCalculator()

		allCells := calculator.GetNeighborhoodCells(grid, distanceThreshold)
		count, _ := calculator.CountNeighborhoodCells(grid, distanceThreshold)

		// The count should equal the size of the set (no duplicates)
		if count != len(allCells) {
			t.Fatalf("Count %d should equal set size %d", count, len(allCells))
		}

		// Calculate sum of individual neighborhoods
		sumOfIndividual := 0
		for _, pos := range positions {
			neighborhood := calculator.EnumerateNeighborhood(grid, pos, distanceThreshold)
			sumOfIndividual += len(neighborhood)
		}

		// Total count should be <= sum of individual counts
		if count > sumOfIndividual {
			t.Fatalf("Total count %d should be <= sum of individual %d", count, sumOfIndividual)
		}
	})
}

// Property 10: Zero Distance Threshold
func TestProperty10ZeroDistanceThreshold(t *testing.T) {
	rapid.Check(t, func(t *rapid.T) {
		height := rapid.IntRange(1, 50).Draw(t, "height")
		width := rapid.IntRange(1, 50).Draw(t, "width")

		// Generate 1-20 unique positive positions
		numPositions := rapid.IntRange(1, 20).Draw(t, "numPositions")
		positions := make([]Position, 0, numPositions)
		posSet := make(map[Position]bool)

		for i := 0; i < numPositions; i++ {
			row := rapid.IntRange(0, height-1).Draw(t, "pos_row")
			col := rapid.IntRange(0, width-1).Draw(t, "pos_col")
			pos := Position{Row: row, Column: col}
			if !posSet[pos] {
				positions = append(positions, pos)
				posSet[pos] = true
			}
		}

		if len(positions) == 0 {
			t.Skip("No valid positions generated")
		}

		grid, _ := NewGrid(height, width, positions)
		calculator := NewNeighborhoodCalculator()

		// With distance threshold 0, only positive cells themselves should be counted
		count, _ := calculator.CountNeighborhoodCells(grid, 0)

		// Count should equal exactly the number of positive cells
		expectedCount := len(positions)
		if count != expectedCount {
			t.Fatalf("Expected count %d, got %d", expectedCount, count)
		}

		// Verify using GetNeighborhoodCells as well
		allCells := calculator.GetNeighborhoodCells(grid, 0)
		if len(allCells) != expectedCount {
			t.Fatalf("Expected %d cells, got %d", expectedCount, len(allCells))
		}

		// All cells in the result should be positive cells
		for _, pos := range positions {
			if !allCells[pos] {
				t.Fatalf("Positive cell %v should be in result", pos)
			}
		}
	})
}

// Property 11: Maximum Distance Threshold
func TestProperty11MaximumDistanceThreshold(t *testing.T) {
	rapid.Check(t, func(t *rapid.T) {
		height := rapid.IntRange(1, 20).Draw(t, "height")
		width := rapid.IntRange(1, 20).Draw(t, "width")

		// Generate at least one positive position
		numPositions := rapid.IntRange(1, 10).Draw(t, "numPositions")
		positions := make([]Position, 0, numPositions)
		posSet := make(map[Position]bool)

		for i := 0; i < numPositions; i++ {
			row := rapid.IntRange(0, height-1).Draw(t, "pos_row")
			col := rapid.IntRange(0, width-1).Draw(t, "pos_col")
			pos := Position{Row: row, Column: col}
			if !posSet[pos] {
				positions = append(positions, pos)
				posSet[pos] = true
			}
		}

		if len(positions) == 0 {
			t.Skip("No valid positions generated")
		}

		grid, _ := NewGrid(height, width, positions)
		calculator := NewNeighborhoodCalculator()

		// Calculate maximum possible Manhattan distance
		maxPossibleDistance := (height - 1) + (width - 1)

		// Use a distance threshold that exceeds the maximum
		excessiveThreshold := maxPossibleDistance + 10

		count, _ := calculator.CountNeighborhoodCells(grid, excessiveThreshold)

		// All grid cells should be counted
		expectedCount := height * width
		if count != expectedCount {
			t.Fatalf("Expected count %d (all cells), got %d", expectedCount, count)
		}

		// Verify using GetNeighborhoodCells
		allCells := calculator.GetNeighborhoodCells(grid, excessiveThreshold)
		if len(allCells) != expectedCount {
			t.Fatalf("Expected %d cells, got %d", expectedCount, len(allCells))
		}
	})
}

// Property 12: Degenerate Grid Handling
func TestProperty12DegenerateGridHandling(t *testing.T) {
	rapid.Check(t, func(t *rapid.T) {
		gridType := rapid.SampledFrom([]string{"1xN", "Nx1", "1x1"}).Draw(t, "gridType")
		dimension := rapid.IntRange(1, 50).Draw(t, "dimension")
		distanceThreshold := rapid.IntRange(0, 20).Draw(t, "distanceThreshold")

		var height, width, positiveRow, positiveCol int

		switch gridType {
		case "1xN":
			height, width = 1, dimension
			positiveRow = 0
			positiveCol = rapid.IntRange(0, width-1).Draw(t, "positiveCol")
		case "Nx1":
			height, width = dimension, 1
			positiveRow = rapid.IntRange(0, height-1).Draw(t, "positiveRow")
			positiveCol = 0
		case "1x1":
			height, width = 1, 1
			positiveRow, positiveCol = 0, 0
		}

		positivePos := Position{Row: positiveRow, Column: positiveCol}
		grid, _ := NewGrid(height, width, []Position{positivePos})

		calculator := NewNeighborhoodCalculator()
		neighborhood := calculator.GetNeighborhoodCells(grid, distanceThreshold)
		count, _ := calculator.CountNeighborhoodCells(grid, distanceThreshold)

		// Verify basic properties
		if len(neighborhood) != count {
			t.Fatalf("Neighborhood size %d should equal count %d", len(neighborhood), count)
		}

		if !neighborhood[positivePos] {
			t.Fatal("Positive cell should be in neighborhood (self-inclusion)")
		}

		// Verify all cells in neighborhood are within distance threshold
		for cell := range neighborhood {
			manhattanDist := positivePos.ManhattanDistance(cell)
			if manhattanDist > distanceThreshold {
				t.Fatalf("Cell %v at distance %d should not be in neighborhood (threshold %d)", cell, manhattanDist, distanceThreshold)
			}
		}

		// Verify all cells within distance threshold are included
		for row := 0; row < height; row++ {
			for col := 0; col < width; col++ {
				candidatePos := Position{Row: row, Column: col}
				if positivePos.ManhattanDistance(candidatePos) <= distanceThreshold {
					if !neighborhood[candidatePos] {
						t.Fatalf("Cell %v should be in neighborhood", candidatePos)
					}
				}
			}
		}

		// Special case for 1x1 grid
		if gridType == "1x1" && distanceThreshold >= 0 {
			if count != 1 {
				t.Fatalf("1x1 grid should have count 1, got %d", count)
			}
		}
	})
}
