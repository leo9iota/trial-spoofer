# List available commands
default:
    @just --list

# Show project info
info:
    @echo "Project: vscode-spoofer"
    @echo "Python version: $(uv run python --version)"
    @echo "UV version: $(uv --version)"
    @echo "Dependencies:"
    @uv tree

# Setup development environment
setup:
    @echo "Setting up development environment..."
    uv sync --dev

# Run spoofer
run:
    uv run python src/main.py

# Install dependencies
install:
    uv sync

# Add new dependency
add package:
    uv add {{package}}

# Add new development dependency
add-dev package:
    uv add --dev {{package}}

# Run specific demo
demo demo:
    uv run python src/demos/{{demo}}

# Run tests
test:
    uv run pytest

# Run tests with coverage
test-cov:
    uv run pytest --cov=src --cov-report=html --cov-report=term

# Format code
format:
    uv run black .

# Check code formatting
format-check:
    uv run black --check .

# Lint code
lint:
    uv run ruff check .

# Fix linting issues
lint-fix:
    uv run ruff check --fix .

# Check types
typecheck:
    uv run mypy .

# Run all quality checks
check:
    format-check lint typecheck

# Fix all auto-fixable issues
fix:
    format lint-fix

# Clean up build artifacts and cache
clean:
    rm -rf .pytest_cache/
    rm -rf htmlcov/
    rm -rf .coverage
    rm -rf dist/
    rm -rf build/
    rm -rf *.egg-info/
    find . -type d -name __pycache__ -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete

# Build the package
build:
    uv build

# Install the package in development mode
dev-install:
    uv pip install -e .

# Update all dependencies
update:
    uv lock --upgrade

# Create a new virtual environment
venv:
    uv venv

# Activate virtual environment
activate-venv:
    source .venv/bin/activate

# Run security audit
audit:
    uv run pip-audit

# Generate requirements file for compatibility
requirements:
    uv export --format requirements-txt --output-file requirements.txt

# Run interactive Python shell
shell:
    uv run python

# Install pre-commit hooks
pre-commit-install:
    uv run pre-commit install

# Run pre-commit on all files
pre-commit:
    uv run pre-commit run --all-files
