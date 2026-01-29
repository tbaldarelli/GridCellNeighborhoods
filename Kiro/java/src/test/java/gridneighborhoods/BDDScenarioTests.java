package gridneighborhoods;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestMethodOrder;
import org.junit.jupiter.api.MethodOrderer;
import org.junit.jupiter.api.Order;
import static org.junit.jupiter.api.Assertions.*;

/**
 * BDD scenario tests for grid neighborhoods.
 * 
 * This test suite implements the 26 BDD scenarios from the design document.
 * Each scenario validates the system against concrete examples with specific expected counts.
 * 
 * All scenarios use an 11x11 grid unless otherwise specified.
 * 
 * Tests are executed in the order specified by @Order annotations.
 */
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class BDDScenarioTests {
    
    // Single Positive Cell Scenarios (1-2)
    
    @Test
    @Order(1)
    void testScenario1_SinglePositiveCellFullyContained() {
        Grid grid = new Grid(11, 11);
        grid.setCellValue(new Position(5, 5), 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        int count = calculator.countNeighborhoodCells(grid, 3);
        
        System.out.println("Scenario 1: Expected=25, Grid=11x11, N=3, Pos=[(5,5)], Got=" + count);
        assertEquals(25, count);
    }
    
    @Test
    @Order(2)
    void testScenario2_SinglePositiveCellNearEdge() {
        Grid grid = new Grid(11, 11);
        grid.setCellValue(new Position(5, 1), 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        int count = calculator.countNeighborhoodCells(grid, 3);
        
        System.out.println("Scenario 2: Expected=21, Grid=11x11, N=3, Pos=[(5,1)], Got=" + count);
        assertEquals(21, count);
    }
    
    // Multiple Positive Cells Non-Overlapping (3)
    
    @Test
    @Order(3)
    void testScenario3_NonOverlappingNeighborhoods() {
        Grid grid = new Grid(11, 11);
        grid.setCellValue(new Position(3, 3), 1);
        grid.setCellValue(new Position(7, 7), 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        int count = calculator.countNeighborhoodCells(grid, 2);
        
        System.out.println("Scenario 3: Expected=26, Grid=11x11, N=2, Pos=[(3,3),(7,7)], Got=" + count);
        assertEquals(26, count);
    }
    
    // Multiple Positive Cells Overlapping (4-14)
    
    @Test
    @Order(4)
    void testScenario4_OverlappingNeighborhoods() {
        Grid grid = new Grid(11, 11);
        grid.setCellValue(new Position(3, 3), 1);
        grid.setCellValue(new Position(4, 5), 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        int count = calculator.countNeighborhoodCells(grid, 2);
        
        System.out.println("Scenario 4: Expected=22, Grid=11x11, N=2, Pos=[(3,3),(4,5)], Got=" + count);
        assertEquals(22, count);
    }
    
    @Test
    @Order(5)
    void testScenario5_OverlappingOutOfBoundsLeft() {
        Grid grid = new Grid(11, 11);
        grid.setCellValue(new Position(3, 0), 1);
        grid.setCellValue(new Position(4, 2), 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        int count = calculator.countNeighborhoodCells(grid, 2);
        
        System.out.println("Scenario 5: Expected=18, Grid=11x11, N=2, Pos=[(3,0),(4,2)], Got=" + count);
        assertEquals(18, count);
    }
    
    @Test
    @Order(6)
    void testScenario6_OverlappingOutOfBoundsBottomLeft() {
        Grid grid = new Grid(11, 11);
        grid.setCellValue(new Position(0, 0), 1);
        grid.setCellValue(new Position(1, 2), 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        int count = calculator.countNeighborhoodCells(grid, 2);
        
        System.out.println("Scenario 6: Expected=14, Grid=11x11, N=2, Pos=[(0,0),(1,2)], Got=" + count);
        assertEquals(14, count);
    }
    
    @Test
    @Order(7)
    void testScenario7_OverlappingOutOfBoundsBottom() {
        Grid grid = new Grid(11, 11);
        grid.setCellValue(new Position(0, 3), 1);
        grid.setCellValue(new Position(1, 5), 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        int count = calculator.countNeighborhoodCells(grid, 2);
        
        System.out.println("Scenario 7: Expected=17, Grid=11x11, N=2, Pos=[(0,3),(1,5)], Got=" + count);
        assertEquals(17, count);
    }
    
    @Test
    @Order(8)
    void testScenario8_OverlappingOutOfBoundsRight() {
        Grid grid = new Grid(11, 11);
        grid.setCellValue(new Position(3, 8), 1);
        grid.setCellValue(new Position(4, 10), 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        int count = calculator.countNeighborhoodCells(grid, 2);
        
        System.out.println("Scenario 8: Expected=18, Grid=11x11, N=2, Pos=[(3,8),(4,10)], Got=" + count);
        assertEquals(18, count);
    }
    
    @Test
    @Order(9)
    void testScenario9_OverlappingOutOfBoundsTop() {
        Grid grid = new Grid(11, 11);
        grid.setCellValue(new Position(9, 3), 1);
        grid.setCellValue(new Position(10, 5), 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        int count = calculator.countNeighborhoodCells(grid, 2);
        
        System.out.println("Scenario 9: Expected=17, Grid=11x11, N=2, Pos=[(9,3),(10,5)], Got=" + count);
        assertEquals(17, count);
    }
    
    @Test
    @Order(10)
    void testScenario10_OverlappingDiagonallyAdjacent() {
        Grid grid = new Grid(11, 11);
        grid.setCellValue(new Position(3, 3), 1);
        grid.setCellValue(new Position(4, 4), 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        int count = calculator.countNeighborhoodCells(grid, 2);
        
        System.out.println("Scenario 10: Expected=18, Grid=11x11, N=2, Pos=[(3,3),(4,4)], Got=" + count);
        assertEquals(18, count);
    }
    
    @Test
    @Order(11)
    void testScenario11_OverlappingSameRowAdjacent() {
        Grid grid = new Grid(11, 11);
        grid.setCellValue(new Position(3, 3), 1);
        grid.setCellValue(new Position(3, 4), 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        int count = calculator.countNeighborhoodCells(grid, 2);
        
        System.out.println("Scenario 11: Expected=18, Grid=11x11, N=2, Pos=[(3,3),(3,4)], Got=" + count);
        assertEquals(18, count);
    }
    
    @Test
    @Order(12)
    void testScenario12_OverlappingSameColumnAdjacent() {
        Grid grid = new Grid(11, 11);
        grid.setCellValue(new Position(3, 4), 1);
        grid.setCellValue(new Position(4, 4), 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        int count = calculator.countNeighborhoodCells(grid, 2);
        
        System.out.println("Scenario 12: Expected=18, Grid=11x11, N=2, Pos=[(3,4),(4,4)], Got=" + count);
        assertEquals(18, count);
    }
    
    @Test
    @Order(13)
    void testScenario13_OppositeCorners() {
        Grid grid = new Grid(11, 11);
        grid.setCellValue(new Position(0, 0), 1);
        grid.setCellValue(new Position(10, 10), 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        int count = calculator.countNeighborhoodCells(grid, 3);
        
        System.out.println("Scenario 13: Expected=20, Grid=11x11, N=3, Pos=[(0,0),(10,10)], Got=" + count);
        assertEquals(20, count);
    }
    
    @Test
    @Order(14)
    void testScenario14_ThreeInOneCorner() {
        Grid grid = new Grid(11, 11);
        grid.setCellValue(new Position(10, 9), 1);
        grid.setCellValue(new Position(9, 10), 1);
        grid.setCellValue(new Position(10, 10), 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        int count = calculator.countNeighborhoodCells(grid, 3);
        
        System.out.println("Scenario 14: Expected=15, Grid=11x11, N=3, Pos=[(10,9),(9,10),(10,10)], Got=" + count);
        assertEquals(15, count);
    }
    
    // Degenerate Grid Scenarios (15-25)
    
    @Test
    @Order(15)
    void testScenario15_1x21Grid() {
        Grid grid = new Grid(1, 21);
        grid.setCellValue(new Position(0, 9), 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        int count = calculator.countNeighborhoodCells(grid, 3);
        
        System.out.println("Scenario 15: Expected=7, Grid=1x21, N=3, Pos=[(0,9)], Got=" + count);
        assertEquals(7, count);
    }
    
    @Test
    @Order(16)
    void testScenario16_21x1Grid() {
        Grid grid = new Grid(21, 1);
        grid.setCellValue(new Position(10, 0), 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        int count = calculator.countNeighborhoodCells(grid, 3);
        
        System.out.println("Scenario 16: Expected=7, Grid=21x1, N=3, Pos=[(10,0)], Got=" + count);
        assertEquals(7, count);
    }
    
    @Test
    @Order(17)
    void testScenario17_1x1Grid() {
        Grid grid = new Grid(1, 1);
        grid.setCellValue(new Position(0, 0), 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        int count = calculator.countNeighborhoodCells(grid, 0);
        
        System.out.println("Scenario 17: Expected=1, Grid=1x1, N=0, Pos=[(0,0)], Got=" + count);
        assertEquals(1, count);
    }
    
    @Test
    @Order(18)
    void testScenario18_20x20GridThresholdZero() {
        Grid grid = new Grid(20, 20);
        grid.setCellValue(new Position(0, 0), 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        int count = calculator.countNeighborhoodCells(grid, 0);
        
        System.out.println("Scenario 18: Expected=1, Grid=20x20, N=0, Pos=[(0,0)], Got=" + count);
        assertEquals(1, count);
    }
    
    @Test
    @Order(19)
    void testScenario19_2x2Grid() {
        Grid grid = new Grid(2, 2);
        grid.setCellValue(new Position(0, 1), 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        int count = calculator.countNeighborhoodCells(grid, 2);
        
        System.out.println("Scenario 19: Expected=4, Grid=2x2, N=2, Pos=[(0,1)], Got=" + count);
        assertEquals(4, count);
    }
    
    @Test
    @Order(20)
    void testScenario20_21x3GridNGreaterThanW() {
        Grid grid = new Grid(21, 3);
        grid.setCellValue(new Position(10, 2), 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        int count = calculator.countNeighborhoodCells(grid, 5);
        
        System.out.println("Scenario 20: Expected=27, Grid=21x3, N=5, Pos=[(10,2)], Got=" + count);
        assertEquals(27, count);
    }
    
    @Test
    @Order(21)
    void testScenario21_4x15GridNGreaterThanH() {
        Grid grid = new Grid(4, 15);
        grid.setCellValue(new Position(2, 9), 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        int count = calculator.countNeighborhoodCells(grid, 5);
        
        System.out.println("Scenario 21: Expected=36, Grid=4x15, N=5, Pos=[(2,9)], Got=" + count);
        assertEquals(36, count);
    }
    
    @Test
    @Order(22)
    void testScenario22_2x2GridNGreaterThanBoth() {
        Grid grid = new Grid(2, 2);
        grid.setCellValue(new Position(0, 1), 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        int count = calculator.countNeighborhoodCells(grid, 3);
        
        System.out.println("Scenario 22: Expected=4, Grid=2x2, N=3, Pos=[(0,1)], Got=" + count);
        assertEquals(4, count);
    }
    
    @Test
    @Order(23)
    void testScenario23_2x2GridNMuchGreater() {
        Grid grid = new Grid(2, 2);
        grid.setCellValue(new Position(0, 1), 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        int count = calculator.countNeighborhoodCells(grid, 100000);
        
        System.out.println("Scenario 23: Expected=4, Grid=2x2, N=100000, Pos=[(0,1)], Got=" + count);
        assertEquals(4, count);
    }
    
    @Test
    @Order(24)
    void testScenario24_11x11GridCornerLargeN() {
        Grid grid = new Grid(11, 11);
        grid.setCellValue(new Position(0, 0), 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        int count = calculator.countNeighborhoodCells(grid, 12);
        
        System.out.println("Scenario 24: Expected=85, Grid=11x11, N=12, Pos=[(0,0)], Got=" + count);
        assertEquals(85, count);
    }
    
    @Test
    @Order(25)
    void testScenario25_11x11GridCenterLargeN() {
        Grid grid = new Grid(11, 11);
        grid.setCellValue(new Position(5, 5), 1);
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        int count = calculator.countNeighborhoodCells(grid, 12);
        
        System.out.println("Scenario 25: Expected=121, Grid=11x11, N=12, Pos=[(5,5)], Got=" + count);
        assertEquals(121, count);
    }
    
    // No Positive Cells Scenario (26)
    
    @Test
    @Order(26)
    void testScenario26_NoPositiveCells() {
        Grid grid = new Grid(10, 10);
        // Grid is created with all zeros by default (no positive cells)
        
        NeighborhoodCalculator calculator = new NeighborhoodCalculator();
        int count = calculator.countNeighborhoodCells(grid, 3);
        
        System.out.println("Scenario 26: Expected=0, Grid=10x10, N=3, Pos=[], Got=" + count);
        assertEquals(0, count);
    }
}
