"""Distance calculator for Manhattan distance computations."""

from position import Position


class DistanceCalculator:
    """Calculator for Manhattan distance between grid positions."""
    
    @staticmethod
    def calculate_manhattan_distance(pos1: Position, pos2: Position) -> int:
        """Calculate Manhattan distance between two positions.
        
        Args:
            pos1: First position
            pos2: Second position
            
        Returns:
            Manhattan distance as a non-negative integer
        """
        return abs(pos1.row - pos2.row) + abs(pos1.column - pos2.column)