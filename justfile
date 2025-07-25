# List available commands
help:
    just --list

# Run spoofer as a module
run:
    sudo -E $(which uv) run python -m src

# Run spoofer directly
run-direct:
    sudo -E $(which uv) run python src/main.py

# Run tests
test:
    uv run pytest tests/ -v

# Run tests with short output
test-short:
    uv run pytest tests/
