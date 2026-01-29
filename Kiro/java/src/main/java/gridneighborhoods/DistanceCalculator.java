package gridneighborhoods;

/**
 * Calculator for Manhattan distance between grid positions.
 */
public class DistanceCalculator {
    
    /**
     * Calculate Manhattan distance between two positions.
     * 
     * @param pos1 First position
     * @param pos2 Second position
     * @return Manhattan distance as a non-negative integer
     */
    public static int calculateManhattanDistance(Position pos1, Position pos2) {
        return Math.abs(pos1.getRow() - pos2.getRow()) + Math.abs(pos1.getColumn() - pos2.getColumn());
    }
}
