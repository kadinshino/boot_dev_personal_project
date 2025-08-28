# functions/git_integration.py

"""
Git Integration Module for Code Analyzer 

"""

import subprocess
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

# Import Analyzer
from functions.code_analyzer import analyze_project
from functions.security_scanner import SecurityScanner
            
class GitAnalyzer:
    """Git analyzer with robust error handling."""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.git_dir = self.repo_path / '.git'
        self._git_available = self._check_git_availability()
    
    def _check_git_availability(self) -> bool:
        """Check if git is available on the system."""
        try:
            git_commands = ['git', 'git.exe']
            
            for git_cmd in git_commands:
                if shutil.which(git_cmd):
                    self._git_command = git_cmd
                    # Test that it actually works
                    result = subprocess.run(
                        [git_cmd, '--version'],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        return True
            
            return False
            
        except Exception:
            return False
    
    def is_git_repo(self) -> bool:
        """Check if the path is a git repository."""
        return self.git_dir.exists() and self._git_available
    
    def get_current_branch(self) -> str:
        """Get the current git branch name."""
        if not self.is_git_repo():
            return "unknown"
            
        try:
            result = subprocess.run(
                [self._git_command, 'branch', '--show-current'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout.strip() or "unknown"
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, AttributeError):
            return "unknown"
    
    def get_staged_files(self) -> List[str]:
        """Get list of staged Python files."""
        if not self.is_git_repo():
            return []
        
        try:
            result = subprocess.run(
                [self._git_command, 'diff', '--cached', '--name-only', '--', '*.py'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            files = result.stdout.strip().split('\n') if result.stdout.strip() else []
            return [f for f in files if f and f.endswith('.py')]
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, AttributeError):
            return []
    
    def get_modified_files(self) -> List[str]:
        """Get list of modified Python files."""
        if not self.is_git_repo():
            return []
            
        try:
            result = subprocess.run(
                [self._git_command, 'diff', '--name-only', 'HEAD', '--', '*.py'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            files = result.stdout.strip().split('\n') if result.stdout.strip() else []
            return [f for f in files if f and f.endswith('.py')]
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, AttributeError):
            return []
    
    def run_pre_commit_analysis(self, config: Optional[Dict[str, Any]] = None) -> int:
        """
        Run pre-commit analysis on staged files.
        """
        if not self.is_git_repo():
            print("⚠️  Not a git repository - skipping analysis")
            return 0
        
        # Get staged Python files
        staged_files = self.get_staged_files()
        
        if not staged_files:
            print("✅ No Python files staged - skipping analysis")
            return 0
        
        print(f"🔍 Running pre-commit analysis on {len(staged_files)} files...")
        
        try:

            # Run code analysis
            code_results = analyze_project(str(self.repo_path))
            issues = code_results.get('issues', [])
            
            # Run security analysis if enabled
            if config and config.get('security_enabled', True):
                security_scanner = SecurityScanner()
                security_results = security_scanner.scan_project(str(self.repo_path))
                issues.extend(security_results.get('security_issues', []))
            
            # Evaluate results
            critical_issues = [i for i in issues if self._get_severity(i) == 'critical']
            error_issues = [i for i in issues if self._get_severity(i) == 'error']
            
            if critical_issues:
                print(f"🚫 COMMIT BLOCKED: {len(critical_issues)} critical issues found")
                self._print_issues(critical_issues[:3])  # Show first 3
                return 2  # Block commit
            elif error_issues and config and config.get('block_on_errors', False):
                print(f"⚠️  COMMIT BLOCKED: {len(error_issues)} errors found")
                self._print_issues(error_issues[:3])  # Show first 3
                return 1  # Block commit
            else:
                total_issues = len(issues)
                print(f"✅ Pre-commit analysis passed ({total_issues} issues found)")
                return 0  # Allow commit
                
        except Exception as e:
            print(f"⚠️  Analysis failed: {e}")
            print("⚠️  Allowing commit despite analysis failure")
            return 0  # Don't block on analysis failure
    
    def _get_severity(self, issue) -> str:
        """Get severity from issue object."""
        if hasattr(issue, 'severity'):
            return issue.severity
        elif isinstance(issue, dict):
            return issue.get('severity', 'info')
        return 'info'
    
    def _print_issues(self, issues: List[Any]) -> None:
        """Print issues in a readable format."""
        for issue in issues:
            file_path = getattr(issue, 'file_path', 'unknown')
            line_number = getattr(issue, 'line_number', 0)
            message = getattr(issue, 'message', 'No message')
            print(f"  • {Path(file_path).name}:{line_number} - {message}")
    
    def install_simple_pre_commit_hook(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """
        Install a simple pre-commit hook that calls back to this analyzer.
        
        Much cleaner than generating complex scripts!
        """
        if not self.is_git_repo():
            print("❌ Not a git repository or git not available")
            return False
        
        hooks_dir = self.git_dir / 'hooks'
        hooks_dir.mkdir(exist_ok=True)
        hook_path = hooks_dir / 'pre-commit'
        
        try:
            # Create a simple hook script that calls back to our analyzer
            hook_script = self._create_simple_hook_script(config or {})
            
            with open(hook_path, 'w', encoding='utf-8') as f:
                f.write(hook_script)
            
            # Make executable
            hook_path.chmod(0o755)
            
            print(f"✅ Simple pre-commit hook installed at: {hook_path}")
            print("🎯 Hook will analyze staged files before each commit")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to install hook: {e}")
            return False
    
    def _create_simple_hook_script(self, config: Dict[str, Any]) -> str:
        """Create a simple hook script that calls back to the analyzer."""
        # This is MUCH simpler than the generative approach!
        return f'''#!/usr/bin/env python3
"""
Simple pre-commit hook - calls back to Code Analyzer
Generated by Code Analyzer git integration
"""

import sys
import subprocess
from pathlib import Path

def find_python():
    """Find the correct Python command."""
    import shutil
    for cmd in ['python3', 'python', 'py']:
        if shutil.which(cmd):
            return cmd
    return 'python3'

def main():
    # Find project root and main.py
    project_root = Path(__file__).parent.parent.parent
    main_py = project_root / "main.py"
    
    if not main_py.exists():
        print("⚠️  main.py not found - skipping analysis")
        return 0
    
    # Get Python command
    python_cmd = find_python()
    
    # Call the analyzer with pre-commit mode
    try:
        cmd = [python_cmd, str(main_py), "--pre-commit", str(project_root)]
        result = subprocess.run(cmd, timeout=60)
        return result.returncode
    except Exception as e:
        print(f"⚠️  Hook failed: {{e}}")
        return 0  # Don't block on hook failure

if __name__ == '__main__':
    sys.exit(main())
'''
    
    def get_git_status(self) -> Dict[str, Any]:
        """Get comprehensive git repository status."""
        if not self.is_git_repo():
            return {
                "is_repo": False,
                "git_available": self._git_available,
                "error": "Not a git repository or git not available"
            }
        
        try:
            return {
                "is_repo": True,
                "git_available": True,
                "current_branch": self.get_current_branch(),
                "modified_files": self.get_modified_files(),
                "staged_files": self.get_staged_files(),
                "has_staged_changes": len(self.get_staged_files()) > 0,
                "has_unstaged_changes": len(self.get_modified_files()) > 0
            }
            
        except Exception as e:
            return {
                "is_repo": True,
                "git_available": self._git_available,
                "error": f"Git operations failed: {e}"
            }


class TeamReportGenerator:
    """Generate team-focused reports and metrics."""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.git_analyzer = GitAnalyzer(repo_path)
    
    def generate_team_report(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive team report."""
        git_status = self.git_analyzer.get_git_status()
        issues = analysis_results.get("issues", [])
        
        # Count issues by severity
        critical_count = sum(1 for issue in issues if self._get_severity(issue) == "critical")
        error_count = sum(1 for issue in issues if self._get_severity(issue) == "error") 
        warning_count = sum(1 for issue in issues if self._get_severity(issue) == "warning")
        
        # Determine commit readiness
        commit_readiness = self._assess_commit_readiness(
            critical_count, error_count, warning_count, git_status
        )
        
        return {
            "timestamp": datetime.now().isoformat(),
            "repository_info": git_status,
            "commit_readiness": commit_readiness,
            "issue_summary": {
                "critical": critical_count,
                "errors": error_count,
                "warnings": warning_count,
                "total": len(issues)
            },
            "team_recommendations": self._generate_recommendations(
                critical_count, error_count, warning_count, git_status
            )
        }
    
    def _assess_commit_readiness(self, critical: int, errors: int, warnings: int, 
                               git_status: Dict[str, Any]) -> Dict[str, Any]:
        """Assess whether code is ready to be committed."""
        if not git_status.get("is_repo"):
            return {
                "status": "unknown",
                "reason": "Not a git repository",
                "action": "⚠️  Initialize git repository for commit tracking"
            }
        
        if critical > 0:
            return {
                "status": "blocked",
                "reason": f"{critical} critical security issues found",
                "action": "🚫 Fix critical issues before committing"
            }
        elif errors > 5:
            return {
                "status": "caution",
                "reason": f"{errors} error-level issues found",
                "action": "⚠️  Review and fix errors before committing"
            }
        elif warnings > 15:
            return {
                "status": "caution",
                "reason": f"High warning count: {warnings}",
                "action": "⚠️  Consider addressing warnings"
            }
        else:
            return {
                "status": "ready",
                "reason": "No blocking issues found",
                "action": "✅ Safe to commit"
            }
    
    def _generate_recommendations(self, critical: int, errors: int, warnings: int,
                                git_status: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        if critical > 0:
            recommendations.append(f"🔴 Fix {critical} critical security issues immediately")
        
        if errors > 0:
            recommendations.append(f"⚠️  Address {errors} error-level issues")
        
        if warnings > 10:
            recommendations.append("📝 Consider addressing warnings for better code quality")
        
        if git_status.get("has_unstaged_changes"):
            recommendations.append("📋 Stage your changes: git add <files>")
        
        if not git_status.get("has_staged_changes"):
            recommendations.append("📂 No staged changes - nothing to commit")
        
        if not recommendations:
            recommendations.append("✅ Code looks good - ready to commit!")
        
        return recommendations
    
    def _get_severity(self, issue) -> str:
        """Get severity from issue object."""
        if hasattr(issue, 'severity'):
            return issue.severity
        elif isinstance(issue, dict):
            return issue.get('severity', 'info')
        return 'info'


# Convenience functions for easier integration
def analyze_for_commit(repo_path: str, config: Optional[Dict[str, Any]] = None) -> int:
    """
    Analyze repository for commit readiness.
    
    Returns:
        0: Ready to commit
        1: Warnings found
        2: Critical issues (block commit)
    """
    git_analyzer = GitAnalyzer(repo_path)
    return git_analyzer.run_pre_commit_analysis(config)


def install_git_hooks(repo_path: str, config: Optional[Dict[str, Any]] = None) -> bool:
    """Install git pre-commit hooks for a repository."""
    git_analyzer = GitAnalyzer(repo_path)
    return git_analyzer.install_simple_pre_commit_hook(config)


def get_team_status(repo_path: str, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
    """Get team collaboration status for a repository."""
    team_generator = TeamReportGenerator(repo_path)
    return team_generator.generate_team_report(analysis_results)