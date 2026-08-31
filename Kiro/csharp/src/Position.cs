namespace GridNeighborhoods;

/// <summary>
/// A cell position in the grid, identified by (row, column).
/// (0,0) represents the bottom-left corner per the spec glossary.
///
/// Requirements 2.1-2.3: Manhattan distance calculation.
/// </summary>
public readonly record struct Position(long Row, long Column)
{
    /// <summary>
    /// Manhattan distance to another position: |r1-r2| + |c1-c2|.
    /// Requirement 2.1: computes |row1 - row2| + |column1 - column2|.
    /// Requirement 2.2: always non-negative.
    /// Requirement 2.3: 0 when positions are identical.
    /// </summary>
    public long ManhattanDistance(Position other)
        => Math.Abs(Row - other.Row) + Math.Abs(Column - other.Column);
}
