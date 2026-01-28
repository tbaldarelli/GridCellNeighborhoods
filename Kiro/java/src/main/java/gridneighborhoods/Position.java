package gridneighborhoods;

import java.util.Objects;

/**
 * Represents a position in a 2D grid with row and column coordinates.
 * 
 * The coordinate system uses (0,0) as the bottom-left corner of the grid.
 */
public class Position {
    private final int row;
    private final int column;
    
    /**
     * Initialize a position with row and column coordinates.
     * 
     * @param row The row coordinate (>= 0)
     * @param column The column coordinate (>= 0)
     * @throws IllegalArgumentException If row or column is negative
     */
    public Position(int row, int column) {
        if (row < 0) {
            throw new IllegalArgumentException("Row must be non-negative, got " + row);
        }
        if (column < 0) {
            throw new IllegalArgumentException("Column must be non-negative, got " + column);
        }
        this.row = row;
        this.column = column;
    }
    
    /**
     * Calculate Manhattan distance to another position.
     * 
     * @param other Another Position instance
     * @return The Manhattan distance as a non-negative integer
     */
    public int manhattanDistance(Position other) {
        return Math.abs(this.row - other.row) + Math.abs(this.column - other.column);
    }
    
    public int getRow() {
        return row;
    }
    
    public int getColumn() {
        return column;
    }
    
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Position position = (Position) o;
        return row == position.row && column == position.column;
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(row, column);
    }
    
    @Override
    public String toString() {
        return "Position(" + row + ", " + column + ")";
    }
}
