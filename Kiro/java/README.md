# Grid Cell Neighborhoods - Java Implementation

This directory contains the Java implementation of the Grid Cell Neighborhoods algorithm.

## Building and Running

### Prerequisites
- Java 11 or higher
- Maven 3.6 or higher (primary and recommended build tool)

### Build with Maven
```bash
mvn clean compile
```

### Run Tests with Maven
```bash
mvn test
```

### Alternative: Gradle
The project includes a `build.gradle` file for Gradle users. However, Maven is the primary build tool and is fully tested. If you prefer Gradle:

```bash
gradle build
gradle test
```

**Note**: Gradle support requires Gradle 7.3+ for Java 11-17, or Gradle 8.5+ for Java 21+. Maven is recommended for the most reliable build experience.

## Test Coverage

The Java implementation includes comprehensive test coverage:

- **12 Property-Based Tests** using jqwik framework
  - Tests universal properties across randomized inputs
  - Validates all 12 correctness properties from the design document
  - Runs 100 iterations per property test

- **26 BDD Scenario Tests** using JUnit 5
  - Tests specific concrete examples from the design document
  - Covers single cells, multiple cells, overlapping neighborhoods, degenerate grids
  - Validates cross-language consistency with Python and C implementations

### Running Specific Test Suites

```bash
# Run only property tests
mvn test -Dtest=PropertyTests

# Run only BDD scenario tests
mvn test -Dtest=BDDScenarioTests
```

## Implementation Structure

```
src/main/java/gridneighborhoods/
├── Position.java                    # Grid position with Manhattan distance
├── Grid.java                        # 2D grid with positive cell storage
├── DistanceCalculator.java          # Manhattan distance calculations
├── BoundaryHandler.java             # Grid boundary validation
├── NeighborhoodCalculator.java      # Main neighborhood enumeration algorithm
└── exceptions/
    ├── InvalidGridDimensionsException.java
    ├── PositionOutOfBoundsException.java
    └── InvalidDistanceThresholdException.java

src/test/java/gridneighborhoods/
├── PropertyTests.java               # Property-based tests (jqwik)
└── BDDScenarioTests.java           # BDD scenario tests (JUnit 5)
```

## Algorithm Overview

The implementation uses an optimized diamond enumeration algorithm:

1. **Diamond Enumeration**: For each positive cell, enumerate all cells within Manhattan distance N
2. **Boundary Awareness**: Skip cells outside grid boundaries during enumeration
3. **Set-Based Union**: Use HashSet operations to combine overlapping neighborhoods
4. **Early Termination**: Optimize for edge cases (zero distance, excessive distance)

## Cross-Language Validation

All test scenarios produce identical results to the Python and C implementations, ensuring algorithmic consistency across languages.

## Testing Frameworks

- **JUnit 5** - Unit testing framework
- **jqwik 1.8.2** - Property-based testing framework for Java

## Implementation Notes

See IMPLEMENTATION_NOTES.md for detailed implementation decisions and optimizations.
