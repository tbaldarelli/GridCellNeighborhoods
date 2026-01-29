package main

import (
	"fmt"
	"gridneighborhoods"
)

// Example program demonstrating the grid neighborhoods calculator
func main() {
	fmt.Println("Grid Cell Neighborhoods Calculator")
	fmt.Println("===================================")

	// Create an 11x11 grid with a positive cell at (5,5)
	grid, err := gridneighborhoods.NewGrid(11, 11, []gridneighborhoods.Position{{Row: 5, Column: 5}})
	if err != nil {
		fmt.Printf("Error creating grid: %v\n", err)
		return
	}

	// Calculate neighborhood with distance threshold 3
	calculator := gridneighborhoods.NewNeighborhoodCalculator()
	count, err := calculator.CountNeighborhoodCells(grid, 3)
	if err != nil {
		fmt.Printf("Error calculating neighborhood: %v\n", err)
		return
	}

	fmt.Printf("\nGrid: %dx%d\n", grid.Height, grid.Width)
	fmt.Printf("Positive cell at: (5,5)\n")
	fmt.Printf("Distance threshold: 3\n")
	fmt.Printf("Neighborhood cell count: %d\n", count)

	// Example 2: Multiple overlapping neighborhoods
	fmt.Println("\n---")
	grid2, _ := gridneighborhoods.NewGrid(11, 11, []gridneighborhoods.Position{{Row: 3, Column: 3}, {Row: 4, Column: 5}})
	count2, _ := calculator.CountNeighborhoodCells(grid2, 2)

	fmt.Printf("\nGrid: %dx%d\n", grid2.Height, grid2.Width)
	fmt.Printf("Positive cells at: (3,3) and (4,5)\n")
	fmt.Printf("Distance threshold: 2\n")
	fmt.Printf("Neighborhood cell count: %d (overlapping neighborhoods)\n", count2)
}
