package gridneighborhoods.exceptions;

import gridneighborhoods.Position;

/**
 * Exception raised when a position is outside grid boundaries.
 * 
 * This exception is raised when attempting to access or validate
 * a position that falls outside the valid grid coordinates.
 */
public class PositionOutOfBoundsException extends RuntimeException {
    private final Position position;
    private final int gridHeight;
    private final int gridWidth;
    
    /**
     * Initialize the exception with position and grid information.
     * 
     * @param position The invalid position
     * @param gridHeight The grid height
     * @param gridWidth The grid width
     */
    public PositionOutOfBoundsException(Position position, int gridHeight, int gridWidth) {
        this(position, gridHeight, gridWidth, null);
    }
    
    /**
     * Initialize the exception with position, grid information, and custom message.
     * 
     * @param position The invalid position
     * @param gridHeight The grid height
     * @param gridWidth The grid width
     * @param message Optional custom error message
     */
    public PositionOutOfBoundsException(Position position, int gridHeight, int gridWidth, String message) {
        super(message != null ? message : buildMessage(position, gridHeight, gridWidth));
        this.position = position;
        this.gridHeight = gridHeight;
        this.gridWidth = gridWidth;
    }
    
    private static String buildMessage(Position position, int gridHeight, int gridWidth) {
        return String.format("Position (%d, %d) is out of bounds for grid %dx%d. Valid range: row [0, %d], column [0, %d]",
                position.getRow(), position.getColumn(), gridHeight, gridWidth, gridHeight - 1, gridWidth - 1);
    }
    
    public Position getPosition() {
        return position;
    }
    
    public int getGridHeight() {
        return gridHeight;
    }
    
    public int getGridWidth() {
        return gridWidth;
    }
}
