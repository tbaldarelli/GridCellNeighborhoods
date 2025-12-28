import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;

/**
 * Hello world!
 *
 */
public class GridCellNeighborhoodsWithinDistance 
{
    private record Position(int y, int x, int value) {}

    
    private final int distanceThreshold;
    private final int height;
    private final int width;
    private boolean debug = false;
    private boolean listUniqueCells = false;
    private final List<List<GridCellNeighborhoodsWithinDistance.Position>> rows;
    private final int numPositiveValues;
    private final String label;
    private boolean alwaysAddHomeBase = false;

    public GridCellNeighborhoodsWithinDistance( int distanceThreshold, int height, int width, String label, Position... positivePositions ) {
        this.distanceThreshold = distanceThreshold;
        this.height = height;
        this.width = width;
        this.label = label;

        rows = buildGrid(height, width, positivePositions);
        this.numPositiveValues = positivePositions != null ? positivePositions.length : 0;
    }

    public boolean isListUniqueCells() {
        return listUniqueCells;
    }

    public void setListUniqueCells(boolean listCells) {
        this.listUniqueCells = listCells;
    }

    public boolean isDebug() {
        return debug;
    }

    
    public boolean isAlwaysAddHomeBase() {
        return alwaysAddHomeBase;
    }

    public void setAlwaysAddHomeBase(boolean alwaysAddHomeBase) {
        this.alwaysAddHomeBase = alwaysAddHomeBase;
    }

    public void setDebug(boolean debug) {
        this.debug = debug;
    }
    
    private List<List<Position>> buildGrid(int height, int width, Position... positivePositions) throws IllegalArgumentException {
        
        List<List<Position>> rows = new ArrayList<>();
        List<Position> positivePositionsAdded = new ArrayList<>();
        for (int y = 0; y < height; y++) {
            List<Position> row = new ArrayList<>();
            for (int x = 0; x < width; x++) {
                boolean isPositivePosition = false;
                if(positivePositions != null) {
                    for (Position pos : positivePositions) {
                        if (pos.y() == y && pos.x() == x) {
                            isPositivePosition = true;
                            row.add(pos);
                            positivePositionsAdded.add(pos);
                            break;
                        }
                    }
                }
                
                if(!isPositivePosition )
                    row.add(new Position(y, x, -1));
            }
            rows.add(row);
        }

        if(positivePositions != null && positivePositionsAdded.size() != positivePositions.length) {
            throw new IllegalArgumentException("Some positive positions were not added to the grid. Check that all positive positions are within the grid bounds.");
        } 

        return rows;
    }

    private int manhattanDistance(Position p1, Position p2) {
        return Math.abs(p1.x() - p2.x()) + Math.abs(p1.y() - p2.y());
    }

    private int countGridCellsWithinNeighborhood() {
        // Unique list of all cells in all neighborhoods
        Set<Position> visited = new TreeSet<Position>( new Comparator<Position>() {
            @Override
            public int compare(Position o1, Position o2) {
                Position p1 = (Position)o1;
                Position p2 = (Position)o2;
                if (p1.y() != p2.y()) {
                    return Integer.compare(p1.y(), p2.y());
                } else {
                    return Integer.compare(p1.x(), p2.x());
                }
            }
        });

        // List of home bases, so cells with positive numbers.
        List<Position> homeBases = new ArrayList<>();

        // Should be a property with setting/getter, but ignoring for now.
        boolean fullSquare = false;


        // find positive value(s) and calculate grid cell neighborhoods
        for( List<Position> row : rows )
        {
            // First of all, find all cells with positive values in current row.
            List<Position> positiveCells = row.stream()
                .filter( p -> p.value() > 0)
                .toList();
            
            if(positiveCells instanceof List && positiveCells.size() > 0)
            {
                // For each positive cell, calculate its neighborhood
                for(Position pos : positiveCells)
                {
                    if(isDebug())
                        System.out.println("Found positive value at (" + pos.y() + ", " + pos.x() + "): " + pos.value());
                    homeBases.add(pos);

                    /* Starting from bottom left corner of square and going row by row to top right corner of square.
                     * We will hit the manhattan distance before the threshold in some cases, but the absolute outer limit is the
                     *  distance threshold, which will be a square.
                     */

                    int minYOffset = -(distanceThreshold);                    
                    int maxYOffset = distanceThreshold;

                    // This ensures the bottom limit stays within the grid
                    if(!fullSquare)
                    {
                        int endPoint = pos.y() + minYOffset;
                        if(isDebug())
                            System.out.println(" minYOffset initial: " + minYOffset + ", endPoint: " + endPoint + ", y: " + pos.y());
                        if( endPoint < 0 )
                        {
                            // we want to add back the amount the endPoint is below zero
                            minYOffset += -endPoint;
                            if(isDebug())
                                System.out.println("  adjusted minYOffset: " + minYOffset);
                        }

                        // this ensures the top limit stays within the grid
                        endPoint = pos.y() + maxYOffset;
                        if(isDebug())
                            System.out.println(" maxYOffset initial: " + maxYOffset + ", endPoint: " + endPoint + ", height: " + height);
                        if( endPoint >= height)
                        {
                            // We want to subtract the amount the endPoint is above the height
                            maxYOffset -= (endPoint - height + 1);
                            if(isDebug())
                                System.out.println("  adjusted maxYOffset: " + maxYOffset);
                        }
                    }
                    
                    /* Even better way: think of it as a diamond shape inside a square.  The square is defined by the distance threshold.
                     * This means that for the lowest row, we actually only care about the cell in the same column as the positive cell.  Next row up,
                     * we care about one cell to the left and one to the right, etc., until we reach the row of the positive cell.  Then as we go above
                     * the positive cell, we reverse the process.
                     * 
                     * 100,0000 took 36 seconds, so we would need to do some sort of optimization for larger grids.
                     */
                    for( int yOffset = minYOffset; yOffset <= maxYOffset; yOffset++ )
                    {
                        // go through each row, but keep in mind that it is a diamond shape
                        int xOffsetMin = 0;
                        int xOffsetMax = 0;

                        if(fullSquare)
                        {
                            xOffsetMin = -distanceThreshold;
                            xOffsetMax = distanceThreshold;
                        }
                        else
                        {
                            // This should start as 0 when yOffset is min or max yOffset
                            xOffsetMin = distanceThreshold - Math.abs(yOffset);
                            if(xOffsetMin != 0)
                                xOffsetMin = -xOffsetMin;
                            if(isDebug())
                                System.out.println("  xOffsetMin initial: " + xOffsetMin + " = " + distanceThreshold + " - " + Math.abs(yOffset));
                            xOffsetMax = distanceThreshold - Math.abs(yOffset);
                            if(isDebug())
                                System.out.println("  xOffsetMax initial: " + xOffsetMin + " = " + distanceThreshold + " - " + Math.abs(yOffset));
                        }

                        /* Old way, could be slow with large thresholds.
                        for( int xOffset = -distanceThreshold; xOffset <= distanceThreshold; xOffset++ )
                         */
                        for( int xOffset = xOffsetMin; xOffset <= xOffsetMax; xOffset++ )
                        {

                            int y = pos.y() + yOffset;
                            int x = pos.x() + xOffset;

                            if(isDebug())
                                System.out.println(" Checking position (" + y + ", " + x + ")");

                            // Always add home base
                            if( y == pos.y() && x == pos.x() ) 
                                visited.add(pos);
                            // Check if within bounds
                            else if (y >= 0 && y < height && x >= 0 && x < width)
                            {
                                Position destination = rows.get(y).get(x);
                                int distance = manhattanDistance(pos, destination);
                                if(distance <= distanceThreshold) {    
                                    visited.add(destination);
                                }
                            }
                        }
                    }
                }
            }
        }

        if(isDebug())
        {
            System.out.println("Total unique neighborhood cells: " + visited.size());
        }

        if(isListUniqueCells() || isDebug())
        {
            System.out.println("Listing all unique neighborhood cells, to double check our work:");
            for(Position p : visited) {
                System.out.println(" Neighborhood cell at (" + p.y() + ", " + p.x() + "): " + p.value());
            }
        }

        return visited.size();
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("GridCellNeighboods{");
        sb.append("distanceThreshold=").append(distanceThreshold);
        sb.append(", height=").append(height);
        sb.append(", width=").append(width);
        sb.append(", # positive values=" + numPositiveValues);
        if(label != null && !label.isEmpty()) {
            sb.append(", label=").append(label);
        }
        sb.append('}');
        return sb.toString();
    }

    public static void main( String[] args )
    {
        List<GridCellNeighborhoodsWithinDistance> examples = new ArrayList<>();

        // Fill one positive value for example 1
        GridCellNeighborhoodsWithinDistance exampleToAdd = new GridCellNeighborhoodsWithinDistance(3, 11, 11,
            "1 positive, center", new Position(5, 5, 5));
        // exampleToAdd.setDebug( true);
        examples.add(exampleToAdd);

        // Fill one positive value for example 2 
        exampleToAdd = new GridCellNeighborhoodsWithinDistance(3, 11, 11,
            "1 positive, to left", new Position(5, 1, 5));
        examples.add(exampleToAdd);

        // Fill two positive values for example 3 
        exampleToAdd = new GridCellNeighborhoodsWithinDistance(2, 11, 11,
            "2 positives, no overlap",
            new Position(7, 7, 5),
            new Position(3, 3, 5));
        // exampleToAdd.setDebug( true);
        examples.add(exampleToAdd);

        // Fill two positive values for example 4 
        exampleToAdd = new GridCellNeighborhoodsWithinDistance(2, 11, 11,
            "2 positives, overlap",
            new Position(3, 3, 5),
            new Position(4, 5, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        // Fill two positive values for example 5, overlap and run out of bounds, shifted example4 to left by 3 
        exampleToAdd = new GridCellNeighborhoodsWithinDistance(2, 11, 11,
            "2 positives, overlap, out of bounds left",
            new Position(3, 0, 5),
            new Position(4, 2, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        // Fill two positive values for example 6, overlap and run out of bounds, shifted example to down by 3 and left by 3
        exampleToAdd = new GridCellNeighborhoodsWithinDistance(2, 11, 11,
            "2 positives, overlap, out of bounds bottom left",
            new Position(0, 0, 5),
            new Position(1, 2, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        // Fill two positive values for example 7, overlap and run out of bounds, shifted example4 to down by 3 
        exampleToAdd = new GridCellNeighborhoodsWithinDistance(2, 11, 11,
            "2 positives, overlap, out of bounds bottom",
            new Position(0, 3, 5),
            new Position(1, 5, 5));
        examples.add(exampleToAdd);

        // Fill two positive values for example 8, overlap and run out of bounds, shifted example4 to right by 5
        exampleToAdd = new GridCellNeighborhoodsWithinDistance(2, 11, 11,
            "2 positives, overlap, out of bounds right",
            new Position(3, 8, 5),
            new Position(4, 10, 5));
        examples.add(exampleToAdd);

        // Fill two positive values for example 9, overlap and run out of bounds, shifted example4 to up by 6
        exampleToAdd = new GridCellNeighborhoodsWithinDistance(2, 11, 11,
            "2 positives, overlap, out of bounds top",
            new Position(9, 3, 5),
            new Position(10, 5, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        // Fill two positive values for example 10, diagonally adjacent positive values
        exampleToAdd = new GridCellNeighborhoodsWithinDistance(2, 11, 11,
            "2 positives, overlap, diagonal adjacent",
            new Position(3, 3, 5),
            new Position(4, 4, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        // Fill two positive values for example 11, directly adjacent positive values, same row
        exampleToAdd = new GridCellNeighborhoodsWithinDistance(2, 11, 11,
            "2 positives, overlap, same row adjacent",
            new Position(3, 3, 5),
            new Position(3, 4, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        // Fill two positive values for example 12, directly adjacent positive values, same column
        exampleToAdd = new GridCellNeighborhoodsWithinDistance(2, 11, 11,
            "2 positives, overlap, same column adjacent",
            new Position(3, 4, 5),
            new Position(4, 4, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        // Fill two positive values for example 13, opposite corners
        exampleToAdd = new GridCellNeighborhoodsWithinDistance(3, 11, 11,
            "opposite corners",
            new Position(0, 0, 5),
            new Position(10, 10, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        // Fill two positive values for example 14, 3 in one corder
        exampleToAdd = new GridCellNeighborhoodsWithinDistance(3, 11, 11,
            "3 in one corner",
            new Position(10, 9, 5),
            new Position(9, 10, 5),
            new Position(10, 10, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        // oddly shaped examples
        exampleToAdd = new GridCellNeighborhoodsWithinDistance(3, 1, 21,
            "1 positive, 1x21 grid",
            new Position(0, 9, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        exampleToAdd = new GridCellNeighborhoodsWithinDistance(3, 21, 1,
            "1 positive, 21x1 grid",
            new Position(10, 0, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        exampleToAdd = new GridCellNeighborhoodsWithinDistance(0, 1, 1,
            "1 positive, 1x1 grid, should be 1",
            new Position(0, 0, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        exampleToAdd = new GridCellNeighborhoodsWithinDistance(0, 20, 20,
            "1 positive, 20x20 grid, should be 1",
            new Position(0, 0, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        exampleToAdd = new GridCellNeighborhoodsWithinDistance(2, 2, 2,
            "1 positive, 2x2 grid, should be 4",
            new Position(0, 1, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        // Another example for where N > W or H (not both, that is already above).  If this is done correctly, nothing should happen to it's runtime, I would think.
        exampleToAdd = new GridCellNeighborhoodsWithinDistance(5, 21, 3,
            "1 positive, 21x3 grid, N > W",
            new Position(10, 2, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        exampleToAdd = new GridCellNeighborhoodsWithinDistance(5, 4, 15,
            "1 positive, 4x15 grid, N > H",
            new Position(2, 9, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);
        
        exampleToAdd = new GridCellNeighborhoodsWithinDistance(3, 2, 2,
            "1 positive, 2x2 grid, N > H and W, should be 4",
            new Position(0, 1, 5));
        examples.add(exampleToAdd);

        exampleToAdd = new GridCellNeighborhoodsWithinDistance(100000, 2, 2,
            "1 positive, 2x2 grid, N much > H and W, should be 4",
            new Position(0, 1, 5));
        examples.add(exampleToAdd);

        exampleToAdd = new GridCellNeighborhoodsWithinDistance(12, 11, 11,
            "1 positive at (0,0), 11x11 grid, N > H and W, should be 85",
            new Position(0, 0, 5));
        examples.add(exampleToAdd);

        exampleToAdd = new GridCellNeighborhoodsWithinDistance(12, 11, 11,
            "1 positive at (5,5), 11x11 grid, N > H and W, should be 121, entire grid",
            new Position(5, 5, 5));
        examples.add(exampleToAdd);

        // All negative, should be 0
        exampleToAdd = new GridCellNeighborhoodsWithinDistance(3, 10, 10,
            "No positive, should be 0");
        examples.add(exampleToAdd);

        // Bad positive position, should throw exception
        Position newPosition = new Position(0, 2, 5);
        try {
            // We expect an Eception here because positive position is out of bounds
            exampleToAdd = new GridCellNeighborhoodsWithinDistance(2, 2, 2,
                "1 positive, 2x2 grid", newPosition );
            examples.add(exampleToAdd);
        } catch( IllegalArgumentException iae ) {
            System.out.println("Caught expected IllegalArgumentException for bad positive position (" + newPosition + "): " + iae);
        }
        
        Instant start = Instant.now();
        for( GridCellNeighborhoodsWithinDistance example : examples ) {
            // example.setDebug( true);
            // example.setListUniqueCells(true);
            int count = example.countGridCellsWithinNeighborhood();
            System.out.println("Total unique neighborhood cells ( " + example.toString() + "), " +
                "example " + (examples.indexOf(example) + 1 ) + ": " + count);
        }
        Instant stop  = Instant.now();
        System.out.println( "Total time: " + Duration.between(start, stop));
    }
}
