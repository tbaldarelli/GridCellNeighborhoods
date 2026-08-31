# frozen_string_literal: true

# Grid Cell Neighborhoods — Ruby implementation.
#
# Counts the total number of unique grid cells that fall within Manhattan
# distance neighborhoods of positive-valued cells in a 2D grid.
#
# Implemented from the spec in ../.kiro/specs/grid-neighborhoods/
# (requirements.md + design.md), not migrated from another language.

require_relative 'grid_neighborhoods/position'
require_relative 'grid_neighborhoods/errors'
require_relative 'grid_neighborhoods/grid'
require_relative 'grid_neighborhoods/boundary_handler'
require_relative 'grid_neighborhoods/neighborhood_calculator'

module GridNeighborhoods
end
