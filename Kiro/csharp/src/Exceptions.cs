namespace GridNeighborhoods;

/// <summary>Base type for grid neighborhood errors.</summary>
public abstract class GridNeighborhoodsException : Exception
{
    protected GridNeighborhoodsException(string message) : base(message) { }
}

/// <summary>
/// Thrown when a grid is created with height &lt;= 0 or width &lt;= 0.
/// Requirement 8.1.
/// </summary>
public sealed class InvalidGridDimensionsException : GridNeighborhoodsException
{
    public InvalidGridDimensionsException(long height, long width)
        : base($"invalid grid dimensions: height={height} width={width} (both must be > 0)") { }
}

/// <summary>
/// Thrown when a positive cell position falls outside the grid boundaries.
/// Requirement 8.2.
/// </summary>
public sealed class PositionOutOfBoundsException : GridNeighborhoodsException
{
    public PositionOutOfBoundsException(Position position, long height, long width)
        : base($"position ({position.Row}, {position.Column}) is out of bounds for a {height}x{width} grid") { }
}

/// <summary>
/// Thrown when the distance threshold N is negative.
/// Requirement 8.3.
/// </summary>
public sealed class InvalidDistanceThresholdException : GridNeighborhoodsException
{
    public InvalidDistanceThresholdException(long threshold)
        : base($"invalid distance threshold: {threshold} (must be >= 0)") { }
}
