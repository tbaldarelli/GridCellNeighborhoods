namespace GridNeighborhoods;

/// <summary>
/// Boundary handling: exclude out-of-bounds cells, no wraparound.
/// Requirements 6.1-6.3.
/// </summary>
public static class BoundaryHandler
{
    /// <summary>Whether a position is within the grid boundaries (Requirement 6.2: no wraparound).</summary>
    public static bool IsWithinBounds(Position pos, Grid grid) => grid.IsValidPosition(pos);

    /// <summary>Retain only positions within the grid boundaries (Requirements 6.1, 6.3).</summary>
    public static HashSet<Position> FilterValidPositions(IEnumerable<Position> positions, Grid grid)
    {
        var result = new HashSet<Position>();
        foreach (var pos in positions)
            if (grid.IsValidPosition(pos))
                result.Add(pos);
        return result;
    }
}
