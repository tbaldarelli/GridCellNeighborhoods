import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;

/**
 * Hello world!
 *
 */
public class GridCellNeighborhoods 
{
    private record Position(int y, int x, int value) {}

    
    private final int distanceThreshold;
    private final int height;
    private final int width;
    private boolean debug = false;
    private boolean listUniqueCells = false;
    private final List<List<GridCellNeighborhoods.Position>> rows;
    private final int numPositiveValues;
    private final String label;
    private boolean alwaysAddHomeBase = false;

    public GridCellNeighborhoods( int distanceThreshold, int height, int width, String label, Position... positivePositions ) {
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

    private Set<Position> getPathToDesination(Position start, Position destination) {
        Set<Position> path = new HashSet<>();
        // Determine if we are going up or down
        int deltaY = destination.y() - start.y();
        int stepY = Integer.signum(deltaY);

        // Determine if we are going left or right
        int deltaX = destination.x() - start.x();
        int stepX = Integer.signum(deltaX);

        // int totalNumSteps = Math.abs(deltaY) + Math.abs(deltaX);

        // Find path vertically first, then horizontally, but only if we need to move vertically.
        if( deltaY != 0 )
        {            
            for( int y = start.y(), x = start.x(), numYSteps = Math.abs(deltaY), numXSteps = Math.abs(deltaX);
                (y != destination.y() || x != destination.x()); ) {

                // First move vertically, if needed.
                if (y != destination.y() && (numYSteps > 0)) {
                    y += stepY;
                    numYSteps--;
                }
                // then move horizontally, if needed.
                else if (x != destination.x() && (numXSteps > 0)) {
                    x += stepX;
                    numXSteps--;
                }

                Position pos = rows.get(y).get(x);
                if(!pos.equals(destination))
                    path.add(rows.get(y).get(x));
            }
        }
        
        /* Find path horizontally first, then vertically, but only if we need to move horizontally.
         *  We do this because sometimes the vertical method above will miss some paths to the destionation.  Sometimes there
         *  are multiple paths to the destination, and we want to make sure we get them all.
         */
        if(deltaX != 0)
        {
            for( int y = start.y(), x = start.x(), numYSteps = Math.abs(deltaY), numXSteps = Math.abs(deltaX);
                (y != destination.y() || x != destination.x()); ) {

                // First move horizontally, if needed. 
                if (x != destination.x() && (numXSteps > 0)) {
                    x += stepX;
                    numXSteps--;
                }
                // then move vertically, if needed.
                else if (y != destination.y() && (numYSteps > 0)) {
                    y += stepY;
                    numYSteps--;
                }

                Position pos = rows.get(y).get(x);
                if(!pos.equals(destination))
                    path.add(rows.get(y).get(x));
            }
        }

        return path;
    }

    private int manhattanDistance(Position p1, Position p2) {
        return Math.abs(p1.x() - p2.x()) + Math.abs(p1.y() - p2.y());
    }

    private void addDesintationAndPathToVisited(Set<Position> visited, Position start, Position destination) {
        // add all cells to visited list
        Set<GridCellNeighborhoods.Position> path = getPathToDesination(start, destination);
        if(isDebug())
        {
            System.out.println("   Adding path to destination:" + path.size() + " cells." );
            for(Position p : path) {
                System.out.println("    Path cell at (" + p.y() + ", " + p.x() + ")");
            }
        }

        visited.addAll(path);

        if(isDebug())
            System.out.println("   Adding destination neighbor at (" + destination.y() + ", " + destination.x() + "): " + destination.value());
        visited.add(destination);           
    }

    private int countGridCellsInNeighborhood() {
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

        // find positive value(s) and calculate grid cell neighborhoods
        for( List<Position> row : rows ) {
            // go through each cell in row
            for( Position pos : row ) {
                // once we find a positive value, we calculate its neighborhood
                if (pos.value() > 0) {
                    if(isDebug())
                        System.out.println("Found positive value at (" + pos.y() + ", " + pos.x() + "): " + pos.value());
                    homeBases.add(pos);

                    boolean addHomeBase = false;

                    /* Calculate neighborhood.  Start from position of positive value
                     * and move clockwise out to the distance threshold at 4 cordinate points.
                     * From each of these coordinate lines, we will find other cells in the neigborhood.
                     * It will look like a diamond.
                     * Upper right corner of square
                     */
                    if(isDebug())
                        System.out.println(" Calculating neighborhood upper right corner of square.");
                    for(int yThresholdAdjust = distanceThreshold, xThresholdAdjust = 0;
                            yThresholdAdjust >= 0 && xThresholdAdjust <= distanceThreshold;
                            yThresholdAdjust--, xThresholdAdjust++)
                    {
                        int y = pos.y() + yThresholdAdjust;
                        int x = pos.x() + xThresholdAdjust;

                        // this makes sure we haven't gone off the grid
                        if(isDebug())
                            System.out.println("  Checking position (" + y + ", " + x + ")");
                        if (y >= 0 && y < height && x >= 0 && x < width) {
                            Position destination = rows.get(y).get(x);
                            int distance = manhattanDistance(pos, destination);
                            if(distance == distanceThreshold) {    
                                addDesintationAndPathToVisited(visited, pos, destination);
                                addHomeBase = true;
                            }
                        }
                    }

                    // Then do bottom right corner of square
                    if(isDebug())
                        System.out.println(" Calculating neighborhood bottom right corner of square.");
                    for(int xThresholdAdjust = distanceThreshold, yThresholdAdjust = 0;
                            xThresholdAdjust >= 0 && yThresholdAdjust <= distanceThreshold;
                            xThresholdAdjust--, yThresholdAdjust++)
                    {
                        int y = pos.y() + (-1 * yThresholdAdjust);
                        int x = pos.x() + xThresholdAdjust;

                        // this makes sure we haven't gone off the grid
                        if(isDebug())
                            System.out.println("  Checking position (" + y + ", " + x + ")");
                        if (y >= 0 && y < height && x >= 0 && x < width) {
                            Position destination = rows.get(y).get(x);
                            int distance = manhattanDistance(pos, destination);
                            if(distance == distanceThreshold) {                                   
                               addDesintationAndPathToVisited(visited, pos, destination);    
                               addHomeBase = true;                            
                            }
                        }
                    }

                    // then do bottom left corner of square
                    if(isDebug())    
                        System.out.println(" Calculating neighborhood bottom left corner of square.");
                    for(int xThresholdAdjust = distanceThreshold, yThresholdAdjust = 0;
                            xThresholdAdjust >= 0 && yThresholdAdjust <= distanceThreshold;
                            xThresholdAdjust--, yThresholdAdjust++)
                    {
                        int y = pos.y() + (-1 * yThresholdAdjust);
                        int x = pos.x() + (-1 * xThresholdAdjust);

                        // this makes sure we haven't gone off the grid
                        if(isDebug())
                            System.out.println("  Checking position (" + y + ", " + x + ")");
                        if (y >= 0 && y < height && x >= 0 && x < width) {
                            Position destination = rows.get(y).get(x);
                            int distance = manhattanDistance(pos, destination);
                            if(distance == distanceThreshold) {                                   
                               addDesintationAndPathToVisited(visited, pos, destination);   
                               addHomeBase = true;                             
                            }
                        }
                    }

                    // then do upper left corner of square
                    if(isDebug())
                        System.out.println(" Calculating neighborhood upper left corner of square.");
                    for(int xThresholdAdjust = distanceThreshold, yThresholdAdjust = 0;
                            xThresholdAdjust >= 0 && yThresholdAdjust <= distanceThreshold;
                            xThresholdAdjust--, yThresholdAdjust++)
                    {
                        int y = pos.y() + yThresholdAdjust;
                        int x = pos.x() + (-1 * xThresholdAdjust);

                        // this makes sure we haven't gone off the grid
                        if(isDebug())
                            System.out.println("  Checking position (" + y + ", " + x + ")");
                        if (y >= 0 && y < height && x >= 0 && x < width) {
                            Position destination = rows.get(y).get(x);
                            int distance = manhattanDistance(pos, destination);
                            if(distance == distanceThreshold) {                                   
                                addDesintationAndPathToVisited(visited, pos, destination);       
                                addHomeBase = true;                          
                            }
                        }
                    }
                    
                    if(addHomeBase || isAlwaysAddHomeBase())
                        visited.add(pos);
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

        /* alternate method: search row by row for positive values using Java streams instead of looping like above.
         * I chose the above loop because it helped me see the problem better.  This time I prefered clarity over conciseness.
         */
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
        List<GridCellNeighborhoods> examples = new ArrayList<>();

        // Fill one positive value for example 1
        GridCellNeighborhoods exampleToAdd = new GridCellNeighborhoods(3, 11, 11,
            "1 positive, center", new Position(5, 5, 5));
        examples.add(exampleToAdd);

        // Fill one positive value for example 2 
        exampleToAdd = new GridCellNeighborhoods(3, 11, 11,
            "1 positive, to left", new Position(5, 1, 5));
        examples.add(exampleToAdd);

        // Fill two positive values for example 3 
        exampleToAdd = new GridCellNeighborhoods(2, 11, 11,
            "2 positives, no overlap",
            new Position(7, 7, 5),
            new Position(3, 3, 5));
        // exampleToAdd.setDebug( true);
        examples.add(exampleToAdd);

        // Fill two positive values for example 4 
        exampleToAdd = new GridCellNeighborhoods(2, 11, 11,
            "2 positives, overlap",
            new Position(3, 3, 5),
            new Position(4, 5, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        // Fill two positive values for example 5, overlap and run out of bounds, shifted example4 to left by 3 
        exampleToAdd = new GridCellNeighborhoods(2, 11, 11,
            "2 positives, overlap, out of bounds left",
            new Position(3, 0, 5),
            new Position(4, 2, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        // Fill two positive values for example 6, overlap and run out of bounds, shifted example to down by 3 and left by 3
        exampleToAdd = new GridCellNeighborhoods(2, 11, 11,
            "2 positives, overlap, out of bounds bottom left",
            new Position(0, 0, 5),
            new Position(1, 2, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        // Fill two positive values for example 7, overlap and run out of bounds, shifted example4 to down by 3 
        exampleToAdd = new GridCellNeighborhoods(2, 11, 11,
            "2 positives, overlap, out of bounds bottom",
            new Position(0, 3, 5),
            new Position(1, 5, 5));
        examples.add(exampleToAdd);

        // Fill two positive values for example 8, overlap and run out of bounds, shifted example4 to right by 5
        exampleToAdd = new GridCellNeighborhoods(2, 11, 11,
            "2 positives, overlap, out of bounds right",
            new Position(3, 8, 5),
            new Position(4, 10, 5));
        examples.add(exampleToAdd);

        // Fill two positive values for example 9, overlap and run out of bounds, shifted example4 to up by 6
        exampleToAdd = new GridCellNeighborhoods(2, 11, 11,
            "2 positives, overlap, out of bounds top",
            new Position(9, 3, 5),
            new Position(10, 5, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        // Fill two positive values for example 10, diagonally adjacent positive values
        exampleToAdd = new GridCellNeighborhoods(2, 11, 11,
            "2 positives, overlap, diagonal adjacent",
            new Position(3, 3, 5),
            new Position(4, 4, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        // Fill two positive values for example 11, directly adjacent positive values, same row
        exampleToAdd = new GridCellNeighborhoods(2, 11, 11,
            "2 positives, overlap, same row adjacent",
            new Position(3, 3, 5),
            new Position(3, 4, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        // Fill two positive values for example 12, directly adjacent positive values, same column
        exampleToAdd = new GridCellNeighborhoods(2, 11, 11,
            "2 positives, overlap, same column adjacent",
            new Position(3, 4, 5),
            new Position(4, 4, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        // Fill two positive values for example 13, opposite corners
        exampleToAdd = new GridCellNeighborhoods(3, 11, 11,
            "opposite corners",
            new Position(0, 0, 5),
            new Position(10, 10, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        // Fill two positive values for example 14, 3 in one corder
        exampleToAdd = new GridCellNeighborhoods(3, 11, 11,
            "3 in one corner",
            new Position(10, 9, 5),
            new Position(9, 10, 5),
            new Position(10, 10, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        // oddly shaped examples
        exampleToAdd = new GridCellNeighborhoods(3, 1, 21,
            "1 positive, 1x21 grid",
            new Position(0, 9, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        exampleToAdd = new GridCellNeighborhoods(3, 21, 1,
            "1 positive, 21x1 grid",
            new Position(10, 0, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        exampleToAdd = new GridCellNeighborhoods(0, 1, 1,
            "1 positive, 1x1 grid, should be 1",
            new Position(0, 0, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        exampleToAdd = new GridCellNeighborhoods(0, 20, 20,
            "1 positive, 20x20 grid, should be 1",
            new Position(0, 0, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        exampleToAdd = new GridCellNeighborhoods(2, 2, 2,
            "1 positive, 2x2 grid, should be 4",
            new Position(0, 1, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        // Another example for where N > W or H (not both, that is already above).  If this is done correctly, nothing should happen to it's runtime, I would think.
        exampleToAdd = new GridCellNeighborhoods(5, 21, 3,
            "1 positive, 21x3 grid, N > W",
            new Position(10, 2, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);

        exampleToAdd = new GridCellNeighborhoods(5, 4, 15,
            "1 positive, 4x15 grid, N > H",
            new Position(2, 9, 5));
        // exampleToAdd.setDebug( true);
        // exampleToAdd.setListUniqueCells(true);
        examples.add(exampleToAdd);
        
        /* In the example below, we only include the home base (positive cell) if we can get to at least one desintation.  Since the assumption, based on some of the test
         *  cases, is that we can  get at at least one desintation, we test it here.
         */
        exampleToAdd = new GridCellNeighborhoods(3, 2, 2,
            "1 positive, 2x2 grid, N > H and W, should be 0, cannot get to any destination",
            new Position(0, 1, 5));
        examples.add(exampleToAdd);
        
        /* In the example below, we always include the home base (positive cell), even if we can't get to any desintations.  This is a possible reading of task point 2,
         *  so we test it here.
        exampleToAdd = new GridCellNeighboods(3, 1, 1,
            "1 positive, 1x1 grid, N > H and W, should be 1 as we always include positive cell",
            new Position(0, 0, 5));
        exampleToAdd.setAlwaysAddHomeBase(true);
        examples.add(exampleToAdd);
         */

        // All negative, should be 0
        exampleToAdd = new GridCellNeighborhoods(3, 10, 10,
            "No positive, should be 0");
        examples.add(exampleToAdd);

        // Bad positive position, should throw exception
        Position newPosition = new Position(0, 2, 5);
        try {
            // We expect an Eception here because positive position is out of bounds
            exampleToAdd = new GridCellNeighborhoods(2, 2, 2,
                "1 positive, 2x2 grid", newPosition );
            examples.add(exampleToAdd);
        } catch( IllegalArgumentException iae ) {
            System.out.println("Caught expected IllegalArgumentException for bad positive position (" + newPosition + "): " + iae);
        }

        for( GridCellNeighborhoods example : examples ) {
            // example.setDebug( true);
            // example.setListUniqueCells(true);
            int count = example.countGridCellsInNeighborhood();
            System.out.println("Total unique neighborhood cells ( " + example.toString() + "), " +
                "example " + (examples.indexOf(example) + 1 ) + ": " + count);
        }
    }
}
