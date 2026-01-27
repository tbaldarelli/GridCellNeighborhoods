"""Boundary handler for grid boundary validation."""

from typing import Set
from position import Position
from grid import Grid


class BoundaryHandler:
    """Handler for grid boundary validation and position filtering."""
    
    @staticmethod
    def is_within_bounds(position: Position, grid: Grid) -> bool:
        """Check if a position is within grid boundaries.
        
        Args:
            position: Position to validate
            grid: Grid to check against
            
        Returns:
            True if position is within grid bounds, False otherwise
        """
        return (0 <= position.row < grid.height and 
                0 <= position.column < grid.width)
    
    @staticmethod
    def filter_valid_positions(positions: Set[Position], grid: Grid) -> Set[Position]:
        """Filter a set of positions to only include those within grid boundaries.
        
        Args:
            positions: Set of positions to filter
            grid: Grid to check against
            
        Returns:
            Set of positions that are within grid boundaries
        """
        return {pos for pos in positions if BoundaryHandler.is_within_bounds(pos, grid)}