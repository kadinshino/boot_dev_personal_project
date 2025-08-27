# Enhanced Code Analyzer Pro

A comprehensive Python development tool that provides code quality analysis, security scanning, dependency management, and team collaboration features through both GUI and CLI interfaces.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg) ![uv](https://img.shields.io/badge/dependency--manager-uv-green.svg) ![License](https://img.shields.io/badge/license-MIT-purple.svg)

---

## 🎯 Overview

**Enhanced Code Analyzer** is a professional-grade Python analysis suite designed for developers and teams who want to maintain high code quality, security standards, and efficient collaboration workflows. It combines multiple analysis modules into a single, easy-to-use tool.

> *"Comprehensive code analysis made simple - from security scanning to team collaboration."*

---

## ✨ Key Features

- 🔍 **Code Quality Analysis** - Analyze complexity, structure, and maintainability
- 🔒 **Security Vulnerability Scanning** - Detect security issues and hardcoded secrets
- 📦 **Dependency Analysis** - Map imports, find unused dependencies, detect circular references
- 🗺️ **Codebase Discovery** - Understand unfamiliar codebases quickly
- 🔄 **Git Integration** - Pre-commit hooks and team collaboration tools
- 🖥️ **Dual Interface** - Both GUI and CLI for different workflows
- 📊 **Comprehensive Reporting** - Detailed analysis reports with actionable insights

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended) or pip

### Installation with uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/code-analyzer-pro.git
cd code-analyzer-pro

# Install using uv (handles everything automatically)
uv sync

# Run the application
uv run python main.py
```

### Alternative Installation with pip

```bash
# Clone the repository
git clone https://github.com/yourusername/code-analyzer-pro.git
cd code-analyzer-pro

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Run the application
python main.py
```

### Optional Feature Installation

```bash
# Install with security analysis enhancements
uv sync --extra security

# Install with development tools
uv sync --extra development

# Install with coverage analysis tools
uv sync --extra coverage

# Install everything
uv sync --extra full
```

---

## 💻 Usage

### GUI Mode (Default)

```bash
# Launch GUI interface
uv run python main.py

# Or simply:
uv run code-analyzer
```

The GUI provides an intuitive interface for:
- Selecting project directories
- Choosing analysis modules
- Viewing results with filtering and search
- Exporting reports to various formats

### CLI Mode

```bash
# Basic code analysis
uv run python main.py --analyze /path/to/project

# Security scan only
uv run python main.py --security /path/to/project

# Comprehensive analysis (all modules)
uv run python main.py --comprehensive /path/to/project

# Legacy codebase discovery
uv run python main.py --legacy /path/to/project

# Team collaboration check
uv run python main.py --team /path/to/project

# Install git hooks
uv run python main.py --install-hooks /path/to/project
```

### Output Options

```bash
# Save results to file
uv run python main.py --analyze /path/to/project --save report.txt

# JSON output format
uv run python main.py --analyze /path/to/project --json

# Verbose output
uv run python main.py --analyze /path/to/project --verbose
```

---

## 🛠️ Project Structure

```
├── main.py                     # Application entry point
├── pyproject.toml              # Project configuration and dependencies
├── uv.lock                     # Locked dependency versions
├── README.md                   # This file
├── LICENSE.md                  # MIT license
│
├── functions/                  # Analysis modules
│   ├── analysis_controller.py  # Main business logic controller
│   ├── code_analyzer.py        # Code quality analysis
│   ├── security_scanner.py     # Security vulnerability detection
│   ├── dependency_analyzer.py  # Dependency and import analysis
│   ├── codebase_discovery.py   # Project structure discovery
│   └── git_integration.py      # Git hooks and team features
│
├── gui/                        # Tkinter GUI components
│   ├── analyzer_gui.py         # Main application window
│   ├── gui_components.py       # Reusable UI components
│   ├── setup_tab.py           # Project setup and configuration
│   ├── results_tab.py         # Analysis results display
│   └── issues_tab.py          # Issue filtering and management
│
├── cli/                        # Command-line interface
│   └── command_handler.py      # CLI command routing and execution
│
└── docs/                       # Documentation
    ├── architecture.md          # System design overview
    ├── development.md          # Development guidelines
    └── api.md                  # API documentation
```

---

## 🔧 Development Setup

### Using uv (Recommended)

```bash
# Clone and setup development environment
git clone https://github.com/yourusername/code-analyzer-pro.git
cd code-analyzer-pro

# Install with development dependencies
uv sync --extra development

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Format code
uv run black .

# Type checking
uv run mypy functions/ gui/ cli/

# Linting
uv run flake8
```

### Pre-commit Hooks

```bash
# Install git hooks for the project itself
uv run python main.py --install-hooks .

# Or manually install pre-commit
uv add --dev pre-commit
uv run pre-commit install
```

---

## 📊 Analysis Modules

### Code Quality Analyzer
- **Function complexity** analysis
- **Code structure** evaluation  
- **Documentation** completeness checks
- **Best practices** enforcement

### Security Scanner
- **Hardcoded secrets** detection (API keys, passwords, tokens)
- **Code injection** vulnerabilities (eval, exec usage)
- **Command injection** risks (subprocess with shell=True)
- **Weak cryptography** identification (MD5, SHA-1 usage)
- **SQL injection** pattern detection

### Dependency Analyzer
- **Import mapping** and dependency trees
- **Unused import** detection with smart filtering
- **Circular dependency** identification
- **Third-party risk** assessment
- **Standard library** vs external dependency analysis

### Codebase Discovery
- **Entry point** identification
- **Framework detection** (Django, Flask, FastAPI, etc.)
- **Business pattern** recognition
- **External service** integration mapping
- **Quick start** guide generation

### Git Integration
- **Pre-commit hooks** for automated quality checks
- **Team collaboration** status
- **Commit readiness** assessment
- **Modified file** analysis

---

## 🎨 Configuration

### Project Configuration

The tool uses `pyproject.toml` for configuration. Key sections:

```toml
[tool.code-analyzer]
# Custom configuration options
max_function_length = 50
ignore_test_files = true
security_scan_enabled = true

[tool.code-analyzer.exclusions]
# Directories to skip
directories = ["__pycache__", ".git", "venv", "build", "dist"]
files = ["setup.py", "conftest.py"]
```

### Environment Variables

```bash
# Disable GUI and force CLI mode
export CODE_ANALYZER_CLI_ONLY=1

# Set default project path
export CODE_ANALYZER_DEFAULT_PATH=/path/to/projects

# Enable debug logging
export CODE_ANALYZER_DEBUG=1
```

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Workflow

```bash
# Fork the repository and clone your fork
git clone https://github.com/yourusername/code-analyzer-pro.git
cd code-analyzer-pro

# Set up development environment
uv sync --extra development

# Create a feature branch
git checkout -b feature/amazing-feature

# Make changes and run tests
uv run pytest
uv run black .
uv run flake8

# Commit and push
git commit -m "Add amazing feature"
git push origin feature/amazing-feature
```

### Code Standards

- **Python 3.8+** compatibility
- **Black** for code formatting (100 character line length)
- **Type hints** for all public functions
- **Comprehensive tests** for new features
- **Clear docstrings** following Google style

### Testing

```bash
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=functions --cov=gui --cov=cli

# Run specific test file
uv run pytest tests/test_code_analyzer.py

# Run tests in parallel (if pytest-xdist installed)
uv run pytest -n auto
```

---

## 📈 Performance & Scalability

### Benchmarks

- **Small projects** (< 100 files): ~5-10 seconds
- **Medium projects** (100-1000 files): ~30-60 seconds  
- **Large projects** (1000+ files): ~2-5 minutes

### Memory Usage

- **Typical usage**: 50-200 MB RAM
- **Large codebases**: Up to 500 MB RAM
- **GUI overhead**: Additional ~50 MB

### Optimization Tips

```bash
# Analyze specific directories only
uv run python main.py --analyze /path/to/project/src

# Skip test files for faster analysis
export CODE_ANALYZER_IGNORE_TESTS=1

# Use CLI for batch processing (lower memory)
uv run python main.py --analyze /path/to/project --json > results.json
```

---

## 🐛 Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Ensure all dependencies are installed
uv sync --extra full

# Check Python version
python --version  # Should be 3.8+
```

**2. Tkinter Issues (Linux)**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL
sudo yum install tkinter
```

**3. Git Integration Issues**
```bash
# Ensure git is available
git --version

# Check repository status
git status
```

**4. Performance Issues**
```bash
# Exclude large directories
export CODE_ANALYZER_EXCLUDE="venv,node_modules,.git"

# Use CLI mode for better performance
uv run python main.py --analyze . --json
```

### Debug Mode

```bash
# Enable detailed logging
export CODE_ANALYZER_DEBUG=1
uv run python main.py

# Check log files
cat ~/.local/share/code-analyzer/debug.log
```

---

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE.md](LICENSE.md) for details.

---

## 🙏 Acknowledgments

**Created by:** The Enhanced Code Analyzer Team  
**Inspired by:** Modern DevOps practices and the need for comprehensive code quality tools  

### Dependencies

We stand on the shoulders of giants:
- **Python Standard Library** - The foundation of our analysis
- **Tkinter** - Cross-platform GUI framework
- **AST Module** - Python's Abstract Syntax Tree parsing
- **Pathlib** - Modern filesystem operations

---

## 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/code-analyzer-pro/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/code-analyzer-pro/discussions)
- **Email**: support@code-analyzer-pro.dev
- **Documentation**: [Full Documentation](https://code-analyzer-pro.readthedocs.io)

---

*Enhanced Code Analyzer Pro - Making code quality accessible to everyone.*