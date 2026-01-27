# Grid Cell Neighborhoods - C Implementation

This directory contains the C implementation of the Grid Cell Neighborhoods algorithm.

## Structure

- `src/` - Source code files
- `tests/` - Test files
- `include/` - Header files
- `Makefile` - Build configuration

## Building

```bash
make
```

## Running Tests

```bash
make test
```

## Testing Framework

This implementation uses:
- **Check** - Unit testing framework for C
- **Theft** - Property-based testing library for C (QuickCheck-style)

## Installation Requirements

### Windows (using MSYS2/MinGW)
```bash
pacman -S mingw-w64-x86_64-check
pacman -S mingw-w64-x86_64-gcc
pacman -S make
```

For Theft (property-based testing), it needs to be built from source:
```bash
git clone https://github.com/silentbicycle/theft.git
cd theft
make
make install
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get install check
sudo apt-get install build-essential
```

### macOS
```bash
brew install check
```

## Implementation Notes

The C implementation follows the same algorithmic approach as the Python version:
- Modular architecture with separate components
- Manhattan distance calculation
- Diamond enumeration for neighborhoods
- Set-based union operations (using hash sets or sorted arrays)
- Proper memory management with allocation/deallocation

## Coordinate System

- (0,0) represents the bottom-left corner
- Row indices increase upward
- Column indices increase rightward
