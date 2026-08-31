# frozen_string_literal: true

require 'set'
require_relative 'position'
require_relative 'errors'

module GridNeighborhoods
  # A 2D grid of height x width with a set of positive-valued cells.
  # Invariants: height > 0, width > 0; all positive cells lie in bounds.
  #
  # Requirements 1.1-1.4: grid initialization and validation.
  class Grid
    attr_reader :height, :width

    # Requirement 1.1: validates height > 0 and width > 0.
    # Requirement 1.2: validates positive cells are in bounds.
    # Requirement 1.4: stores positive cell positions.
    def initialize(height, width, positive_cells = [])
      raise InvalidGridDimensionsError.new(height, width) if height <= 0 || width <= 0

      @height = height
      @width = width
      @positive_cells = Set.new

      positive_cells.each do |pos|
        if pos.row.negative? || pos.row >= height || pos.column.negative? || pos.column >= width
          raise PositionOutOfBoundsError.new(pos, height, width)
        end

        @positive_cells.add(pos)
      end
    end

    # The stored positive cell positions (Requirement 1.4).
    attr_reader :positive_cells

    # Whether the position lies within the grid boundaries.
    # Requirement 1.3 / 6.x: no wraparound.
    def valid_position?(pos)
      pos.row >= 0 && pos.row < height && pos.column >= 0 && pos.column < width
    end
  end
end
