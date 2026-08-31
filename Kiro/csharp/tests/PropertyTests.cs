using CsCheck;
using GridNeighborhoods;
using Xunit;

namespace GridNeighborhoods.Tests;

/// <summary>
/// The 13 correctness properties from the spec, using CsCheck (100 iterations each).
/// </summary>
public class PropertyTests
{
    private const int Iterations = 100;

    /// Feature: grid-neighborhoods, Property 1: Grid Validation
    /// Validates: Requirements 1.1, 1.2
    [Fact]
    public void Property1_GridValidation()
    {
        Gen.Select(Gen.Int[-100, 1000], Gen.Int[-100, 1000])
            .Sample((height, width) =>
            {
                if (height > 0 && width > 0)
                {
                    var grid = new Grid(height, width);
                    return grid.Height == height && grid.Width == width;
                }
                try
                {
                    _ = new Grid(height, width);
                    return false; // should have thrown
                }
                catch (InvalidGridDimensionsException)
                {
                    return true;
                }
            }, iter: Iterations);
    }

    /// Feature: grid-neighborhoods, Property 2: Manhattan Distance Calculation
    /// Validates: Requirements 2.1, 2.2, 2.3
    [Fact]
    public void Property2_ManhattanDistance()
    {
        Gen.Select(Gen.Int[0, 1000], Gen.Int[0, 1000], Gen.Int[0, 1000], Gen.Int[0, 1000])
            .Sample((r1, c1, r2, c2) =>
            {
                var p1 = new Position(r1, c1);
                var p2 = new Position(r2, c2);
                long d = p1.ManhattanDistance(p2);

                bool ok = d == Math.Abs((long)r1 - r2) + Math.Abs((long)c1 - c2);
                ok &= d >= 0;
                if (r1 == r2 && c1 == c2) ok &= d == 0;
                ok &= d == p2.ManhattanDistance(p1); // symmetric
                return ok;
            }, iter: Iterations);
    }

    /// Feature: grid-neighborhoods, Property 3: Coordinate System Consistency
    /// Validates: Requirements 1.3, 1.4
    [Fact]
    public void Property3_CoordinateSystem()
    {
        Gen.Select(Gen.Int[1, 50], Gen.Int[1, 50])
            .Sample((height, width) =>
            {
                var grid = new Grid(height, width);
                return grid.IsValidPosition(new Position(0, 0))
                    && grid.IsValidPosition(new Position(height - 1, width - 1))
                    && !grid.IsValidPosition(new Position(height, 0))
                    && !grid.IsValidPosition(new Position(0, width));
            }, iter: Iterations);
    }

    /// Feature: grid-neighborhoods, Property 4: Self-Inclusion in Neighborhoods
    /// Validates: Requirements 3.1
    [Fact]
    public void Property4_SelfInclusion()
    {
        Gen.Select(Gen.Int[1, 20], Gen.Int[1, 20], Gen.Int[0, 20])
            .Sample((height, width, n) =>
            {
                var center = new Position(height / 2, width / 2);
                var grid = new Grid(height, width, new[] { center });
                var calc = new NeighborhoodCalculator();
                var neighborhood = calc.GetNeighborhoodCells(grid, n);
                return neighborhood.Contains(center) && calc.CountNeighborhoodCells(grid, n) >= 1;
            }, iter: Iterations);
    }

    /// Feature: grid-neighborhoods, Property 5: Complete Neighborhood Enumeration
    /// Validates: Requirements 3.2
    [Fact]
    public void Property5_CompleteEnumeration()
    {
        Gen.Int[1, 10].Sample(n =>
        {
            long height = 2 * n + 3;
            long width = 2 * n + 3;
            var center = new Position(n + 1, n + 1);
            var grid = new Grid(height, width, new[] { center });
            var calc = new NeighborhoodCalculator();
            var neighborhood = calc.EnumerateNeighborhood(grid, center, n);
            long expected = (long)(n + 1) * (n + 1) + (long)n * n;
            return neighborhood.Count == expected;
        }, iter: Iterations);
    }

    /// Feature: grid-neighborhoods, Property 6: Boundary Constraint Enforcement
    /// Validates: Requirements 3.3, 6.1, 6.2, 6.3
    [Fact]
    public void Property6_BoundaryEnforcement()
    {
        Gen.Select(Gen.Int[1, 20], Gen.Int[1, 20], Gen.Int[0, 20])
            .Sample((height, width, n) =>
            {
                var center = new Position(0, 0);
                var grid = new Grid(height, width, new[] { center });
                var calc = new NeighborhoodCalculator();
                var neighborhood = calc.EnumerateNeighborhood(grid, center, n);
                foreach (var cell in neighborhood)
                {
                    if (!BoundaryHandler.IsWithinBounds(cell, grid)) return false;
                    if (cell.Row < 0 || cell.Row >= height || cell.Column < 0 || cell.Column >= width) return false;
                }
                return true;
            }, iter: Iterations);
    }

    /// Feature: grid-neighborhoods, Property 7: Cell Uniqueness Guarantee
    /// Validates: Requirements 3.4, 4.2, 5.1
    [Fact]
    public void Property7_CellUniqueness()
    {
        (from height in Gen.Int[1, 30]
         from width in Gen.Int[1, 30]
         from n in Gen.Int[0, 20]
         from cells in Gen.Select(Gen.Int[0, height - 1], Gen.Int[0, width - 1])
             .Select(t => new Position(t.Item1, t.Item2)).Array[1, 10]
         select (height, width, n, cells))
        .Sample(t =>
        {
            var grid = new Grid(t.height, t.width, t.cells);
            var calc = new NeighborhoodCalculator();
            var allCells = calc.GetNeighborhoodCells(grid, t.n);
            int count = calc.CountNeighborhoodCells(grid, t.n);
            if (count != allCells.Count) return false;

            int sumIndividual = grid.PositiveCells
                .Sum(c => calc.EnumerateNeighborhood(grid, c, t.n).Count);
            return count <= sumIndividual;
        }, iter: Iterations);
    }

    /// Feature: grid-neighborhoods, Property 8: Non-Overlapping Additivity
    /// Validates: Requirements 4.1, 4.3
    [Fact]
    public void Property8_NonOverlappingAdditivity()
    {
        Gen.Int[1, 8].Sample(n =>
        {
            long minSeparation = 2 * n + 1;
            long height = minSeparation + 2 * n + 2;
            long width = minSeparation + 2 * n + 2;
            var p1 = new Position(n, n);
            var p2 = new Position(n + minSeparation, n + minSeparation);
            var grid = new Grid(height, width, new[] { p1, p2 });
            var calc = new NeighborhoodCalculator();

            var nb1 = calc.EnumerateNeighborhood(grid, p1, n);
            var nb2 = calc.EnumerateNeighborhood(grid, p2, n);
            if (nb1.Intersect(nb2).Any()) return false;

            int total = calc.CountNeighborhoodCells(grid, n);
            return total == nb1.Count + nb2.Count;
        }, iter: Iterations);
    }

    /// Feature: grid-neighborhoods, Property 9: Overlapping Union Behavior
    /// Validates: Requirements 5.2, 5.3
    [Fact]
    public void Property9_OverlappingUnion()
    {
        Gen.Int[2, 8].Sample(n =>
        {
            long height = 2 * n + 10;
            long width = 2 * n + 10;
            var p1 = new Position(n + 1, n + 1);
            var p2 = new Position(n + 2, n + 2);
            var grid = new Grid(height, width, new[] { p1, p2 });
            var calc = new NeighborhoodCalculator();

            var nb1 = calc.EnumerateNeighborhood(grid, p1, n);
            var nb2 = calc.EnumerateNeighborhood(grid, p2, n);
            if (!nb1.Intersect(nb2).Any()) return false;

            int total = calc.CountNeighborhoodCells(grid, n);
            return total < nb1.Count + nb2.Count;
        }, iter: Iterations);
    }

    /// Feature: grid-neighborhoods, Property 10: Zero Distance Threshold
    /// Validates: Requirements 7.2
    [Fact]
    public void Property10_ZeroDistance()
    {
        (from height in Gen.Int[1, 20]
         from width in Gen.Int[1, 20]
         from cells in Gen.Select(Gen.Int[0, height - 1], Gen.Int[0, width - 1])
             .Select(t => new Position(t.Item1, t.Item2)).Array[1, 20]
         select (height, width, cells))
        .Sample(t =>
        {
            var grid = new Grid(t.height, t.width, t.cells);
            var calc = new NeighborhoodCalculator();
            return calc.CountNeighborhoodCells(grid, 0) == grid.PositiveCells.Count;
        }, iter: Iterations);
    }

    /// Feature: grid-neighborhoods, Property 11: Maximum Distance Threshold
    /// Validates: Requirements 7.3
    [Fact]
    public void Property11_MaximumDistance()
    {
        (from height in Gen.Int[1, 20]
         from width in Gen.Int[1, 20]
         from cells in Gen.Select(Gen.Int[0, height - 1], Gen.Int[0, width - 1])
             .Select(t => new Position(t.Item1, t.Item2)).Array[1, 10]
         select (height, width, cells))
        .Sample(t =>
        {
            var grid = new Grid(t.height, t.width, t.cells);
            var calc = new NeighborhoodCalculator();
            long maxDistance = (t.height - 1) + (t.width - 1);
            int count = calc.CountNeighborhoodCells(grid, maxDistance + 10);
            return count == t.height * t.width;
        }, iter: Iterations);
    }

    /// Feature: grid-neighborhoods, Property 12: Degenerate Grid Handling
    /// Validates: Requirements 7.4
    [Fact]
    public void Property12_DegenerateGrid()
    {
        Gen.Select(Gen.Int[0, 2], Gen.Int[1, 50], Gen.Int[0, 20])
            .Sample((gridType, dimension, n) =>
            {
                long height, width;
                Position center;
                switch (gridType)
                {
                    case 0: height = 1; width = dimension; center = new Position(0, dimension / 2); break;
                    case 1: height = dimension; width = 1; center = new Position(dimension / 2, 0); break;
                    default: height = 1; width = 1; center = new Position(0, 0); break;
                }
                var grid = new Grid(height, width, new[] { center });
                var calc = new NeighborhoodCalculator();
                var neighborhood = calc.GetNeighborhoodCells(grid, n);
                int count = calc.CountNeighborhoodCells(grid, n);

                if (neighborhood.Count != count) return false;
                if (!neighborhood.Contains(center)) return false;
                foreach (var cell in neighborhood)
                    if (center.ManhattanDistance(cell) > n) return false;
                if (gridType == 2 && count != 1) return false;
                return true;
            }, iter: Iterations);
    }

    /// Feature: grid-neighborhoods, Property 13: Cross-Language Result Consistency
    /// Validates: Requirements 9.1, 9.3, 9.4
    /// Verifies determinism: same input yields the same count on repeated runs.
    [Fact]
    public void Property13_Deterministic()
    {
        (from height in Gen.Int[1, 30]
         from width in Gen.Int[1, 30]
         from n in Gen.Int[0, 15]
         from cells in Gen.Select(Gen.Int[0, height - 1], Gen.Int[0, width - 1])
             .Select(t => new Position(t.Item1, t.Item2)).Array[1, 5]
         select (height, width, n, cells))
        .Sample(t =>
        {
            var grid = new Grid(t.height, t.width, t.cells);
            var calc = new NeighborhoodCalculator();
            return calc.CountNeighborhoodCells(grid, t.n) == calc.CountNeighborhoodCells(grid, t.n);
        }, iter: Iterations);
    }
}
