package gridneighborhoods_test

import (
	"fmt"
	"testing"

	. "gridneighborhoods"
)

// TestSinglePositiveCellScenarios tests BDD Scenarios 1-2
func TestScenario1SinglePositiveCellFullyContained(t *testing.T) {
	grid, _ := NewGrid(11, 11, []Position{{Row: 5, Column: 5}})
	calculator := NewNeighborhoodCalculator()
	count, _ := calculator.CountNeighborhoodCells(grid, 3)

	fmt.Printf("Scenario 1: Expected=25, Grid=11x11, N=3, Pos=[(5,5)], Got=%d\n", count)
	if count != 25 {
		t.Errorf("Expected 25, got %d", count)
	}
}

func TestScenario2SinglePositiveCellNearEdge(t *testing.T) {
	grid, _ := NewGrid(11, 11, []Position{{Row: 5, Column: 1}})
	calculator := NewNeighborhoodCalculator()
	count, _ := calculator.CountNeighborhoodCells(grid, 3)

	fmt.Printf("Scenario 2: Expected=21, Grid=11x11, N=3, Pos=[(5,1)], Got=%d\n", count)
	if count != 21 {
		t.Errorf("Expected 21, got %d", count)
	}
}

// TestMultiplePositiveCellsNonOverlapping tests BDD Scenario 3
func TestScenario3NonOverlappingNeighborhoods(t *testing.T) {
	grid, _ := NewGrid(11, 11, []Position{{Row: 3, Column: 3}, {Row: 7, Column: 7}})
	calculator := NewNeighborhoodCalculator()
	count, _ := calculator.CountNeighborhoodCells(grid, 2)

	fmt.Printf("Scenario 3: Expected=26, Grid=11x11, N=2, Pos=[(3,3),(7,7)], Got=%d\n", count)
	if count != 26 {
		t.Errorf("Expected 26, got %d", count)
	}
}

// TestMultiplePositiveCellsOverlapping tests BDD Scenarios 4-14
func TestScenario4OverlappingNeighborhoods(t *testing.T) {
	grid, _ := NewGrid(11, 11, []Position{{Row: 3, Column: 3}, {Row: 4, Column: 5}})
	calculator := NewNeighborhoodCalculator()
	count, _ := calculator.CountNeighborhoodCells(grid, 2)

	fmt.Printf("Scenario 4: Expected=22, Grid=11x11, N=2, Pos=[(3,3),(4,5)], Got=%d\n", count)
	if count != 22 {
		t.Errorf("Expected 22, got %d", count)
	}
}

func TestScenario5OverlappingOutOfBoundsLeft(t *testing.T) {
	grid, _ := NewGrid(11, 11, []Position{{Row: 3, Column: 0}, {Row: 4, Column: 2}})
	calculator := NewNeighborhoodCalculator()
	count, _ := calculator.CountNeighborhoodCells(grid, 2)

	fmt.Printf("Scenario 5: Expected=18, Grid=11x11, N=2, Pos=[(3,0),(4,2)], Got=%d\n", count)
	if count != 18 {
		t.Errorf("Expected 18, got %d", count)
	}
}

func TestScenario6OverlappingOutOfBoundsBottomLeft(t *testing.T) {
	grid, _ := NewGrid(11, 11, []Position{{Row: 0, Column: 0}, {Row: 1, Column: 2}})
	calculator := NewNeighborhoodCalculator()
	count, _ := calculator.CountNeighborhoodCells(grid, 2)

	fmt.Printf("Scenario 6: Expected=14, Grid=11x11, N=2, Pos=[(0,0),(1,2)], Got=%d\n", count)
	if count != 14 {
		t.Errorf("Expected 14, got %d", count)
	}
}

func TestScenario7OverlappingOutOfBoundsBottom(t *testing.T) {
	grid, _ := NewGrid(11, 11, []Position{{Row: 0, Column: 3}, {Row: 1, Column: 5}})
	calculator := NewNeighborhoodCalculator()
	count, _ := calculator.CountNeighborhoodCells(grid, 2)

	fmt.Printf("Scenario 7: Expected=17, Grid=11x11, N=2, Pos=[(0,3),(1,5)], Got=%d\n", count)
	if count != 17 {
		t.Errorf("Expected 17, got %d", count)
	}
}

func TestScenario8OverlappingOutOfBoundsRight(t *testing.T) {
	grid, _ := NewGrid(11, 11, []Position{{Row: 3, Column: 8}, {Row: 4, Column: 10}})
	calculator := NewNeighborhoodCalculator()
	count, _ := calculator.CountNeighborhoodCells(grid, 2)

	fmt.Printf("Scenario 8: Expected=18, Grid=11x11, N=2, Pos=[(3,8),(4,10)], Got=%d\n", count)
	if count != 18 {
		t.Errorf("Expected 18, got %d", count)
	}
}

func TestScenario9OverlappingOutOfBoundsTop(t *testing.T) {
	grid, _ := NewGrid(11, 11, []Position{{Row: 9, Column: 3}, {Row: 10, Column: 5}})
	calculator := NewNeighborhoodCalculator()
	count, _ := calculator.CountNeighborhoodCells(grid, 2)

	fmt.Printf("Scenario 9: Expected=17, Grid=11x11, N=2, Pos=[(9,3),(10,5)], Got=%d\n", count)
	if count != 17 {
		t.Errorf("Expected 17, got %d", count)
	}
}

func TestScenario10OverlappingDiagonallyAdjacent(t *testing.T) {
	grid, _ := NewGrid(11, 11, []Position{{Row: 3, Column: 3}, {Row: 4, Column: 4}})
	calculator := NewNeighborhoodCalculator()
	count, _ := calculator.CountNeighborhoodCells(grid, 2)

	fmt.Printf("Scenario 10: Expected=18, Grid=11x11, N=2, Pos=[(3,3),(4,4)], Got=%d\n", count)
	if count != 18 {
		t.Errorf("Expected 18, got %d", count)
	}
}

func TestScenario11OverlappingSameRowAdjacent(t *testing.T) {
	grid, _ := NewGrid(11, 11, []Position{{Row: 3, Column: 3}, {Row: 3, Column: 4}})
	calculator := NewNeighborhoodCalculator()
	count, _ := calculator.CountNeighborhoodCells(grid, 2)

	fmt.Printf("Scenario 11: Expected=18, Grid=11x11, N=2, Pos=[(3,3),(3,4)], Got=%d\n", count)
	if count != 18 {
		t.Errorf("Expected 18, got %d", count)
	}
}

func TestScenario12OverlappingSameColumnAdjacent(t *testing.T) {
	grid, _ := NewGrid(11, 11, []Position{{Row: 3, Column: 4}, {Row: 4, Column: 4}})
	calculator := NewNeighborhoodCalculator()
	count, _ := calculator.CountNeighborhoodCells(grid, 2)

	fmt.Printf("Scenario 12: Expected=18, Grid=11x11, N=2, Pos=[(3,4),(4,4)], Got=%d\n", count)
	if count != 18 {
		t.Errorf("Expected 18, got %d", count)
	}
}

func TestScenario13OppositeCorners(t *testing.T) {
	grid, _ := NewGrid(11, 11, []Position{{Row: 0, Column: 0}, {Row: 10, Column: 10}})
	calculator := NewNeighborhoodCalculator()
	count, _ := calculator.CountNeighborhoodCells(grid, 3)

	fmt.Printf("Scenario 13: Expected=20, Grid=11x11, N=3, Pos=[(0,0),(10,10)], Got=%d\n", count)
	if count != 20 {
		t.Errorf("Expected 20, got %d", count)
	}
}

func TestScenario14ThreeInOneCorner(t *testing.T) {
	grid, _ := NewGrid(11, 11, []Position{{Row: 10, Column: 9}, {Row: 9, Column: 10}, {Row: 10, Column: 10}})
	calculator := NewNeighborhoodCalculator()
	count, _ := calculator.CountNeighborhoodCells(grid, 3)

	fmt.Printf("Scenario 14: Expected=15, Grid=11x11, N=3, Pos=[(10,9),(9,10),(10,10)], Got=%d\n", count)
	if count != 15 {
		t.Errorf("Expected 15, got %d", count)
	}
}

// TestDegenerateGridScenarios tests BDD Scenarios 15-25
func TestScenario15_1x21Grid(t *testing.T) {
	grid, _ := NewGrid(1, 21, []Position{{Row: 0, Column: 9}})
	calculator := NewNeighborhoodCalculator()
	count, _ := calculator.CountNeighborhoodCells(grid, 3)

	fmt.Printf("Scenario 15: Expected=7, Grid=1x21, N=3, Pos=[(0,9)], Got=%d\n", count)
	if count != 7 {
		t.Errorf("Expected 7, got %d", count)
	}
}

func TestScenario16_21x1Grid(t *testing.T) {
	grid, _ := NewGrid(21, 1, []Position{{Row: 10, Column: 0}})
	calculator := NewNeighborhoodCalculator()
	count, _ := calculator.CountNeighborhoodCells(grid, 3)

	fmt.Printf("Scenario 16: Expected=7, Grid=21x1, N=3, Pos=[(10,0)], Got=%d\n", count)
	if count != 7 {
		t.Errorf("Expected 7, got %d", count)
	}
}

func TestScenario17_1x1Grid(t *testing.T) {
	grid, _ := NewGrid(1, 1, []Position{{Row: 0, Column: 0}})
	calculator := NewNeighborhoodCalculator()
	count, _ := calculator.CountNeighborhoodCells(grid, 0)

	fmt.Printf("Scenario 17: Expected=1, Grid=1x1, N=0, Pos=[(0,0)], Got=%d\n", count)
	if count != 1 {
		t.Errorf("Expected 1, got %d", count)
	}
}

func TestScenario18_20x20GridThresholdZero(t *testing.T) {
	grid, _ := NewGrid(20, 20, []Position{{Row: 0, Column: 0}})
	calculator := NewNeighborhoodCalculator()
	count, _ := calculator.CountNeighborhoodCells(grid, 0)

	fmt.Printf("Scenario 18: Expected=1, Grid=20x20, N=0, Pos=[(0,0)], Got=%d\n", count)
	if count != 1 {
		t.Errorf("Expected 1, got %d", count)
	}
}

func TestScenario19_2x2Grid(t *testing.T) {
	grid, _ := NewGrid(2, 2, []Position{{Row: 0, Column: 1}})
	calculator := NewNeighborhoodCalculator()
	count, _ := calculator.CountNeighborhoodCells(grid, 2)

	fmt.Printf("Scenario 19: Expected=4, Grid=2x2, N=2, Pos=[(0,1)], Got=%d\n", count)
	if count != 4 {
		t.Errorf("Expected 4, got %d", count)
	}
}

func TestScenario20_21x3GridNGreaterThanW(t *testing.T) {
	grid, _ := NewGrid(21, 3, []Position{{Row: 10, Column: 2}})
	calculator := NewNeighborhoodCalculator()
	count, _ := calculator.CountNeighborhoodCells(grid, 5)

	fmt.Printf("Scenario 20: Expected=27, Grid=21x3, N=5, Pos=[(10,2)], Got=%d\n", count)
	if count != 27 {
		t.Errorf("Expected 27, got %d", count)
	}
}

func TestScenario21_4x15GridNGreaterThanH(t *testing.T) {
	grid, _ := NewGrid(4, 15, []Position{{Row: 2, Column: 9}})
	calculator := NewNeighborhoodCalculator()
	count, _ := calculator.CountNeighborhoodCells(grid, 5)

	fmt.Printf("Scenario 21: Expected=36, Grid=4x15, N=5, Pos=[(2,9)], Got=%d\n", count)
	if count != 36 {
		t.Errorf("Expected 36, got %d", count)
	}
}

func TestScenario22_2x2GridNGreaterThanBoth(t *testing.T) {
	grid, _ := NewGrid(2, 2, []Position{{Row: 0, Column: 1}})
	calculator := NewNeighborhoodCalculator()
	count, _ := calculator.CountNeighborhoodCells(grid, 3)

	fmt.Printf("Scenario 22: Expected=4, Grid=2x2, N=3, Pos=[(0,1)], Got=%d\n", count)
	if count != 4 {
		t.Errorf("Expected 4, got %d", count)
	}
}

func TestScenario23_2x2GridNMuchGreater(t *testing.T) {
	grid, _ := NewGrid(2, 2, []Position{{Row: 0, Column: 1}})
	calculator := NewNeighborhoodCalculator()
	count, _ := calculator.CountNeighborhoodCells(grid, 100000)

	fmt.Printf("Scenario 23: Expected=4, Grid=2x2, N=100000, Pos=[(0,1)], Got=%d\n", count)
	if count != 4 {
		t.Errorf("Expected 4, got %d", count)
	}
}

func TestScenario24_11x11GridCornerLargeN(t *testing.T) {
	grid, _ := NewGrid(11, 11, []Position{{Row: 0, Column: 0}})
	calculator := NewNeighborhoodCalculator()
	count, _ := calculator.CountNeighborhoodCells(grid, 12)

	fmt.Printf("Scenario 24: Expected=85, Grid=11x11, N=12, Pos=[(0,0)], Got=%d\n", count)
	if count != 85 {
		t.Errorf("Expected 85, got %d", count)
	}
}

func TestScenario25_11x11GridCenterLargeN(t *testing.T) {
	grid, _ := NewGrid(11, 11, []Position{{Row: 5, Column: 5}})
	calculator := NewNeighborhoodCalculator()
	count, _ := calculator.CountNeighborhoodCells(grid, 12)

	fmt.Printf("Scenario 25: Expected=121, Grid=11x11, N=12, Pos=[(5,5)], Got=%d\n", count)
	if count != 121 {
		t.Errorf("Expected 121, got %d", count)
	}
}

// TestNoPositiveCellsScenario tests BDD Scenario 26
func TestScenario26NoPositiveCells(t *testing.T) {
	grid, _ := NewGrid(10, 10, []Position{})
	calculator := NewNeighborhoodCalculator()
	count, _ := calculator.CountNeighborhoodCells(grid, 3)

	fmt.Printf("Scenario 26: Expected=0, Grid=10x10, N=3, Pos=[], Got=%d\n", count)
	if count != 0 {
		t.Errorf("Expected 0, got %d", count)
	}
}
