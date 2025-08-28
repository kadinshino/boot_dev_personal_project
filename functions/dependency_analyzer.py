"""
Streamlined Dependency Analyzer
========================================================
Purpose: Analyze dependencies
"""

import ast
import sys
from pathlib import Path
from typing import Dict, List, Any, Set
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class DependencyIssue:
    """Simple dependency issue container."""
    file: str
    line: int
    type: str
    message: str
    severity: str = "warning"


# Standard library modules
STDLIB_MODULES = {
    'os', 'sys', 'json', 'csv', 'datetime', 'pathlib', 'typing', 'collections',
    'itertools', 'functools', 're', 'math', 'random', 'subprocess', 'threading',
    'asyncio', 'unittest', 'logging', 'argparse', 'urllib', 'http', 'socket'
}

if hasattr(sys, 'stdlib_module_names'):
    STDLIB_MODULES.update(sys.stdlib_module_names)


class DependencyAnalyzer:
    """Streamlined dependency analyzer."""
    
    def __init__(self):
        self.issues: List[DependencyIssue] = []
        self.all_imports: Dict[str, Set[str]] = defaultdict(set)
        self.unused_imports: List[Dict[str, Any]] = []
    
    def analyze_dependencies(self, project_path: str) -> Dict[str, Any]:
        """Main analysis entry point."""
        path = Path(project_path)
        if not path.exists():
            raise FileNotFoundError(f"Project path not found: {project_path}")
        
        python_files = [f for f in path.rglob("*.py") if self._should_analyze(f)]
        if not python_files:
            return self._empty_results()
        
        for file_path in python_files:
            try:
                self._analyze_file(file_path)
            except Exception as e:
                self.issues.append(DependencyIssue(
                    file=str(file_path), line=0, type="parse_error",
                    message=f"Failed to parse: {e}", severity="error"
                ))
        
        return self._compile_results(len(python_files))
    
    def _should_analyze(self, file_path: Path) -> bool:
        """Quick file filtering."""
        file_str = str(file_path).lower()
        skip_dirs = {'__pycache__', '.git', '.venv', 'venv', 'env', 'build', 'dist'}
        return not any(skip_dir in file_str for skip_dir in skip_dirs)
    
    def _analyze_file(self, file_path: Path):
        """Analyze single file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content, filename=str(file_path))
            visitor = SmartImportVisitor(str(file_path), content)
            visitor.visit(tree)
            
            # Record imports
            for import_name in visitor.imports:
                self.all_imports[import_name].add(str(file_path))
            
            # Find unused with smart filtering
            unused = visitor.get_unused_imports()
            for unused_import in unused:
                self.unused_imports.append({
                    'module_name': unused_import,
                    'file_path': str(file_path),
                    'line_number': visitor.import_lines.get(unused_import, 0)
                })
            
            self.issues.extend(visitor.issues)
            
        except SyntaxError as e:
            self.issues.append(DependencyIssue(
                file=str(file_path), line=e.lineno or 0, type="syntax_error",
                message=f"Syntax error: {e.msg}", severity="error"
            ))
    
    def _compile_results(self, files_analyzed: int) -> Dict[str, Any]:
        """Compile final results."""
        stdlib_count = sum(1 for imp in self.all_imports.keys() if self._is_stdlib(imp))
        third_party_count = sum(1 for imp in self.all_imports.keys() if self._is_third_party(imp))
        local_count = len(self.all_imports) - stdlib_count - third_party_count
        
        risk_level = "HIGH" if third_party_count > 50 else "MEDIUM" if third_party_count > 20 else "LOW"
        
        return {
            'stats': {
                'total_files': files_analyzed,
                'total_dependencies': len(self.all_imports),
                'standard_library': stdlib_count,
                'third_party': third_party_count,
                'local': local_count,
                'unused_imports': len(self.unused_imports)
            },
            'all_dependencies': dict(self.all_imports),
            'unused_imports': self.unused_imports,
            'circular_dependencies': [],  # Simplified - remove complex cycle detection
            'issues': self.issues,
            'risk_assessment': {
                'risk_level': risk_level,
                'risk_factors': self._get_risk_factors(third_party_count),
                'recommendations': self._get_recommendations(third_party_count)
            }
        }
    
    def _is_stdlib(self, module_name: str) -> bool:
        """Check if module is standard library."""
        return module_name.split('.')[0] in STDLIB_MODULES
    
    def _is_third_party(self, module_name: str) -> bool:
        """Check if module is third-party."""
        return not self._is_stdlib(module_name) and not module_name.startswith('.')
    
    def _get_risk_factors(self, third_party_count: int) -> List[str]:
        """Get risk factors."""
        factors = []
        if third_party_count > 50:
            factors.append(f"{third_party_count} third-party dependencies (very high)")
        elif third_party_count > 20:
            factors.append(f"{third_party_count} third-party dependencies (high)")
        
        if len(self.unused_imports) > 10:
            factors.append(f"{len(self.unused_imports)} unused imports")
        
        return factors or ["No significant risk factors"]
    
    def _get_recommendations(self, third_party_count: int) -> List[str]:
        """Get recommendations."""
        recommendations = []
        if third_party_count > 30:
            recommendations.append("📦 Consider reducing third-party dependency count")
        if len(self.unused_imports) > 5:
            recommendations.append("🧹 Remove unused imports to clean up codebase")
        return recommendations or ["✅ Dependency structure looks healthy!"]
    
    def _empty_results(self) -> Dict[str, Any]:
        """Empty results."""
        return {
            'stats': {'total_files': 0, 'total_dependencies': 0, 'standard_library': 0, 'third_party': 0, 'local': 0},
            'all_dependencies': {}, 'unused_imports': [], 'circular_dependencies': [], 'issues': [],
            'risk_assessment': {'risk_level': 'UNKNOWN', 'risk_factors': [], 'recommendations': []}
        }


class SmartImportVisitor(ast.NodeVisitor):
    """Smart visitor with ONLY the tkinter alias fix - no other changes."""
    
    def __init__(self, file_path: str, content: str):
        self.file_path = file_path
        self.content = content.lower()  # Use raw content for smart checks
        self.imports: Set[str] = set()
        self.import_lines: Dict[str, int] = {}
        self.import_aliases: Dict[str, str] = {}  # ONLY CHANGE: track aliases
        self.used_names: Set[str] = set()
        self.issues: List[DependencyIssue] = []
    
    def visit_Import(self, node: ast.Import):
        """Handle import statements - ONLY CHANGE: track aliases properly."""
        for alias in node.names:
            # Store the full module name
            self.imports.add(alias.name)
            self.import_lines[alias.name] = node.lineno
            
            # ONLY CHANGE: If there's an alias, track it
            if alias.asname:
                self.import_aliases[alias.name] = alias.asname
        
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node: ast.ImportFrom):
        """Handle from...import statements."""
        module = node.module or ""
        for alias in node.names:
            if alias.name == "*":
                self.issues.append(DependencyIssue(
                    file=self.file_path, line=node.lineno, type="star_import",
                    message=f"Star import from {module} - avoid using 'from {module} import *'",
                    severity="warning"
                ))
            else:
                full_name = f"{module}.{alias.name}" if module else alias.name
                self.imports.add(full_name)
                self.import_lines[full_name] = node.lineno
        self.generic_visit(node)
    
    def visit_Name(self, node: ast.Name):
        """Track name usage."""
        self.used_names.add(node.id)
        self.generic_visit(node)
    
    def visit_Attribute(self, node: ast.Attribute):
        """Track attribute usage like os.path."""
        if isinstance(node.value, ast.Name):
            self.used_names.add(node.value.id)
        self.generic_visit(node)
    
    def get_unused_imports(self) -> Set[str]:
        """Get unused imports - ONLY CHANGE: check aliases."""
        unused = set()
        
        for imported_module in self.imports:
            # Figure out what name is actually used in the code
            if imported_module in self.import_aliases:
                # ONLY CHANGE: If there's an alias, check for the alias name
                check_name = self.import_aliases[imported_module]
            else:
                # Original logic - unchanged
                if '.' in imported_module:
                    if imported_module.count('.') == 1 and not self._looks_like_submodule(imported_module):
                        check_name = imported_module.split('.')[1]  # from x import y
                    else:
                        check_name = imported_module.split('.')[0]  # import x.y -> x
                else:
                    check_name = imported_module  # import x -> x
            
            # Same smart checks as before - unchanged
            if not self._is_likely_used(check_name, imported_module):
                unused.add(imported_module)
        
        return unused
    
    def _looks_like_submodule(self, module_path: str) -> bool:
        """Check if this looks like a submodule import (import x.y)."""
        # Simple heuristic: if it's a common pattern like os.path, sys.argv, etc.
        common_submodules = ['os.path', 'sys.argv', 'json.loads', 'urllib.request']
        return any(module_path.startswith(sub.split('.')[0]) for sub in common_submodules)
    
    def _is_likely_used(self, check_name: str, full_module: str) -> bool:
        """Smart content-based detection - UNCHANGED."""
        # 1. Direct usage in AST
        if check_name in self.used_names:
            return True
        
        # 2. Content-based checks (catches most missed cases)
        content_checks = [
            f"{check_name}.",      # module.something
            f"{check_name}(",      # module()
            f"@{check_name}",      # @decorator
            f"{check_name}:",      # type hints
            f"[{check_name}]",     # typing[Module]
            f'"{check_name}"',     # in strings
            f"'{check_name}'",     # in strings
        ]
        
        if any(pattern in self.content for pattern in content_checks):
            return True
        
        # 3. Framework patterns that cause false positives
        framework_patterns = {
            'typing', 'dataclasses', 'abc', 'enum', 'pytest', 'unittest', 'logging'
        }
        
        if any(fw in full_module for fw in framework_patterns):
            return True
        
        # 4. Test files are more lenient
        if 'test' in self.file_path.lower():
            return True
        
        return False


# Simple public API
def analyze_project(project_path: str) -> Dict[str, Any]:
    """Analyze project dependencies."""
    analyzer = DependencyAnalyzer()
    return analyzer.analyze_dependencies(project_path)


# CLI interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python dependency_analyzer.py <project_path>")
        sys.exit(1)
    
    try:
        results = analyze_project(sys.argv[1])
        stats = results['stats']
        
        print("📦 DEPENDENCY ANALYSIS")
        print("=" * 30)
        print(f"Dependencies: {stats['total_dependencies']}")
        print(f"Third-party: {stats['third_party']}")
        print(f"Unused imports: {stats['unused_imports']}")
        print(f"Risk level: {results['risk_assessment']['risk_level']}")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"Dependency analysis failed: {e}")
        sys.exit(1)