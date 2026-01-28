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
