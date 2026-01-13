"""Property-based tests for grid neighborhoods core components."""

import pytest
from hypothesis import given, strategies as st, assume
from position import Position
from grid import Grid
from boundary_handler import BoundaryHandler
from neighborhood_calculator import NeighborhoodCalculator


class TestPositionProperties:
    """Property-based tests for Position class."""
    
    @given(
        row1=st.integers(min_value=0, max_value=1000),
        col1=st.integers(min_value=0, max_value=1000),
        row2=st.integers(min_value=0, max_value=1000),
        col2=st.integers(min_value=0, max_value=1000)
    )
    def test_manhattan_distance_calculation(self, row1, col1, row2, col2):
        """Property 2: Manhattan Distance Calculation
        
        For any two positions in a coordinate system, the Manhattan distance should 
        equal |row1 - row2| + |column1 - column2|, always return a non-negative 
        integer, and return 0 when both positions are identical.
        
        **Feature: grid-neighborhoods, Property 2: Manhattan Distance Calculation**
        **Validates: Requirements 2.1, 2.2, 2.3**
        """
        pos1 = Position(row1, col1)
        pos2 = Position(row2, col2)
        
        distance = pos1.manhattan_distance(pos2)
        expected_distance = abs(row1 - row2) + abs(col1 - col2)
        
        # Distance should equal the Manhattan formula
        assert distance == expected_distance
        
        # Distance should always be non-negative
        assert distance >= 0
        
        # Distance should be 0 when positions are identical
        if row1 == row2 and col1 == col2:
            assert distance == 0
        
        # Distance should be symmetric
        assert pos1.manhattan_distance(pos2) == pos2.manhattan_distance(pos1)


class TestGridProperties:
    """Property-based tests for Grid class."""
    
    @given(
        height=st.integers(min_value=-100, max_value=1000),
        width=st.integers(min_value=-100, max_value=1000)
    )
    def test_grid_validation(self, height, width):
        """Property 1: Grid Validation
        
        For any height and width values, grid creation should succeed if and only if 
        both height > 0 and width > 0, and all specified positive cell positions 
        should be within the resulting grid boundaries.
        
        **Feature: grid-neighborhoods, Property 1: Grid Validation**
        **Validates: Requirements 1.1, 1.2**
        """
        if height > 0 and width > 0:
            # Valid dimensions should create a grid successfully
            grid = Grid(height, width)
            assert grid.height == height
            assert grid.width == width
            assert len(grid.cells) == height
            for row in grid.cells:
                assert len(row) == width
        else:
            # Invalid dimensions should raise ValueError
            with pytest.raises(ValueError):
                Grid(height, width)
    
    @given(
        height=st.integers(min_value=1, max_value=100),
        width=st.integers(min_value=1, max_value=100),
        positive_positions=st.lists(
            st.tuples(
                st.integers(min_value=0, max_value=99),
                st.integers(min_value=0, max_value=99)
            ),
            max_size=20
        )
    )
    def test_coordinate_system_consistency(self, height, width, positive_positions):
        """Property 3: Coordinate System Consistency
        
        For any grid dimensions, position (0,0) should consistently represent the 
        bottom-left corner, and stored positive cell positions should be retrievable 
        for neighborhood calculations.
        
        **Feature: grid-neighborhoods, Property 3: Coordinate System Consistency**
        **Validates: Requirements 1.3, 1.4**
        """
        grid = Grid(height, width)
        
        # Filter positions to be within grid bounds
        valid_positions = [
            (row, col) for row, col in positive_positions 
            if 0 <= row < height and 0 <= col < width
        ]
        
        # Set positive values at valid positions
        for row, col in valid_positions:
            pos = Position(row, col)
            grid.set_cell_value(pos, 1)  # Set to positive value
        
        # Retrieve positive cells
        retrieved_positive_cells = grid.get_positive_cells()
        
        # Convert to sets for comparison
        expected_positions = {Position(row, col) for row, col in valid_positions}
        retrieved_positions = set(retrieved_positive_cells)
        
        # All set positive positions should be retrievable
        assert retrieved_positions == expected_positions
        
        # Position (0,0) should be valid for any grid
        bottom_left = Position(0, 0)
        assert grid.is_valid_position(bottom_left)
        
        # Position (height-1, width-1) should be valid (top-right corner)
        top_right = Position(height - 1, width - 1)
        assert grid.is_valid_position(top_right)
        
        # Positions outside bounds should be invalid
        if height < 1000:  # Avoid overflow
            out_of_bounds = Position(height, 0)
            assert not grid.is_valid_position(out_of_bounds)
        
        if width < 1000:  # Avoid overflow
            out_of_bounds = Position(0, width)
            assert not grid.is_valid_position(out_of_bounds)


class TestBoundaryHandlerProperties:
    """Property-based tests for BoundaryHandler class."""
    
    @given(
        height=st.integers(min_value=1, max_value=100),
        width=st.integers(min_value=1, max_value=100),
        positions=st.lists(
            st.tuples(
                st.integers(min_value=-50, max_value=150),
                st.integers(min_value=-50, max_value=150)
            ),
            max_size=50
        )
    )
    def test_boundary_constraint_enforcement(self, height, width, positions):
        """Property 6: Boundary Constraint Enforcement
        
        For any positive cell and distance threshold, the neighborhood count should 
        exclude all cells that would fall outside the grid boundaries, with no 
        wraparound behavior.
        
        **Feature: grid-neighborhoods, Property 6: Boundary Constraint Enforcement**
        **Validates: Requirements 3.3, 6.1, 6.2, 6.3**
        """
        grid = Grid(height, width)
        position_set = {Position(row, col) for row, col in positions if row >= 0 and col >= 0}
        
        # Filter positions using boundary handler
        valid_positions = BoundaryHandler.filter_valid_positions(position_set, grid)
        
        # All valid positions should be within bounds
        for pos in valid_positions:
            assert BoundaryHandler.is_within_bounds(pos, grid)
            assert 0 <= pos.row < height
            assert 0 <= pos.column < width
        
        # No position outside bounds should be in valid set
        for pos in position_set:
            if not (0 <= pos.row < height and 0 <= pos.column < width):
                assert pos not in valid_positions
        
        # Valid positions should match grid's validation
        for pos in position_set:
            boundary_valid = BoundaryHandler.is_within_bounds(pos, grid)
            grid_valid = grid.is_valid_position(pos)
            assert boundary_valid == grid_valid
        
        # No wraparound behavior - positions outside bounds stay outside
        for row, col in positions:
            if row >= 0 and col >= 0:  # Only test non-negative positions
                pos = Position(row, col)
                is_valid = BoundaryHandler.is_within_bounds(pos, grid)
                
                # Position should be valid iff it's within bounds
                expected_valid = (0 <= row < height and 0 <= col < width)
                assert is_valid == expected_valid


class TestNeighborhoodCalculatorProperties:
    """Property-based tests for NeighborhoodCalculator class."""
    
    @given(
        height=st.integers(min_value=1, max_value=50),
        width=st.integers(min_value=1, max_value=50),
        positive_row=st.integers(min_value=0, max_value=49),
        positive_col=st.integers(min_value=0, max_value=49),
        distance_threshold=st.integers(min_value=0, max_value=100)
    )
    def test_self_inclusion_in_neighborhoods(self, height, width, positive_row, positive_col, distance_threshold):
        """Property 4: Self-Inclusion in Neighborhoods
        
        For any positive cell at any valid position, that cell should always be 
        included in its own neighborhood count regardless of distance threshold 
        (when N >= 0).
        
        **Feature: grid-neighborhoods, Property 4: Self-Inclusion in Neighborhoods**
        **Validates: Requirements 3.1**
        """
        # Ensure positive cell is within grid bounds
        assume(positive_row < height and positive_col < width)
        
        grid = Grid(height, width)
        positive_pos = Position(positive_row, positive_col)
        grid.set_cell_value(positive_pos, 1)  # Set as positive cell
        
        calculator = NeighborhoodCalculator()
        
        # Get neighborhood cells for this positive cell
        neighborhood = calculator.enumerate_neighborhood(positive_pos, distance_threshold, grid)
        
        # The positive cell should always be included in its own neighborhood
        assert positive_pos in neighborhood
        
        # Also test via the main counting method
        total_count = calculator.count_neighborhood_cells(grid, distance_threshold)
        assert total_count >= 1  # At least the positive cell itself
        
        # Get all neighborhood cells and verify positive cell is included
        all_cells = calculator.get_neighborhood_cells(grid, distance_threshold)
        assert positive_pos in all_cells
    
    @given(
        height=st.integers(min_value=3, max_value=20),
        width=st.integers(min_value=3, max_value=20),
        distance_threshold=st.integers(min_value=1, max_value=10)
    )
    def test_complete_neighborhood_enumeration(self, height, width, distance_threshold):
        """Property 5: Complete Neighborhood Enumeration
        
        For any positive cell positioned away from grid boundaries, the neighborhood 
        should include all cells within N Manhattan steps when the full diamond 
        fits within the grid.
        
        **Feature: grid-neighborhoods, Property 5: Complete Neighborhood Enumeration**
        **Validates: Requirements 3.2**
        """
        # Place positive cell away from boundaries so full diamond fits
        center_row = distance_threshold + 1
        center_col = distance_threshold + 1
        
        # Ensure the full diamond fits within the grid
        assume(center_row + distance_threshold < height)
        assume(center_col + distance_threshold < width)
        assume(center_row - distance_threshold >= 0)
        assume(center_col - distance_threshold >= 0)
        
        grid = Grid(height, width)
        center_pos = Position(center_row, center_col)
        grid.set_cell_value(center_pos, 1)  # Set as positive cell
        
        calculator = NeighborhoodCalculator()
        neighborhood = calculator.enumerate_neighborhood(center_pos, distance_threshold, grid)
        
        # Calculate expected neighborhood size for a complete diamond
        # Diamond size formula: 1 + 4 + 8 + ... + 4*N = (N+1)^2 + N^2
        expected_size = (distance_threshold + 1) ** 2 + distance_threshold ** 2
        
        # Verify we got the expected complete diamond
        assert len(neighborhood) == expected_size
        
        # Verify all cells in the diamond are present
        for delta_row in range(-distance_threshold, distance_threshold + 1):
            remaining_distance = distance_threshold - abs(delta_row)
            for delta_col in range(-remaining_distance, remaining_distance + 1):
                expected_pos = Position(center_row + delta_row, center_col + delta_col)
                assert expected_pos in neighborhood
    
    @given(
        height=st.integers(min_value=1, max_value=30),
        width=st.integers(min_value=1, max_value=30),
        positive_positions=st.lists(
            st.tuples(
                st.integers(min_value=0, max_value=29),
                st.integers(min_value=0, max_value=29)
            ),
            min_size=1,
            max_size=10,
            unique=True
        ),
        distance_threshold=st.integers(min_value=0, max_value=20)
    )
    def test_cell_uniqueness_guarantee(self, height, width, positive_positions, distance_threshold):
        """Property 7: Cell Uniqueness Guarantee
        
        For any grid configuration with positive cells, each cell should be counted 
        at most once in the total neighborhood count, regardless of how many positive 
        cell neighborhoods it falls within.
        
        **Feature: grid-neighborhoods, Property 7: Cell Uniqueness Guarantee**
        **Validates: Requirements 3.4, 4.2, 5.1**
        """
        # Filter positions to be within grid bounds
        valid_positions = [
            (row, col) for row, col in positive_positions 
            if row < height and col < width
        ]
        assume(len(valid_positions) > 0)  # Need at least one positive cell
        
        grid = Grid(height, width)
        
        # Set positive values at valid positions
        for row, col in valid_positions:
            pos = Position(row, col)
            grid.set_cell_value(pos, 1)
        
        calculator = NeighborhoodCalculator()
        
        # Get all neighborhood cells
        all_neighborhood_cells = calculator.get_neighborhood_cells(grid, distance_threshold)
        total_count = calculator.count_neighborhood_cells(grid, distance_threshold)
        
        # The count should equal the size of the set (no duplicates)
        assert total_count == len(all_neighborhood_cells)
        
        # Calculate individual neighborhoods and their union
        individual_neighborhoods = []
        for row, col in valid_positions:
            pos = Position(row, col)
            neighborhood = calculator.enumerate_neighborhood(pos, distance_threshold, grid)
            individual_neighborhoods.append(neighborhood)
        
        # Union of all individual neighborhoods
        union_of_neighborhoods = set()
        for neighborhood in individual_neighborhoods:
            union_of_neighborhoods.update(neighborhood)
        
        # The result should be the same as the union
        assert all_neighborhood_cells == union_of_neighborhoods
        assert total_count == len(union_of_neighborhoods)
        
        # Total count should be <= sum of individual counts (due to potential overlaps)
        sum_of_individual_counts = sum(len(neighborhood) for neighborhood in individual_neighborhoods)
        assert total_count <= sum_of_individual_counts
        
        # Each cell in the result should be unique
        cell_list = list(all_neighborhood_cells)
        assert len(cell_list) == len(set(cell_list))  # No duplicates
    
    @given(
        height=st.integers(min_value=5, max_value=50),
        width=st.integers(min_value=5, max_value=50),
        distance_threshold=st.integers(min_value=1, max_value=10)
    )
    def test_non_overlapping_additivity(self, height, width, distance_threshold):
        """Property 8: Non-Overlapping Additivity
        
        For any set of positive cells whose neighborhoods do not overlap, the total 
        neighborhood count should equal the sum of individual neighborhood counts.
        
        **Feature: grid-neighborhoods, Property 8: Non-Overlapping Additivity**
        **Validates: Requirements 4.1, 4.3**
        """
        # Create two positive cells far enough apart that their neighborhoods don't overlap
        # Minimum separation needed: 2 * distance_threshold + 1
        min_separation = 2 * distance_threshold + 1
        
        # Ensure we have enough space for two non-overlapping neighborhoods
        assume(height >= min_separation + 2 * distance_threshold)
        assume(width >= min_separation + 2 * distance_threshold)
        
        grid = Grid(height, width)
        
        # Place first positive cell
        pos1_row = distance_threshold
        pos1_col = distance_threshold
        pos1 = Position(pos1_row, pos1_col)
        grid.set_cell_value(pos1, 1)
        
        # Place second positive cell far enough away to ensure no overlap
        pos2_row = pos1_row + min_separation
        pos2_col = pos1_col + min_separation
        
        # Ensure second position is within bounds
        assume(pos2_row < height - distance_threshold)
        assume(pos2_col < width - distance_threshold)
        
        pos2 = Position(pos2_row, pos2_col)
        grid.set_cell_value(pos2, 1)
        
        calculator = NeighborhoodCalculator()
        
        # Calculate individual neighborhoods
        neighborhood1 = calculator.enumerate_neighborhood(pos1, distance_threshold, grid)
        neighborhood2 = calculator.enumerate_neighborhood(pos2, distance_threshold, grid)
        
        # Verify neighborhoods don't overlap
        overlap = neighborhood1.intersection(neighborhood2)
        assert len(overlap) == 0, f"Neighborhoods should not overlap, but found {len(overlap)} overlapping cells"
        
        # Calculate total neighborhood count
        total_count = calculator.count_neighborhood_cells(grid, distance_threshold)
        
        # For non-overlapping neighborhoods, total should equal sum of individual counts
        expected_count = len(neighborhood1) + len(neighborhood2)
        assert total_count == expected_count
        
        # Verify using get_neighborhood_cells as well
        all_cells = calculator.get_neighborhood_cells(grid, distance_threshold)
        assert len(all_cells) == expected_count
        
        # Verify the union equals the sum for non-overlapping sets
        union_cells = neighborhood1.union(neighborhood2)
        assert len(union_cells) == len(neighborhood1) + len(neighborhood2)
        assert all_cells == union_cells
    
    @given(
        height=st.integers(min_value=10, max_value=50),
        width=st.integers(min_value=10, max_value=50),
        distance_threshold=st.integers(min_value=2, max_value=8)
    )
    def test_overlapping_union_behavior(self, height, width, distance_threshold):
        """Property 9: Overlapping Union Behavior
        
        For any set of positive cells with overlapping neighborhoods, the total count 
        should equal the size of the union of all neighborhoods and be less than or 
        equal to the sum of individual neighborhood counts.
        
        **Feature: grid-neighborhoods, Property 9: Overlapping Union Behavior**
        **Validates: Requirements 5.2, 5.3**
        """
        # Create two positive cells close enough that their neighborhoods overlap
        # Place them within overlapping distance but ensure both fit in grid
        overlap_distance = distance_threshold - 1  # Guaranteed to create overlap
        
        # Ensure we have enough space for both neighborhoods
        assume(height >= 2 * distance_threshold + overlap_distance + 2)
        assume(width >= 2 * distance_threshold + overlap_distance + 2)
        
        grid = Grid(height, width)
        
        # Place first positive cell with enough border space
        pos1_row = distance_threshold + 1
        pos1_col = distance_threshold + 1
        pos1 = Position(pos1_row, pos1_col)
        grid.set_cell_value(pos1, 1)
        
        # Place second positive cell close enough to create overlap
        pos2_row = pos1_row + overlap_distance
        pos2_col = pos1_col + overlap_distance
        
        # Ensure second position is within bounds and has enough space
        assume(pos2_row < height - distance_threshold - 1)
        assume(pos2_col < width - distance_threshold - 1)
        
        pos2 = Position(pos2_row, pos2_col)
        grid.set_cell_value(pos2, 1)
        
        calculator = NeighborhoodCalculator()
        
        # Calculate individual neighborhoods
        neighborhood1 = calculator.enumerate_neighborhood(pos1, distance_threshold, grid)
        neighborhood2 = calculator.enumerate_neighborhood(pos2, distance_threshold, grid)
        
        # Verify neighborhoods do overlap (this is the key difference from test 5.1)
        overlap = neighborhood1.intersection(neighborhood2)
        assert len(overlap) > 0, f"Neighborhoods should overlap, but found no overlapping cells"
        
        # Calculate total neighborhood count
        total_count = calculator.count_neighborhood_cells(grid, distance_threshold)
        
        # Calculate the union manually
        union_cells = neighborhood1.union(neighborhood2)
        expected_count = len(union_cells)
        
        # For overlapping neighborhoods, total should equal union size
        assert total_count == expected_count
        
        # Total should be less than sum of individual counts (due to overlap)
        sum_of_individual = len(neighborhood1) + len(neighborhood2)
        assert total_count < sum_of_individual, f"Expected {total_count} < {sum_of_individual} due to overlap"
        
        # The difference should equal the overlap size
        overlap_size = len(overlap)
        assert sum_of_individual - total_count == overlap_size
        
        # Verify using get_neighborhood_cells as well
        all_cells = calculator.get_neighborhood_cells(grid, distance_threshold)
        assert len(all_cells) == expected_count
        assert all_cells == union_cells
        
        # Mathematical relationship: |A ∪ B| = |A| + |B| - |A ∩ B|
        assert len(union_cells) == len(neighborhood1) + len(neighborhood2) - len(overlap)