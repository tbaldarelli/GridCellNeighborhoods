"""Neighborhood calculator for enumerating cells within Manhattan distance."""

from typing import Set, List
from position import Position
from grid import Grid
from boundary_handler import BoundaryHandler
from exceptions import InvalidDistanceThresholdException


class NeighborhoodCalculator:
    """Calculator for neighborhood enumeration using diamond-shaped Manhattan distance.
    
    This class provides optimized algorithms for calculating neighborhoods of positive
    cells in a grid using Manhattan distance. It includes several performance optimizations:
    
    - Early termination when distance threshold exceeds grid dimensions
    - Memory-efficient set operations for large neighborhoods
    - Boundary-aware enumeration to avoid unnecessary calculations
    - Special handling for edge cases (zero distance, no positive cells)
    """
    
    def __init__(self):
        """Initialize the neighborhood calculator."""
        pass
    
    def enumerate_neighborhood(self, center: Position, distance_threshold: int, grid: Grid) -> Set[Position]:
        """Enumerate all cells within Manhattan distance of a center position.
        
        Uses optimized diamond enumeration algorithm to find all cells within the specified
        Manhattan distance threshold, respecting grid boundaries.
        
        Optimizations:
        - Boundary-aware iteration to skip out-of-bounds calculations
        - Early row/column range clamping to grid dimensions
        - Memory-efficient set construction
        
        Args:
            center: Center position for the neighborhood
            distance_threshold: Maximum Manhattan distance (N >= 0)
            grid: Grid to check boundaries against
            
        Returns:
            Set of positions within the neighborhood
            
        Raises:
            InvalidDistanceThresholdException: If distance_threshold is negative
        """
        if distance_threshold < 0:
            raise InvalidDistanceThresholdException(distance_threshold)
        
        # Optimization: Calculate actual row range considering grid boundaries
        min_row = max(0, center.row - distance_threshold)
        max_row = min(grid.height - 1, center.row + distance_threshold)
        
        neighborhood = set()
        
        # Diamond enumeration: for each row offset, calculate column range
        for row in range(min_row, max_row + 1):
            delta_row = row - center.row
            remaining_distance = distance_threshold - abs(delta_row)
            
            # Optimization: Calculate actual column range considering grid boundaries
            min_col = max(0, center.column - remaining_distance)
            max_col = min(grid.width - 1, center.column + remaining_distance)
            
            # Add all valid columns in this row
            for col in range(min_col, max_col + 1):
                neighborhood.add(Position(row, col))
        
        return neighborhood
    
    def count_neighborhood_cells(self, grid: Grid, distance_threshold: int) -> int:
        """Count total unique cells in neighborhoods of all positive cells.
        
        This method implements several performance optimizations:
        - Early termination when distance threshold exceeds grid dimensions
        - Zero distance threshold optimization (returns count of positive cells)
        - Empty grid handling (returns 0 immediately)
        - Memory-efficient set operations for large neighborhoods
        
        Args:
            grid: Grid containing positive cells
            distance_threshold: Maximum Manhattan distance
            
        Returns:
            Total count of unique cells in all neighborhoods
            
        Raises:
            InvalidDistanceThresholdException: If distance_threshold is negative
        """
        if distance_threshold < 0:
            raise InvalidDistanceThresholdException(distance_threshold)
        
        positive_cells = grid.get_positive_cells()
        
        # Optimization: Handle edge case - no positive cells
        if not positive_cells:
            return 0
        
        # Optimization: Early termination - if distance threshold exceeds grid dimensions,
        # all grid cells will be included (when at least one positive cell exists)
        max_possible_distance = (grid.height - 1) + (grid.width - 1)
        if distance_threshold >= max_possible_distance:
            return grid.height * grid.width
        
        # Optimization: Handle edge case - zero distance threshold
        # Only positive cells themselves are counted
        if distance_threshold == 0:
            return len(positive_cells)
        
        # Optimization: For single positive cell, use direct enumeration
        if len(positive_cells) == 1:
            neighborhood = self.enumerate_neighborhood(positive_cells[0], distance_threshold, grid)
            return len(neighborhood)
        
        # Optimization: Use memory-efficient set operations for multiple positive cells
        # Pre-allocate with estimated size based on first neighborhood
        all_neighborhood_cells = set()
        
        for positive_cell in positive_cells:
            neighborhood = self.enumerate_neighborhood(positive_cell, distance_threshold, grid)
            # Use update() for efficient set union
            all_neighborhood_cells.update(neighborhood)
        
        return len(all_neighborhood_cells)
    
    def get_neighborhood_cells(self, grid: Grid, distance_threshold: int) -> Set[Position]:
        """Get all unique cells in neighborhoods of all positive cells.
        
        This method returns the actual set of positions rather than just the count.
        It implements the same optimizations as count_neighborhood_cells.
        
        Args:
            grid: Grid containing positive cells
            distance_threshold: Maximum Manhattan distance
            
        Returns:
            Set of all unique positions in neighborhoods
            
        Raises:
            InvalidDistanceThresholdException: If distance_threshold is negative
        """
        if distance_threshold < 0:
            raise InvalidDistanceThresholdException(distance_threshold)
        
        positive_cells = grid.get_positive_cells()
        
        # Optimization: Handle edge case - no positive cells
        if not positive_cells:
            return set()
        
        # Optimization: Early termination - if distance threshold exceeds grid dimensions,
        # return all grid cells
        max_possible_distance = (grid.height - 1) + (grid.width - 1)
        if distance_threshold >= max_possible_distance:
            return {Position(row, col) for row in range(grid.height) for col in range(grid.width)}
        
        # Optimization: Handle edge case - zero distance threshold
        if distance_threshold == 0:
            return set(positive_cells)
        
        # Optimization: For single positive cell, use direct enumeration
        if len(positive_cells) == 1:
            return self.enumerate_neighborhood(positive_cells[0], distance_threshold, grid)
        
        # Optimization: Use memory-efficient set operations for multiple positive cells
        all_neighborhood_cells = set()
        
        for positive_cell in positive_cells:
            neighborhood = self.enumerate_neighborhood(positive_cell, distance_threshold, grid)
            # Use update() for efficient set union
            all_neighborhood_cells.update(neighborhood)
        
        return all_neighborhood_cells