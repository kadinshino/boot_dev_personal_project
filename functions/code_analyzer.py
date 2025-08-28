"""
Code Analyzer - Fixed File Path Issue
============================================================
The problem: GUI shows "Unknown:0" while CLI shows correct file paths

Issue: The Issue dataclass uses 'file' but IssueVisitor expects 'file_path'
"""

import ast
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class Issue:
    """Simple issue container with CONSISTENT field names."""
    file_path: str  # Changed from 'file' to 'file_path' for consistency
    line_number: int  # Changed from 'line' to 'line_number' for consistency  
    issue_type: str   # Changed from 'type' to 'issue_type' for consistency
    message: str
    severity: str = "warning"


# Configuration - easily adjustable
CONFIG = {
    'max_function_length': 50,
    'max_function_args': 7,
    'max_class_methods': 20,
    'ignore_private': True,
    'ignore_test_files': True,
    'exclude_patterns': {'__pycache__', '.git', '*.pyc', 'venv', 'env'}
}


class CodeAnalyzer:
    """Just finds problems."""
    
    def __init__(self):
        self.issues: List[Issue] = []
        self.stats = {'files': 0, 'functions': 0, 'classes': 0, 'lines': 0}
    
    def analyze_project(self, project_path: str) -> Dict[str, Any]:
        """Main analysis entry point."""
        path = Path(project_path)
        if not path.exists():
            raise FileNotFoundError(f"Path not found: {project_path}")
        
        # Find and analyze Python files
        python_files = [f for f in path.rglob("*.py") if self._should_analyze(f)]
        
        for file_path in python_files:
            try:
                self._analyze_file(file_path)
            except Exception as e:
                self.issues.append(Issue(
                    file_path=str(file_path),  # FIXED: Use full file path
                    line_number=0, 
                    issue_type="parse_error",
                    message=f"Failed to parse: {e}", 
                    severity="error"
                ))
        
        return {
            'issues': self.issues,
            'total_files': self.stats['files'],
            'total_functions': self.stats['functions'], 
            'total_classes': self.stats['classes'],
            'total_lines': self.stats['lines'],
            'project_path': str(path),
            'files_analyzed': len(python_files)
        }
    
    def _should_analyze(self, file_path: Path) -> bool:
        """Quick file filtering."""
        file_str = str(file_path).lower()
        
        # Skip excluded patterns
        for pattern in CONFIG['exclude_patterns']:
            if pattern.replace('*', '') in file_str:
                return False
        
        # Skip test files if configured
        if CONFIG['ignore_test_files'] and 'test' in file_str:
            return False
            
        return True
    
    def _analyze_file(self, file_path: Path):
        """Analyze single file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update stats
        self.stats['files'] += 1
        self.stats['lines'] += len(content.splitlines())
        
        try:
            tree = ast.parse(content, filename=str(file_path))
            visitor = IssueVisitor(str(file_path))  # FIXED: Pass full path
            visitor.visit(tree)
            
            # Collect results
            self.issues.extend(visitor.issues)
            self.stats['functions'] += visitor.function_count
            self.stats['classes'] += visitor.class_count
            
        except SyntaxError as e:
            self.issues.append(Issue(
                file_path=str(file_path),  # FIXED: Use full file path
                line_number=e.lineno or 0, 
                issue_type="syntax_error",
                message=f"Syntax error: {e.msg}", 
                severity="error"
            ))


class IssueVisitor(ast.NodeVisitor):
    """AST visitor that finds code issues."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path  # Store the full file path
        self.issues: List[Issue] = []
        self.function_count = 0
        self.class_count = 0
        self.current_class = None
    
    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Check function issues."""
        self.function_count += 1
        self._check_function(node)
        self.generic_visit(node)
    
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        """Check async function issues."""
        self.function_count += 1
        self._check_function(node)
        self.generic_visit(node)
    
    def visit_ClassDef(self, node: ast.ClassDef):
        """Check class issues."""
        self.class_count += 1
        old_class = self.current_class
        self.current_class = node.name
        
        self._check_class(node)
        self.generic_visit(node)
        
        self.current_class = old_class
    
    def _check_function(self, node):
        """Check function for issues."""
        name = node.name
        
        # Skip private functions if configured
        if CONFIG['ignore_private'] and name.startswith('_'):
            return
        
        # Missing docstring
        if not ast.get_docstring(node) and not name.startswith('_'):
            self.issues.append(Issue(
                file_path=self.file_path,  # FIXED: Use stored file path
                line_number=node.lineno, 
                issue_type="missing_docstring",
                message=f"Function '{name}' missing docstring"
            ))
        
        # Too many arguments
        arg_count = len(node.args.args)
        if arg_count > CONFIG['max_function_args']:
            self.issues.append(Issue(
                file_path=self.file_path,  # FIXED: Use stored file path
                line_number=node.lineno, 
                issue_type="too_many_args",
                message=f"Function '{name}' has {arg_count} args (max: {CONFIG['max_function_args']})"
            ))
        
        # Function too long
        if hasattr(node, 'end_lineno'):
            length = node.end_lineno - node.lineno
            if length > CONFIG['max_function_length']:
                self.issues.append(Issue(
                    file_path=self.file_path,  # FIXED: Use stored file path
                    line_number=node.lineno, 
                    issue_type="long_function",
                    message=f"Function '{name}' is {length} lines (max: {CONFIG['max_function_length']})",
                    severity="info"
                ))
    
    def _check_class(self, node):
        """Check class for issues."""
        name = node.name
        
        # Missing docstring
        if not ast.get_docstring(node):
            self.issues.append(Issue(
                file_path=self.file_path,  # FIXED: Use stored file path
                line_number=node.lineno, 
                issue_type="missing_docstring",
                message=f"Class '{name}' missing docstring"
            ))
        
        # Count methods
        method_count = sum(1 for child in node.body 
                          if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)))
        
        if method_count > CONFIG['max_class_methods']:
            self.issues.append(Issue(
                file_path=self.file_path,  # FIXED: Use stored file path
                line_number=node.lineno, 
                issue_type="too_many_methods",
                message=f"Class '{name}' has {method_count} methods (max: {CONFIG['max_class_methods']})"
            ))


# Simple public API
def analyze_project(project_path: str) -> Dict[str, Any]:
    """Analyze project and return results."""
    analyzer = CodeAnalyzer()
    return analyzer.analyze_project(project_path)


def format_summary(results: Dict[str, Any]) -> str:
    """Create simple text summary."""
    issues = results['issues']
    
    lines = [
        f"Code Analysis Results",
        f"=====================",
        f"Files: {results.get('total_files', 0)} | Functions: {results.get('total_functions', 0)} | Classes: {results.get('total_classes', 0)}",
        f"Issues: {len(issues)} total",
        ""
    ]
    
    if not issues:
        lines.append("🎉 No issues found!")
        return "\n".join(lines)
    
    # Group by severity
    by_severity = {}
    for issue in issues:
        severity = issue.severity
        if severity not in by_severity:
            by_severity[severity] = []
        by_severity[severity].append(issue)
    
    # Show summary
    for severity in ['error', 'warning', 'info']:
        if severity in by_severity:
            count = len(by_severity[severity])
            lines.append(f"{severity.upper()}: {count}")
    
    lines.append("\nTop Issues:")
    lines.append("-----------")
    
    # Show first 10 issues
    for i, issue in enumerate(issues[:10], 1):
        file_name = Path(issue.file_path).name
        lines.append(f"{i}. {issue.severity.upper()}: {issue.message}")
        lines.append(f"   📄 {file_name}:{issue.line_number}")
    
    if len(issues) > 10:
        lines.append(f"... and {len(issues) - 10} more issues")
    
    return "\n".join(lines)


# CLI interface (if run directly)
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python code_analyzer.py <project_path>")
        sys.exit(1)
    
    try:
        results = analyze_project(sys.argv[1])
        print(format_summary(results))
        
        # Exit with error code if issues found
        errors = [i for i in results['issues'] if i.severity == 'error']
        sys.exit(1 if errors else 0)
        
    except Exception as e:
        print(f"Analysis failed: {e}")
        sys.exit(1)