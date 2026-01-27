"""Position class for grid coordinates with Manhattan distance calculation."""

from typing import Tuple


class Position:
    """Represents a position in a 2D grid with row and column coordinates.
    
    The coordinate system uses (0,0) as the bottom-left corner of the grid.
    """
    
    def __init__(self, row: int, column: int):
        """Initialize a position with row and column coordinates.
        
        Args:
            row: The row coordinate (>= 0)
            column: The column coordinate (>= 0)
            
        Raises:
            ValueError: If row or column is negative (coordinates must be non-negative)
        """
        if row < 0:
            raise ValueError(f"Row must be non-negative, got {row}")
        if column < 0:
            raise ValueError(f"Column must be non-negative, got {column}")
            
        self.row = row
        self.column = column
    
    def manhattan_distance(self, other: 'Position') -> int:
        """Calculate Manhattan distance to another position.
        
        Args:
            other: Another Position instance
            
        Returns:
            The Manhattan distance as a non-negative integer
        """
        return abs(self.row - other.row) + abs(self.column - other.column)
    
    def __eq__(self, other) -> bool:
        """Check equality with another Position."""
        if not isinstance(other, Position):
            return False
        return self.row == other.row and self.column == other.column
    
    def __hash__(self) -> int:
        """Hash function for use in sets and dictionaries."""
        return hash((self.row, self.column))
    
    def __repr__(self) -> str:
        """String representation of the position."""
        return f"Position({self.row}, {self.column})"