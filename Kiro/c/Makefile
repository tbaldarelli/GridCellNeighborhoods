# Makefile for Grid Cell Neighborhoods - C Implementation

CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -Iinclude
LDFLAGS = -lcheck -lm -lpthread

SRC_DIR = src
TEST_DIR = tests
BUILD_DIR = build
OBJ_DIR = $(BUILD_DIR)/obj
BIN_DIR = $(BUILD_DIR)/bin

# Source files
SOURCES = $(wildcard $(SRC_DIR)/*.c)
OBJECTS = $(patsubst $(SRC_DIR)/%.c,$(OBJ_DIR)/%.o,$(SOURCES))

# Test files
TEST_SOURCES = $(wildcard $(TEST_DIR)/*.c)
TEST_OBJECTS = $(patsubst $(TEST_DIR)/%.c,$(OBJ_DIR)/%.o,$(TEST_SOURCES))

# Executables
TEST_PROPERTIES_EXEC = $(BIN_DIR)/test_properties
TEST_BDD_EXEC = $(BIN_DIR)/test_bdd_scenarios
TEST_EXEC = $(TEST_PROPERTIES_EXEC) $(TEST_BDD_EXEC)

.PHONY: all clean test directories

all: directories $(TEST_EXEC)

directories:
	@mkdir -p $(OBJ_DIR) $(BIN_DIR)

# Compile source files
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
	$(CC) $(CFLAGS) -c $< -o $@

# Compile test files
$(OBJ_DIR)/%.o: $(TEST_DIR)/%.c
	$(CC) $(CFLAGS) -c $< -o $@

# Link test executables
$(TEST_PROPERTIES_EXEC): $(OBJECTS) $(OBJ_DIR)/test_properties.o
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)

$(TEST_BDD_EXEC): $(OBJECTS) $(OBJ_DIR)/test_bdd_scenarios.o
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)

# Run tests
test: $(TEST_EXEC)
	@echo "Running property tests..."
	./$(TEST_PROPERTIES_EXEC)
	@echo ""
	@echo "Running BDD scenario tests..."
	./$(TEST_BDD_EXEC)

# Clean build artifacts
clean:
	rm -rf $(BUILD_DIR)

# Help
help:
	@echo "Available targets:"
	@echo "  all       - Build everything (default)"
	@echo "  test      - Build and run tests"
	@echo "  clean     - Remove build artifacts"
	@echo "  help      - Show this help message"
