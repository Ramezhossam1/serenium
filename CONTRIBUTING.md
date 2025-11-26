# Contributing to Serenium

Thank you for your interest in contributing to Serenium! This document provides guidelines and information for contributors.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic knowledge of Python and Debian packaging

### Development Setup

1. **Fork the Repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/yourusername/serenium.git
   cd serenium
   ```

2. **Set Up Development Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install in development mode with dev dependencies
   pip install -e ".[dev]"
   
   # Install pre-commit hooks
   pre-commit install
   ```

3. **Verify Setup**
   ```bash
   # Run tests to ensure everything works
   pytest
   
   # Run code quality checks
   black --check serenium.py themes.py tests/
   flake8 serenium.py themes.py tests/
   mypy serenium.py themes.py
   ```

## Development Workflow

### 1. Create a Branch

```bash
# Create a feature branch from main
git checkout -b feature/your-feature-name

# Or a bugfix branch
git checkout -b fix/bug-description
```

### 2. Make Changes

- Follow the existing code style
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass

### 3. Code Quality

Before committing, ensure:

```bash
# Format code
black serenium.py themes.py tests/

# Run linting
flake8 serenium.py themes.py tests/

# Type checking
mypy serenium.py themes.py

# Run tests
pytest

# Check test coverage
pytest --cov=.
```

### 4. Commit Changes

```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "feat: add new feature description"

# Push to your fork
git push origin feature/your-feature-name
```

### 5. Create Pull Request

- Open a pull request against the `main` branch
- Fill out the PR template completely
- Wait for code review
- Address any feedback

## Code Style

### Formatting

We use [Black](https://black.readthedocs.io/) for code formatting:

```bash
black serenium.py themes.py tests/
```

Configuration:
- Line length: 100 characters
- Target Python versions: 3.8-3.12

### Linting

We use [flake8](https://flake8.pycqa.org/) for linting:

```bash
flake8 serenium.py themes.py tests/
```

Configuration:
- Max line length: 100
- Ignore: E203, W503 (conflicts with Black)

### Type Checking

We use [mypy](https://mypy.readthedocs.io/) for static type checking:

```bash
mypy serenium.py themes.py
```

### Documentation

- Use docstrings for all public functions and classes
- Follow Google-style docstring format
- Update README.md for user-facing changes
- Update man page for CLI changes

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_serenium.py

# Run with verbose output
pytest -v

# Run only fast tests
pytest -m "not slow"
```

### Writing Tests

- Add tests for all new functionality
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies when appropriate
- Aim for high test coverage

### Test Structure

```
tests/
├── __init__.py
├── test_serenium.py      # Main application tests
├── test_themes.py        # Theme system tests
└── conftest.py           # Shared test fixtures
```

## Types of Contributions

### Bug Fixes

1. Create an issue describing the bug
2. Create a branch: `fix/bug-description`
3. Write tests that reproduce the bug
4. Fix the bug
5. Ensure all tests pass
6. Submit a pull request

### New Features

1. Create an issue to discuss the feature
2. Create a branch: `feature/feature-name`
3. Implement the feature with tests
4. Update documentation
5. Submit a pull request

### Documentation

- Fix typos and grammatical errors
- Improve existing documentation
- Add examples and tutorials
- Update man pages

### Performance Improvements

- Profile the application
- Identify bottlenecks
- Implement optimizations
- Add benchmarks

## Submitting Changes

### Pull Request Process

1. **Update Documentation**
   - Update README.md if needed
   - Update CHANGELOG.md
   - Update man page for CLI changes

2. **Quality Checks**
   - Ensure all tests pass
   - Check code coverage
   - Verify code style compliance

3. **Pull Request Template**
   - Use the provided PR template
   - Describe the changes clearly
   - Link to relevant issues
   - Include screenshots for UI changes

### Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Tests
- `chore`: Maintenance

Examples:
```
feat: add configuration file support
fix: resolve package name validation issue
docs: update installation instructions
test: add tests for theme system
```

## Release Process

Releases are handled by maintainers:

1. Update version in pyproject.toml
2. Update CHANGELOG.md
3. Create git tag
4. Build and publish to PyPI
5. Create GitHub release

## Community

### Code of Conduct

Please be respectful and professional in all interactions. We follow the [Python Community Code of Conduct](https://www.python.org/psf/conduct/).

### Getting Help

- Create an issue for bugs or feature requests
- Start a discussion for questions
- Check existing issues and documentation

### Communication

- GitHub Issues: Bug reports and feature requests
- GitHub Discussions: General questions and ideas
- Email: team@serenium.org

## Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- Git commit history
- GitHub contributors list

## Resources

### Documentation

- [Python Packaging User Guide](https://packaging.python.org/)
- [Debian Packaging Guide](https://www.debian.org/doc/manuals/debmake-doc/)
- [pytest Documentation](https://docs.pytest.org/)
- [Black Documentation](https://black.readthedocs.io/)

### Tools

- [pre-commit](https://pre-commit.com/) - Git hooks
- [tox](https://tox.readthedocs.io/) - Test automation
- [sphinx](https://www.sphinx-doc.org/) - Documentation

## Questions?

If you have questions about contributing:

1. Check existing issues and discussions
2. Read the documentation
3. Create a discussion for general questions
4. Create an issue for specific problems

Thank you for contributing to Serenium! 🚀
