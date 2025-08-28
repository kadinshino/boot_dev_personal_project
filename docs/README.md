# Enhanced Code Analyzer

A Python development tool that analyzes code quality, security vulnerabilities, dependencies, and project structure through both GUI and CLI interfaces.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg) ![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg) ![License](https://img.shields.io/badge/license-MIT-purple.svg)

> *"Analyze, understand, and improve your Python projects with confidence."*

---

## ✨ Features

- 🔍 **Code Quality Analysis** - Detect issues in code structure, complexity, and style
- 🔒 **Security Scanning** - Find potential vulnerabilities and security risks
- 📦 **Dependency Analysis** - Map imports, find unused dependencies, detect circular imports
- 🗺️ **Codebase Discovery** - Understand project structure and identify frameworks
- 🔗 **Git Integration** - Repository analysis and pre-commit hook installation
- 🖥️ **Dual Interface** - Full-featured GUI and powerful CLI options
- 📊 **Export Reports** - Save results in text or JSON format

---

## 🚀 Quick Start

### **Installation**
```bash
# Clone the repository
git clone https://github.com/kadinshino/boot_dev_personal_project.git
cd boot_dev_personal_project

# Run the application
python main.py
```

### **Requirements**
- Python 3.8+
- Tkinter (included with Python)
- No additional dependencies needed!

### **Usage**

#### **GUI Mode** (Recommended)
```bash
python main.py
```
1. Click "Browse" to select your Python project
2. Choose which analysis modules to run
3. Click "Run Analysis" and view results

#### **CLI Mode** (Advanced)
```bash
# Basic code analysis
python main.py --analyze ./my_project

# Security scan
python main.py --security ./my_project

# Full comprehensive analysis
python main.py --comprehensive ./my_project

# Save results to file
python main.py --analyze ./my_project --save report.txt
```

---

## 📊 What It Analyzes

| Module | What It Finds | Example Issues |
|--------|---------------|----------------|
| **Code Quality** | Long functions, missing docs, complexity | "Function too long (75 lines)", "Missing docstring" |
| **Security** | Hardcoded secrets, injection risks | "Hardcoded API key detected", "SQL injection risk" |
| **Dependencies** | Unused imports, circular deps | "Unused import 'pandas'", "Circular dependency A→B→A" |
| **Discovery** | Frameworks, entry points, patterns | "Flask web app detected", "Entry point: app.py" |
| **Git Integration** | Repo status, commit readiness | "Safe to commit", "3 staged files" |

---

## 🏗️ Project Structure

```
enhanced-code-analyzer/
├── main.py                  # Application entry point
├── functions/               # Analysis modules
│   ├── analysis_controller.py
│   ├── code_analyzer.py
│   ├── security_scanner.py
│   ├── dependency_analyzer.py
│   ├── codebase_discovery.py
│   └── git_integration.py
├── gui/                     # GUI components  
│   ├── analyzer_gui.py
│   ├── setup_tab.py
│   ├── results_tab.py
│   └── issues_tab.py
├── cli/                     # CLI interface
│   └── command_handler.py
└── docs/                    # Documentation
    ├── user-guide.md
    ├── api-reference.md
    └── architecture.md
```

---

## 🎯 Use Cases

- **Before Code Review** - Find issues before your team does
- **Security Audits** - Scan for common vulnerabilities  
- **New Project Onboarding** - Understand unfamiliar codebases
- **CI/CD Integration** - Automated code quality checks
- **Refactoring Prep** - Identify technical debt and complexity hotspots

---

## 📋 Sample Output

```
🎯 CODE ANALYSIS RESULTS
========================
📁 Project: my-awesome-project
📊 Total Issues: 12
🔧 Modules: code_analyzer, security_scanner

🔒 SECURITY ANALYSIS
--------------------
🚨 Risk Level: MEDIUM  
🛡️ Vulnerabilities: 3
  🟡 Medium: 2
  🔵 Low: 1

📋 NEXT STEPS:
🟡 Consider fixing 2 warnings for better code quality
📊 Check the Issues tab for detailed information
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 👨‍💻 About

**Created by:** Kadin Shino  
**Project Type:** Boot.dev Personal Project  
**GitHub:** [boot_dev_personal_project](https://github.com/kadinshino/boot_dev_personal_project)

*Built as a comprehensive milestone project demonstrating Python development skills, software architecture, and practical tool creation.*
