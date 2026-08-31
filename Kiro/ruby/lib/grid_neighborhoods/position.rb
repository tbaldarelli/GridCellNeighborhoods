# frozen_string_literal: true

module GridNeighborhoods
  # A cell position in the grid, identified by (row, column).
  # (0,0) represents the bottom-left corner per the spec glossary.
  #
  # Requirements 2.1-2.3: Manhattan distance calculation.
  class Position
    attr_reader :row, :column

    def initialize(row, column)
      @row = row
      @column = column
    end

    # Manhattan distance to another position: |r1-r2| + |c1-c2|.
    # Requirement 2.1: computes |row1 - row2| + |column1 - column2|.
    # Requirement 2.2: always non-negative.
    # Requirement 2.3: 0 when positions are identical.
    def manhattan_distance(other)
      (row - other.row).abs + (column - other.column).abs
    end

    # Value equality so positions can live in a Set / Hash key.
    def ==(other)
      other.is_a?(Position) && row == other.row && column == other.column
    end
    alias eql? ==

    def hash
      [row, column].hash
    end

    def to_s
      "(#{row},#{column})"
    end
  end
end
