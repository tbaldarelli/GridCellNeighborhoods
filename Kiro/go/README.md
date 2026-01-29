# Grid Cell Neighborhoods - Go Implementation

## Overview

Go implementation of the Grid Cell Neighborhoods algorithm using idiomatic Go patterns and the standard testing library.

## Structure

```
go/
├── go.mod                      # Go module definition
├── README.md                   # This file
├── IMPLEMENTATION_NOTES.md     # Implementation decisions and notes
├── position.go                 # Position struct and methods
├── grid.go                     # Grid struct and validation
├── distance_calculator.go      # Manhattan distance calculation
├── boundary_handler.go         # Boundary validation
├── neighborhood_calculator.go  # Main neighborhood calculation logic
├── exceptions.go               # Custom error types
├── bdd_scenarios_test.go       # BDD scenario tests
├── properties_test.go          # Property-based tests
└── examples/                   # Example programs
    └── basic/                  # Basic usage example
        ├── main.go
        └── go.mod
```

## Running Tests

```bash
# Run all tests
go test -v

# Run specific test file
go test -v -run TestBDDScenarios

# Run property-based tests
go test -v -run TestProperties

# Run with coverage
go test -v -cover
```

## Running Examples

```bash
# Run the basic example
cd examples/basic
go run .

# Or compile and run
go build -o example.exe
./example.exe
```

## Property-Based Testing

This implementation uses the `rapid` library for property-based testing, which provides:
- Automatic test case generation
- Shrinking of failing examples
- Deterministic replay of failures

Install rapid:
```bash
go get pgregory.net/rapid
```

## Implementation Notes

See [IMPLEMENTATION_NOTES.md](IMPLEMENTATION_NOTES.md) for detailed implementation decisions and Go-specific patterns used.

## Testing Strategy

- **BDD Scenarios**: 26 concrete test cases validating expected behavior
- **Property Tests**: 13 universal properties with 100+ iterations each
- **Integration Tests**: End-to-end validation with complex scenarios
- **Error Handling Tests**: Input validation and edge cases

## Cross-Language Validation

All test scenarios produce identical results to Python, Java, and C implementations.
