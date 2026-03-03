# Grid Neighborhoods Examples

This directory contains example programs demonstrating how to use the `gridneighborhoods` library.

## Basic Example

The `basic/` directory contains a simple example showing:
- Creating grids with positive cells
- Calculating neighborhood counts
- Handling single and multiple positive cells
- Working with overlapping neighborhoods

### Running the Basic Example

```bash
cd basic
go run .
```

### Building the Example

```bash
cd basic
go build -o example.exe
./example.exe
```

## Using the Library in Your Own Code

To use the gridneighborhoods library in your own Go project:

1. **Import the package:**
```go
import "gridneighborhoods"
```

2. **Create a grid with positive cells:**
```go
grid, err := gridneighborhoods.NewGrid(11, 11, []gridneighborhoods.Position{
    {Row: 5, Column: 5},
})
if err != nil {
    // Handle error
}
```

3. **Calculate neighborhood:**
```go
calculator := gridneighborhoods.NewNeighborhoodCalculator()
count, err := calculator.CountNeighborhoodCells(grid, 3)
if err != nil {
    // Handle error
}
fmt.Printf("Neighborhood count: %d\n", count)
```

## Key Types and Functions

### Position
```go
type Position struct {
    Row    int
    Column int
}
```

### Grid
```go
func NewGrid(height, width int, positiveCells []Position) (*Grid, error)
```

### NeighborhoodCalculator
```go
func NewNeighborhoodCalculator() *NeighborhoodCalculator
func (nc *NeighborhoodCalculator) CountNeighborhoodCells(grid *Grid, distanceThreshold int) (int, error)
func (nc *NeighborhoodCalculator) GetNeighborhoodCells(grid *Grid, distanceThreshold int) map[Position]bool
```

## Error Handling

The library provides custom error types:
- `InvalidGridDimensionsError` - Grid dimensions must be > 0
- `PositionOutOfBoundsError` - Position outside grid boundaries
- `InvalidDistanceThresholdError` - Distance threshold must be >= 0
