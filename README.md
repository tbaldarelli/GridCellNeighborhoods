# Grid Cell Neighborhoods

This project implements a solution to count the number of unique grid cells within a Manhattan distance neighborhood of positive-valued cells in a 2D grid. It was developed as part of an interview coding challenge.

## Problem Description

Given a 2D grid of signed numeric values, identify all cells containing positive values (> 0). For each positive cell, determine the neighborhood consisting of all cells within Manhattan distance N (where N >= 0). The Manhattan distance between two cells at positions (r1, c1) and (r2, c2) is |r1 - r2| + |c1 - c2|.

The goal is to count the total number of unique cells that fall within at least one such neighborhood, ensuring no double-counting of overlapping areas.

### Key Requirements
- Grid does not wrap around edges
- Cells outside grid boundaries are not counted
- Each cell is counted at most once, even if within multiple neighborhoods
- Distance threshold N can be 0 or greater

## Solution

Two Java implementations are provided:

1. **GridCellNeighborhoods.java** - Original implementation.  This was actually a bad understanind of the problem, where I assumed I had to hit the exact Manhattan distance.
2. **GridCellNeighborhoodsWithinDistance.java** - Alternative implementation.  This was my fix to the above.  Originally I did things with reference to the square around the positive cell, but then, based on feedback in the interview, I realized I could treat it as a diamond around the postive cell.

Both classes provide methods to:
- Initialize a grid with specified dimensions and positive cell positions
- Calculate the neighborhood count based on Manhattan distance
- Support debugging and cell listing options.  The test cases are coded directly into the main function, going to stdout.  Not ideal, but it kept things simple.

## Building and Running

### Prerequisites
- Java Development Kit (JDK) 11 or higher
- Command line access

### Compilation
```bash
javac GridCellNeighborhoods.java
javac GridCellNeighborhoodsWithinDistance.java
```

### Running
```bash
java -cp . GridCellNeighborhoods
java -cp . GridCellNeighborhoodsWithinDistance
```

Each program includes example scenarios that demonstrate the functionality and validate against the expected counts from the feature specifications.

## Project Structure
- `grid-neighborhoods.feature.md` - Detailed feature specifications and test scenarios
- `GridCellNeighborhoods.java` - Primary implementation
- `GridCellNeighborhoodsWithinDistance.java` - Alternative implementation.  This is a better implementation, see above.
- `README.md` - This file
- `Kiro` - a place to use Kiro to implement the feature specifications in various languages.  This is just to see how to solve the problem in other languages, to get a little exposure to thos languages, and to see how those solutions compare to my solution.
- FUTURE: `Warp` - a place to use Warp to implement the feature specifications in various languages.  This is just to see how to solve the problem in other languages, to get a little exposure to thos languages, and to see how those solutions compare to my solution.

## Interview Notes

As we examined edge cases in the interview, we realized it took to long in one case.  This is where the interviewers guided me to seeing things as a diamond.  I also saw some other areas I could make improvements in as we talked, but this was the biggest change.  While we did not have time to try it then, I have since made that change and it is much better.

