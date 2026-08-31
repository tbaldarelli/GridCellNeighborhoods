# frozen_string_literal: true

# Minimal self-contained property-based testing helper.
#
# Ruby 2.7 on this machine (MinGW) has no reliable offline PBT gem, so this
# harness provides a small, dependency-free equivalent: a seeded random loop
# of >= 100 iterations per property, with the seed reported on failure so any
# case can be reproduced.
module PropertyHelper
  DEFAULT_ITERATIONS = 100

  # Run at least `iterations` successful cases.
  #
  #   for_all(generate: ->(rng) { ... input ... }) do |input|
  #     # return truthy if the property holds for this input
  #   end
  #
  # The generator may return nil to skip an input (does not count toward the
  # iteration total). On failure the seed and input are reported so the exact
  # case can be reproduced.
  def for_all(generate:, iterations: DEFAULT_ITERATIONS, seed: nil)
    seed ||= Random.new_seed
    rng = Random.new(seed)
    successful = 0
    attempts = 0
    max_attempts = iterations * 100

    while successful < iterations && attempts < max_attempts
      attempts += 1
      input = generate.call(rng)
      next if input.nil?

      successful += 1
      result = yield(input)
      unless result
        flunk "property failed (seed=#{seed}, case #{successful}, input=#{input.inspect})"
      end
    end

    assert successful >= iterations,
           "generator produced only #{successful}/#{iterations} usable cases (seed=#{seed})"
  end

  # A random integer in an inclusive range.
  def rand_int(rng, min, max)
    min + rng.rand(max - min + 1)
  end
end
