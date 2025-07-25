# List available commands
help:
    just --list

# Run spoofer as a module
mod:
    sudo -E $(which uv) run python -m src

# Run spoofer directly
run:
    sudo -E $(which uv) run python src/main.py

# Run tests
test:
    uv run pytest tests/ -v
