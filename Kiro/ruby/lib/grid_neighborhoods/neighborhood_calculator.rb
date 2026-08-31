# frozen_string_literal: true

require 'set'
require_relative 'position'
require_relative 'errors'

module GridNeighborhoods
  # Neighborhood calculator: diamond enumeration + union.
  #
  # Core algorithm from design.md:
  #   for delta_row in -N..N:
  #       remaining = N - |delta_row|
  #       for delta_col in -remaining..remaining:
  #           candidate = (center.row + delta_row, center.column + delta_col)
  #           add to set if valid_position?(candidate)
  #
  # Requirements 3.x, 4.x, 5.x, 7.x.
  class NeighborhoodCalculator
    # Enumerate the neighborhood of a single center within Manhattan distance n,
    # clipped to the grid boundaries.
    #
    # Requirement 3.1: center is included. 3.2: full in-bounds diamond. 3.3: no OOB cells.
    # Requirement 8.3 / design "Early Termination": the delta ranges are clamped to the
    # farthest reachable grid cell so an n far larger than the grid does not drive a huge
    # empty scan (e.g. scenario 23: 2x2 grid, N=100000).
    def enumerate_neighborhood(grid, center, n)
      neighborhood = Set.new

      max_row_reach = [center.row, grid.height - 1 - center.row].max
      row_span = [n, max_row_reach].min

      (-row_span..row_span).each do |delta_row|
        remaining = n - delta_row.abs
        max_col_reach = [center.column, grid.width - 1 - center.column].max
        col_span = [remaining, max_col_reach].min

        (-col_span..col_span).each do |delta_col|
          candidate = Position.new(center.row + delta_row, center.column + delta_col)
          neighborhood.add(candidate) if grid.valid_position?(candidate)
        end
      end

      neighborhood
    end

    # The union of all positive-cell neighborhoods within distance n.
    # Requirements 3.4 / 4.2 / 5.1 (uniqueness), 5.2 (union), 7.1 (empty set -> empty).
    def get_neighborhood_cells(grid, distance_threshold)
      raise InvalidDistanceThresholdError, distance_threshold if distance_threshold.negative?

      all_cells = Set.new
      grid.positive_cells.each do |center|
        all_cells.merge(enumerate_neighborhood(grid, center, distance_threshold))
      end
      all_cells
    end

    # Count of unique cells across all positive-cell neighborhoods.
    # Requirement 7.2: N=0 counts only positive cells. 7.3: large N counts all reachable cells.
    def count_neighborhood_cells(grid, distance_threshold)
      get_neighborhood_cells(grid, distance_threshold).size
    end
  end
end
