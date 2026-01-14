# Kiro Workspace Documentation

## File Reference Pattern

This workspace uses a file reference pattern for linking to external documents:

### Reference Files

- **`original-requirements.md`**: Contains a file path pointing to the BDD feature specification
- **`parent-README.md`**: Contains a file path pointing to the parent project README

### How to Read Referenced Files

These files contain absolute paths to the actual documents. To read them:

1. First, read the reference file to get the path:
   ```
   readFile: original-requirements.md
   ```

2. Then use PowerShell to read the actual file:
   ```powershell
   type "C:/Users/Tony Baldarelli/Documents/Development projects/VSCode/InterviewProjects/GridCellNeighborhoods/grid-neighborhoods.feature.md"
   ```

### Why This Pattern?

- **Cross-platform compatibility**: Avoids Windows symlink issues
- **Git-friendly**: No special Git configuration needed
- **Single source of truth**: References the original files without duplication
- **Simple**: Just text files with paths

### For AI Agents

When you see `original-requirements.md` or `parent-README.md`:
1. Read the file to get the target path
2. Use `executePwsh` with `type` command to read the actual content
3. The actual BDD scenarios are in the file at that path

## Project Structure

```
.kiro/
├── specs/
│   └── grid-neighborhoods/
│       ├── requirements.md    # Generated from BDD scenarios
│       ├── design.md          # System design
│       └── tasks.md           # Implementation tasks
└── README.md                  # This file

original-requirements.md       # Reference to BDD feature file
parent-README.md              # Reference to parent README

python/                       # Python implementation
├── *.py                      # Source files
└── test_*.py                 # Test files
```

## BDD Scenarios

The 26 BDD scenarios are defined in the file referenced by `original-requirements.md`. These scenarios drive:
- Requirements specification
- Design decisions
- Test implementation across all languages
