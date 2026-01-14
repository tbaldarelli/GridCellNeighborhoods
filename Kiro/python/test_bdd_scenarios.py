"""BDD scenario tests for grid neighborhoods.

This test suite implements the 26 BDD scenarios from grid-neighborhoods.feature.md
Each scenario validates the system against concrete examples with specific expected counts.

All scenarios use an 11x11 grid unless otherwise specified.
"""

import pytest
from position import Position
from grid import Grid
from neighborhood_calculator import NeighborhoodCalculator


class TestSinglePositiveCellScenarios:
    """BDD Scenarios 1-2: Single positive cell scenarios."""
    
    def test_scenario_1_single_positive_cell_fully_contained(self):
        """Scenario 1: Single positive cell fully contained
        
        Given a grid with exactly one positive cell
        And the positive cell is far enough from all grid boundaries
        And the positive cell at position (5,5)
        And a distance threshold 3
        And H = 11
        And W = 11
        
        When the neighborhood count is calculated
        
        Then the result includes the positive cell itself
        And includes all cells within 3 Manhattan steps
        And includes no cells outside the grid
        And includes 25 cells in the neighborhood
        
        **Validates: Requirements 3.1, 3.2, 3.4**
        """
        grid = Grid(11, 11)
        grid.set_cell_value(Position(5, 5), 1)
        
        calculator = NeighborhoodCalculator()
        count = calculator.count_neighborhood_cells(grid, distance_threshold=3)
        
        print(f"Scenario 1: Expected=25, Grid=11x11, N=3, Pos=[(5,5)], Got={count}")
        assert count == 25
    
    def test_scenario_2_single_positive_cell_near_edge(self):
        """Scenario 2: Single positive cell near a grid edge
        
        Given a grid with exactly one positive cell
        And the positive cell is near at least one grid boundary
        And the positive cell at position (5,1)
        And a distance threshold 3
        And H = 11
        And W = 11
        
        When the neighborhood count is calculated
        
        Then cells outside the grid are not counted
        And only valid grid cells within 3 Manhattan steps are included
        And includes 21 cells in the neighborhood
        
        **Validates: Requirements 3.1, 3.2, 6.1, 6.2, 6.3**
        """
        grid = Grid(11, 11)
        grid.set_cell_value(Position(5, 1), 1)
        
        calculator = NeighborhoodCalculator()
        count = calculator.count_neighborhood_cells(grid, distance_threshold=3)
        
        print(f"Scenario 2: Expected=21, Grid=11x11, N=3, Pos=[(5,1)], Got={count}")
        assert count == 21


class TestMultiplePositiveCellsNonOverlapping:
    """BDD Scenario 3: Multiple positive cells with non-overlapping neighborhoods."""
    
    def test_scenario_3_non_overlapping_neighborhoods(self):
        """Scenario 3: Multiple positive cells with non-overlapping neighborhoods
        
        Given a grid with more than one positive cell
        And the neighborhoods of those positive cells do not overlap
        And one positive cell at position (3,3)
        And one positive cell at position (7,7)
        And a distance threshold 2
        And H = 11
        And W = 11
        
        When the neighborhood count is calculated
        
        Then all neighborhood cells are included
        And the total count is the sum of the individual neighborhoods
        And includes 26 cells between the two neighborhoods
        
        **Validates: Requirements 4.1, 4.2, 4.3**
        """
        grid = Grid(11, 11)
        grid.set_cell_value(Position(3, 3), 1)
        grid.set_cell_value(Position(7, 7), 1)
        
        calculator = NeighborhoodCalculator()
        count = calculator.count_neighborhood_cells(grid, distance_threshold=2)
        
        print(f"Scenario 3: Expected=26, Grid=11x11, N=2, Pos=[(3,3),(7,7)], Got={count}")
        assert count == 26


class TestMultiplePositiveCellsOverlapping:
    """BDD Scenarios 4-14: Multiple positive cells with overlapping neighborhoods."""
    
    def test_scenario_4_overlapping_neighborhoods(self):
        """Scenario 4: Multiple positive cells with overlapping neighborhoods
        
        Given a grid with more than one positive cell
        And the neighborhoods of those positive cells overlap
        And one positive cell at position (3,3)
        And one positive cell at position (4,5)
        And a distance threshold 2
        And H = 11
        And W = 11
        
        When the neighborhood count is calculated
        
        Then overlapping cells are counted only once
        And the result reflects the union of all neighborhoods
        And includes 22 cells in the combined neighborhood
        
        **Validates: Requirements 5.1, 5.2, 5.3**
        """
        grid = Grid(11, 11)
        grid.set_cell_value(Position(3, 3), 1)
        grid.set_cell_value(Position(4, 5), 1)
        
        calculator = NeighborhoodCalculator()
        count = calculator.count_neighborhood_cells(grid, distance_threshold=2)
        
        print(f"Scenario 4: Expected=22, Grid=11x11, N=2, Pos=[(3,3),(4,5)], Got={count}")
        assert count == 22
    
    def test_scenario_5_overlapping_out_of_bounds_left(self):
        """Scenario 5: Multiple positive cells with overlapping neighborhoods, out of bounds on left
        
        Given a grid with more than one positive cell
        And the neighborhoods of those positive cells overlap
        And one positive cell at position (3,0)
        And one positive cell at position (4,2)
        And a distance threshold 2
        And H = 11
        And W = 11
        
        When the neighborhood count is calculated
        
        Then overlapping cells are counted only once
        And the result reflects the union of all neighborhoods
        And includes 18 cells in the combined neighborhood
        
        **Validates: Requirements 5.1, 5.2, 6.1, 6.2**
        """
        grid = Grid(11, 11)
        grid.set_cell_value(Position(3, 0), 1)
        grid.set_cell_value(Position(4, 2), 1)
        
        calculator = NeighborhoodCalculator()
        count = calculator.count_neighborhood_cells(grid, distance_threshold=2)
        
        print(f"Scenario 5: Expected=18, Grid=11x11, N=2, Pos=[(3,0),(4,2)], Got={count}")
        assert count == 18
    
    def test_scenario_6_overlapping_out_of_bounds_bottom_left(self):
        """Scenario 6: Multiple positive cells with overlapping neighborhoods, out of bounds on bottom left
        
        Given a grid with more than one positive cell
        And the neighborhoods of those positive cells overlap
        And one positive cell at position (0,0)
        And one positive cell at position (1,2)
        And a distance threshold 2
        And H = 11
        And W = 11
        
        When the neighborhood count is calculated
        
        Then overlapping cells are counted only once
        And the result reflects the union of all neighborhoods
        And includes 14 cells in the combined neighborhood
        
        **Validates: Requirements 5.1, 5.2, 6.1, 6.2**
        """
        grid = Grid(11, 11)
        grid.set_cell_value(Position(0, 0), 1)
        grid.set_cell_value(Position(1, 2), 1)
        
        calculator = NeighborhoodCalculator()
        count = calculator.count_neighborhood_cells(grid, distance_threshold=2)
        
        print(f"Scenario 6: Expected=14, Grid=11x11, N=2, Pos=[(0,0),(1,2)], Got={count}")
        assert count == 14
    
    def test_scenario_7_overlapping_out_of_bounds_bottom(self):
        """Scenario 7: Multiple positive cells with overlapping neighborhoods, out of bounds on bottom
        
        Given a grid with more than one positive cell
        And the neighborhoods of those positive cells overlap
        And one positive cell at position (0,3)
        And one positive cell at position (1,5)
        And a distance threshold 2
        And H = 11
        And W = 11
        
        When the neighborhood count is calculated
        
        Then overlapping cells are counted only once
        And the result reflects the union of all neighborhoods
        And includes 17 cells in the combined neighborhood
        
        **Validates: Requirements 5.1, 5.2, 6.1, 6.2**
        """
        grid = Grid(11, 11)
        grid.set_cell_value(Position(0, 3), 1)
        grid.set_cell_value(Position(1, 5), 1)
        
        calculator = NeighborhoodCalculator()
        count = calculator.count_neighborhood_cells(grid, distance_threshold=2)
        
        print(f"Scenario 7: Expected=17, Grid=11x11, N=2, Pos=[(0,3),(1,5)], Got={count}")
        assert count == 17
    
    def test_scenario_8_overlapping_out_of_bounds_right(self):
        """Scenario 8: Multiple positive cells with overlapping neighborhoods, out of bounds right
        
        Given a grid with more than one positive cell
        And the neighborhoods of those positive cells overlap
        And one positive cell at position (3,8)
        And one positive cell at position (4,10)
        And a distance threshold 2
        And H = 11
        And W = 11
        
        When the neighborhood count is calculated
        
        Then overlapping cells are counted only once
        And the result reflects the union of all neighborhoods
        And includes 18 cells in the combined neighborhood
        
        **Validates: Requirements 5.1, 5.2, 6.1, 6.2**
        """
        grid = Grid(11, 11)
        grid.set_cell_value(Position(3, 8), 1)
        grid.set_cell_value(Position(4, 10), 1)
        
        calculator = NeighborhoodCalculator()
        count = calculator.count_neighborhood_cells(grid, distance_threshold=2)
        
        print(f"Scenario 8: Expected=18, Grid=11x11, N=2, Pos=[(3,8),(4,10)], Got={count}")
        assert count == 18
    
    def test_scenario_9_overlapping_out_of_bounds_top(self):
        """Scenario 9: Multiple positive cells with overlapping neighborhoods, out of bounds top
        
        Given a grid with more than one positive cell
        And the neighborhoods of those positive cells overlap
        And one positive cell at position (9,3)
        And one positive cell at position (10,5)
        And a distance threshold 2
        And H = 11
        And W = 11
        
        When the neighborhood count is calculated
        
        Then overlapping cells are counted only once
        And the result reflects the union of all neighborhoods
        And includes 17 cells in the combined neighborhood
        
        **Validates: Requirements 5.1, 5.2, 6.1, 6.2**
        """
        grid = Grid(11, 11)
        grid.set_cell_value(Position(9, 3), 1)
        grid.set_cell_value(Position(10, 5), 1)
        
        calculator = NeighborhoodCalculator()
        count = calculator.count_neighborhood_cells(grid, distance_threshold=2)
        
        print(f"Scenario 9: Expected=17, Grid=11x11, N=2, Pos=[(9,3),(10,5)], Got={count}")
        assert count == 17
    
    def test_scenario_10_overlapping_diagonally_adjacent(self):
        """Scenario 10: Multiple positive cells with overlapping neighborhoods, diagonally adjacent
        
        Given a grid with more than one positive cell
        And the neighborhoods of those positive cells overlap
        And one positive cell at position (3,3)
        And one positive cell at position (4,4)
        And a distance threshold 2
        And H = 11
        And W = 11
        
        When the neighborhood count is calculated
        
        Then overlapping cells are counted only once
        And the result reflects the union of all neighborhoods
        And includes 18 cells in the combined neighborhood
        
        **Validates: Requirements 5.1, 5.2, 5.3**
        """
        grid = Grid(11, 11)
        grid.set_cell_value(Position(3, 3), 1)
        grid.set_cell_value(Position(4, 4), 1)
        
        calculator = NeighborhoodCalculator()
        count = calculator.count_neighborhood_cells(grid, distance_threshold=2)
        
        print(f"Scenario 10: Expected=18, Grid=11x11, N=2, Pos=[(3,3),(4,4)], Got={count}")
        assert count == 18
    
    def test_scenario_11_overlapping_same_row_adjacent(self):
        """Scenario 11: Multiple positive cells with overlapping neighborhoods, same row adjacent
        
        Given a grid with more than one positive cell
        And the neighborhoods of those positive cells overlap
        And one positive cell at position (3,3)
        And one positive cell at position (3,4)
        And a distance threshold 2
        And H = 11
        And W = 11
        
        When the neighborhood count is calculated
        
        Then overlapping cells are counted only once
        And the result reflects the union of all neighborhoods
        And includes 18 cells in the combined neighborhood
        
        **Validates: Requirements 5.1, 5.2, 5.3**
        """
        grid = Grid(11, 11)
        grid.set_cell_value(Position(3, 3), 1)
        grid.set_cell_value(Position(3, 4), 1)
        
        calculator = NeighborhoodCalculator()
        count = calculator.count_neighborhood_cells(grid, distance_threshold=2)
        
        print(f"Scenario 11: Expected=18, Grid=11x11, N=2, Pos=[(3,3),(3,4)], Got={count}")
        assert count == 18
    
    def test_scenario_12_overlapping_same_column_adjacent(self):
        """Scenario 12: Multiple positive cells with overlapping neighborhoods, same column adjacent
        
        Given a grid with more than one positive cell
        And the neighborhoods of those positive cells overlap
        And one positive cell at position (3,4)
        And one positive cell at position (4,4)
        And a distance threshold 2
        And H = 11
        And W = 11
        
        When the neighborhood count is calculated
        
        Then overlapping cells are counted only once
        And the result reflects the union of all neighborhoods
        And includes 18 cells in the combined neighborhood
        
        **Validates: Requirements 5.1, 5.2, 5.3**
        """
        grid = Grid(11, 11)
        grid.set_cell_value(Position(3, 4), 1)
        grid.set_cell_value(Position(4, 4), 1)
        
        calculator = NeighborhoodCalculator()
        count = calculator.count_neighborhood_cells(grid, distance_threshold=2)
        
        print(f"Scenario 12: Expected=18, Grid=11x11, N=2, Pos=[(3,4),(4,4)], Got={count}")
        assert count == 18
    
    def test_scenario_13_opposite_corners(self):
        """Scenario 13: Multiple positive cells, opposite corners
        
        Given a grid with more than one positive cell
        And the neighborhoods of those positive cells overlap
        And one positive cell at position (0,0)
        And one positive cell at position (10,10)
        And a distance threshold 3
        And H = 11
        And W = 11
        
        When the neighborhood count is calculated
        
        Then overlapping cells are counted only once
        And the result reflects the union of all neighborhoods
        And includes 20 cells in the combined neighborhood
        
        **Validates: Requirements 5.1, 5.2, 6.1, 6.2**
        """
        grid = Grid(11, 11)
        grid.set_cell_value(Position(0, 0), 1)
        grid.set_cell_value(Position(10, 10), 1)
        
        calculator = NeighborhoodCalculator()
        count = calculator.count_neighborhood_cells(grid, distance_threshold=3)
        
        print(f"Scenario 13: Expected=20, Grid=11x11, N=3, Pos=[(0,0),(10,10)], Got={count}")
        assert count == 20
    
    def test_scenario_14_three_in_one_corner(self):
        """Scenario 14: Multiple positive cells, 3 in one corner
        
        Given a grid with more than one positive cell
        And the neighborhoods of those positive cells overlap
        And one positive cell at position (10,9)
        And one positive cell at position (9,10)
        And one positive cell at position (10,10)
        And a distance threshold 3
        And H = 11
        And W = 11
        
        When the neighborhood count is calculated
        
        Then overlapping cells are counted only once
        And the result reflects the union of all neighborhoods
        And includes 15 cells in the combined neighborhood
        
        **Validates: Requirements 5.1, 5.2, 6.1, 6.2**
        """
        grid = Grid(11, 11)
        grid.set_cell_value(Position(10, 9), 1)
        grid.set_cell_value(Position(9, 10), 1)
        grid.set_cell_value(Position(10, 10), 1)
        
        calculator = NeighborhoodCalculator()
        count = calculator.count_neighborhood_cells(grid, distance_threshold=3)
        
        print(f"Scenario 14: Expected=15, Grid=11x11, N=3, Pos=[(10,9),(9,10),(10,10)], Got={count}")
        assert count == 15



class TestDegenerateGridScenarios:
    """BDD Scenarios 15-25: Degenerate grids and extreme cases."""
    
    def test_scenario_15_1x21_grid(self):
        """Scenario 15: One positive cell, 1x21 grid
        
        Given a grid with one positive cell
        And one positive cell at position (0,9)
        And a distance threshold 3
        And H = 1
        And W = 21
        
        When the neighborhood count is calculated
        
        Then includes 7 cells in the combined neighborhood
        
        **Validates: Requirements 7.4**
        """
        grid = Grid(1, 21)
        grid.set_cell_value(Position(0, 9), 1)
        
        calculator = NeighborhoodCalculator()
        count = calculator.count_neighborhood_cells(grid, distance_threshold=3)
        
        print(f"Scenario 15: Expected=7, Grid=1x21, N=3, Pos=[(0,9)], Got={count}")
        assert count == 7
    
    def test_scenario_16_21x1_grid(self):
        """Scenario 16: One positive cell, 21x1 grid
        
        Given a grid with one positive cell
        And one positive cell at position (10,0)
        And a distance threshold 3
        And H = 21
        And W = 1
        
        When the neighborhood count is calculated
        
        Then includes 7 cells in the combined neighborhood
        
        **Validates: Requirements 7.4**
        """
        grid = Grid(21, 1)
        grid.set_cell_value(Position(10, 0), 1)
        
        calculator = NeighborhoodCalculator()
        count = calculator.count_neighborhood_cells(grid, distance_threshold=3)
        
        print(f"Scenario 16: Expected=7, Grid=21x1, N=3, Pos=[(10,0)], Got={count}")
        assert count == 7
    
    def test_scenario_17_1x1_grid(self):
        """Scenario 17: one positive cell, 1x1 grid
        
        Given a grid with exactly one positive cell
        And one positive cell at position (0,0)
        And a distance threshold 0
        And H = 1
        And W = 1
        
        When the neighborhood count is calculated
        
        Then includes 1 cells in the combined neighborhood
        
        **Validates: Requirements 7.2, 7.4**
        """
        grid = Grid(1, 1)
        grid.set_cell_value(Position(0, 0), 1)
        
        calculator = NeighborhoodCalculator()
        count = calculator.count_neighborhood_cells(grid, distance_threshold=0)
        
        print(f"Scenario 17: Expected=1, Grid=1x1, N=0, Pos=[(0,0)], Got={count}")
        assert count == 1
    
    def test_scenario_18_20x20_grid_threshold_zero(self):
        """Scenario 18: One positive cell, 20x20 grid
        
        Given a grid with exactly one positive cell
        And one positive cell at position (0,0)
        And a distance threshold 0
        And H = 20
        And W = 20
        
        When the neighborhood count is calculated
        
        Then includes 1 cells in the combined neighborhood
        
        **Validates: Requirements 7.2**
        """
        grid = Grid(20, 20)
        grid.set_cell_value(Position(0, 0), 1)
        
        calculator = NeighborhoodCalculator()
        count = calculator.count_neighborhood_cells(grid, distance_threshold=0)
        
        print(f"Scenario 18: Expected=1, Grid=20x20, N=0, Pos=[(0,0)], Got={count}")
        assert count == 1
    
    def test_scenario_19_2x2_grid(self):
        """Scenario 19: one positive cell, 2x2 grid
        
        Given a grid with exactly one positive cell
        And one positive cell at position (0,1)
        And a distance threshold 2
        And H = 2
        And W = 2
        
        When the neighborhood count is calculated
        
        Then includes 4 cells in the combined neighborhood
        
        **Validates: Requirements 7.3, 7.4**
        """
        grid = Grid(2, 2)
        grid.set_cell_value(Position(0, 1), 1)
        
        calculator = NeighborhoodCalculator()
        count = calculator.count_neighborhood_cells(grid, distance_threshold=2)
        
        print(f"Scenario 19: Expected=4, Grid=2x2, N=2, Pos=[(0,1)], Got={count}")
        assert count == 4
    
    def test_scenario_20_21x3_grid_n_greater_than_w(self):
        """Scenario 20: One positive cell, 21x3 grid, N > W
        
        Given a grid with exactly one positive cell
        And one positive cell at position (10,2)
        And a distance threshold 5
        And H = 21
        And W = 3
        
        When the neighborhood count is calculated
        
        Then includes 27 cells in the combined neighborhood
        
        **Validates: Requirements 7.3, 7.4**
        """
        grid = Grid(21, 3)
        grid.set_cell_value(Position(10, 2), 1)
        
        calculator = NeighborhoodCalculator()
        count = calculator.count_neighborhood_cells(grid, distance_threshold=5)
        
        print(f"Scenario 20: Expected=27, Grid=21x3, N=5, Pos=[(10,2)], Got={count}")
        assert count == 27
    
    def test_scenario_21_4x15_grid_n_greater_than_h(self):
        """Scenario 21: One positive cell, 4x15 grid, N > H
        
        Given a grid with exactly one positive cell
        And one positive cell at position (2,9)
        And a distance threshold 5
        And H = 4
        And W = 15
        
        When the neighborhood count is calculated
        
        Then includes 36 cells in the combined neighborhood
        
        **Validates: Requirements 7.3, 7.4**
        """
        grid = Grid(4, 15)
        grid.set_cell_value(Position(2, 9), 1)
        
        calculator = NeighborhoodCalculator()
        count = calculator.count_neighborhood_cells(grid, distance_threshold=5)
        
        print(f"Scenario 21: Expected=36, Grid=4x15, N=5, Pos=[(2,9)], Got={count}")
        assert count == 36
    
    def test_scenario_22_2x2_grid_n_greater_than_both(self):
        """Scenario 22: One positive cell, 2x2 grid, N > H and W
        
        Given a grid with exactly one positive cell
        And one positive cell at position (0,1)
        And a distance threshold 3
        And H = 2
        And W = 2
        
        When the neighborhood count is calculated
        
        Then includes 4 cells in the combined neighborhood
        
        **Validates: Requirements 7.3, 7.4**
        """
        grid = Grid(2, 2)
        grid.set_cell_value(Position(0, 1), 1)
        
        calculator = NeighborhoodCalculator()
        count = calculator.count_neighborhood_cells(grid, distance_threshold=3)
        
        print(f"Scenario 22: Expected=4, Grid=2x2, N=3, Pos=[(0,1)], Got={count}")
        assert count == 4
    
    def test_scenario_23_2x2_grid_n_much_greater(self):
        """Scenario 23: One positive cell, 2x2 grid, N much > H and W
        
        Given a grid with exactly one positive cell
        And one positive cell at position (0,1)
        And a distance threshold 100000
        And H = 2
        And W = 2
        
        When the neighborhood count is calculated
        
        Then includes 4 cells in the combined neighborhood
        
        **Validates: Requirements 7.3, 7.4, 8.1**
        """
        grid = Grid(2, 2)
        grid.set_cell_value(Position(0, 1), 1)
        
        calculator = NeighborhoodCalculator()
        count = calculator.count_neighborhood_cells(grid, distance_threshold=100000)
        
        print(f"Scenario 23: Expected=4, Grid=2x2, N=100000, Pos=[(0,1)], Got={count}")
        assert count == 4
    
    def test_scenario_24_11x11_grid_corner_large_n(self):
        """Scenario 24: One positive cell at (0,0), 11x11 grid, N > H and W
        
        Given a grid with exactly one positive cell
        And one positive cell at position (0,0)
        And a distance threshold 12
        And H = 11
        And W = 11
        
        When the neighborhood count is calculated
        
        Then includes 85 cells in the combined neighborhood
        
        **Validates: Requirements 7.3**
        """
        grid = Grid(11, 11)
        grid.set_cell_value(Position(0, 0), 1)
        
        calculator = NeighborhoodCalculator()
        count = calculator.count_neighborhood_cells(grid, distance_threshold=12)
        
        print(f"Scenario 24: Expected=85, Grid=11x11, N=12, Pos=[(0,0)], Got={count}")
        assert count == 85
    
    def test_scenario_25_11x11_grid_center_large_n(self):
        """Scenario 25: One positive cell at (5,5), 11x11 grid, N > H and W
        
        Given a grid with exactly one positive cell
        And one positive cell at position (5,5)
        And a distance threshold 12
        And H = 11
        And W = 11
        
        When the neighborhood count is calculated
        
        Then includes 121 cells in the combined neighborhood
        
        **Validates: Requirements 7.3**
        """
        grid = Grid(11, 11)
        grid.set_cell_value(Position(5, 5), 1)
        
        calculator = NeighborhoodCalculator()
        count = calculator.count_neighborhood_cells(grid, distance_threshold=12)
        
        print(f"Scenario 25: Expected=121, Grid=11x11, N=12, Pos=[(5,5)], Got={count}")
        assert count == 121


class TestNoPositiveCellsScenario:
    """BDD Scenario 26: No positive cells."""
    
    def test_scenario_26_no_positive_cells(self):
        """Scenario 26: No positive cells
        
        Given a grid with no positive cells
        And a distance threshold 3
        And H = 10
        And W = 10
        
        When the neighborhood count is calculated
        
        Then includes 0 cells in the combined neighborhood
        
        **Validates: Requirements 7.1**
        """
        grid = Grid(10, 10)
        # Grid is created with all zeros by default (no positive cells)
        
        calculator = NeighborhoodCalculator()
        count = calculator.count_neighborhood_cells(grid, distance_threshold=3)
        
        print(f"Scenario 26: Expected=0, Grid=10x10, N=3, Pos=[], Got={count}")
        assert count == 0
