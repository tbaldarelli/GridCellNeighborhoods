"""Integration tests for grid neighborhoods system.

This test suite validates end-to-end functionality with complex scenarios
and tests performance characteristics on larger grids.
"""

import pytest
import time
from position import Position
from grid import Grid
from neighborhood_calculator import NeighborhoodCalculator


class TestEndToEndFunctionality:
    """Integration tests for end-to-end functionality with complex scenarios."""
    
    def test_complex_scenario_multiple_overlapping_regions(self):
        """Test complex scenario with multiple overlapping neighborhood regions.
        
        This test validates the complete workflow:
        1. Create a grid
        2. Place multiple positive cells in strategic positions
        3. Calculate neighborhoods with overlapping regions
        4. Verify correct union behavior
        """
        # Create a 20x20 grid
        grid = Grid(20, 20)
        
        # Place positive cells in a pattern that creates overlapping neighborhoods
        positive_positions = [
            (5, 5),   # Center-left region
            (5, 10),  # Center-right region
            (10, 5),  # Bottom-left region
            (10, 10), # Bottom-right region
            (7, 7),   # Central overlapping position
        ]
        
        for row, col in positive_positions:
            grid.set_cell_value(Position(row, col), 1)
        
        calculator = NeighborhoodCalculator()
        
        # Test with distance threshold that creates significant overlap
        distance_threshold = 3
        
        # Get both count and cells
        total_count = calculator.count_neighborhood_cells(grid, distance_threshold)
        all_cells = calculator.get_neighborhood_cells(grid, distance_threshold)
        
        # Verify consistency between count and cells
        assert total_count == len(all_cells)
        
        # Verify all positive cells are included
        for row, col in positive_positions:
            assert Position(row, col) in all_cells
        
        # Verify no duplicates
        cell_list = list(all_cells)
        assert len(cell_list) == len(set(cell_list))
        
        # Verify all cells are within grid bounds
        for cell in all_cells:
            assert 0 <= cell.row < 20
            assert 0 <= cell.column < 20
        
        # Verify count is less than sum of individual neighborhoods (due to overlap)
        individual_counts = []
        for row, col in positive_positions:
            neighborhood = calculator.enumerate_neighborhood(Position(row, col), distance_threshold, grid)
            individual_counts.append(len(neighborhood))
        
        sum_of_individual = sum(individual_counts)
        assert total_count < sum_of_individual, "Expected overlap to reduce total count"
        
        # Verify the count is reasonable (not too small, not too large)
        assert total_count > 0
        assert total_count <= 400  # Maximum possible for 20x20 grid
    
    def test_complex_scenario_boundary_interactions(self):
        """Test complex scenario with neighborhoods interacting with multiple boundaries.
        
        This test validates:
        1. Neighborhoods near corners
        2. Neighborhoods near edges
        3. Correct boundary clipping
        4. Union behavior near boundaries
        """
        # Create a 15x15 grid
        grid = Grid(15, 15)
        
        # Place positive cells near all four corners and edges
        positive_positions = [
            (0, 0),    # Bottom-left corner
            (0, 14),   # Bottom-right corner
            (14, 0),   # Top-left corner
            (14, 14),  # Top-right corner
            (0, 7),    # Bottom edge center
            (14, 7),   # Top edge center
            (7, 0),    # Left edge center
            (7, 14),   # Right edge center
        ]
        
        for row, col in positive_positions:
            grid.set_cell_value(Position(row, col), 1)
        
        calculator = NeighborhoodCalculator()
        distance_threshold = 4
        
        # Calculate neighborhoods
        total_count = calculator.count_neighborhood_cells(grid, distance_threshold)
        all_cells = calculator.get_neighborhood_cells(grid, distance_threshold)
        
        # Verify consistency
        assert total_count == len(all_cells)
        
        # Verify all cells are within bounds
        for cell in all_cells:
            assert 0 <= cell.row < 15
            assert 0 <= cell.column < 15
        
        # Verify corner cells have smaller neighborhoods than center cells
        corner_neighborhood = calculator.enumerate_neighborhood(Position(0, 0), distance_threshold, grid)
        # Corner neighborhood should be clipped by boundaries
        assert len(corner_neighborhood) < (distance_threshold + 1) ** 2 + distance_threshold ** 2
        
        # Verify all positive cells are included
        for row, col in positive_positions:
            assert Position(row, col) in all_cells
    
    def test_complex_scenario_sparse_grid(self):
        """Test complex scenario with sparse positive cells across large grid.
        
        This test validates:
        1. Handling of widely separated positive cells
        2. Non-overlapping neighborhoods
        3. Efficient processing of sparse grids
        """
        # Create a 30x30 grid
        grid = Grid(30, 30)
        
        # Place positive cells sparsely (far apart)
        positive_positions = [
            (2, 2),
            (2, 27),
            (15, 15),
            (27, 2),
            (27, 27),
        ]
        
        for row, col in positive_positions:
            grid.set_cell_value(Position(row, col), 1)
        
        calculator = NeighborhoodCalculator()
        distance_threshold = 2
        
        # Calculate neighborhoods
        total_count = calculator.count_neighborhood_cells(grid, distance_threshold)
        all_cells = calculator.get_neighborhood_cells(grid, distance_threshold)
        
        # Verify consistency
        assert total_count == len(all_cells)
        
        # For sparse grids with small threshold, neighborhoods shouldn't overlap
        # Calculate individual neighborhoods
        individual_neighborhoods = []
        for row, col in positive_positions:
            neighborhood = calculator.enumerate_neighborhood(Position(row, col), distance_threshold, grid)
            individual_neighborhoods.append(neighborhood)
        
        # Check for overlaps
        all_individual_cells = set()
        for neighborhood in individual_neighborhoods:
            all_individual_cells.update(neighborhood)
        
        # For this sparse configuration, total should equal sum (no overlap)
        sum_of_individual = sum(len(n) for n in individual_neighborhoods)
        assert total_count == sum_of_individual, "Sparse cells should have non-overlapping neighborhoods"
        assert total_count == len(all_individual_cells)
    
    def test_complex_scenario_dense_grid(self):
        """Test complex scenario with dense positive cells.
        
        This test validates:
        1. Handling of many positive cells
        2. Extensive overlapping neighborhoods
        3. Efficient union operations
        """
        # Create a 20x20 grid
        grid = Grid(20, 20)
        
        # Place positive cells in a dense pattern (checkerboard)
        positive_positions = []
        for row in range(5, 15):
            for col in range(5, 15):
                if (row + col) % 2 == 0:  # Checkerboard pattern
                    positive_positions.append((row, col))
                    grid.set_cell_value(Position(row, col), 1)
        
        calculator = NeighborhoodCalculator()
        distance_threshold = 2
        
        # Calculate neighborhoods
        total_count = calculator.count_neighborhood_cells(grid, distance_threshold)
        all_cells = calculator.get_neighborhood_cells(grid, distance_threshold)
        
        # Verify consistency
        assert total_count == len(all_cells)
        
        # With dense positive cells and threshold 2, expect significant overlap
        individual_counts = []
        for row, col in positive_positions:
            neighborhood = calculator.enumerate_neighborhood(Position(row, col), distance_threshold, grid)
            individual_counts.append(len(neighborhood))
        
        sum_of_individual = sum(individual_counts)
        
        # Total should be much less than sum due to extensive overlap
        assert total_count < sum_of_individual * 0.5, "Dense grid should have significant overlap"
        
        # Verify all positive cells are included
        for row, col in positive_positions:
            assert Position(row, col) in all_cells
    
    def test_complex_scenario_varying_thresholds(self):
        """Test complex scenario with varying distance thresholds.
        
        This test validates:
        1. Consistent behavior across different thresholds
        2. Monotonic growth of neighborhoods with increasing threshold
        3. Correct handling of threshold edge cases
        """
        # Create a 25x25 grid
        grid = Grid(25, 25)
        
        # Place positive cells in a pattern
        positive_positions = [
            (12, 12),  # Center
            (8, 8),    # Offset 1
            (16, 16),  # Offset 2
        ]
        
        for row, col in positive_positions:
            grid.set_cell_value(Position(row, col), 1)
        
        calculator = NeighborhoodCalculator()
        
        # Test with increasing thresholds
        previous_count = 0
        previous_cells = set()
        
        for threshold in [0, 1, 2, 3, 5, 8, 10, 15, 20, 30]:
            count = calculator.count_neighborhood_cells(grid, threshold)
            cells = calculator.get_neighborhood_cells(grid, threshold)
            
            # Verify consistency
            assert count == len(cells)
            
            # Verify monotonic growth (neighborhoods can only grow or stay same)
            assert count >= previous_count, f"Count should not decrease: {count} < {previous_count}"
            
            # Verify previous cells are subset of current cells
            assert previous_cells.issubset(cells), "Previous neighborhood should be subset of larger threshold"
            
            # Verify all cells are within bounds
            for cell in cells:
                assert 0 <= cell.row < 25
                assert 0 <= cell.column < 25
            
            previous_count = count
            previous_cells = cells
        
        # At very large threshold, should cover entire grid
        assert previous_count == 625  # 25 * 25


class TestPerformanceCharacteristics:
    """Integration tests for performance characteristics on larger grids."""
    
    def test_performance_large_grid_single_cell(self):
        """Test performance with large grid and single positive cell.
        
        This test validates:
        1. Reasonable performance on 100x100 grid
        2. Efficient neighborhood enumeration
        3. Correct results on large grids
        """
        # Create a 100x100 grid
        grid = Grid(100, 100)
        
        # Place single positive cell in center
        grid.set_cell_value(Position(50, 50), 1)
        
        calculator = NeighborhoodCalculator()
        distance_threshold = 10
        
        # Measure performance
        start_time = time.time()
        count = calculator.count_neighborhood_cells(grid, distance_threshold)
        elapsed_time = time.time() - start_time
        
        # Should complete quickly (under 1 second)
        assert elapsed_time < 1.0, f"Large grid calculation took too long: {elapsed_time:.3f}s"
        
        # Verify correct count (complete diamond)
        expected_count = (distance_threshold + 1) ** 2 + distance_threshold ** 2
        assert count == expected_count
    
    def test_performance_large_grid_multiple_cells(self):
        """Test performance with large grid and multiple positive cells.
        
        This test validates:
        1. Reasonable performance with multiple positive cells
        2. Efficient set union operations
        3. Correct results with overlapping neighborhoods
        """
        # Create a 100x100 grid
        grid = Grid(100, 100)
        
        # Place multiple positive cells
        positive_positions = [
            (25, 25),
            (25, 75),
            (50, 50),
            (75, 25),
            (75, 75),
        ]
        
        for row, col in positive_positions:
            grid.set_cell_value(Position(row, col), 1)
        
        calculator = NeighborhoodCalculator()
        distance_threshold = 15
        
        # Measure performance
        start_time = time.time()
        count = calculator.count_neighborhood_cells(grid, distance_threshold)
        elapsed_time = time.time() - start_time
        
        # Should complete quickly (under 1 second)
        assert elapsed_time < 1.0, f"Large grid with multiple cells took too long: {elapsed_time:.3f}s"
        
        # Verify reasonable count
        assert count > 0
        assert count <= 10000  # Maximum possible for 100x100 grid
    
    def test_performance_high_distance_threshold(self):
        """Test performance with high distance threshold (early termination optimization).
        
        This test validates:
        1. Early termination optimization works correctly
        2. Performance is good even with very high threshold
        3. Correct result (all grid cells)
        """
        # Create a 50x50 grid
        grid = Grid(50, 50)
        
        # Place positive cell
        grid.set_cell_value(Position(25, 25), 1)
        
        calculator = NeighborhoodCalculator()
        
        # Use very high distance threshold (should trigger early termination)
        distance_threshold = 1000
        
        # Measure performance
        start_time = time.time()
        count = calculator.count_neighborhood_cells(grid, distance_threshold)
        elapsed_time = time.time() - start_time
        
        # Should complete very quickly due to early termination (under 0.1 seconds)
        assert elapsed_time < 0.1, f"Early termination optimization failed: {elapsed_time:.3f}s"
        
        # Should return all grid cells
        assert count == 2500  # 50 * 50
    
    def test_performance_many_positive_cells(self):
        """Test performance with many positive cells.
        
        This test validates:
        1. Reasonable performance with many positive cells
        2. Efficient handling of many overlapping neighborhoods
        3. Correct union calculation
        """
        # Create a 50x50 grid
        grid = Grid(50, 50)
        
        # Place many positive cells (every 5th cell)
        positive_positions = []
        for row in range(0, 50, 5):
            for col in range(0, 50, 5):
                positive_positions.append((row, col))
                grid.set_cell_value(Position(row, col), 1)
        
        # Should have 100 positive cells (10x10 pattern)
        assert len(positive_positions) == 100
        
        calculator = NeighborhoodCalculator()
        distance_threshold = 3
        
        # Measure performance
        start_time = time.time()
        count = calculator.count_neighborhood_cells(grid, distance_threshold)
        elapsed_time = time.time() - start_time
        
        # Should complete in reasonable time (under 2 seconds)
        assert elapsed_time < 2.0, f"Many positive cells took too long: {elapsed_time:.3f}s"
        
        # Verify reasonable count
        assert count > 0
        assert count <= 2500  # Maximum possible for 50x50 grid
    
    def test_performance_degenerate_large_grid(self):
        """Test performance with degenerate large grid (1xN or Nx1).
        
        This test validates:
        1. Efficient handling of degenerate grids
        2. Correct results on long thin grids
        3. Good performance characteristics
        """
        # Create a 1x1000 grid
        grid = Grid(1, 1000)
        
        # Place positive cells at various positions
        positive_positions = [100, 300, 500, 700, 900]
        for col in positive_positions:
            grid.set_cell_value(Position(0, col), 1)
        
        calculator = NeighborhoodCalculator()
        distance_threshold = 50
        
        # Measure performance
        start_time = time.time()
        count = calculator.count_neighborhood_cells(grid, distance_threshold)
        elapsed_time = time.time() - start_time
        
        # Should complete quickly (under 0.5 seconds)
        assert elapsed_time < 0.5, f"Degenerate grid took too long: {elapsed_time:.3f}s"
        
        # Verify reasonable count
        assert count > 0
        assert count <= 1000  # Maximum possible for 1x1000 grid
    
    def test_performance_zero_threshold_many_cells(self):
        """Test performance with zero threshold and many positive cells.
        
        This test validates:
        1. Zero threshold optimization works correctly
        2. Performance is excellent with optimization
        3. Correct result (count equals number of positive cells)
        """
        # Create a 100x100 grid
        grid = Grid(100, 100)
        
        # Place many positive cells
        positive_count = 0
        for row in range(0, 100, 2):
            for col in range(0, 100, 2):
                grid.set_cell_value(Position(row, col), 1)
                positive_count += 1
        
        # Should have 2500 positive cells (50x50 pattern)
        assert positive_count == 2500
        
        calculator = NeighborhoodCalculator()
        distance_threshold = 0
        
        # Measure performance
        start_time = time.time()
        count = calculator.count_neighborhood_cells(grid, distance_threshold)
        elapsed_time = time.time() - start_time
        
        # Should complete very quickly due to optimization (under 0.1 seconds)
        assert elapsed_time < 0.1, f"Zero threshold optimization failed: {elapsed_time:.3f}s"
        
        # Should return exactly the number of positive cells
        assert count == positive_count


class TestIntegrationEdgeCases:
    """Integration tests for edge cases in complete workflows."""
    
    def test_integration_all_cells_positive(self):
        """Test integration when all cells in grid are positive.
        
        This validates the extreme case where every cell is positive.
        """
        # Create a 10x10 grid
        grid = Grid(10, 10)
        
        # Make all cells positive
        for row in range(10):
            for col in range(10):
                grid.set_cell_value(Position(row, col), 1)
        
        calculator = NeighborhoodCalculator()
        
        # With any threshold > 0, should cover entire grid
        for threshold in [1, 2, 5, 10]:
            count = calculator.count_neighborhood_cells(grid, threshold)
            assert count == 100, f"All positive cells should cover entire grid at threshold {threshold}"
    
    def test_integration_single_row_positive(self):
        """Test integration when only a single row has positive cells."""
        # Create a 20x20 grid
        grid = Grid(20, 20)
        
        # Make middle row positive
        for col in range(20):
            grid.set_cell_value(Position(10, col), 1)
        
        calculator = NeighborhoodCalculator()
        distance_threshold = 3
        
        count = calculator.count_neighborhood_cells(grid, distance_threshold)
        cells = calculator.get_neighborhood_cells(grid, distance_threshold)
        
        # Verify consistency
        assert count == len(cells)
        
        # All cells should be within 3 rows of row 10
        for cell in cells:
            assert 7 <= cell.row <= 13
    
    def test_integration_single_column_positive(self):
        """Test integration when only a single column has positive cells."""
        # Create a 20x20 grid
        grid = Grid(20, 20)
        
        # Make middle column positive
        for row in range(20):
            grid.set_cell_value(Position(row, 10), 1)
        
        calculator = NeighborhoodCalculator()
        distance_threshold = 3
        
        count = calculator.count_neighborhood_cells(grid, distance_threshold)
        cells = calculator.get_neighborhood_cells(grid, distance_threshold)
        
        # Verify consistency
        assert count == len(cells)
        
        # All cells should be within 3 columns of column 10
        for cell in cells:
            assert 7 <= cell.column <= 13
    
    def test_integration_diagonal_positive_cells(self):
        """Test integration with positive cells along diagonal."""
        # Create a 15x15 grid
        grid = Grid(15, 15)
        
        # Place positive cells along main diagonal
        for i in range(15):
            grid.set_cell_value(Position(i, i), 1)
        
        calculator = NeighborhoodCalculator()
        distance_threshold = 2
        
        count = calculator.count_neighborhood_cells(grid, distance_threshold)
        cells = calculator.get_neighborhood_cells(grid, distance_threshold)
        
        # Verify consistency
        assert count == len(cells)
        
        # Verify all diagonal cells are included
        for i in range(15):
            assert Position(i, i) in cells
        
        # Verify reasonable count (should be more than just diagonal due to neighborhoods)
        assert count > 15
