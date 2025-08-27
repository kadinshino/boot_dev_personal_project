# User Guide - Enhanced Code Analyzer

## 🚀 Quick Start

### **Installation**
1. Download or clone the project
2. Make sure you have Python 3.8+ installed
3. No additional dependencies needed - uses built-in libraries!

### **Run the App**
```bash
# GUI Mode (recommended for beginners)
python main.py

# CLI Mode (for power users)
python main.py --analyze ./my_project
```

That's it! 🎉

---

## 🖥️ Using the GUI (Easy Mode)

### **Step 1: Launch the App**
```bash
python main.py
```
A window opens with three tabs: Setup, Results, and Issues.

### **Step 2: Select Your Project**
1. Click the **"Browse..."** button
2. Navigate to your Python project folder
3. Click **"Select Folder"**

### **Step 3: Choose What to Analyze**
Check the boxes for what you want:
- ✅ **Code Quality** - Find code problems (recommended)
- ✅ **Security Scan** - Find security issues (recommended)  
- ✅ **Dependencies** - Analyze imports and dependencies (recommended)
- ⬜ **Codebase Discovery** - Understand unfamiliar projects
- ⬜ **Git Integration** - Check git repository status

### **Step 4: Run Analysis**
1. Click **"🚀 Run Analysis"**
2. Wait for it to finish (progress bar shows status)
3. Results appear automatically in the **Results** tab

### **Step 5: Review Results**
- **Results Tab**: Overview of your project analysis
- **Issues Tab**: Filter and search through specific problems found
- **Save Report**: Click "💾 Save Report" to export results

---

## 💻 Using the CLI (Power User Mode)

### **Basic Commands**

#### **Analyze Code Quality**
```bash
python main.py --analyze ./my_project
```
Shows code issues, complexity problems, and structure analysis.

#### **Security Scan**  
```bash
python main.py --security ./my_project
```
Finds security vulnerabilities like hardcoded passwords, SQL injection risks.

#### **Full Analysis**
```bash
python main.py --comprehensive ./my_project
```
Runs everything: code quality + security + dependencies.

#### **Understand Unknown Projects**
```bash
python main.py --legacy ./unfamiliar_project
```
Helps you understand what a codebase does and how to run it.

### **Save Results**
```bash
# Save as text file
python main.py --analyze ./project --save report.txt

# Save as JSON (for scripts)
python main.py --analyze ./project --json --save report.json
```

### **Git Integration**
```bash
# Check if code is ready to commit
python main.py --team ./my_project

# Install automatic pre-commit checks
python main.py --install-hooks ./my_project
```

---

## 🎯 What Each Analyzer Does

### **Code Quality Analyzer**
**Finds:** Long functions, missing documentation, too many parameters, complex code

**Example Issues:**
- "Function 'process_data' is 75 lines long (max: 50)"
- "Function 'calculate' missing docstring"  
- "Function 'handle_request' has 9 arguments (max: 7)"

**Why It Matters:** Cleaner code is easier to maintain and has fewer bugs.

### **Security Scanner**
**Finds:** Hardcoded passwords, code injection risks, weak encryption, debug mode enabled

**Example Issues:**
- "Hardcoded API key detected in config.py:15"
- "eval() usage can lead to code injection in parser.py:42"
- "SQL query uses string formatting - potential SQL injection"

**Why It Matters:** Security vulnerabilities can expose your app to attacks.

### **Dependency Analyzer**
**Finds:** Unused imports, circular dependencies, third-party package risks

**Example Issues:**
- "Unused import 'pandas' in data_processor.py:5"
- "Circular dependency detected: module A imports B, B imports A"
- "45 third-party dependencies detected (HIGH risk level)"

**Why It Matters:** Clean dependencies reduce security risks and improve performance.

### **Codebase Discovery**
**Finds:** What frameworks are used, main entry points, business logic patterns

**Example Output:**
- "🎯 This appears to be a Flask web application"
- "🚪 Primary entry point: app.py"
- "💼 Business logic includes: user authentication, payment processing"

**Why It Matters:** Helps you quickly understand unfamiliar codebases.

### **Git Integration**
**Finds:** Repository status, commit readiness, team collaboration info

**Example Output:**
- "✅ Safe to commit - no blocking issues found"
- "🚫 COMMIT BLOCKED: 3 critical security issues found"  
- "📋 Staged Files: 2 | Modified Files: 5"

**Why It Matters:** Prevents committing code with serious problems.

---

## 📊 Understanding Results

### **Issue Severity Levels**
- 🔴 **Critical**: Must fix immediately (security vulnerabilities)
- 🟠 **High**: Should fix soon (major code problems)
- 🟡 **Medium/Warning**: Good to fix (code quality improvements)
- 🔵 **Info/Low**: Optional improvements

### **Reading the Results Tab**
```
🎯 CODE ANALYSIS RESULTS
========================
📁 Project: /path/to/my_project  
📊 Total Issues: 23
🔧 Modules Used: code_analyzer, security_scanner
⏱️ Analysis Time: 2024-01-15T10:30:00

📋 CODE ANALYSIS
----------------
📄 Files: 45
🔧 Functions: 127
🗂️ Classes: 23
📝 Lines of Code: 3,456

🔒 SECURITY ANALYSIS  
--------------------
🚨 Risk Level: MEDIUM
🛡️ Vulnerabilities: 5
  🟡 Medium: 3
  🔵 Low: 2
```

### **Using the Issues Tab**
1. **Filter by Severity**: Dropdown to show only critical/high/medium/low issues
2. **Search**: Type keywords to find specific issues
3. **Issue Details**: Each issue shows:
   - File name and line number
   - Problem description  
   - Severity level
   - Issue type

---

## 🛠️ Common Use Cases

### **Before Committing Code**
```bash
# Quick check before git commit
python main.py --security ./my_project

# If any critical issues found, fix them first
# Then commit your code
```

### **Code Review Preparation**
```bash
# Get comprehensive analysis for code review  
python main.py --comprehensive ./my_project --save review_report.txt

# Share the report with your team
```

### **Understanding a New Codebase**
```bash
# Just joined a project? Understand it quickly
python main.py --legacy ./new_project

# Shows frameworks, entry points, and business logic
```

### **CI/CD Integration**
```bash
# Add to your build pipeline
python main.py --security ./project --json

# Returns exit code 2 if critical issues found (fails the build)
```

### **Regular Code Health Checks**
```bash
# Weekly code quality check
python main.py --analyze ./project --save weekly_report_$(date +%Y%m%d).txt
```

---

## 🎓 Tips for Better Results

### **Organize Your Project**
- Keep Python files in logical folders
- Use descriptive file and function names
- Add docstrings to functions and classes

### **Fix Issues by Priority**
1. **Critical Security Issues** - Fix immediately
2. **High Priority Issues** - Fix before next release  
3. **Code Quality Warnings** - Fix during refactoring
4. **Info Messages** - Fix when you have time

### **Use Git Integration**
```bash
# Install pre-commit hooks to catch issues early
python main.py --install-hooks ./my_project

# Now analysis runs automatically before each commit
```

### **Regular Maintenance**
- Run comprehensive analysis weekly
- Focus on security scans before releases
- Use dependency analysis to keep imports clean

---

## ❓ Troubleshooting

### **"No Python files found"**
- Make sure you selected the right folder
- Check that your project has `.py` files
- Try selecting the parent directory

### **"Module not available"**
- Some analyzers may be disabled if dependencies are missing
- The app works with built-in modules, but some advanced features need extra packages
- Click "🔄 Refresh Modules" to check again

### **"Analysis failed"**  
- Check that you have read permissions for the project folder
- Make sure Python files are valid (no syntax errors)
- Try analyzing a smaller subset of files first

### **GUI won't start**
- Make sure you have tkinter installed: `python -c "import tkinter"`  
- Try CLI mode instead: `python main.py --analyze ./project`

### **Slow analysis**
- Large projects take longer to analyze
- Try analyzing specific modules first
- Consider excluding test files or build directories

---

## 🏁 Getting Started Checklist

- [ ] Download/clone the Enhanced Code Analyzer
- [ ] Open terminal/command prompt in the analyzer folder
- [ ] Run `python main.py` to launch GUI mode
- [ ] Click "Browse" and select your Python project
- [ ] Check "Code Quality", "Security Scan", and "Dependencies" 
- [ ] Click "🚀 Run Analysis"
- [ ] Review results in the Results tab
- [ ] Filter issues in the Issues tab
- [ ] Save report with "💾 Save Report"
- [ ] Fix critical and high priority issues first

**You're ready to analyze code like a pro!** 🎉