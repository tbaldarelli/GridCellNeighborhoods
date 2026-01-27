"""Grid class for storing 2D grid data and positive cell positions."""

from typing import List, Set
from position import Position
from exceptions import InvalidGridDimensionsException, PositionOutOfBoundsException


class Grid:
    """Represents a 2D grid with height, width, and positive cell storage.
    
    The grid uses (0,0) as the bottom-left corner coordinate system.
    """
    
    def __init__(self, height: int, width: int, cells: List[List[int]] = None):
        """Initialize a grid with specified dimensions.
        
        Args:
            height: Grid height (must be > 0)
            width: Grid width (must be > 0)
            cells: Optional 2D array of cell values. If not provided, creates empty grid.
                  Expected format: cells[row][column] where row 0 is bottom of grid.
                  
        Raises:
            InvalidGridDimensionsException: If height <= 0 or width <= 0
            ValueError: If cells dimensions don't match grid dimensions
        """
        if height <= 0 or width <= 0:
            raise InvalidGridDimensionsException(height, width)
            
        self.height = height
        self.width = width
        
        if cells is None:
            # Create empty grid (all zeros)
            self.cells = [[0 for _ in range(width)] for _ in range(height)]
        else:
            # Validate provided cells
            if len(cells) != height:
                raise ValueError(f"Cells height {len(cells)} doesn't match grid height {height}")
            for i, row in enumerate(cells):
                if len(row) != width:
                    raise ValueError(f"Cells row {i} width {len(row)} doesn't match grid width {width}")
            self.cells = [row[:] for row in cells]  # Deep copy
    
    def get_positive_cells(self) -> List[Position]:
        """Get all positions containing positive values (> 0).
        
        Returns:
            List of Position objects for cells with values > 0
        """
        positive_cells = []
        for row in range(self.height):
            for col in range(self.width):
                if self.cells[row][col] > 0:
                    positive_cells.append(Position(row, col))
        return positive_cells
    
    def is_valid_position(self, position: Position) -> bool:
        """Check if a position is within grid boundaries.
        
        Args:
            position: Position to validate
            
        Returns:
            True if position is within grid bounds, False otherwise
        """
        return (0 <= position.row < self.height and 
                0 <= position.column < self.width)
    
    def get_cell_value(self, position: Position) -> int:
        """Get the value at a specific position.
        
        Args:
            position: Position to query
            
        Returns:
            The cell value at the position
            
        Raises:
            PositionOutOfBoundsException: If position is out of bounds
        """
        if not self.is_valid_position(position):
            raise PositionOutOfBoundsException(position, self.height, self.width)
        return self.cells[position.row][position.column]
    
    def set_cell_value(self, position: Position, value: int) -> None:
        """Set the value at a specific position.
        
        Args:
            position: Position to set
            value: Value to set
            
        Raises:
            PositionOutOfBoundsException: If position is out of bounds
        """
        if not self.is_valid_position(position):
            raise PositionOutOfBoundsException(position, self.height, self.width)
        self.cells[position.row][position.column] = value
    
    def __repr__(self) -> str:
        """String representation of the grid."""
        return f"Grid({self.height}x{self.width})"