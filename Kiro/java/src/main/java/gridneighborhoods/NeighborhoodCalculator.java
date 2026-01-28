package gridneighborhoods;

import gridneighborhoods.exceptions.InvalidDistanceThresholdException;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * Calculator for neighborhood enumeration using diamond-shaped Manhattan distance.
 * 
 * This class provides optimized algorithms for calculating neighborhoods of positive
 * cells in a grid using Manhattan distance. It includes several performance optimizations:
 * 
 * - Early termination when distance threshold exceeds grid dimensions
 * - Memory-efficient set operations for large neighborhoods
 * - Boundary-aware enumeration to avoid unnecessary calculations
 * - Special handling for edge cases (zero distance, no positive cells)
 */
public class NeighborhoodCalculator {
    
    /**
     * Enumerate all cells within Manhattan distance of a center position.
     * 
     * Uses optimized diamond enumeration algorithm to find all cells within the specified
     * Manhattan distance threshold, respecting grid boundaries.
     * 
     * Optimizations:
     * - Boundary-aware iteration to skip out-of-bounds calculations
     * - Early row/column range clamping to grid dimensions
     * - Memory-efficient set construction
     * 
     * @param center Center position for the neighborhood
     * @param distanceThreshold Maximum Manhattan distance (N >= 0)
     * @param grid Grid to check boundaries against
     * @return Set of positions within the neighborhood
     * @throws InvalidDistanceThresholdException If distanceThreshold is negative
     */
    public Set<Position> enumerateNeighborhood(Position center, int distanceThreshold, Grid grid) {
        if (distanceThreshold < 0) {
            throw new InvalidDistanceThresholdException(distanceThreshold);
        }
        
        // Optimization: Calculate actual row range considering grid boundaries
        int minRow = Math.max(0, center.getRow() - distanceThreshold);
        int maxRow = Math.min(grid.getHeight() - 1, center.getRow() + distanceThreshold);
        
        Set<Position> neighborhood = new HashSet<>();
        
        // Diamond enumeration: for each row offset, calculate column range
        for (int row = minRow; row <= maxRow; row++) {
            int deltaRow = row - center.getRow();
            int remainingDistance = distanceThreshold - Math.abs(deltaRow);
            
            // Optimization: Calculate actual column range considering grid boundaries
            int minCol = Math.max(0, center.getColumn() - remainingDistance);
            int maxCol = Math.min(grid.getWidth() - 1, center.getColumn() + remainingDistance);
            
            // Add all valid columns in this row
            for (int col = minCol; col <= maxCol; col++) {
                neighborhood.add(new Position(row, col));
            }
        }
        
        return neighborhood;
    }
    
    /**
     * Count total unique cells in neighborhoods of all positive cells.
     * 
     * This method implements several performance optimizations:
     * - Early termination when distance threshold exceeds grid dimensions
     * - Zero distance threshold optimization (returns count of positive cells)
     * - Empty grid handling (returns 0 immediately)
     * - Memory-efficient set operations for large neighborhoods
     * 
     * @param grid Grid containing positive cells
     * @param distanceThreshold Maximum Manhattan distance
     * @return Total count of unique cells in all neighborhoods
     * @throws InvalidDistanceThresholdException If distanceThreshold is negative
     */
    public int countNeighborhoodCells(Grid grid, int distanceThreshold) {
        if (distanceThreshold < 0) {
            throw new InvalidDistanceThresholdException(distanceThreshold);
        }
        
        List<Position> positiveCells = grid.getPositiveCells();
        
        // Optimization: Handle edge case - no positive cells
        if (positiveCells.isEmpty()) {
            return 0;
        }
        
        // Optimization: Early termination - if distance threshold exceeds grid dimensions,
        // all grid cells will be included (when at least one positive cell exists)
        int maxPossibleDistance = (grid.getHeight() - 1) + (grid.getWidth() - 1);
        if (distanceThreshold >= maxPossibleDistance) {
            return grid.getHeight() * grid.getWidth();
        }
        
        // Optimization: Handle edge case - zero distance threshold
        // Only positive cells themselves are counted
        if (distanceThreshold == 0) {
            return positiveCells.size();
        }
        
        // Optimization: For single positive cell, use direct enumeration
        if (positiveCells.size() == 1) {
            Set<Position> neighborhood = enumerateNeighborhood(positiveCells.get(0), distanceThreshold, grid);
            return neighborhood.size();
        }
        
        // Optimization: Use memory-efficient set operations for multiple positive cells
        Set<Position> allNeighborhoodCells = new HashSet<>();
        
        for (Position positiveCell : positiveCells) {
            Set<Position> neighborhood = enumerateNeighborhood(positiveCell, distanceThreshold, grid);
            // Use addAll() for efficient set union
            allNeighborhoodCells.addAll(neighborhood);
        }
        
        return allNeighborhoodCells.size();
    }
    
    /**
     * Get all unique cells in neighborhoods of all positive cells.
     * 
     * This method returns the actual set of positions rather than just the count.
     * It implements the same optimizations as countNeighborhoodCells.
     * 
     * @param grid Grid containing positive cells
     * @param distanceThreshold Maximum Manhattan distance
     * @return Set of all unique positions in neighborhoods
     * @throws InvalidDistanceThresholdException If distanceThreshold is negative
     */
    public Set<Position> getNeighborhoodCells(Grid grid, int distanceThreshold) {
        if (distanceThreshold < 0) {
            throw new InvalidDistanceThresholdException(distanceThreshold);
        }
        
        List<Position> positiveCells = grid.getPositiveCells();
        
        // Optimization: Handle edge case - no positive cells
        if (positiveCells.isEmpty()) {
            return new HashSet<>();
        }
        
        // Optimization: Early termination - if distance threshold exceeds grid dimensions,
        // return all grid cells
        int maxPossibleDistance = (grid.getHeight() - 1) + (grid.getWidth() - 1);
        if (distanceThreshold >= maxPossibleDistance) {
            Set<Position> allCells = new HashSet<>();
            for (int row = 0; row < grid.getHeight(); row++) {
                for (int col = 0; col < grid.getWidth(); col++) {
                    allCells.add(new Position(row, col));
                }
            }
            return allCells;
        }
        
        // Optimization: Handle edge case - zero distance threshold
        if (distanceThreshold == 0) {
            return new HashSet<>(positiveCells);
        }
        
        // Optimization: For single positive cell, use direct enumeration
        if (positiveCells.size() == 1) {
            return enumerateNeighborhood(positiveCells.get(0), distanceThreshold, grid);
        }
        
        // Optimization: Use memory-efficient set operations for multiple positive cells
        Set<Position> allNeighborhoodCells = new HashSet<>();
        
        for (Position positiveCell : positiveCells) {
            Set<Position> neighborhood = enumerateNeighborhood(positiveCell, distanceThreshold, grid);
            // Use addAll() for efficient set union
            allNeighborhoodCells.addAll(neighborhood);
        }
        
        return allNeighborhoodCells;
    }
}
