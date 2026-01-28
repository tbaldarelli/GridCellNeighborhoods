package gridneighborhoods;

import gridneighborhoods.exceptions.InvalidGridDimensionsException;
import gridneighborhoods.exceptions.PositionOutOfBoundsException;

import java.util.ArrayList;
import java.util.List;

/**
 * Represents a 2D grid with height, width, and positive cell storage.
 * 
 * The grid uses (0,0) as the bottom-left corner coordinate system.
 */
public class Grid {
    private final int height;
    private final int width;
    private final int[][] cells;
    
    /**
     * Initialize a grid with specified dimensions.
     * 
     * @param height Grid height (must be > 0)
     * @param width Grid width (must be > 0)
     * @throws InvalidGridDimensionsException If height <= 0 or width <= 0
     */
    public Grid(int height, int width) {
        this(height, width, null);
    }
    
    /**
     * Initialize a grid with specified dimensions and cell values.
     * 
     * @param height Grid height (must be > 0)
     * @param width Grid width (must be > 0)
     * @param cells Optional 2D array of cell values. If not provided, creates empty grid.
     *              Expected format: cells[row][column] where row 0 is bottom of grid.
     * @throws InvalidGridDimensionsException If height <= 0 or width <= 0
     * @throws IllegalArgumentException If cells dimensions don't match grid dimensions
     */
    public Grid(int height, int width, int[][] cells) {
        if (height <= 0 || width <= 0) {
            throw new InvalidGridDimensionsException(height, width);
        }
        
        this.height = height;
        this.width = width;
        
        if (cells == null) {
            // Create empty grid (all zeros)
            this.cells = new int[height][width];
        } else {
            // Validate provided cells
            if (cells.length != height) {
                throw new IllegalArgumentException("Cells height " + cells.length + " doesn't match grid height " + height);
            }
            for (int i = 0; i < cells.length; i++) {
                if (cells[i].length != width) {
                    throw new IllegalArgumentException("Cells row " + i + " width " + cells[i].length + " doesn't match grid width " + width);
                }
            }
            // Deep copy
            this.cells = new int[height][width];
            for (int i = 0; i < height; i++) {
                System.arraycopy(cells[i], 0, this.cells[i], 0, width);
            }
        }
    }
    
    /**
     * Get all positions containing positive values (> 0).
     * 
     * @return List of Position objects for cells with values > 0
     */
    public List<Position> getPositiveCells() {
        List<Position> positiveCells = new ArrayList<>();
        for (int row = 0; row < height; row++) {
            for (int col = 0; col < width; col++) {
                if (cells[row][col] > 0) {
                    positiveCells.add(new Position(row, col));
                }
            }
        }
        return positiveCells;
    }
    
    /**
     * Check if a position is within grid boundaries.
     * 
     * @param position Position to validate
     * @return True if position is within grid bounds, False otherwise
     */
    public boolean isValidPosition(Position position) {
        return position.getRow() >= 0 && position.getRow() < height &&
               position.getColumn() >= 0 && position.getColumn() < width;
    }
    
    /**
     * Get the value at a specific position.
     * 
     * @param position Position to query
     * @return The cell value at the position
     * @throws PositionOutOfBoundsException If position is out of bounds
     */
    public int getCellValue(Position position) {
        if (!isValidPosition(position)) {
            throw new PositionOutOfBoundsException(position, height, width);
        }
        return cells[position.getRow()][position.getColumn()];
    }
    
    /**
     * Set the value at a specific position.
     * 
     * @param position Position to set
     * @param value Value to set
     * @throws PositionOutOfBoundsException If position is out of bounds
     */
    public void setCellValue(Position position, int value) {
        if (!isValidPosition(position)) {
            throw new PositionOutOfBoundsException(position, height, width);
        }
        cells[position.getRow()][position.getColumn()] = value;
    }
    
    public int getHeight() {
        return height;
    }
    
    public int getWidth() {
        return width;
    }
    
    @Override
    public String toString() {
        return "Grid(" + height + "x" + width + ")";
    }
}
