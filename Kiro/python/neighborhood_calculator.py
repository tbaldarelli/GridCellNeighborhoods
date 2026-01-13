"""Neighborhood calculator for enumerating cells within Manhattan distance."""

from typing import Set, List
from position import Position
from grid import Grid
from boundary_handler import BoundaryHandler
from exceptions import InvalidDistanceThresholdException


class NeighborhoodCalculator:
    """Calculator for neighborhood enumeration using diamond-shaped Manhattan distance."""
    
    def __init__(self):
        """Initialize the neighborhood calculator."""
        pass
    
    def enumerate_neighborhood(self, center: Position, distance_threshold: int, grid: Grid) -> Set[Position]:
        """Enumerate all cells within Manhattan distance of a center position.
        
        Uses diamond enumeration algorithm to find all cells within the specified
        Manhattan distance threshold, respecting grid boundaries.
        
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
        
        neighborhood = set()
        
        # Diamond enumeration: for each row offset, calculate column range
        for delta_row in range(-distance_threshold, distance_threshold + 1):
            remaining_distance = distance_threshold - abs(delta_row)
            
            for delta_col in range(-remaining_distance, remaining_distance + 1):
                candidate_row = center.row + delta_row
                candidate_col = center.column + delta_col
                
                # Only add if position is valid (non-negative coordinates)
                if candidate_row >= 0 and candidate_col >= 0:
                    candidate_pos = Position(candidate_row, candidate_col)
                    
                    # Only add if within grid boundaries
                    if BoundaryHandler.is_within_bounds(candidate_pos, grid):
                        neighborhood.add(candidate_pos)
        
        return neighborhood
    
    def count_neighborhood_cells(self, grid: Grid, distance_threshold: int) -> int:
        """Count total unique cells in neighborhoods of all positive cells.
        
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
        
        # Handle edge case: no positive cells
        if not positive_cells:
            return 0
        
        # Optimization: if distance threshold exceeds grid dimensions,
        # all grid cells will be included
        max_possible_distance = (grid.height - 1) + (grid.width - 1)
        if distance_threshold >= max_possible_distance:
            return grid.height * grid.width
        
        # Handle edge case: zero distance threshold
        if distance_threshold == 0:
            return len(positive_cells)
        
        # Collect all neighborhood cells using set union
        all_neighborhood_cells = set()
        
        for positive_cell in positive_cells:
            neighborhood = self.enumerate_neighborhood(positive_cell, distance_threshold, grid)
            all_neighborhood_cells.update(neighborhood)
        
        return len(all_neighborhood_cells)
    
    def get_neighborhood_cells(self, grid: Grid, distance_threshold: int) -> Set[Position]:
        """Get all unique cells in neighborhoods of all positive cells.
        
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
        
        # Handle edge case: no positive cells
        if not positive_cells:
            return set()
        
        # Optimization: if distance threshold exceeds grid dimensions,
        # return all grid cells
        max_possible_distance = (grid.height - 1) + (grid.width - 1)
        if distance_threshold >= max_possible_distance:
            return {Position(row, col) for row in range(grid.height) for col in range(grid.width)}
        
        # Handle edge case: zero distance threshold
        if distance_threshold == 0:
            return set(positive_cells)
        
        # Collect all neighborhood cells using set union
        all_neighborhood_cells = set()
        
        for positive_cell in positive_cells:
            neighborhood = self.enumerate_neighborhood(positive_cell, distance_threshold, grid)
            all_neighborhood_cells.update(neighborhood)
        
        return all_neighborhood_cells