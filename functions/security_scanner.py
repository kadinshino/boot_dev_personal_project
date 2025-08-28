"""
Security Scanner
======================================================================
Purpose: Find security vulnerabilities in Python code.
"""

import re
from pathlib import Path
from typing import List, Dict, Any, Pattern
from dataclasses import dataclass

from utils.security_patterns import COMPILED_PATTERNS

@dataclass
class SecurityIssue:
    """Security vulnerability found in code."""
    file: str
    line: int
    type: str
    message: str
    severity: str  # critical, high, medium, low
    cwe_id: str = ""

class SecurityScanner:
    """Fast, focused security scanner."""
    
    def __init__(self):
        self.issues: List[SecurityIssue] = []
        
        # Files to exclude from scanning (they contain patterns by design)
        self.excluded_files = {
            'security_scanner.py',      # This file contains patterns
            'test_security.py',         # Test files with intentional vulnerabilities
            'security_patterns.py',
        }
    
    def scan_project(self, project_path: str) -> Dict[str, Any]:
        """Main entry point - scan project for security vulnerabilities."""
        path = Path(project_path)
        if not path.exists():
            raise FileNotFoundError(f"Project path not found: {project_path}")
        
        # Find Python files to scan
        python_files = [f for f in path.rglob("*.py") if self._should_scan(f)]
        
        if not python_files:
            return self._empty_results()
        
        # Scan each file
        for file_path in python_files:
            try:
                self._scan_file(file_path)
            except Exception as e:
                # Log error but continue scanning
                print(f"Warning: Failed to scan {file_path}: {e}")
        
        return self._compile_results(len(python_files))
    
    def _should_scan(self, file_path: Path) -> bool:
        """Check if file should be scanned."""
        file_name = file_path.name
        file_str = str(file_path).lower()
        
        # Skip excluded files
        if file_name in self.excluded_files:
            return False
        
        # Skip common directories
        skip_dirs = {'__pycache__', '.git', '.venv', 'venv', 'env', 'test'}
        if any(skip_dir in file_str for skip_dir in skip_dirs):
            return False
            
        return True
    
    def _scan_file(self, file_path: Path):
        """Scan single file for security issues."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except Exception:
            return  # Skip files we can't read
        
        # Check each line against all patterns
        for line_num, line in enumerate(lines, 1):
            for pattern_info in COMPILED_PATTERNS:
                if pattern_info['pattern'].search(line):
                    self.issues.append(SecurityIssue(
                        file=str(file_path),
                        line=line_num,
                        type=pattern_info['name'],
                        message=pattern_info['message'],
                        severity=pattern_info['severity'],
                        cwe_id=pattern_info['cwe_id']
                    ))
    
    def _compile_results(self, files_scanned: int) -> Dict[str, Any]:
        """Compile final results."""
        # Count by severity
        severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        for issue in self.issues:
            if issue.severity in severity_counts:
                severity_counts[issue.severity] += 1
        
        # Determine risk level
        risk_level = self._calculate_risk_level(severity_counts)
        
        return {
            'total_files_scanned': files_scanned,
            'total_vulnerabilities': len(self.issues),
            'vulnerability_counts': severity_counts,
            'security_issues': self.issues,
            'risk_level': risk_level,
            'scan_summary': self._generate_summary(severity_counts, risk_level)
        }
    
    def _calculate_risk_level(self, counts: Dict[str, int]) -> str:
        """Calculate overall risk level."""
        if counts['critical'] > 0:
            return "CRITICAL"
        elif counts['high'] > 2:
            return "HIGH"
        elif counts['high'] > 0 or counts['medium'] > 5:
            return "MEDIUM"
        elif counts['medium'] > 0 or counts['low'] > 10:
            return "LOW"
        else:
            return "MINIMAL"
    
    def _generate_summary(self, counts: Dict[str, int], risk_level: str) -> str:
        """Generate human-readable summary."""
        total = sum(counts.values())
        if total == 0:
            return "🎉 No security vulnerabilities found!"
        
        parts = []
        for severity in ['critical', 'high', 'medium', 'low']:
            count = counts[severity]
            if count > 0:
                parts.append(f"{count} {severity}")
        
        return f"⚠️ Found {total} security issues: {', '.join(parts)} | Risk: {risk_level}"
    
    def _empty_results(self) -> Dict[str, Any]:
        """Return empty results when no files found."""
        return {
            'total_files_scanned': 0,
            'total_vulnerabilities': 0,
            'vulnerability_counts': {'critical': 0, 'high': 0, 'medium': 0, 'low': 0},
            'security_issues': [],
            'risk_level': 'UNKNOWN',
            'scan_summary': 'No Python files found to scan'
        }


# Simple public API
def scan_project(project_path: str) -> Dict[str, Any]:
    """Scan project for security vulnerabilities."""
    scanner = SecurityScanner()
    return scanner.scan_project(project_path)


def create_security_report(results: Dict[str, Any]) -> str:
    """Create formatted security report."""
    lines = [
        "🔒 SECURITY SCAN RESULTS",
        "=" * 40,
        f"📁 Files scanned: {results['total_files_scanned']}",
        f"🚨 Vulnerabilities: {results['total_vulnerabilities']}",
        f"⚠️  Risk level: {results['risk_level']}",
        ""
    ]
    
    # Show severity breakdown
    counts = results['vulnerability_counts']
    severity_icons = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🔵'}
    
    for severity in ['critical', 'high', 'medium', 'low']:
        count = counts.get(severity, 0)
        if count > 0:
            icon = severity_icons[severity]
            lines.append(f"{icon} {severity.title()}: {count}")
    
    # Show individual issues
    issues = results['security_issues']
    if issues:
        lines.extend(["", "🔍 SECURITY ISSUES:", "-" * 25])
        
        for i, issue in enumerate(issues[:10], 1):  # Show first 10
            file_name = Path(issue.file).name
            lines.extend([
                f"{i}. {severity_icons.get(issue.severity, '⚪')} {issue.severity.upper()}: {issue.message}",
                f"   📄 {file_name}:{issue.line} ({issue.cwe_id})",
                ""
            ])
        
        if len(issues) > 10:
            lines.append(f"... and {len(issues) - 10} more issues")
    
    return "\n".join(lines)


# CLI interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python security_scanner.py <project_path>")
        sys.exit(1)
    
    try:
        results = scan_project(sys.argv[1])
        print(create_security_report(results))
        
        # Exit with error code based on severity
        critical_count = results['vulnerability_counts']['critical']
        high_count = results['vulnerability_counts']['high']
        
        if critical_count > 0:
            sys.exit(2)  # Critical issues found
        elif high_count > 0:
            sys.exit(1)  # High severity issues found
        else:
            sys.exit(0)  # Success
            
    except Exception as e:
        print(f"Security scan failed: {e}")
        sys.exit(1)