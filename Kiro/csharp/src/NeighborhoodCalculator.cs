namespace GridNeighborhoods;

/// <summary>
/// Neighborhood calculator: diamond enumeration + union.
///
/// Core algorithm from design.md:
///   for deltaRow in -N..N:
///       remaining = N - |deltaRow|
///       for deltaCol in -remaining..remaining:
///           candidate = (center.Row + deltaRow, center.Column + deltaCol)
///           if IsValidPosition(candidate): add to set
///
/// Requirements 3.x, 4.x, 5.x, 7.x.
/// </summary>
public sealed class NeighborhoodCalculator
{
    /// <summary>
    /// Enumerate the neighborhood of a single center within Manhattan distance N,
    /// clipped to the grid boundaries.
    ///
    /// Requirement 3.1: center is included. 3.2: full in-bounds diamond. 3.3: no OOB cells.
    /// Requirement 8.3 / design "Early Termination": the delta ranges are clamped to the
    /// farthest reachable grid cell so an N far larger than the grid does not drive a huge
    /// empty scan (e.g. scenario 23: 2x2 grid, N=100000).
    /// </summary>
    public HashSet<Position> EnumerateNeighborhood(Grid grid, Position center, long n)
    {
        var neighborhood = new HashSet<Position>();

        long maxRowReach = Math.Max(center.Row, grid.Height - 1 - center.Row);
        long rowSpan = Math.Min(n, maxRowReach);

        for (long deltaRow = -rowSpan; deltaRow <= rowSpan; deltaRow++)
        {
            long remaining = n - Math.Abs(deltaRow);
            long maxColReach = Math.Max(center.Column, grid.Width - 1 - center.Column);
            long colSpan = Math.Min(remaining, maxColReach);

            for (long deltaCol = -colSpan; deltaCol <= colSpan; deltaCol++)
            {
                var candidate = new Position(center.Row + deltaRow, center.Column + deltaCol);
                if (grid.IsValidPosition(candidate))
                    neighborhood.Add(candidate);
            }
        }
        return neighborhood;
    }

    /// <summary>
    /// The union of all positive-cell neighborhoods within distance N.
    /// Requirements 3.4 / 4.2 / 5.1 (uniqueness), 5.2 (union), 7.1 (empty set -&gt; empty).
    /// </summary>
    public HashSet<Position> GetNeighborhoodCells(Grid grid, long distanceThreshold)
    {
        if (distanceThreshold < 0)
            throw new InvalidDistanceThresholdException(distanceThreshold);

        var allCells = new HashSet<Position>();
        foreach (var center in grid.PositiveCells)
            allCells.UnionWith(EnumerateNeighborhood(grid, center, distanceThreshold));
        return allCells;
    }

    /// <summary>
    /// Count of unique cells across all positive-cell neighborhoods.
    /// Requirement 7.2: N=0 counts only positive cells. 7.3: large N counts all reachable cells.
    /// </summary>
    public int CountNeighborhoodCells(Grid grid, long distanceThreshold)
        => GetNeighborhoodCells(grid, distanceThreshold).Count;
}
