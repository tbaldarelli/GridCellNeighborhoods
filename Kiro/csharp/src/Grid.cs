namespace GridNeighborhoods;

/// <summary>
/// A 2D grid of Height x Width with a set of positive-valued cells.
/// Invariants: Height &gt; 0, Width &gt; 0; all positive cells lie in bounds.
///
/// Requirements 1.1-1.4: grid initialization and validation.
/// </summary>
public sealed class Grid
{
    public long Height { get; }
    public long Width { get; }

    private readonly HashSet<Position> _positiveCells;

    /// <summary>
    /// Create a grid with the given dimensions and positive cell positions.
    /// Requirement 1.1: validates Height &gt; 0 and Width &gt; 0.
    /// Requirement 1.2: validates positive cells are in bounds.
    /// Requirement 1.4: stores positive cell positions.
    /// </summary>
    public Grid(long height, long width, IEnumerable<Position>? positiveCells = null)
    {
        if (height <= 0 || width <= 0)
            throw new InvalidGridDimensionsException(height, width);

        Height = height;
        Width = width;
        _positiveCells = new HashSet<Position>();

        if (positiveCells is not null)
        {
            foreach (var pos in positiveCells)
            {
                if (pos.Row < 0 || pos.Row >= height || pos.Column < 0 || pos.Column >= width)
                    throw new PositionOutOfBoundsException(pos, height, width);
                _positiveCells.Add(pos);
            }
        }
    }

    /// <summary>The stored positive cell positions (Requirement 1.4).</summary>
    public IReadOnlyCollection<Position> PositiveCells => _positiveCells;

    /// <summary>
    /// Whether the position lies within the grid boundaries.
    /// Requirement 1.3 / 6.x: no wraparound.
    /// </summary>
    public bool IsValidPosition(Position pos)
        => pos.Row >= 0 && pos.Row < Height && pos.Column >= 0 && pos.Column < Width;
}
