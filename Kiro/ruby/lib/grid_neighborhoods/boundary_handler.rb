# frozen_string_literal: true

require 'set'

module GridNeighborhoods
  # Boundary handling: exclude out-of-bounds cells, no wraparound.
  # Requirements 6.1-6.3.
  module BoundaryHandler
    module_function

    # Whether a position is within the grid boundaries (Requirement 6.2: no wraparound).
    def within_bounds?(pos, grid)
      grid.valid_position?(pos)
    end

    # Retain only positions within the grid boundaries (Requirements 6.1, 6.3).
    def filter_valid_positions(positions, grid)
      positions.select { |pos| grid.valid_position?(pos) }.to_set
    end
  end
end
