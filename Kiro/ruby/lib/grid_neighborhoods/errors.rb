# frozen_string_literal: true

module GridNeighborhoods
  # Base type for grid neighborhood errors.
  class Error < StandardError; end

  # Raised when a grid is created with height <= 0 or width <= 0.
  # Requirement 8.1.
  class InvalidGridDimensionsError < Error
    def initialize(height, width)
      super("invalid grid dimensions: height=#{height} width=#{width} (both must be > 0)")
    end
  end

  # Raised when a positive cell position falls outside the grid boundaries.
  # Requirement 8.2.
  class PositionOutOfBoundsError < Error
    def initialize(position, height, width)
      super("position #{position} is out of bounds for a #{height}x#{width} grid")
    end
  end

  # Raised when the distance threshold N is negative.
  # Requirement 8.3.
  class InvalidDistanceThresholdError < Error
    def initialize(threshold)
      super("invalid distance threshold: #{threshold} (must be >= 0)")
    end
  end
end
