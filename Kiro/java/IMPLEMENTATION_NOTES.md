# Java Implementation Notes

## Language-Specific Decisions

### Testing Framework Choice
- **JUnit 5 (Jupiter)**: Modern Java testing framework with excellent IDE support
- **jqwik**: Property-based testing framework for Java
  - Modern alternative to QuickCheck
  - Integrates seamlessly with JUnit 5
  - Provides `@Property` annotation for property tests
  - Supports custom generators and arbitraries
  - Minimum 100 iterations per property (configurable via `@Property(tries = 100)`)

### Data Structures
- **HashSet<Position>**: For storing unique cell positions (efficient union operations)
- **ArrayList<Position>**: For storing positive cell lists
- **Immutable Position**: Position class should be immutable with proper equals/hashCode

### Java Idioms
- Use Java Collections Framework (Set, List, Map)
- Implement proper equals() and hashCode() for Position class
- Use custom exceptions extending RuntimeException or Exception
- Follow Java naming conventions (camelCase for methods, PascalCase for classes)
- Use Java Streams API where appropriate for functional operations

### Build System
Both Maven and Gradle configurations are provided:
- **Maven**: Traditional Java build tool, uses `pom.xml`
- **Gradle**: Modern build tool, uses `build.gradle`

Choose one based on preference. Maven is more widely used in enterprise, Gradle is more flexible.

## Property-Based Testing with jqwik

### Basic Property Test Structure
```java
@Property
void propertyName(@ForAll("generatorName") Type param) {
    // Test logic
    assertThat(result).satisfies(condition);
}

@Provide
Arbitrary<Type> generatorName() {
    return Arbitraries.integers()
        .between(min, max)
        .map(i -> new Type(i));
}
```

### Test Tagging Format
Each property test must include a comment referencing the design document:
```java
/**
 * Feature: grid-neighborhoods, Property 1: Grid Validation
 * Validates: Requirements 1.1, 1.2
 */
@Property
void testGridValidation() { ... }
```

## Cross-Language Consistency

The Java implementation must produce identical results to Python and C implementations for all BDD scenarios. Use the standardized output format for comparison:

```java
System.out.println(String.format(
    "Scenario %d: Expected=%d, Grid=%dx%d, N=%d, Pos=%s, Got=%d",
    scenarioNum, expected, height, width, threshold, positions, actual
));
```

## Some notes when comparing to my Java implementation, and lessons learned.  Everything above automatically generated, for most part.

 - I can confirm that test results from Java give same results as ../log/GridCellNeighborhoodsWithinDistance_EndPointLogic2E.log

### Implementation Comparison

  - The biggest difference between this version and my by-hand version is that my by-hand version, GridCellNeighborhoodsWithinDistance, is all in one file, with tests as part of the main method, and it went from using a square boundary to using a diamond boundary, among other things.  So it was a more iterative approach, as I learned things and received feedback.
  - As with Python version and by-hand versions, we build a 2-D array, but unlike my by-hand version, we used a real 2-D array.  In my by-hand version, I used a list of lists.  I suppose that using a 2-D array is faster and clearer, but I tend to choose Lists of Lists because they allow growth.  In this case, that is no such a concern, though.
  - If no positive cells, my by-hand version initialzes othere cells to `-1`, while Python and this version initialze it to '0'.  As implied in Pythin version IMPLEMENTATION_NOTES.md, Python allows use to be clearer on the fact that we are setting them all to 0, while Java version is implied.
  - We do a deep copy in Python and AI Java versions.  Python is easier to read.  The C version doesn't need it (doesn't create full 2-D array), and my by-hand version doesn't need it either.  Granted, my by-hand version doesn't need it because it always loads the positive cells as it creates the full grid and doesn't really let us initialize grid cells to anything but -1.
  - Unlike my by-hand version, but similar to the AI versions, we don't really calculate the manhattan distance, we just trust the diamond formation to prodce the correct results.  This works because manhatten distance always produces a diamond shape in the grid.
    - There is a trade-off between correctness and performance here.  By not calculating Manhattan distance, we save time, but we assume that the diamond shape is correct.  This is a safe assumption for the problem as defined, but might not be for other problems.
    - The `PropertyTest.java` does verify Manhattan distance calculation, so we are good there.
    - We use max possible distance as (height - 1) + (width - 1) which is the maximum Manhattan distance possible in the grid.  It works out to the same as |height-0| + |width-0|.  As an example, for an 11x11 grid, left bottom corner is `0,0`, and top right corner is `10,10`. |10-0| + |10-0| = 20, and (11 - 1 ) + (11 -1 ) = 20, so the math works.