# API Reference - Enhanced Code Analyzer

## 🎯 Quick Reference

### **Main Entry Points**
```python
# Direct analyzer usage
from functions.code_analyzer import analyze_project
from functions.security_scanner import SecurityScanner
from functions.dependency_analyzer import analyze_project
from functions.codebase_discovery import analyze_codebase
```

### **Controller API**
```python
# Programmatic integration
from functions.analysis_controller import AnalysisController
controller = AnalysisController()
results = controller.run_analysis_sync(path, modules)
```

### **CLI Commands**
```bash
# Command-line usage
python main.py --analyze ./project
python main.py --security ./project
python main.py --comprehensive ./project --json
```

---

## 📚 Function APIs

### **Code Analyzer**

#### `analyze_project(project_path: str) -> Dict[str, Any]`
Analyzes Python code for quality issues, complexity, and structure problems.

**Parameters:**
- `project_path` (str): Path to Python project directory

**Returns:**
```python
{
    'issues': [Issue],           # List of code issues found
    'stats': {                   # Project statistics
        'files': int,
        'functions': int, 
        'classes': int,
        'lines': int
    },
    'project_path': str,         # Input path
    'files_analyzed': int        # Number of files processed
}
```

**Example:**
```python
from functions.code_analyzer import analyze_project

results = analyze_project("./my_project")
print(f"Found {len(results['issues'])} issues in {results['stats']['files']} files")
```

### **Security Scanner**

#### `SecurityScanner.scan_project(project_path: str) -> Dict[str, Any]`
Scans for security vulnerabilities using pattern matching.

**Parameters:**
- `project_path` (str): Path to project directory

**Returns:**
```python
{
    'total_files_scanned': int,
    'total_vulnerabilities': int,
    'vulnerability_counts': {    # Count by severity
        'critical': int,
        'high': int,
        'medium': int,
        'low': int
    },
    'security_issues': [SecurityIssue],
    'risk_level': str,          # "CRITICAL", "HIGH", "MEDIUM", "LOW", "MINIMAL"
    'scan_summary': str         # Human-readable summary
}
```

**Example:**
```python
from functions.security_scanner import SecurityScanner

scanner = SecurityScanner()
results = scanner.scan_project("./my_project")
print(f"Risk level: {results['risk_level']}")
```

---

## 🎛️ Controller API

### **AnalysisController Class**

#### `__init__()`
Initialize the controller and discover available modules.

#### `get_available_modules() -> Dict[str, bool]`
Returns which analysis modules are available on the system.

#### `run_analysis_sync(project_path, enabled_modules) -> AnalysisResults`
Run analysis synchronously (for CLI/scripting usage).

#### `run_analysis_async(project_path, enabled_modules, progress_callback, completion_callback)`
Run analysis with async callbacks (for GUI usage).

**Example:**
```python
from functions.analysis_controller import AnalysisController

controller = AnalysisController()

# Check what's available
modules = controller.get_available_modules()
print(f"Available modules: {modules}")

# Run analysis
results = controller.run_analysis_sync(
    project_path="./my_project",
    enabled_modules={
        "code_analyzer": True,
        "security_scanner": True,
        "dependency_analyzer": False
    }
)

print(f"Analysis complete: {len(results.issues)} issues found")
```

---

## 💻 CLI API

### **Analysis Commands**

#### Basic Analysis
```bash
python main.py --analyze <project_path>
```
Runs code quality analysis only.

#### Security Analysis  
```bash
python main.py --security <project_path>
```
Runs security vulnerability scan only.

#### Comprehensive Analysis
```bash
python main.py --comprehensive <project_path>
```
Runs all available analysis modules.

#### Codebase Discovery
```bash
python main.py --legacy <project_path>
```
Analyzes unfamiliar codebases to understand structure and frameworks.

### **Output Options**

#### JSON Output
```bash
python main.py --analyze <path> --json
```
Returns results in JSON format instead of human-readable text.

#### Save to File
```bash
python main.py --analyze <path> --save report.txt
```
Saves analysis results to specified file.

#### Verbose Output
```bash
python main.py --analyze <path> --verbose
```
Shows detailed progress and debug information.

### **Git Integration**

#### Install Pre-commit Hooks
```bash
python main.py --install-hooks <project_path>
```
Installs git pre-commit hooks for automatic analysis.

#### Team Collaboration Check
```bash
python main.py --team <project_path>
```
Checks git repository status and commit readiness.

---

## 📋 Data Structures

### **Issue Object**
```python
@dataclass
class Issue:
    file: str        # File path where issue was found
    line: int        # Line number
    type: str        # Issue type identifier
    message: str     # Human-readable description
    severity: str    # "error", "warning", "info"
```

### **AnalysisResults Object**
```python
@dataclass
class AnalysisResults:
    success: bool                    # Whether analysis completed successfully
    results: Dict[str, Any]         # Raw analysis data from all modules
    issues: List[Any]               # Aggregated issues from all modules
    error_message: Optional[str]    # Error details if success=False
    modules_used: List[str]         # Which modules were executed
    
    def to_json(self) -> str        # Export as JSON string
    def to_dict(self) -> Dict       # Export as dictionary
```

---

## 🔌 Integration Examples

### **Integrate into CI/CD**
```python
#!/usr/bin/env python3
from functions.analysis_controller import AnalysisController

def check_code_quality():
    controller = AnalysisController()
    results = controller.run_analysis_sync(
        project_path=".",
        enabled_modules={"security_scanner": True}
    )
    
    # Block CI if critical security issues
    critical_issues = [
        issue for issue in results.issues 
        if getattr(issue, 'severity', '') == 'critical'
    ]
    
    if critical_issues:
        print(f"BLOCKING: {len(critical_issues)} critical security issues")
        exit(1)
    
    print("✅ Security check passed")
    exit(0)

if __name__ == "__main__":
    check_code_quality()
```

### **Custom Analysis Script**
```python
from functions.code_analyzer import analyze_project
from functions.security_scanner import SecurityScanner

def custom_analysis(project_path):
    # Run code analysis
    code_results = analyze_project(project_path)
    
    # Run security scan
    security_scanner = SecurityScanner()
    security_results = security_scanner.scan_project(project_path)
    
    # Combine and filter results
    all_issues = code_results['issues'] + security_results['security_issues']
    critical_issues = [i for i in all_issues if getattr(i, 'severity', '') == 'critical']
    
    return {
        'total_issues': len(all_issues),
        'critical_issues': len(critical_issues),
        'safe_to_deploy': len(critical_issues) == 0
    }
```

---

## ⚠️ Error Handling

All API functions handle errors gracefully:
- **File not found**: Raises `FileNotFoundError` with clear message
- **Permission errors**: Continues analysis, logs warnings  
- **Parse errors**: Adds parse error to issues list, continues with other files
- **Module unavailable**: Controller reports module as unavailable

### **Checking Module Availability**
```python
controller = AnalysisController()
available = controller.get_available_modules()

if not available['security_scanner']:
    print("Security scanner not available - install required dependencies")
```

---

## 🚀 Exit Codes (CLI)

- **0**: Success, no critical issues
- **1**: Warnings or errors found
- **2**: Critical security vulnerabilities found

Use these for CI/CD pipeline integration:
```bash
python main.py --security ./project
if [ $? -eq 2 ]; then
    echo "CRITICAL: Security issues block deployment"
    exit 1
fi
```