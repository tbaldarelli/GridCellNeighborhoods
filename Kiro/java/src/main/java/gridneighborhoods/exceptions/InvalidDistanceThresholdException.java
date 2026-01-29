package gridneighborhoods.exceptions;

/**
 * Exception raised when distance threshold is invalid.
 * 
 * This exception is raised when attempting to use a negative
 * distance threshold for neighborhood calculations.
 */
public class InvalidDistanceThresholdException extends RuntimeException {
    private final int distanceThreshold;
    
    /**
     * Initialize the exception with the invalid distance threshold.
     * 
     * @param distanceThreshold The invalid distance threshold value
     */
    public InvalidDistanceThresholdException(int distanceThreshold) {
        this(distanceThreshold, null);
    }
    
    /**
     * Initialize the exception with the invalid distance threshold and custom message.
     * 
     * @param distanceThreshold The invalid distance threshold value
     * @param message Optional custom error message
     */
    public InvalidDistanceThresholdException(int distanceThreshold, String message) {
        super(message != null ? message : "Distance threshold must be non-negative: got " + distanceThreshold);
        this.distanceThreshold = distanceThreshold;
    }
    
    public int getDistanceThreshold() {
        return distanceThreshold;
    }
}
