# Grid Cell Neighborhoods — Ruby

Ruby implementation of the Grid Cell Neighborhoods algorithm: counts the total
number of unique grid cells within Manhattan distance `N` of any positive-valued
cell in a 2D grid.

Implemented directly from the spec in `../.kiro/specs/grid-neighborhoods/`
(requirements.md + design.md), not migrated from the other language versions.

## Layout

```
ruby/
  Gemfile
  Rakefile
  lib/
    grid_neighborhoods.rb                       # top-level require
    grid_neighborhoods/
      position.rb                               # Position + Manhattan distance
      grid.rb                                   # Grid model + validation
      errors.rb                                 # error hierarchy
      boundary_handler.rb                       # bounds checks / filtering
      neighborhood_calculator.rb                # diamond enumeration + union
  test/
    bdd_scenarios_test.rb                       # 26 canonical BDD scenarios (minitest)
    properties_test.rb                          # 13 correctness properties
    property_helper.rb                          # self-contained PBT harness
```

## Run tests

minitest ships with Ruby, so no `bundle install` is required:

```
ruby -Ilib -Itest test/bdd_scenarios_test.rb   # 26 BDD scenarios + output lines
ruby -Ilib -Itest test/properties_test.rb      # 13 properties
rake test                                       # both (needs the rake gem)
```

## Cross-language output

Each BDD scenario prints:

```
Scenario {N}: Expected={expected}, Grid={H}x{W}, N={threshold}, Pos=[{positions}], Got={actual}
```

matching the format used by the C, Go, Java, Rust, and C# implementations.
