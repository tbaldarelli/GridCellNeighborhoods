package gridneighborhoods.exceptions;

/**
 * Exception raised when grid dimensions are invalid.
 * 
 * This exception is raised when attempting to create a grid with
 * non-positive height or width values.
 */
public class InvalidGridDimensionsException extends RuntimeException {
    private final int height;
    private final int width;
    
    /**
     * Initialize the exception with grid dimensions.
     * 
     * @param height The invalid height value
     * @param width The invalid width value
     */
    public InvalidGridDimensionsException(int height, int width) {
        this(height, width, null);
    }
    
    /**
     * Initialize the exception with grid dimensions and custom message.
     * 
     * @param height The invalid height value
     * @param width The invalid width value
     * @param message Optional custom error message
     */
    public InvalidGridDimensionsException(int height, int width, String message) {
        super(message != null ? message : buildMessage(height, width));
        this.height = height;
        this.width = width;
    }
    
    private static String buildMessage(int height, int width) {
        if (height <= 0 && width <= 0) {
            return "Grid dimensions must be positive: height=" + height + ", width=" + width;
        } else if (height <= 0) {
            return "Grid height must be positive: height=" + height;
        } else {
            return "Grid width must be positive: width=" + width;
        }
    }
    
    public int getHeight() {
        return height;
    }
    
    public int getWidth() {
        return width;
    }
}
