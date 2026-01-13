"""Custom exception classes for grid neighborhoods validation."""


class InvalidGridDimensionsException(Exception):
    """Exception raised when grid dimensions are invalid.
    
    This exception is raised when attempting to create a grid with
    non-positive height or width values.
    """
    
    def __init__(self, height: int, width: int, message: str = None):
        """Initialize the exception with grid dimensions.
        
        Args:
            height: The invalid height value
            width: The invalid width value
            message: Optional custom error message
        """
        self.height = height
        self.width = width
        
        if message is None:
            if height <= 0 and width <= 0:
                message = f"Grid dimensions must be positive: height={height}, width={width}"
            elif height <= 0:
                message = f"Grid height must be positive: height={height}"
            else:
                message = f"Grid width must be positive: width={width}"
        
        self.message = message
        super().__init__(self.message)


class PositionOutOfBoundsException(Exception):
    """Exception raised when a position is outside grid boundaries.
    
    This exception is raised when attempting to access or validate
    a position that falls outside the valid grid coordinates.
    """
    
    def __init__(self, position, grid_height: int, grid_width: int, message: str = None):
        """Initialize the exception with position and grid information.
        
        Args:
            position: The invalid position (Position object or tuple)
            grid_height: The grid height
            grid_width: The grid width
            message: Optional custom error message
        """
        self.position = position
        self.grid_height = grid_height
        self.grid_width = grid_width
        
        if message is None:
            if hasattr(position, 'row') and hasattr(position, 'column'):
                pos_str = f"({position.row}, {position.column})"
            else:
                pos_str = str(position)
            
            message = (f"Position {pos_str} is out of bounds for grid "
                      f"{grid_height}x{grid_width}. Valid range: "
                      f"row [0, {grid_height-1}], column [0, {grid_width-1}]")
        
        self.message = message
        super().__init__(self.message)


class InvalidDistanceThresholdException(Exception):
    """Exception raised when distance threshold is invalid.
    
    This exception is raised when attempting to use a negative
    distance threshold for neighborhood calculations.
    """
    
    def __init__(self, distance_threshold: int, message: str = None):
        """Initialize the exception with the invalid distance threshold.
        
        Args:
            distance_threshold: The invalid distance threshold value
            message: Optional custom error message
        """
        self.distance_threshold = distance_threshold
        
        if message is None:
            message = (f"Distance threshold must be non-negative: "
                      f"got {distance_threshold}")
        
        self.message = message
        super().__init__(self.message)