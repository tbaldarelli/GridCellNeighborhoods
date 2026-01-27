"""Unit tests for error handling and validation in grid neighborhoods."""

import pytest
from position import Position
from grid import Grid
from neighborhood_calculator import NeighborhoodCalculator
from exceptions import (
    InvalidGridDimensionsException,
    PositionOutOfBoundsException,
    InvalidDistanceThresholdException
)


class TestInvalidGridDimensionsException:
    """Test cases for InvalidGridDimensionsException."""
    
    def test_invalid_height_zero(self):
        """Test that zero height raises InvalidGridDimensionsException."""
        with pytest.raises(InvalidGridDimensionsException) as exc_info:
            Grid(0, 5)
        
        exception = exc_info.value
        assert exception.height == 0
        assert exception.width == 5
        assert "height" in exception.message.lower()
        assert "positive" in exception.message.lower()
    
    def test_invalid_width_zero(self):
        """Test that zero width raises InvalidGridDimensionsException."""
        with pytest.raises(InvalidGridDimensionsException) as exc_info:
            Grid(5, 0)
        
        exception = exc_info.value
        assert exception.height == 5
        assert exception.width == 0
        assert "width" in exception.message.lower()
        assert "positive" in exception.message.lower()
    
    def test_invalid_height_negative(self):
        """Test that negative height raises InvalidGridDimensionsException."""
        with pytest.raises(InvalidGridDimensionsException) as exc_info:
            Grid(-3, 5)
        
        exception = exc_info.value
        assert exception.height == -3
        assert exception.width == 5
        assert "height" in exception.message.lower()
        assert "positive" in exception.message.lower()
    
    def test_invalid_width_negative(self):
        """Test that negative width raises InvalidGridDimensionsException."""
        with pytest.raises(InvalidGridDimensionsException) as exc_info:
            Grid(5, -2)
        
        exception = exc_info.value
        assert exception.height == 5
        assert exception.width == -2
        assert "width" in exception.message.lower()
        assert "positive" in exception.message.lower()
    
    def test_both_dimensions_invalid(self):
        """Test that both invalid dimensions are reported in the message."""
        with pytest.raises(InvalidGridDimensionsException) as exc_info:
            Grid(-1, -1)
        
        exception = exc_info.value
        assert exception.height == -1
        assert exception.width == -1
        assert "height" in exception.message.lower()
        assert "width" in exception.message.lower()
        assert "positive" in exception.message.lower()
    
    def test_custom_message(self):
        """Test InvalidGridDimensionsException with custom message."""
        custom_message = "Custom error message for testing"
        
        # We can't directly test this since Grid constructor doesn't accept custom messages,
        # but we can test the exception class directly
        exception = InvalidGridDimensionsException(-1, -1, custom_message)
        assert exception.message == custom_message
        assert str(exception) == custom_message
    
    def test_valid_dimensions_no_exception(self):
        """Test that valid dimensions don't raise exceptions."""
        # These should not raise any exceptions
        grid1 = Grid(1, 1)
        assert grid1.height == 1
        assert grid1.width == 1
        
        grid2 = Grid(10, 20)
        assert grid2.height == 10
        assert grid2.width == 20
        
        grid3 = Grid(100, 1)
        assert grid3.height == 100
        assert grid3.width == 1


class TestPositionOutOfBoundsException:
    """Test cases for PositionOutOfBoundsException."""
    
    def test_position_row_too_high(self):
        """Test that position with row >= height raises PositionOutOfBoundsException."""
        grid = Grid(3, 3)
        out_of_bounds_pos = Position(3, 1)  # Row 3 is out of bounds for height 3
        
        with pytest.raises(PositionOutOfBoundsException) as exc_info:
            grid.get_cell_value(out_of_bounds_pos)
        
        exception = exc_info.value
        assert exception.position == out_of_bounds_pos
        assert exception.grid_height == 3
        assert exception.grid_width == 3
        assert "(3, 1)" in exception.message
        assert "3x3" in exception.message
        assert "out of bounds" in exception.message.lower()
    
    def test_position_column_too_high(self):
        """Test that position with column >= width raises PositionOutOfBoundsException."""
        grid = Grid(3, 3)
        out_of_bounds_pos = Position(1, 3)  # Column 3 is out of bounds for width 3
        
        with pytest.raises(PositionOutOfBoundsException) as exc_info:
            grid.set_cell_value(out_of_bounds_pos, 5)
        
        exception = exc_info.value
        assert exception.position == out_of_bounds_pos
        assert exception.grid_height == 3
        assert exception.grid_width == 3
        assert "(1, 3)" in exception.message
        assert "3x3" in exception.message
        assert "out of bounds" in exception.message.lower()
    
    def test_position_both_coordinates_too_high(self):
        """Test that position with both coordinates out of bounds raises PositionOutOfBoundsException."""
        grid = Grid(2, 2)
        out_of_bounds_pos = Position(5, 5)
        
        with pytest.raises(PositionOutOfBoundsException) as exc_info:
            grid.get_cell_value(out_of_bounds_pos)
        
        exception = exc_info.value
        assert exception.position == out_of_bounds_pos
        assert exception.grid_height == 2
        assert exception.grid_width == 2
        assert "(5, 5)" in exception.message
        assert "2x2" in exception.message
    
    def test_valid_range_description(self):
        """Test that exception message includes valid range description."""
        grid = Grid(5, 7)
        out_of_bounds_pos = Position(5, 0)  # Row 5 is out of bounds for height 5
        
        with pytest.raises(PositionOutOfBoundsException) as exc_info:
            grid.get_cell_value(out_of_bounds_pos)
        
        exception = exc_info.value
        assert "row [0, 4]" in exception.message  # Valid row range
        assert "column [0, 6]" in exception.message  # Valid column range
    
    def test_custom_message(self):
        """Test PositionOutOfBoundsException with custom message."""
        custom_message = "Custom position error message"
        pos = Position(1, 1)
        
        exception = PositionOutOfBoundsException(pos, 3, 3, custom_message)
        assert exception.message == custom_message
        assert str(exception) == custom_message
    
    def test_valid_positions_no_exception(self):
        """Test that valid positions don't raise exceptions."""
        grid = Grid(3, 3)
        
        # These should not raise any exceptions
        valid_positions = [
            Position(0, 0),  # Bottom-left corner
            Position(2, 2),  # Top-right corner
            Position(1, 1),  # Center
            Position(0, 2),  # Bottom-right corner
            Position(2, 0),  # Top-left corner
        ]
        
        for pos in valid_positions:
            # Should not raise exceptions
            value = grid.get_cell_value(pos)
            assert value == 0  # Default value
            
            grid.set_cell_value(pos, 42)
            assert grid.get_cell_value(pos) == 42


class TestInvalidDistanceThresholdException:
    """Test cases for InvalidDistanceThresholdException."""
    
    def test_negative_distance_threshold_enumerate_neighborhood(self):
        """Test that negative distance threshold raises InvalidDistanceThresholdException in enumerate_neighborhood."""
        grid = Grid(5, 5)
        center = Position(2, 2)
        calculator = NeighborhoodCalculator()
        
        with pytest.raises(InvalidDistanceThresholdException) as exc_info:
            calculator.enumerate_neighborhood(center, -1, grid)
        
        exception = exc_info.value
        assert exception.distance_threshold == -1
        assert "non-negative" in exception.message.lower()
        assert "-1" in exception.message
    
    def test_negative_distance_threshold_count_neighborhood_cells(self):
        """Test that negative distance threshold raises InvalidDistanceThresholdException in count_neighborhood_cells."""
        grid = Grid(3, 3)
        grid.set_cell_value(Position(1, 1), 1)  # Add a positive cell
        calculator = NeighborhoodCalculator()
        
        with pytest.raises(InvalidDistanceThresholdException) as exc_info:
            calculator.count_neighborhood_cells(grid, -5)
        
        exception = exc_info.value
        assert exception.distance_threshold == -5
        assert "non-negative" in exception.message.lower()
        assert "-5" in exception.message
    
    def test_negative_distance_threshold_get_neighborhood_cells(self):
        """Test that negative distance threshold raises InvalidDistanceThresholdException in get_neighborhood_cells."""
        grid = Grid(3, 3)
        grid.set_cell_value(Position(0, 0), 1)  # Add a positive cell
        calculator = NeighborhoodCalculator()
        
        with pytest.raises(InvalidDistanceThresholdException) as exc_info:
            calculator.get_neighborhood_cells(grid, -10)
        
        exception = exc_info.value
        assert exception.distance_threshold == -10
        assert "non-negative" in exception.message.lower()
        assert "-10" in exception.message
    
    def test_zero_distance_threshold_valid(self):
        """Test that zero distance threshold is valid and doesn't raise exceptions."""
        grid = Grid(3, 3)
        grid.set_cell_value(Position(1, 1), 1)  # Add a positive cell
        calculator = NeighborhoodCalculator()
        
        # These should not raise any exceptions
        neighborhood = calculator.enumerate_neighborhood(Position(1, 1), 0, grid)
        assert len(neighborhood) == 1
        assert Position(1, 1) in neighborhood
        
        count = calculator.count_neighborhood_cells(grid, 0)
        assert count == 1
        
        cells = calculator.get_neighborhood_cells(grid, 0)
        assert len(cells) == 1
        assert Position(1, 1) in cells
    
    def test_positive_distance_threshold_valid(self):
        """Test that positive distance thresholds are valid and don't raise exceptions."""
        grid = Grid(5, 5)
        grid.set_cell_value(Position(2, 2), 1)  # Add a positive cell
        calculator = NeighborhoodCalculator()
        
        # These should not raise any exceptions
        for threshold in [1, 2, 5, 10, 100]:
            neighborhood = calculator.enumerate_neighborhood(Position(2, 2), threshold, grid)
            assert len(neighborhood) >= 1  # At least the center cell
            
            count = calculator.count_neighborhood_cells(grid, threshold)
            assert count >= 1
            
            cells = calculator.get_neighborhood_cells(grid, threshold)
            assert len(cells) >= 1
    
    def test_custom_message(self):
        """Test InvalidDistanceThresholdException with custom message."""
        custom_message = "Custom distance threshold error message"
        
        exception = InvalidDistanceThresholdException(-5, custom_message)
        assert exception.message == custom_message
        assert str(exception) == custom_message


class TestPositionValidation:
    """Test cases for Position coordinate validation."""
    
    def test_negative_row_position(self):
        """Test that negative row raises ValueError in Position constructor."""
        with pytest.raises(ValueError) as exc_info:
            Position(-1, 5)
        
        assert "row" in str(exc_info.value).lower()
        assert "non-negative" in str(exc_info.value).lower()
        assert "-1" in str(exc_info.value)
    
    def test_negative_column_position(self):
        """Test that negative column raises ValueError in Position constructor."""
        with pytest.raises(ValueError) as exc_info:
            Position(5, -2)
        
        assert "column" in str(exc_info.value).lower()
        assert "non-negative" in str(exc_info.value).lower()
        assert "-2" in str(exc_info.value)
    
    def test_both_negative_coordinates(self):
        """Test that both negative coordinates raise ValueError."""
        with pytest.raises(ValueError) as exc_info:
            Position(-3, -4)
        
        # Should fail on the first check (row)
        assert "row" in str(exc_info.value).lower()
        assert "-3" in str(exc_info.value)
    
    def test_valid_coordinates_no_exception(self):
        """Test that valid coordinates don't raise exceptions."""
        # These should not raise any exceptions
        valid_positions = [
            Position(0, 0),
            Position(1, 0),
            Position(0, 1),
            Position(10, 20),
            Position(100, 100),
        ]
        
        for pos in valid_positions:
            assert pos.row >= 0
            assert pos.column >= 0


class TestErrorMessageQuality:
    """Test cases to ensure error messages are descriptive and helpful."""
    
    def test_grid_dimension_error_messages_are_descriptive(self):
        """Test that grid dimension error messages provide clear guidance."""
        test_cases = [
            (0, 5, ["height", "positive"]),
            (5, 0, ["width", "positive"]),
            (-1, 5, ["height", "positive"]),
            (5, -2, ["width", "positive"]),
            (-1, -1, ["height", "width", "positive"]),
        ]
        
        for height, width, expected_keywords in test_cases:
            with pytest.raises(InvalidGridDimensionsException) as exc_info:
                Grid(height, width)
            
            message = exc_info.value.message.lower()
            for keyword in expected_keywords:
                assert keyword in message, f"Expected '{keyword}' in message: {message}"
    
    def test_position_error_messages_include_valid_ranges(self):
        """Test that position error messages include valid coordinate ranges."""
        grid = Grid(3, 5)  # 3 rows, 5 columns
        
        test_cases = [
            Position(3, 2),  # Row out of bounds
            Position(1, 5),  # Column out of bounds
            Position(10, 10),  # Both out of bounds
        ]
        
        for pos in test_cases:
            with pytest.raises(PositionOutOfBoundsException) as exc_info:
                grid.get_cell_value(pos)
            
            message = exc_info.value.message
            assert "3x5" in message  # Grid dimensions
            assert "row [0, 2]" in message  # Valid row range
            assert "column [0, 4]" in message  # Valid column range
            assert f"({pos.row}, {pos.column})" in message  # Invalid position
    
    def test_distance_threshold_error_messages_are_clear(self):
        """Test that distance threshold error messages are clear and actionable."""
        grid = Grid(3, 3)
        calculator = NeighborhoodCalculator()
        
        test_cases = [-1, -5, -100]
        
        for threshold in test_cases:
            with pytest.raises(InvalidDistanceThresholdException) as exc_info:
                calculator.count_neighborhood_cells(grid, threshold)
            
            message = exc_info.value.message.lower()
            assert "non-negative" in message
            assert str(threshold) in message
            assert "distance threshold" in message
    
    def test_position_coordinate_error_messages_are_specific(self):
        """Test that position coordinate error messages specify which coordinate is invalid."""
        # Test negative row
        with pytest.raises(ValueError) as exc_info:
            Position(-5, 10)
        
        message = str(exc_info.value).lower()
        assert "row" in message
        assert "non-negative" in message
        assert "-5" in message
        
        # Test negative column
        with pytest.raises(ValueError) as exc_info:
            Position(10, -3)
        
        message = str(exc_info.value).lower()
        assert "column" in message
        assert "non-negative" in message
        assert "-3" in message


class TestExceptionInheritance:
    """Test cases to verify custom exceptions inherit from Exception properly."""
    
    def test_invalid_grid_dimensions_exception_inheritance(self):
        """Test that InvalidGridDimensionsException inherits from Exception."""
        exception = InvalidGridDimensionsException(-1, -1)
        assert isinstance(exception, Exception)
        assert isinstance(exception, InvalidGridDimensionsException)
    
    def test_position_out_of_bounds_exception_inheritance(self):
        """Test that PositionOutOfBoundsException inherits from Exception."""
        pos = Position(0, 0)
        exception = PositionOutOfBoundsException(pos, 1, 1)
        assert isinstance(exception, Exception)
        assert isinstance(exception, PositionOutOfBoundsException)
    
    def test_invalid_distance_threshold_exception_inheritance(self):
        """Test that InvalidDistanceThresholdException inherits from Exception."""
        exception = InvalidDistanceThresholdException(-1)
        assert isinstance(exception, Exception)
        assert isinstance(exception, InvalidDistanceThresholdException)