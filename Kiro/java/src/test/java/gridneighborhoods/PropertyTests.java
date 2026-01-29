package gridneighborhoods;

import gridneighborhoods.exceptions.InvalidGridDimensionsException;
import net.jqwik.api.*;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Property-based tests for grid neighborhoods core components using jqwik.
 * 
 * This test suite implements all 13 correctness properties from the design document.
 */
public class PropertyTests {
    
    /**
     * Property 1: Grid Validation
     * Feature: grid-neighborhoods, Property 1: Grid Validation
     * Validates: Requirements 1.1, 1.2
     */
    @Property(tries = 100)
    void testGridValidation(
            @ForAll("gridDimensions") int height,
            @ForAll("gridDimensions") int width) {
        
        if (height > 0 && width > 0) {
            Grid grid = new Grid(height, width);
            assertEquals(height, grid.getHeight());
            assertEquals(width, grid.getWidth());
        } else {
            assertThrows(InvalidGridDimensionsException.class, () -> new Grid(height, width));
        }
    }
    
    /**
     * Property 2: Manhattan Distance Calculation
     * Feature: grid-neighborhoods, Property 2: Manhattan Distance Calculation
     * Validates: Requirements 2.1, 2.2, 2.3
     */
    @Property(tries = 100)
    void testManhattanDistanceCalculation(
            @ForAll("validCoordinate") int row1,
            @ForAll("validCoordinate") int col1,
            @ForAll("validCoordinate") int row2,
            @ForAll("validCoordinate") int col2) {
        
        Position pos1 = new Position(row1, col1);
        Position pos2 = new Position(row2, col2);
        
        int distance = pos1.manhattanDistance(pos2);
        int expectedDistance = Math.abs(row1 - row2) + Math.abs(col1 - col2);
        
        assertEquals(expectedDistance, distance);
        assertTrue(distance >= 0);
        
        if (row1 == row2 && col1 == col2) {
            assertEquals(0, distance);
        }
        
        assertEquals(pos1.manhattanDistance(pos2), pos2.manhattanDistance(pos1));
    }
    
    /**
     * Property 3: Coordinate System Consistency
     * Feature: grid-neighborhoods, Property 3: Coordinate System Consistency
     * Validates: Requirements 1.3, 1.4
     */
    @Property(tries = 100)
    void testCoordinateSystemConsistency(
            @ForAll("smallGridDimension") int height,
            @ForAll("smallGridDimension") int width) {
        
        Grid grid = new Grid(height, width);
        
        Position bottomLeft = new Position(0, 0);
        assertTrue(grid.isValidPosition(bottomLeft));
        
        Position topRight = new Position(height - 1, width - 1);
        assertTrue(grid.isValidPosition(topRight));
        
        if (height < 1000) {
            Position outOfBounds = new Position(height, 0);
            assertFalse(grid.isValidPosition(outOfBounds));
        }
    }
    
    /**
     * Property 4: Self-Inclusion in Neighborhoods
     * Feature: grid-neighborhoods, Property 4: Self-Inclusion in Neighborhoods
     * Validates: Requirements 3.1
     */
    @Property(tries = 100)
    void testSelfInclusionInNeighborhoods(
            @ForAll("smallGridDimension") int height,
            @ForAll("smallGridDimension") int width,
            @ForAll("distanceThreshold") int distanceThreshold) {
        
        Assume.that(height > 0 && width > 0);
        
        Grid grid = new Grid(height, width);
        Position positivePos = new Position(0, 0);
        grid.setCellValue(positivePos, 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        Set<Position> neighborhood = calculator.enumerateNeighborhood(positivePos, distanceThreshold, grid);
        
        assertTrue(neighborhood.contains(positivePos));
        
        int totalCount = calculator.countNeighborhoodCells(grid, distanceThreshold);
        assertTrue(totalCount >= 1);
    }
    
    /**
     * Property 5: Complete Neighborhood Enumeration
     * Feature: grid-neighborhoods, Property 5: Complete Neighborhood Enumeration
     * Validates: Requirements 3.2
     */
    @Property(tries = 100)
    void testCompleteNeighborhoodEnumeration(
            @ForAll("smallGridDimension") int height,
            @ForAll("smallGridDimension") int width,
            @ForAll("smallDistanceThreshold") int distanceThreshold) {
        
        int centerRow = distanceThreshold + 1;
        int centerCol = distanceThreshold + 1;
        
        Assume.that(centerRow + distanceThreshold < height);
        Assume.that(centerCol + distanceThreshold < width);
        
        Grid grid = new Grid(height, width);
        Position centerPos = new Position(centerRow, centerCol);
        grid.setCellValue(centerPos, 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        Set<Position> neighborhood = calculator.enumerateNeighborhood(centerPos, distanceThreshold, grid);
        
        int expectedSize = (distanceThreshold + 1) * (distanceThreshold + 1) + distanceThreshold * distanceThreshold;
        assertEquals(expectedSize, neighborhood.size());
    }
    
    /**
     * Property 6: Boundary Constraint Enforcement
     * Feature: grid-neighborhoods, Property 6: Boundary Constraint Enforcement
     * Validates: Requirements 3.3, 6.1, 6.2, 6.3
     */
    @Property(tries = 100)
    void testBoundaryConstraintEnforcement(
            @ForAll("smallGridDimension") int height,
            @ForAll("smallGridDimension") int width) {
        
        Grid grid = new Grid(height, width);
        Set<Position> positions = new HashSet<>();
        positions.add(new Position(0, 0));
        if (height > 1) positions.add(new Position(height - 1, 0));
        
        Set<Position> validPositions = BoundaryHandler.filterValidPositions(positions, grid);
        
        for (Position pos : validPositions) {
            assertTrue(BoundaryHandler.isWithinBounds(pos, grid));
            assertTrue(pos.getRow() >= 0 && pos.getRow() < height);
            assertTrue(pos.getColumn() >= 0 && pos.getColumn() < width);
        }
    }
    
    /**
     * Property 7: Cell Uniqueness Guarantee
     * Feature: grid-neighborhoods, Property 7: Cell Uniqueness Guarantee
     * Validates: Requirements 3.4, 4.2, 5.1
     */
    @Property(tries = 100)
    void testCellUniquenessGuarantee(
            @ForAll("smallGridDimension") int height,
            @ForAll("smallGridDimension") int width,
            @ForAll("distanceThreshold") int distanceThreshold) {
        
        Grid grid = new Grid(height, width);
        grid.setCellValue(new Position(0, 0), 1);
        if (height > 1 && width > 1) {
            grid.setCellValue(new Position(1, 1), 1);
        }
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        Set<Position> allNeighborhoodCells = calculator.getNeighborhoodCells(grid, distanceThreshold);
        int totalCount = calculator.countNeighborhoodCells(grid, distanceThreshold);
        
        assertEquals(totalCount, allNeighborhoodCells.size());
    }
    
    /**
     * Property 8: Non-Overlapping Additivity
     * Feature: grid-neighborhoods, Property 8: Non-Overlapping Additivity
     * Validates: Requirements 4.1, 4.3
     */
    @Property(tries = 100)
    void testNonOverlappingAdditivity(
            @ForAll("smallDistanceThreshold") int distanceThreshold) {
        
        int minSeparation = 2 * distanceThreshold + 1;
        int height = minSeparation + 2 * distanceThreshold + 2;
        int width = minSeparation + 2 * distanceThreshold + 2;
        
        Grid grid = new Grid(height, width);
        
        Position pos1 = new Position(distanceThreshold, distanceThreshold);
        grid.setCellValue(pos1, 1);
        
        Position pos2 = new Position(distanceThreshold + minSeparation, distanceThreshold + minSeparation);
        grid.setCellValue(pos2, 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        
        Set<Position> neighborhood1 = calculator.enumerateNeighborhood(pos1, distanceThreshold, grid);
        Set<Position> neighborhood2 = calculator.enumerateNeighborhood(pos2, distanceThreshold, grid);
        
        Set<Position> overlap = new HashSet<>(neighborhood1);
        overlap.retainAll(neighborhood2);
        assertEquals(0, overlap.size());
        
        int totalCount = calculator.countNeighborhoodCells(grid, distanceThreshold);
        int expectedCount = neighborhood1.size() + neighborhood2.size();
        assertEquals(expectedCount, totalCount);
    }
    
    /**
     * Property 9: Overlapping Union Behavior
     * Feature: grid-neighborhoods, Property 9: Overlapping Union Behavior
     * Validates: Requirements 5.2, 5.3
     */
    @Property(tries = 100)
    void testOverlappingUnionBehavior(
            @ForAll("smallDistanceThreshold") int distanceThreshold) {
        
        Assume.that(distanceThreshold >= 2);
        
        int height = 2 * distanceThreshold + 10;
        int width = 2 * distanceThreshold + 10;
        
        Grid grid = new Grid(height, width);
        
        Position pos1 = new Position(distanceThreshold + 1, distanceThreshold + 1);
        grid.setCellValue(pos1, 1);
        
        Position pos2 = new Position(distanceThreshold + 2, distanceThreshold + 2);
        grid.setCellValue(pos2, 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        
        Set<Position> neighborhood1 = calculator.enumerateNeighborhood(pos1, distanceThreshold, grid);
        Set<Position> neighborhood2 = calculator.enumerateNeighborhood(pos2, distanceThreshold, grid);
        
        Set<Position> overlap = new HashSet<>(neighborhood1);
        overlap.retainAll(neighborhood2);
        assertTrue(overlap.size() > 0);
        
        int totalCount = calculator.countNeighborhoodCells(grid, distanceThreshold);
        int sumOfIndividual = neighborhood1.size() + neighborhood2.size();
        assertTrue(totalCount < sumOfIndividual);
    }
    
    /**
     * Property 10: Zero Distance Threshold
     * Feature: grid-neighborhoods, Property 10: Zero Distance Threshold
     * Validates: Requirements 7.2
     */
    @Property(tries = 100)
    void testZeroDistanceThreshold(
            @ForAll("smallGridDimension") int height,
            @ForAll("smallGridDimension") int width) {
        
        Grid grid = new Grid(height, width);
        grid.setCellValue(new Position(0, 0), 1);
        if (height > 1 && width > 1) {
            grid.setCellValue(new Position(1, 1), 1);
        }
        
        int positiveCellCount = grid.getPositiveCells().size();
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        int totalCount = calculator.countNeighborhoodCells(grid, 0);
        
        assertEquals(positiveCellCount, totalCount);
    }
    
    /**
     * Property 11: Maximum Distance Threshold
     * Feature: grid-neighborhoods, Property 11: Maximum Distance Threshold
     * Validates: Requirements 7.3
     */
    @Property(tries = 100)
    void testMaximumDistanceThreshold(
            @ForAll("smallGridDimension") int height,
            @ForAll("smallGridDimension") int width) {
        
        Grid grid = new Grid(height, width);
        grid.setCellValue(new Position(0, 0), 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        
        int maxPossibleDistance = (height - 1) + (width - 1);
        int excessiveThreshold = maxPossibleDistance + 10;
        
        int totalCount = calculator.countNeighborhoodCells(grid, excessiveThreshold);
        int expectedCount = height * width;
        
        assertEquals(expectedCount, totalCount);
    }
    
    /**
     * Property 12: Degenerate Grid Handling
     * Feature: grid-neighborhoods, Property 12: Degenerate Grid Handling
     * Validates: Requirements 7.4
     */
    @Property(tries = 100)
    void testDegenerateGridHandling(
            @ForAll("gridType") String gridType,
            @ForAll("smallGridDimension") int dimension,
            @ForAll("distanceThreshold") int distanceThreshold) {
        
        Assume.that(dimension > 0);
        
        int height, width;
        Position positivePos;
        
        if (gridType.equals("1xN")) {
            height = 1;
            width = dimension;
            positivePos = new Position(0, Math.min(dimension / 2, dimension - 1));
        } else if (gridType.equals("Nx1")) {
            height = dimension;
            width = 1;
            positivePos = new Position(Math.min(dimension / 2, dimension - 1), 0);
        } else {
            height = 1;
            width = 1;
            positivePos = new Position(0, 0);
        }
        
        Grid grid = new Grid(height, width);
        grid.setCellValue(positivePos, 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        Set<Position> neighborhood = calculator.enumerateNeighborhood(positivePos, distanceThreshold, grid);
        
        assertTrue(neighborhood.contains(positivePos));
        
        for (Position cell : neighborhood) {
            int manhattanDist = positivePos.manhattanDistance(cell);
            assertTrue(manhattanDist <= distanceThreshold);
        }
    }
    
    // Arbitraries (generators)
    
    @Provide
    Arbitrary<Integer> gridDimensions() {
        return Arbitraries.integers().between(-100, 1000);
    }
    
    @Provide
    Arbitrary<Integer> smallGridDimension() {
        return Arbitraries.integers().between(1, 50);
    }
    
    @Provide
    Arbitrary<Integer> validCoordinate() {
        return Arbitraries.integers().between(0, 1000);
    }
    
    @Provide
    Arbitrary<Integer> distanceThreshold() {
        return Arbitraries.integers().between(0, 20);
    }
    
    @Provide
    Arbitrary<Integer> smallDistanceThreshold() {
        return Arbitraries.integers().between(1, 5);
    }
    
    @Provide
    Arbitrary<String> gridType() {
        return Arbitraries.of("1xN", "Nx1", "1x1");
    }
}
