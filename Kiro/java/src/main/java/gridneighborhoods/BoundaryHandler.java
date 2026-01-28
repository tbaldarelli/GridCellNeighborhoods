package gridneighborhoods;

import java.util.HashSet;
import java.util.Set;

/**
 * Handler for grid boundary validation and position filtering.
 */
public class BoundaryHandler {
    
    /**
     * Check if a position is within grid boundaries.
     * 
     * @param position Position to validate
     * @param grid Grid to check against
     * @return True if position is within grid bounds, False otherwise
     */
    public static boolean isWithinBounds(Position position, Grid grid) {
        return position.getRow() >= 0 && position.getRow() < grid.getHeight() &&
               position.getColumn() >= 0 && position.getColumn() < grid.getWidth();
    }
    
    /**
     * Filter a set of positions to only include those within grid boundaries.
     * 
     * @param positions Set of positions to filter
     * @param grid Grid to check against
     * @return Set of positions that are within grid boundaries
     */
    public static Set<Position> filterValidPositions(Set<Position> positions, Grid grid) {
        Set<Position> validPositions = new HashSet<>();
        for (Position pos : positions) {
            if (isWithinBounds(pos, grid)) {
                validPositions.add(pos);
            }
        }
        return validPositions;
    }
}
