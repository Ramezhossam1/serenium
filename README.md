# Serenium

A production-ready tool to scaffold new packages with proper Debian packaging structure. Serenium provides an intuitive interface for creating both regular packages and metapackages with comprehensive validation, configuration file support, and beautiful terminal themes.

## Features

- ⚡ **Production-Ready**: Robust error handling, logging, and input validation
- 🎨 **Beautiful Themes**: Multiple terminal themes for enhanced user experience
- 📦 **Debian Packaging**: Complete Debian packaging structure (control, rules, changelog, etc.)
- 🖥️ **Desktop Entry Support**: Automatic generation of .desktop files for GUI applications
- 📂 **Menu Integration**: Proper placement in application menu structure
- 🔄 **Metapackage Support**: Create dependency-only packages
- 🛠️ **Build Scripts**: Automated build scripts for easy package compilation
- 📝 **Configuration Files**: Support for YAML and JSON configuration files
- 🧪 **Unit Tests**: Comprehensive test coverage
- 🔧 **CLI Interface**: Full command-line interface with argparse
- 📊 **Logging**: Detailed logging for debugging and monitoring

## Installation

### From PyPI (Recommended)

```bash
pip install serenium
```

### From Source

```bash
git clone https://github.com/serenium/serenium.git
cd serenium
pip install -e .
```

### Development Installation

```bash
git clone https://github.com/serenium/serenium.git
cd serenium
pip install -e ".[dev]"
```

## Quick Start

### Interactive Mode

```bash
serenium
```

### Using Configuration File

```bash
# Create a sample configuration
serenium --create-sample-config

# Use the configuration file
serenium --config config.yaml
```

### Command Line Options

```bash
serenium --help
serenium --theme ocean --config my-config.yaml
serenium --version
```

## Configuration Files

Serenium supports both YAML and JSON configuration files for automated package creation.

### Sample YAML Configuration

```yaml
name: my-awesome-package
version: 1.0.0
description: An awesome package created with Serenium
long_description: This is a longer description of what the package does and its purpose.
is_metapackage: false
tools:
  - tool1
  - tool2
create_desktop: true
desktop_name: My Awesome Package
desktop_comment: Launch my awesome package
desktop_icon: applications-system
desktop_categories: System
dependencies:
  - python3
  - python3-yaml
menu_section: 01-System
maintainer: Your Name
email: your.email@example.com
```

### Using Configuration Files

```bash
# Create a package from configuration
serenium --config my-package.yaml

# Override theme while using config
serenium --config my-package.yaml --theme cyberpunk
```

## Usage Examples

### Example: Creating a Security Tools Package

```bash
serenium
```

Interactive prompts:
```
⚡ Serenium Package Builder
========================================
Package name (e.g., serenium-toolkit): serenium-security-tools
Version (e.g., 1.0.0): 1.0.0
Short description: Collection of security analysis tools
Long description (optional): A comprehensive set of security tools for analysis

Package type:
1. Regular package (with files)
2. Metapackage (dependencies only)
Choose type [1/2]: 1

Tools to include (comma-separated, e.g., nmap, wireshark, john): 
nmap, wireshark, john, hashcat, sqlmap

Create desktop entry? [y/N]: y
Desktop entry name: Security Tools
Desktop comment: Launch security analysis tools
Icon name (optional): security-high
Categories (e.g., System;Security): System;Security

Dependencies (comma-separated, e.g., python3, git): 
python3, python3-pip

Menu section (e.g., 01-System): 02-Security

Maintainer name: Security Team
Maintainer email: security@serenium.org
```

### Example: Creating a Metapackage

```bash
serenium
```

For a metapackage that just installs dependencies:
```
Package name: serenium-dev-environment
Package type: 2 (Metapackage)
Dependencies: build-essential, git, python3, nodejs, npm
```

## Generated Package Structure

The tool creates a complete Debian package structure:

```
serenium-security-tools-1.0.0/
├── debian/
│   ├── changelog
│   ├── compat
│   ├── control
│   ├── rules
│   └── source/
│       └── format
├── usr/
│   ├── bin/
│   │   └── serenium-security-tools    # Launcher script
│   └── share/
│       ├── applications/
│       │   └── serenium-security-tools.desktop
│       └── serenium-menu/
│           └── applications/
│               └── 02-Security/
│                   └── serenium-security-tools.desktop -> ../../../applications/serenium-security-tools.desktop
├── build.sh                          # Build script
├── README.md                         # Package documentation
└── serenium-config.yaml              # Saved configuration
```

## Building the Package

After the scaffold is created:

```bash
cd serenium-security-tools-1.0.0
./build.sh
```

This will create a `.deb` file in the parent directory that can be installed:

```bash
sudo dpkg -i ../serenium-security-tools_1.0.0_all.deb
sudo apt-get install -f  # Fix dependencies if needed
```

## Available Themes

Serenium includes multiple beautiful terminal themes:

- **Serenium** (default) - Clean cyan and blue theme
- **Cyberpunk** - Bold magenta and cyan theme
- **Ocean** - Calming blue theme
- **Forest** - Natural green theme
- **Sunset** - Warm yellow and red theme
- **Monochrome** - Clean black and white theme
- **Neon** - Bright electric colors
- **Matrix** - Classic green matrix theme

### Using Themes

```bash
# Interactive theme selection
serenium

# Specify theme directly
serenium --theme ocean
serenium --theme cyberpunk
serenium --theme matrix
```

## Development

### Setting Up Development Environment

```bash
git clone https://github.com/serenium/serenium.git
cd serenium

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

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
```

### Code Quality

```bash
# Format code
black serenium.py themes.py tests/

# Check code style
flake8 serenium.py themes.py tests/

# Type checking
mypy serenium.py themes.py
```

### Building Distribution

```bash
# Build wheel and source distribution
python -m build

# Upload to PyPI (requires credentials)
twine upload dist/*
```

## Package Types

### Regular Packages
- Include actual files and scripts
- Can have desktop entries
- Appear in application menus
- Include launcher scripts for tools

### Metapackages
- Only install dependencies
- No files included (except Debian packaging)
- Useful for creating tool collections
- Smaller package size

## Menu Categories

Common menu sections:
- `01-System`: System utilities
- `02-Security`: Security tools
- `03-Development`: Development tools
- `04-Multimedia`: Multimedia applications
- `05-Graphics`: Graphics and design
- `99-Misc`: Miscellaneous tools

## Validation and Error Handling

Serenium includes comprehensive validation:

- **Package Name Validation**: Ensures names follow Debian standards
- **Version Validation**: Semantic versioning format checking
- **Email Validation**: Basic email format verification
- **Input Sanitization**: Removes potentially dangerous characters
- **File Permission Checks**: Ensures executable files have correct permissions
- **Dependency Validation**: Warns about potential issues

## Logging

Serenium provides detailed logging for debugging:

```bash
# Logs are written to serenium.log
tail -f serenium.log
```

Log levels:
- `INFO`: Normal operation messages
- `WARNING`: Non-critical issues
- `ERROR`: Serious errors
- `DEBUG`: Detailed debugging information

## Troubleshooting

### Build Errors
- Ensure all dependencies are installed: `sudo apt-get install build-essential debhelper`
- Check package naming conventions (no uppercase letters, no spaces)
- Verify dependencies exist in repositories

### Permission Issues
```bash
chmod +x serenium.py
chmod +x build.sh
```

### Menu Not Appearing
- Verify desktop entry syntax
- Check menu section exists
- Restart your desktop environment

### Configuration File Issues
- Validate YAML/JSON syntax
- Check file permissions
- Ensure all required fields are present

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests for new functionality
5. Run tests: `pytest`
6. Commit your changes: `git commit -m 'Add amazing feature'`
7. Push to branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📖 [Documentation](https://serenium.readthedocs.io)
- 🐛 [Issue Tracker](https://github.com/serenium/serenium/issues)
- 💬 [Discussions](https://github.com/serenium/serenium/discussions)
- 📧 [Email Support](mailto:team@serenium.org)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history.

---

**Generated by Serenium Package Builder** ⚡
