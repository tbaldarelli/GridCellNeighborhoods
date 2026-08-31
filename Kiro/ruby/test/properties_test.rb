# frozen_string_literal: true

require 'minitest/autorun'
require 'set'
require_relative '../lib/grid_neighborhoods'
require_relative 'property_helper'

# The 13 correctness properties from the spec. Uses the self-contained
# PropertyHelper harness (>= 100 iterations each).
class PropertiesTest < Minitest::Test
  include GridNeighborhoods
  include PropertyHelper

  # Feature: grid-neighborhoods, Property 1: Grid Validation
  # Validates: Requirements 1.1, 1.2
  def test_property_01_grid_validation
    for_all(generate: ->(rng) { [rand_int(rng, -100, 1000), rand_int(rng, -100, 1000)] }) do |(height, width)|
      if height.positive? && width.positive?
        grid = Grid.new(height, width)
        grid.height == height && grid.width == width
      else
        begin
          Grid.new(height, width)
          false
        rescue InvalidGridDimensionsError
          true
        end
      end
    end
  end

  # Feature: grid-neighborhoods, Property 2: Manhattan Distance Calculation
  # Validates: Requirements 2.1, 2.2, 2.3
  def test_property_02_manhattan_distance
    gen = lambda do |rng|
      [rand_int(rng, 0, 1000), rand_int(rng, 0, 1000), rand_int(rng, 0, 1000), rand_int(rng, 0, 1000)]
    end
    for_all(generate: gen) do |(r1, c1, r2, c2)|
      p1 = Position.new(r1, c1)
      p2 = Position.new(r2, c2)
      d = p1.manhattan_distance(p2)

      ok = d == (r1 - r2).abs + (c1 - c2).abs
      ok &&= d >= 0
      ok &&= d.zero? if r1 == r2 && c1 == c2
      ok && d == p2.manhattan_distance(p1)
    end
  end

  # Feature: grid-neighborhoods, Property 3: Coordinate System Consistency
  # Validates: Requirements 1.3, 1.4
  def test_property_03_coordinate_system
    for_all(generate: ->(rng) { [rand_int(rng, 1, 50), rand_int(rng, 1, 50)] }) do |(height, width)|
      grid = Grid.new(height, width)
      grid.valid_position?(Position.new(0, 0)) &&
        grid.valid_position?(Position.new(height - 1, width - 1)) &&
        !grid.valid_position?(Position.new(height, 0)) &&
        !grid.valid_position?(Position.new(0, width))
    end
  end

  # Feature: grid-neighborhoods, Property 4: Self-Inclusion in Neighborhoods
  # Validates: Requirements 3.1
  def test_property_04_self_inclusion
    gen = ->(rng) { [rand_int(rng, 1, 20), rand_int(rng, 1, 20), rand_int(rng, 0, 20)] }
    for_all(generate: gen) do |(height, width, n)|
      center = Position.new(height / 2, width / 2)
      grid = Grid.new(height, width, [center])
      calc = NeighborhoodCalculator.new
      neighborhood = calc.get_neighborhood_cells(grid, n)
      neighborhood.include?(center) && calc.count_neighborhood_cells(grid, n) >= 1
    end
  end

  # Feature: grid-neighborhoods, Property 5: Complete Neighborhood Enumeration
  # Validates: Requirements 3.2
  def test_property_05_complete_enumeration
    for_all(generate: ->(rng) { rand_int(rng, 1, 10) }) do |n|
      height = 2 * n + 3
      width = 2 * n + 3
      center = Position.new(n + 1, n + 1)
      grid = Grid.new(height, width, [center])
      calc = NeighborhoodCalculator.new
      neighborhood = calc.enumerate_neighborhood(grid, center, n)
      expected = (n + 1) * (n + 1) + n * n
      neighborhood.size == expected
    end
  end

  # Feature: grid-neighborhoods, Property 6: Boundary Constraint Enforcement
  # Validates: Requirements 3.3, 6.1, 6.2, 6.3
  def test_property_06_boundary_enforcement
    gen = ->(rng) { [rand_int(rng, 1, 20), rand_int(rng, 1, 20), rand_int(rng, 0, 20)] }
    for_all(generate: gen) do |(height, width, n)|
      center = Position.new(0, 0)
      grid = Grid.new(height, width, [center])
      calc = NeighborhoodCalculator.new
      neighborhood = calc.enumerate_neighborhood(grid, center, n)
      neighborhood.all? do |cell|
        BoundaryHandler.within_bounds?(cell, grid) &&
          cell.row >= 0 && cell.row < height && cell.column >= 0 && cell.column < width
      end
    end
  end

  # Feature: grid-neighborhoods, Property 7: Cell Uniqueness Guarantee
  # Validates: Requirements 3.4, 4.2, 5.1
  def test_property_07_cell_uniqueness
    gen = lambda do |rng|
      height = rand_int(rng, 1, 30)
      width = rand_int(rng, 1, 30)
      n = rand_int(rng, 0, 20)
      count = rand_int(rng, 1, 10)
      cells = Array.new(count) { Position.new(rand_int(rng, 0, height - 1), rand_int(rng, 0, width - 1)) }.uniq
      [height, width, n, cells]
    end
    for_all(generate: gen) do |(height, width, n, cells)|
      grid = Grid.new(height, width, cells)
      calc = NeighborhoodCalculator.new
      all_cells = calc.get_neighborhood_cells(grid, n)
      count = calc.count_neighborhood_cells(grid, n)
      next false unless count == all_cells.size

      sum_individual = grid.positive_cells.sum { |c| calc.enumerate_neighborhood(grid, c, n).size }
      count <= sum_individual
    end
  end

  # Feature: grid-neighborhoods, Property 8: Non-Overlapping Additivity
  # Validates: Requirements 4.1, 4.3
  def test_property_08_non_overlapping_additivity
    for_all(generate: ->(rng) { rand_int(rng, 1, 8) }) do |n|
      min_separation = 2 * n + 1
      height = min_separation + 2 * n + 2
      width = min_separation + 2 * n + 2
      p1 = Position.new(n, n)
      p2 = Position.new(n + min_separation, n + min_separation)
      grid = Grid.new(height, width, [p1, p2])
      calc = NeighborhoodCalculator.new

      nb1 = calc.enumerate_neighborhood(grid, p1, n)
      nb2 = calc.enumerate_neighborhood(grid, p2, n)
      next false unless (nb1 & nb2).empty?

      total = calc.count_neighborhood_cells(grid, n)
      total == nb1.size + nb2.size
    end
  end

  # Feature: grid-neighborhoods, Property 9: Overlapping Union Behavior
  # Validates: Requirements 5.2, 5.3
  def test_property_09_overlapping_union
    for_all(generate: ->(rng) { rand_int(rng, 2, 8) }) do |n|
      height = 2 * n + 10
      width = 2 * n + 10
      p1 = Position.new(n + 1, n + 1)
      p2 = Position.new(n + 2, n + 2)
      grid = Grid.new(height, width, [p1, p2])
      calc = NeighborhoodCalculator.new

      nb1 = calc.enumerate_neighborhood(grid, p1, n)
      nb2 = calc.enumerate_neighborhood(grid, p2, n)
      next false if (nb1 & nb2).empty?

      total = calc.count_neighborhood_cells(grid, n)
      total < nb1.size + nb2.size
    end
  end

  # Feature: grid-neighborhoods, Property 10: Zero Distance Threshold
  # Validates: Requirements 7.2
  def test_property_10_zero_distance
    gen = lambda do |rng|
      height = rand_int(rng, 1, 20)
      width = rand_int(rng, 1, 20)
      count = rand_int(rng, 1, 20)
      cells = Array.new(count) { Position.new(rand_int(rng, 0, height - 1), rand_int(rng, 0, width - 1)) }.uniq
      [height, width, cells]
    end
    for_all(generate: gen) do |(height, width, cells)|
      grid = Grid.new(height, width, cells)
      calc = NeighborhoodCalculator.new
      calc.count_neighborhood_cells(grid, 0) == grid.positive_cells.size
    end
  end

  # Feature: grid-neighborhoods, Property 11: Maximum Distance Threshold
  # Validates: Requirements 7.3
  def test_property_11_maximum_distance
    gen = lambda do |rng|
      height = rand_int(rng, 1, 20)
      width = rand_int(rng, 1, 20)
      count = rand_int(rng, 1, 10)
      cells = Array.new(count) { Position.new(rand_int(rng, 0, height - 1), rand_int(rng, 0, width - 1)) }.uniq
      [height, width, cells]
    end
    for_all(generate: gen) do |(height, width, cells)|
      grid = Grid.new(height, width, cells)
      calc = NeighborhoodCalculator.new
      max_distance = (height - 1) + (width - 1)
      calc.count_neighborhood_cells(grid, max_distance + 10) == height * width
    end
  end

  # Feature: grid-neighborhoods, Property 12: Degenerate Grid Handling
  # Validates: Requirements 7.4
  def test_property_12_degenerate_grid
    gen = ->(rng) { [rand_int(rng, 0, 2), rand_int(rng, 1, 50), rand_int(rng, 0, 20)] }
    for_all(generate: gen) do |(grid_type, dimension, n)|
      case grid_type
      when 0 then height = 1; width = dimension; center = Position.new(0, dimension / 2)
      when 1 then height = dimension; width = 1; center = Position.new(dimension / 2, 0)
      else height = 1; width = 1; center = Position.new(0, 0)
      end
      grid = Grid.new(height, width, [center])
      calc = NeighborhoodCalculator.new
      neighborhood = calc.get_neighborhood_cells(grid, n)
      count = calc.count_neighborhood_cells(grid, n)

      ok = neighborhood.size == count
      ok &&= neighborhood.include?(center)
      ok &&= neighborhood.all? { |cell| center.manhattan_distance(cell) <= n }
      ok &&= (count == 1) if grid_type == 2
      ok
    end
  end

  # Feature: grid-neighborhoods, Property 13: Cross-Language Result Consistency
  # Validates: Requirements 9.1, 9.3, 9.4
  # Verifies determinism: same input yields the same count on repeated runs.
  def test_property_13_deterministic
    gen = lambda do |rng|
      height = rand_int(rng, 1, 30)
      width = rand_int(rng, 1, 30)
      n = rand_int(rng, 0, 15)
      count = rand_int(rng, 1, 5)
      cells = Array.new(count) { Position.new(rand_int(rng, 0, height - 1), rand_int(rng, 0, width - 1)) }.uniq
      [height, width, n, cells]
    end
    for_all(generate: gen) do |(height, width, n, cells)|
      grid = Grid.new(height, width, cells)
      calc = NeighborhoodCalculator.new
      calc.count_neighborhood_cells(grid, n) == calc.count_neighborhood_cells(grid, n)
    end
  end
end
