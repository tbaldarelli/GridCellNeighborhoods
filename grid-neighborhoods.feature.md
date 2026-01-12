# Feature: Grid Cell Neighborhood Counting

## Purpose
Count the number of cells that fall within a neighborhood of one or more positive cells in a 2D grid.
A neighborhood is defined as all cells within the Manhattan-distance.

---

## Definitions

- **Grid**: A two-dimensional array of single signed numeric values.
- **Positive cell**: Any grid cell containing a value greater than zero.
- **Neighborhood**: The set of grid cells whose Manhattan distance from a positive cell
  is less than or equal to `N`.  So these cells are within the neighborhood.
- **Manhattan distance**: The sum of the absolute differences of row and column indices.  So distance = |row1 - row2| + |column1-column2|.
- **Grid boundaries**: The grid does not wrap; movement outside the grid is not allowed.  So the bottom row is not adjacent to the top row, nor the left column adjacent to the right column.

---

## Assumptions

- Grid height (`H`) is greater than 0.
- Grid width (`W`) is greater than 0.
- Distance threshold `N` is greater than or equal to 0.
- Cell locations are identified as `(row, column)`.
- Each grid cell is counted at most once, even if it is within range of multiple positive cells.
- Normal grid behavior, such that (0,0) is in bottom left corner.

---

## Feature: Count Neighborhood Cells

The system calculates the total number of unique grid cells that fall within `N` Manhattan steps
of at least one positive-valued cell.

---

## Scenario 1: Single positive cell fully contained

**Given** a grid with exactly one positive cell
**And** the positive cell is far enough from all grid boundaries  
**And** the positive cell at position `(5,5)`
**And** a distance threshold `3`  
**And** H = `11`
**And** W = `11`

**When** the neighborhood count is calculated  

**Then** the result includes the positive cell itself  
**And** includes all cells within `3` Manhattan steps  
**And** includes no cells outside the grid  
**And** includes `25` cells in the neighborhood

---

## Scenario 2: Single positive cell near a grid edge

**Given** a grid with exactly one positive cell  
**And** the positive cell is near at least one grid boundary  
**And** the positive cell at position `(5,1)`
**And** a distance threshold `3`  
**And** H = `11`
**And** W = `11`

**When** the neighborhood count is calculated  

**Then** cells outside the grid are not counted  
**And** only valid grid cells within `3` Manhattan steps are included  
**And** includes `21` cells in the neighborhood

---

## Scenario 3: Multiple positive cells with non-overlapping neighborhoods

**Given** a grid with more than one positive cell  
**And** the neighborhoods of those positive cells do not overlap  
**And** one positive cell at position `(3,3)`
**And** one positive cell at position `(7,7)`
**And** a distance threshold `2`  
**And** H = `11`
**And** W = `11`

**When** the neighborhood count is calculated  

**Then** all neighborhood cells are included  
**And** the total count is the sum of the individual neighborhoods  
**And** includes `26` cells between the two neighborhoods

---

## Scenario 4: Multiple positive cells with overlapping neighborhoods

**Given** a grid with more than one positive cell  
**And** the neighborhoods of those positive cells overlap  
**And** one positive cell at position `(3,3)`
**And** one positive cell at position `(4,5)`
**And** a distance threshold `2`  
**And** H = `11`
**And** W = `11`

**When** the neighborhood count is calculated  

**Then** overlapping cells are counted only once  
**And** the result reflects the union of all neighborhoods  
**And** includes `22` cells in the combined neighborhood

---

## Scenario 5: Multiple positive cells with overlapping neighborhoods, out of bounds on left

**Given** a grid with more than one positive cell  
**And** the neighborhoods of those positive cells overlap  
**And** one positive cell at position `(3,0)`
**And** one positive cell at position `(4,2)`
**And** a distance threshold `2`  
**And** H = `11`
**And** W = `11`

**When** the neighborhood count is calculated  

**Then** overlapping cells are counted only once  
**And** the result reflects the union of all neighborhoods  
**And** includes `18` cells in the combined neighborhood

---

## Scenario 6: Multiple positive cells with overlapping neighborhoods, out of bounds on bottom left

**Given** a grid with more than one positive cell  
**And** the neighborhoods of those positive cells overlap  
**And** one positive cell at position `(0,0)`
**And** one positive cell at position `(1,2)`
**And** a distance threshold `2`  
**And** H = `11`
**And** W = `11`

**When** the neighborhood count is calculated  

**Then** overlapping cells are counted only once  
**And** the result reflects the union of all neighborhoods  
**And** includes `14` cells in the combined neighborhood

---

## Scenario 7: Multiple positive cells with overlapping neighborhoods, out of bounds on bottom

**Given** a grid with more than one positive cell  
**And** the neighborhoods of those positive cells overlap  
**And** one positive cell at position `(0,3)`
**And** one positive cell at position `(1,5)`
**And** a distance threshold `2`  
**And** H = `11`
**And** W = `11`

**When** the neighborhood count is calculated  

**Then** overlapping cells are counted only once  
**And** the result reflects the union of all neighborhoods  
**And** includes `17` cells in the combined neighborhood

---

## Scenario 8: Multiple positive cells with overlapping neighborhoods, out of bounds right

**Given** a grid with more than one positive cell  
**And** the neighborhoods of those positive cells overlap  
**And** one positive cell at position `(3,8)`
**And** one positive cell at position `(4,10)`
**And** a distance threshold `2`  
**And** H = `11`
**And** W = `11`

**When** the neighborhood count is calculated  

**Then** overlapping cells are counted only once  
**And** the result reflects the union of all neighborhoods  
**And** includes `18` cells in the combined neighborhood

---

## Scenario 9: Multiple positive cells with overlapping neighborhoods, out of bounds top

**Given** a grid with more than one positive cell  
**And** the neighborhoods of those positive cells overlap  
**And** one positive cell at position `(9,3)`
**And** one positive cell at position `(10,5)`
**And** a distance threshold `2`  
**And** H = `11`
**And** W = `11`

**When** the neighborhood count is calculated  

**Then** overlapping cells are counted only once  
**And** the result reflects the union of all neighborhoods  
**And** includes `17` cells in the combined neighborhood

---

## Scenario 10: Multiple positive cells with overlapping neighborhoods, diagonally adjacent

**Given** a grid with more than one positive cell  
**And** the neighborhoods of those positive cells overlap  
**And** one positive cell at position `(3,3)`
**And** one positive cell at position `(4,4)`
**And** a distance threshold `2`  
**And** H = `11`
**And** W = `11`

**When** the neighborhood count is calculated  

**Then** overlapping cells are counted only once  
**And** the result reflects the union of all neighborhoods  
**And** includes `18` cells in the combined neighborhood

---

## Scenario 5: Distance threshold of zero

**Given** a grid with one or more positive cells  
**And** the distance threshold `N` is zero  

**When** the neighborhood count is calculated  

**Then** only the cells containing positive values are counted  

---

## Scenario 6: Distance threshold larger than grid dimensions

**Given** a grid with at least one positive cell  
**And** the distance threshold `N` is greater than one or more grid dimensions  

**When** the neighborhood count is calculated  

**Then** only valid grid cells are considered  
**And** the calculation follows Manhattan distance rules  
**And** no assumptions are made about full grid coverage  

---

## Non-Functional Expectations

- The calculation should complete in reasonable time for large grids.
- The solution should handle narrow or oddly shaped grids (e.g., 1×N, N×1).
- The behavior described here must remain consistent regardless of implementation language.

---

## Notes

- This document specifies *what* the system must do, not *how* it does it.
- All numeric examples should be derived from the problem description, not hard-coded assumptions.