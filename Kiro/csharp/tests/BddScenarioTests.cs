using GridNeighborhoods;
using Xunit;
using Xunit.Abstractions;

namespace GridNeighborhoods.Tests;

/// <summary>
/// The 26 canonical BDD scenarios from the spec. Each test prints the
/// standardized cross-language output line and asserts the expected count.
/// </summary>
public class BddScenarioTests
{
    private readonly ITestOutputHelper _output;

    public BddScenarioTests(ITestOutputHelper output) => _output = output;

    private void RunScenario(int scenario, int expected, long height, long width, long n,
        params (long Row, long Column)[] positions)
    {
        var cells = positions.Select(p => new Position(p.Row, p.Column)).ToArray();
        var grid = new Grid(height, width, cells);
        var calculator = new NeighborhoodCalculator();
        int got = calculator.CountNeighborhoodCells(grid, n);

        string posStr = string.Join(",", positions.Select(p => $"({p.Row},{p.Column})"));
        _output.WriteLine(
            $"Scenario {scenario}: Expected={expected}, Grid={height}x{width}, N={n}, Pos=[{posStr}], Got={got}");
        Assert.Equal(expected, got);
    }

    [Fact] public void Scenario1_SingleCellFullyContained() => RunScenario(1, 25, 11, 11, 3, (5, 5));
    [Fact] public void Scenario2_SingleCellNearEdge() => RunScenario(2, 21, 11, 11, 3, (5, 1));
    [Fact] public void Scenario3_NonOverlapping() => RunScenario(3, 26, 11, 11, 2, (3, 3), (7, 7));
    [Fact] public void Scenario4_Overlapping() => RunScenario(4, 22, 11, 11, 2, (3, 3), (4, 5));
    [Fact] public void Scenario5_OverlappingOobLeft() => RunScenario(5, 18, 11, 11, 2, (3, 0), (4, 2));
    [Fact] public void Scenario6_OverlappingOobBottomLeft() => RunScenario(6, 14, 11, 11, 2, (0, 0), (1, 2));
    [Fact] public void Scenario7_OverlappingOobBottom() => RunScenario(7, 17, 11, 11, 2, (0, 3), (1, 5));
    [Fact] public void Scenario8_OverlappingOobRight() => RunScenario(8, 18, 11, 11, 2, (3, 8), (4, 10));
    [Fact] public void Scenario9_OverlappingOobTop() => RunScenario(9, 17, 11, 11, 2, (9, 3), (10, 5));
    [Fact] public void Scenario10_DiagonallyAdjacent() => RunScenario(10, 18, 11, 11, 2, (3, 3), (4, 4));
    [Fact] public void Scenario11_SameRowAdjacent() => RunScenario(11, 18, 11, 11, 2, (3, 3), (3, 4));
    [Fact] public void Scenario12_SameColumnAdjacent() => RunScenario(12, 18, 11, 11, 2, (3, 4), (4, 4));
    [Fact] public void Scenario13_OppositeCorners() => RunScenario(13, 20, 11, 11, 3, (0, 0), (10, 10));
    [Fact] public void Scenario14_ThreeInOneCorner() => RunScenario(14, 15, 11, 11, 3, (10, 9), (9, 10), (10, 10));
    [Fact] public void Scenario15_1x21Grid() => RunScenario(15, 7, 1, 21, 3, (0, 9));
    [Fact] public void Scenario16_21x1Grid() => RunScenario(16, 7, 21, 1, 3, (10, 0));
    [Fact] public void Scenario17_1x1Grid() => RunScenario(17, 1, 1, 1, 0, (0, 0));
    [Fact] public void Scenario18_20x20ThresholdZero() => RunScenario(18, 1, 20, 20, 0, (0, 0));
    [Fact] public void Scenario19_2x2Grid() => RunScenario(19, 4, 2, 2, 2, (0, 1));
    [Fact] public void Scenario20_21x3NGreaterThanW() => RunScenario(20, 27, 21, 3, 5, (10, 2));
    [Fact] public void Scenario21_4x15NGreaterThanH() => RunScenario(21, 36, 4, 15, 5, (2, 9));
    [Fact] public void Scenario22_2x2NGreaterThanBoth() => RunScenario(22, 4, 2, 2, 3, (0, 1));
    [Fact] public void Scenario23_2x2NMuchGreater() => RunScenario(23, 4, 2, 2, 100000, (0, 1));
    [Fact] public void Scenario24_11x11CornerLargeN() => RunScenario(24, 85, 11, 11, 12, (0, 0));
    [Fact] public void Scenario25_11x11CenterLargeN() => RunScenario(25, 121, 11, 11, 12, (5, 5));
    [Fact] public void Scenario26_NoPositiveCells() => RunScenario(26, 0, 10, 10, 3);
}
