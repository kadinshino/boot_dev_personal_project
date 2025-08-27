# Code Analyzer

A comprehensive Python development tool that analyzes code quality, security vulnerabilities, dependencies, and project structure through both GUI and CLI interfaces.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg) ![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg) ![License](https://img.shields.io/badge/license-MIT-purple.svg)

---

## 🔍 Overview

**Code Analyzer** is a modular, extensible tool that provides deep insights into Python codebases. It features a clean GUI interface, comprehensive CLI commands, and follows MVC architecture principles for maintainable code organization.

> *"Analyze, understand, and improve your Python projects with confidence."*

---

## ✨ Key Features

- 🔍 **Code Quality Analysis** - Detect issues in code structure, complexity, and style
- 🔒 **Security Scanning** - Find potential vulnerabilities and security risks
- 📦 **Dependency Analysis** - Map imports, find unused dependencies, detect circular imports
- 🗺️ **Codebase Discovery** - Understand project structure and identify frameworks
- 🔗 **Git Integration** - Repository analysis and pre-commit hook installation
- 🖥️ **Dual Interface** - Full-featured GUI and powerful CLI options
- 📊 **Comprehensive Reports** - Export results in multiple formats (text, JSON, HTML)

---

## 🏗️ Architecture

The application follows a clean **MVC-inspired architecture** with proper separation of concerns:

### **Core Components**
- **`main.py`** - Entry point and interface routing
- **`analysis_controller.py`** - Business logic controller (Model layer)
- **`analyzer_gui.py`** - Main GUI application (View layer)
- **`command_handler.py`** - CLI command processing (Controller layer)

### **GUI Components**
- **`gui_components.py`** - Reusable UI widgets and components
- **`setup_tab.py`** - Project setup and module selection interface
- **`results_tab.py`** - Analysis results display with export options
- **`issues_tab.py`** - Issue filtering, search, and detailed view

### **Analysis Functions**
- **`code_analyzer.py`** - Code quality and structure analysis
- **`security_scanner.py`** - Security vulnerability detection
- **`dependency_analyzer.py`** - Import and dependency analysis
- **`codebase_discovery.py`** - Project structure and framework detection
- **`git_integration.py`** - Git repository analysis and hooks

---

## 🖼️ Screenshots

![Main Interface](screenshots/main_interface.png)
*Main analysis setup interface with module selection*

![Results View](screenshots/results_view.png)
*Comprehensive analysis results with detailed reporting*

![Issues Tab](screenshots/issues_tab.png)
*Issue filtering and search functionality*

---

## 🚀 Getting Started

### **Requirements**
- Python 3.8 or higher
- Tkinter (usually included with Python)
- Standard library modules (pathlib, ast, subprocess, etc.)

### **Installation**

```bash
# Clone the repository
git clone https://github.com/kadinshino/boot_dev_personal_project.git
cd enhanced-code-analyzer

# Install dependencies (minimal - uses standard library)
pip install -r requirements.txt

# Run the GUI application
python main.py

# Or use CLI mode
python main.py --analyze ./my_project
```

### **Quick Start**

1. **Launch GUI**: Run `python main.py` without arguments
2. **Select Project**: Browse to your Python project directory
3. **Choose Modules**: Select which analysis modules to run
4. **Run Analysis**: Click "Run Analysis" and view results
5. **Export Results**: Save reports in your preferred format

---

## 🎯 Usage Examples

### **GUI Mode**
```bash
# Launch with default project path
python main.py

# Launch with specific project
python main.py /path/to/project
```

### **CLI Mode**
```bash
# Basic code analysis
python main.py --analyze ./my_project

# Security scan only
python main.py --security ./my_project

# Comprehensive analysis with JSON output
python main.py --security ./my_project --json --save report.json

# Codebase discovery for unfamiliar projects
python main.py --legacy ./unknown_project

# Install git pre-commit hooks
python main.py --install-hooks ./my_project

# Team collaboration check
python main.py --team ./my_project
```

### **Module-Specific Analysis**
```bash
# Run individual analyzers directly
python -m functions.code_analyzer ./project_path
python -m functions.security_scanner ./project_path
python -m functions.dependency_analyzer ./project_path
```

---

## 🗂️ Project Structure

```
boot_dev_personal_project/  #code analyzer
│
├── main.py                      # Application entry point
├── LICENSE                      # MIT license
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
│
├── functions/                   # Analysis modules (Business Logic)
│   ├── __init__.py
│   ├── analysis_controller.py   # Main controller for all analysis
│   ├── code_analyzer.py         # Code quality analysis
│   ├── security_scanner.py      # Security vulnerability scanning  
│   ├── dependency_analyzer.py   # Import and dependency analysis
│   ├── codebase_discovery.py    # Project structure discovery
│   └── git_integration.py       # Git repository integration
│
├── gui/                         # GUI components (Presentation Layer)
│   ├── __init__.py
│   ├── analyzer_gui.py          # Main GUI application
│   ├── gui_components.py        # Reusable UI components
│   ├── setup_tab.py             # Setup and configuration tab
│   ├── results_tab.py           # Results display tab
│   └── issues_tab.py            # Issues filtering and search tab
│
├── cli/                         # CLI components (Interface Layer)
│   ├── __init__.py
│   └── command_handler.py       # CLI command processing
│
└── docs/                        # Documentation
    ├── architecture.md          # System design documentation
    ├── user-guide.md            # User manual
    └── api-reference.md         # API documentation
```

---

## 🔧 Configuration

### **Module Selection**
Available analysis modules:
- ✅ **Code Quality Analysis** (default: enabled)
- ✅ **Security Scanner** (default: enabled)  
- ✅ **Dependency Analysis** (default: enabled)
- ⚪ **Codebase Discovery** (default: disabled)
- ⚪ **Git Integration** (default: disabled)

### **Output Formats**
- **Text Reports** - Human-readable analysis summaries
- **JSON Export** - Structured data for integration
- **HTML Reports** - Formatted reports for sharing

### **Git Integration**
```bash
# Install pre-commit hooks for automatic analysis
python main.py --install-hooks ./my_project

# Check team collaboration status
python main.py --team ./my_project
```

---

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) for details.

---

## 🙏 Credits

**Created by:** [Kadin Shino]  
**GitHub:** [github.com/kadinshino/boot_dev_personal_project]  

### **Acknowledgments**
- Python AST module for code parsing capabilities
- Tkinter team for the GUI framework
- Open source community for inspiration and feedback

---

*Analyze with confidence. Build with quality. Ship with security.*