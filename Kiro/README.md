# Multi-Language Grid Cell Neighborhoods

This directory contains implementations of the Grid Cell Neighborhoods algorithm in multiple programming languages. Each implementation is built from scratch using only the BDD scenarios and problem description, allowing for natural discovery of language-appropriate solutions.

## Project Goal

Implement the same algorithm across different languages to:
- Explore how different languages approach the same problem
- Learn language-specific idioms and patterns
- Compare implementation strategies and performance
- Validate that the BDD scenarios are complete and unambiguous

## Problem Summary

Count unique grid cells within Manhattan distance neighborhoods of positive-valued cells in a 2D grid. See the [BDD scenarios](original-requirements.md) for complete specification.

**Key Constraints:**
- Grid uses (0,0) as bottom-left corner.  This was a personal choice, and not really required by the problem statement.
- Manhattan distance: |row1 - row2| + |column1 - column2|
- No wraparound at boundaries
- Each cell counted at most once (union of overlapping neighborhoods)

## Implementations

### Python
- **Status**: ✅ Complete (84 tests passing)
- **Implementation Notes**: [python/IMPLEMENTATION_NOTES.md](python/IMPLEMENTATION_NOTES.md)
- **Testing**: pytest + Hypothesis (property-based testing)
- **Run Tests**: `cd python && python -m pytest -v`

### Java
- **Status**: ✅ Complete
- **Implementation Notes**: [java/IMPLEMENTATION_NOTES.md](java/IMPLEMENTATION_NOTES.md)
- **Testing**: JUnit + jqwik (property-based testing)
- **Run Tests**: `cd java && ./gradlew test`

### C
- **Status**: ✅ Complete
- **Implementation Notes**: [c/IMPLEMENTATION_NOTES.md](c/IMPLEMENTATION_NOTES.md)
- **Testing**: Custom test framework
- **Run Tests**: `cd c && make test`

### Go
- **Status**: ✅ Complete (34 tests passing)
- **Implementation Notes**: [go/IMPLEMENTATION_NOTES.md](go/IMPLEMENTATION_NOTES.md)
- **Testing**: Go testing + rapid (property-based testing)
- **Run Tests**: `cd go && go test -v`

### Future Languages
- TypeScript
- Rust
- C++
- JavaScript
- Others as desired

## Implementation Approach

Each language implementation:
1. **Starts from scratch** - Only uses BDD scenarios and problem description
2. **No code copying** - Discovers solutions naturally for each language
3. **Validates against all 26 scenarios** - Ensures correctness
4. **Uses language idioms** - Leverages language-specific strengths
5. **Documents decisions** - Records implementation choices and lessons learned

## Project Structure

```
Kiro/
├── README.md                          # This file
├── .kiro/
│   ├── README.md                      # Workspace documentation
│   └── specs/grid-neighborhoods/      # Spec-driven development artifacts
│       ├── requirements.md            # EARS-formatted requirements
│       ├── design.md                  # System design with correctness properties
│       └── tasks.md                   # Implementation task list
├── original-requirements.md           # Reference to BDD scenarios
├── parent-README.md                   # Reference to parent project README
├── python/
│   ├── IMPLEMENTATION_NOTES.md        # Python-specific notes
│   ├── *.py                           # Source files
│   └── test_*.py                      # Test files
├── java/
│   ├── IMPLEMENTATION_NOTES.md        # Java-specific notes (coming soon)
│   └── *.java                         # Source files
└── [other-languages]/
    ├── IMPLEMENTATION_NOTES.md
    └── source files
```

## BDD Scenarios

The 26 BDD scenarios cover:
- **Scenarios 1-2**: Single positive cell (fully contained, near edge)
- **Scenarios 3-14**: Multiple positive cells (overlapping and non-overlapping)
- **Scenarios 15-25**: Edge cases (1×N grids, N=0, N >> grid size)
- **Scenario 26**: No positive cells

See [grid-neighborhoods.feature.md](original-requirements.md) for complete scenarios.

## Spec-Driven Development

This project uses a formal spec-driven development approach:

1. **Requirements** - EARS-formatted requirements derived from BDD scenarios
2. **Design** - Architectural design with 13 correctness properties
3. **Tasks** - Implementation plan with property-based testing tasks
4. **Implementation** - Code that satisfies all requirements and properties

See [.kiro/specs/grid-neighborhoods/](.kiro/specs/grid-neighborhoods/) for complete specification.

## Testing Strategy

Each implementation includes:
- **Unit Tests**: Validate all 26 BDD scenarios
- **Property-Based Tests**: Validate 13 correctness properties with 100+ iterations
- **Integration Tests**: End-to-end validation
- **Error Handling Tests**: Input validation and edge cases

## Cross-Language Observations

*(To be filled in as implementations are compared)*

### Algorithm Convergence
- All implementations likely to use diamond enumeration for Manhattan distance
- Set-based operations for handling overlapping neighborhoods
- Boundary-aware iteration to avoid out-of-bounds checks

### Language-Specific Patterns
- Python: Sets, list comprehensions, type hints
- Java: HashSet, Stream API, strong typing
- Go: Maps, goroutines (potentially), explicit error handling
- TypeScript: Map/Set, functional methods, type safety

## Running Implementations

### Python
```bash
cd python
python -m pytest -v                    # Run all tests
python -m pytest test_properties.py    # Run property-based tests only
```

### Java
```bash
cd java
javac *.java                           # Compile
java GridCellNeighborhoods             # Run with test scenarios
```

### Other Languages
*(Instructions to be added as implementations are completed)*

## Contributing Notes

When adding a new language:
1. Create a new directory: `[language-name]/`
2. Implement from BDD scenarios only (no peeking at other implementations!)
3. Validate against all 26 scenarios
4. Create `IMPLEMENTATION_NOTES.md` documenting:
   - Implementation approach
   - Language features used
   - Lessons learned
   - Performance characteristics
   - Interesting differences from other implementations

## References

- **BDD Scenarios**: See `original-requirements.md` for path
- **Parent Project**: See `parent-README.md` for path
- **Spec Documentation**: [.kiro/specs/grid-neighborhoods/](.kiro/specs/grid-neighborhoods/)
