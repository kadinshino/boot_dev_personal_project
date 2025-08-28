"""
Analysis Controller
===============================================================
This handles ALL analysis operations - GUI just calls these methods
"""

import threading
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable, Union


@dataclass
class AnalysisResults:
    """Clean container for analysis results."""
    success: bool
    results: Dict[str, Any]
    issues: List[Any]
    error_message: Optional[str] = None
    modules_used: List[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, default=str)


class AnalysisController:
    """
    Business logic controller for running code analysis.
    
    GUI should ONLY call these methods - never import analysis modules directly.
    """
    
    def __init__(self):
        self.available_modules = self._discover_modules()
        self._current_thread: Optional[threading.Thread] = None
        self._is_running = False
        
    def get_available_modules(self) -> Dict[str, bool]:
        """Return which analysis modules are available."""
        return self.available_modules.copy()
    
    def refresh_module_availability(self) -> Dict[str, bool]:
        """Refresh and return updated module availability."""
        self.available_modules = self._discover_modules()
        return self.get_available_modules()
    
    def is_analysis_running(self) -> bool:
        """Check if analysis is currently running."""
        return self._is_running
    
    def cancel_analysis(self) -> bool:
        """Cancel running analysis if possible."""
        if self._current_thread and self._current_thread.is_alive():
            # Note: Python threading doesn't support true cancellation
            # This is a placeholder for potential future implementation
            return False
        return True
    
    def run_analysis_async(self, 
                          project_path: str,
                          enabled_modules: Dict[str, bool],
                          progress_callback: Callable[[str], None],
                          completion_callback: Callable[[AnalysisResults], None]) -> None:
        """
        Run analysis in background thread with callbacks to update GUI.
        
        This is the MAIN way GUI should trigger analysis.
        """
        if self._current_thread and self._current_thread.is_alive():
            progress_callback("❌ Analysis already running")
            return
            
        def worker():
            """
            Background worker thread that executes the analysis process.
            """

            self._is_running = True
            try:
                progress_callback("🔍 Starting analysis...")
                results = self._run_analysis_sync(project_path, enabled_modules, progress_callback)
                completion_callback(results)
            except Exception as e:
                error_result = AnalysisResults(
                    success=False,
                    results={},
                    issues=[],
                    error_message=str(e)
                )
                completion_callback(error_result)
            finally:
                self._is_running = False
        
        self._current_thread = threading.Thread(target=worker, daemon=True)
        self._current_thread.start()
    
    def run_analysis_sync(self, 
                         project_path: str,
                         enabled_modules: Dict[str, bool]) -> AnalysisResults:
        """
        Run analysis synchronously - mainly for CLI usage.
        GUI should use run_analysis_async instead.
        """
        def dummy_progress(msg: str):
            """Simple progress callback that prints messages to stdout."""
            print(f"Progress: {msg}")
        
        return self._run_analysis_sync(project_path, enabled_modules, dummy_progress)
    
    def _run_analysis_sync(self, 
                          project_path: str, 
                          enabled_modules: Dict[str, bool],
                          progress_callback: Callable[[str], None]) -> AnalysisResults:
        """Internal sync analysis - GUI should never call this directly."""
        
        # Validate project path
        if not Path(project_path).exists():
            raise ValueError(f"Project path does not exist: {project_path}")
        
        # Filter enabled modules to only available ones
        enabled_list = [
            k for k, v in enabled_modules.items() 
            if v and self.available_modules.get(k, False)
        ]
        
        if not enabled_list:
            raise ValueError("No valid modules enabled")
        
        progress_callback(f"🔧 Running: {', '.join(enabled_list)}")
        
        # Initialize results container
        results = {
            "analysis_metadata": {
                "project_path": project_path,
                "modules_used": enabled_list,
                "timestamp": datetime.now().isoformat(),
                "controller_version": "2.0"
            }
        }
        all_issues = []
        
        # Run each module with proper error handling
        total_modules = len(enabled_list)
        for i, module_name in enumerate(enabled_list, 1):
            try:
                progress_callback(f"📊 ({i}/{total_modules}) Running {module_name}...")
                module_issues = self._run_single_module(module_name, results, project_path)
                all_issues.extend(module_issues)
            except Exception as e:
                # Log error but continue with other modules
                print(f"Warning: {module_name} failed: {e}")
                results[f"{module_name}_error"] = str(e)
        
        progress_callback(f"✅ Complete - {len(all_issues)} issues found")
        
        return AnalysisResults(
            success=True,
            results=results,
            issues=all_issues,
            modules_used=enabled_list
        )
    
    def _run_single_module(self, module_name: str, results: Dict[str, Any], 
                          project_path: str) -> List[Any]:
        """Run a single analysis module."""
        if module_name == "code_analyzer":
            return self._run_code_analysis(results, project_path)
        elif module_name == "security_scanner":
            return self._run_security_analysis(results, project_path)
        elif module_name == "dependency_analyzer":
            return self._run_dependency_analysis(results, project_path)
        elif module_name == "codebase_discovery":
            self._run_codebase_discovery(results, project_path)
            return []  # Discovery doesn't typically produce "issues"
        elif module_name == "git_integration":
            self._run_git_analysis(results, project_path)
            return []  # Git analysis doesn't produce "issues"
        else:
            raise ValueError(f"Unknown module: {module_name}")
    
    def _run_code_analysis(self, results: Dict[str, Any], project_path: str) -> List[Any]:
        """Run code quality analysis."""
        try:
            from functions.code_analyzer import analyze_project
            analysis_results = analyze_project(project_path)
            results.update(analysis_results)
            return analysis_results.get("issues", [])
        except Exception as e:
            print(f"Code analysis failed: {e}")
            results["code_analysis_error"] = str(e)
            return []
    
    def _run_security_analysis(self, results: Dict[str, Any], project_path: str) -> List[Any]:
        """Run security vulnerability scanning."""
        try:
            from functions.security_scanner import SecurityScanner
            security_results = SecurityScanner().scan_project(project_path)
            results["security_scan"] = security_results
            return security_results.get("security_issues", [])
        except Exception as e:
            print(f"Security analysis failed: {e}")
            results["security_analysis_error"] = str(e)
            return []
    
    def _run_dependency_analysis(self, results: Dict[str, Any], project_path: str) -> List[Any]:
        """Run dependency analysis using simplified API."""
        try:
            # Use the new simplified API - no project_path in constructor
            from functions.dependency_analyzer import analyze_project
            
            # Call the simplified function directly
            dependency_results = analyze_project(project_path)
            results["dependencies"] = dependency_results
            return dependency_results.get("issues", [])
            
        except Exception as e:
            print(f"Dependency analysis failed: {e}")
            results["dependency_analysis_error"] = str(e)
            return []
    
    def _run_codebase_discovery(self, results: Dict[str, Any], project_path: str) -> None:
        """Run codebase discovery using simplified API."""
        try:
            # Use the new simplified API
            from functions.codebase_discovery import analyze_codebase
            discovery_result = analyze_codebase(project_path)
            
            # Map to the expected result structure
            results["legacy_analysis"] = {
                "entry_points": discovery_result.entry_points,
                "framework_detection": discovery_result.frameworks,
                "business_patterns": discovery_result.business_patterns,
                "external_services": discovery_result.external_services,
                "quick_start_guide": discovery_result.quick_start_guide,
                "operational_notes": discovery_result.project_insights,
                "total_files_analyzed": discovery_result.total_files_analyzed
            }
        except Exception as e:
            print(f"Codebase discovery failed: {e}")
            results["codebase_discovery_error"] = str(e)
    
    def _run_git_analysis(self, results: Dict[str, Any], project_path: str) -> None:
        """Run git repository analysis."""
        try:
            from functions.git_integration import GitAnalyzer
            git_analyzer = GitAnalyzer(project_path)
            
            if git_analyzer.is_git_repo():
                results["git_info"] = {
                    "is_repo": True,
                    "current_branch": git_analyzer.get_current_branch(),
                    "modified_files": git_analyzer.get_modified_files(),
                    "staged_files": git_analyzer.get_staged_files(),
                }
            else:
                results["git_info"] = {"is_repo": False}
        except Exception as e:
            print(f"Git analysis failed: {e}")
            results["git_info"] = {"is_repo": False, "error": str(e)}
    
    def _discover_modules(self) -> Dict[str, bool]:
        """Discover which analysis modules are available."""
        modules = {
            "code_analyzer": "functions.code_analyzer",
            "security_scanner": "functions.security_scanner", 
            "dependency_analyzer": "functions.dependency_analyzer",
            "codebase_discovery": "functions.codebase_discovery",
            "git_integration": "functions.git_integration",
        }
        
        available = {}
        for module_id, import_path in modules.items():
            try:
                __import__(import_path)
                available[module_id] = True
            except Exception:
                available[module_id] = False
        
        return available
    
    # === UTILITY METHODS FOR ADVANCED USAGE ===
    
    def get_module_info(self) -> Dict[str, Dict[str, Any]]:
        """Get detailed information about each module."""
        return {
            "code_analyzer": {
                "name": "Code Quality Analyzer",
                "description": "Analyzes code structure, complexity, and quality issues",
                "available": self.available_modules.get("code_analyzer", False),
                "produces_issues": True
            },
            "security_scanner": {
                "name": "Security Scanner",
                "description": "Scans for security vulnerabilities and potential threats",
                "available": self.available_modules.get("security_scanner", False),
                "produces_issues": True
            },
            "dependency_analyzer": {
                "name": "Dependency Analyzer", 
                "description": "Analyzes project dependencies and import structure",
                "available": self.available_modules.get("dependency_analyzer", False),
                "produces_issues": True
            },
            "codebase_discovery": {
                "name": "Codebase Discovery",
                "description": "Discovers project structure, frameworks, and entry points",
                "available": self.available_modules.get("codebase_discovery", False),
                "produces_issues": False
            },
            "git_integration": {
                "name": "Git Integration",
                "description": "Analyzes git repository information and status",
                "available": self.available_modules.get("git_integration", False),
                "produces_issues": False
            }
        }
    
    def validate_project_path(self, project_path: Union[str, Path]) -> tuple[bool, str]:
        """
        Validate a project path for analysis.
        
        Returns:
            (is_valid, message)
        """
        path = Path(project_path)
        
        if not path.exists():
            return False, f"Path does not exist: {path}"
        
        if not path.is_dir():
            return False, f"Path is not a directory: {path}"
        
        # Check for Python files
        python_files = list(path.rglob("*.py"))
        if not python_files:
            return False, f"No Python files found in: {path}"
        
        return True, f"Valid project with {len(python_files)} Python files"
    
    def get_project_stats(self, project_path: Union[str, Path]) -> Dict[str, Any]:
        """Get basic statistics about a project without running full analysis."""
        path = Path(project_path)
        
        if not path.exists():
            return {"error": "Path does not exist"}
        
        try:
            python_files = list(path.rglob("*.py"))
            total_lines = 0
            
            for file_path in python_files[:100]:  # Limit to first 100 files for speed
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        total_lines += len(f.readlines())
                except Exception:
                    continue
            
            return {
                "total_python_files": len(python_files),
                "estimated_lines": total_lines,
                "project_name": path.name,
                "project_path": str(path)
            }
        except Exception as e:
            return {"error": str(e)}

# === FORMATTING FUNCTIONS (MOVED FROM GUI) ===

def format_results_for_display(results: AnalysisResults) -> str:
    """Format results for display - moved from GUI to business logic."""
    if not results or not results.success:
        return "❌ No results to display or analysis failed."
    
    lines = [
        "🎯 CODE ANALYSIS RESULTS",
        "=" * 60,
        f"📁 Project: {results.results.get('analysis_metadata', {}).get('project_path', 'Unknown')}",
        f"📊 Total Issues: {len(results.issues)}",
        f"🔧 Modules Used: {', '.join(results.modules_used or [])}",
        f"⏱️ Analysis Time: {results.results.get('analysis_metadata', {}).get('timestamp', 'Unknown')}",
        "",
    ]
    
    # Add sections based on what was actually analyzed
    sections_added = 0
    
    # Code Analysis section
    if "total_files" in results.results:
        lines.extend(_format_code_analysis_section(results.results))
        sections_added += 1
    
    # Security Analysis section  
    if "security_scan" in results.results:
        lines.extend(_format_security_section(results.results["security_scan"]))
        sections_added += 1
    
    # Dependency Analysis section
    if "dependencies" in results.results:
        lines.extend(_format_dependency_section(results.results["dependencies"]))
        sections_added += 1
    
    # Codebase Discovery section
    if "legacy_analysis" in results.results:
        lines.extend(_format_discovery_section(results.results["legacy_analysis"]))
        sections_added += 1
    
    # Git Integration section
    if "git_info" in results.results:
        lines.extend(_format_git_section(results.results["git_info"]))
        sections_added += 1
    
    # Add summary footer
    lines.extend([
        "=" * 60,
        f"📋 Analysis Complete - {sections_added} modules analyzed",
        f"🐛 Total Issues Found: {len(results.issues)}",
    ])
    
    # Add recommendations if no issues found
    if len(results.issues) == 0:
        lines.extend([
            "",
            "🎉 CONGRATULATIONS!",
            "No issues were found in your codebase.",
            "Your code appears to be well-structured and follows good practices!",
        ])
    elif len(results.issues) > 0:
        # Categorize issues by severity
        critical = sum(1 for issue in results.issues if getattr(issue, 'severity', '') == 'critical')
        high = sum(1 for issue in results.issues if getattr(issue, 'severity', '') == 'high')
        warnings = sum(1 for issue in results.issues if getattr(issue, 'severity', '') in ['warning', 'medium'])
        
        lines.append("")
        lines.append("💡 NEXT STEPS:")
        if critical > 0:
            lines.append(f"  🔴 Address {critical} critical security issues immediately")
        if high > 0:
            lines.append(f"  🟠 Review {high} high-priority issues")  
        if warnings > 0:
            lines.append(f"  🟡 Consider fixing {warnings} warnings for better code quality")
        lines.append("  📊 Check the Issues tab for detailed information")
    
    return "\n".join(lines)


def save_results_to_file(results: AnalysisResults, filename: str) -> None:
    """Save results to file - handles different formats."""
    if filename.lower().endswith('.json'):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(results.to_json())
    else:
        formatted_text = format_results_for_display(results)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(formatted_text)


def _format_code_analysis_section(results: Dict) -> List[str]:
    """Format code analysis section."""
    return [
        "📋 CODE ANALYSIS",
        "-" * 30,
        f"📄 Files: {results.get('total_files', 0)}",
        f"🔧 Functions: {results.get('total_functions', 0)}",
        f"🗂️ Classes: {results.get('total_classes', 0)}",
        f"📝 Lines of Code: {results.get('total_lines', 0)}",
        ""
    ]


def _format_security_section(security_results: Dict) -> List[str]:
    """Format security analysis section."""
    severity_icons = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵"}
    
    lines = [
        "🔒 SECURITY ANALYSIS",
        "-" * 30,
        f"🚨 Risk Level: {security_results.get('risk_level', 'Unknown')}",
        f"🛡️ Vulnerabilities: {security_results.get('total_vulnerabilities', 0)}",
        ""
    ]
    
    # Vulnerability breakdown
    counts = security_results.get('vulnerability_counts', {})
    if any(counts.values()):
        lines.append("Severity Breakdown:")
        for severity in ['critical', 'high', 'medium', 'low']:
            count = counts.get(severity, 0)
            if count > 0:
                icon = severity_icons.get(severity, '⚪')
                lines.append(f"  {icon} {severity.title()}: {count}")
        lines.append("")
    
    return lines


def _format_dependency_section(dependency_results: Dict) -> List[str]:
    """Format dependency analysis section."""
    lines = [
        "📦 DEPENDENCY ANALYSIS",
        "-" * 30
    ]
    
    # Handle both new and legacy result formats
    if "stats" in dependency_results:
        # New format
        stats = dependency_results["stats"]
        lines.extend([
            f"📊 Total Dependencies: {stats.get('total_dependencies', 0)}",
            f"📚 Standard Library: {stats.get('standard_library', 0)}",
            f"🌐 Third-party: {stats.get('third_party', 0)}",
            f"🏠 Local Modules: {stats.get('local', 0)}",
        ])
        
        risk = dependency_results.get("risk_assessment", {})
        risk_level = risk.get("risk_level", "UNKNOWN")
        risk_icons = {"MINIMAL": "🟢", "LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴", "CRITICAL": "🔴"}
        icon = risk_icons.get(risk_level, "⚪")
        lines.append(f"{icon} Risk Level: {risk_level}")
    
    lines.append("")
    return lines


def _format_discovery_section(discovery_results: Dict) -> List[str]:
    """Format codebase discovery section."""
    lines = [
        "🗺️ CODEBASE DISCOVERY",
        "-" * 30
    ]
    
    # Entry points
    entry_points = discovery_results.get("entry_points", [])
    if entry_points:
        lines.append("🚪 Entry Points:")
        for ep in entry_points[:3]:
            filename = ep.get("filename", "Unknown")
            confidence = ep.get("confidence", 0)
            conf_str = f"{confidence:.0%}" if isinstance(confidence, (int, float)) else str(confidence)
            lines.append(f"  • {filename} ({conf_str} confidence)")
    
    # Frameworks
    frameworks = discovery_results.get("framework_detection", {})
    if frameworks:
        lines.append("\n🔧 Frameworks Detected:")
        for fw, conf in frameworks.items():
            conf_str = f"{conf:.0%}" if isinstance(conf, (int, float)) else str(conf)
            lines.append(f"  • {fw.title()}: {conf_str}")
    
    lines.append("")
    return lines


def _format_git_section(git_results: Dict) -> List[str]:
    """Format git analysis section."""
    if not git_results.get("is_repo", False):
        return ["📊 GIT REPOSITORY: Not a git repository", ""]
    
    return [
        "📊 GIT REPOSITORY INFO",
        "-" * 30,
        f"🌿 Branch: {git_results.get('current_branch', 'unknown')}",
        f"📝 Modified Files: {len(git_results.get('modified_files', []))}",
        f"📋 Staged Files: {len(git_results.get('staged_files', []))}",
        ""
    ]


# === ISSUES PROCESSING FUNCTIONS (MOVED FROM GUI) ===

def get_severity_options(issues: List[Any]) -> List[str]:
    """Get available severity options from issues."""
    if not issues:
        return ["all"]
    
    severities = set(getattr(issue, "severity", "unknown") for issue in issues)
    return ["all"] + sorted(severities)


def filter_issues(issues: List[Any], severity_filter: str = "all", search_term: str = "") -> List[Any]:
    """Filter issues by severity and search term."""
    filtered = issues
    
    # Apply severity filter
    if severity_filter != "all":
        filtered = [issue for issue in filtered 
                   if getattr(issue, "severity", "unknown") == severity_filter]
    
    # Apply search filter
    if search_term:
        search_lower = search_term.lower()
        filtered = [issue for issue in filtered if _issue_matches_search(issue, search_lower)]
    
    return filtered


def format_issues_for_display(issues: List[Any], show_limit: int = 100) -> str:
    """Format issues for display in GUI."""
    if not issues:
        return "🎉 No issues found! Your code looks great!"
    
    severity_icons = {
        "critical": "🔴", "high": "🟠", "error": "❌", "warning": "⚠️",
        "medium": "🟡", "info": "ℹ️", "low": "🔵"
    }
    
    lines = [f"🐛 ISSUES FOUND ({len(issues)} total)", "=" * 60, ""]
    
    for i, issue in enumerate(issues[:show_limit], 1):
        severity = getattr(issue, "severity", "unknown")
        message = getattr(issue, "message", "No message")
        file_path = getattr(issue, "file_path", getattr(issue, "file", "Unknown"))
        line_num = getattr(issue, "line_number", getattr(issue, "line", 0))
        issue_type = getattr(issue, "issue_type", getattr(issue, "type", "unknown"))
        
        icon = severity_icons.get(severity, "⚪")
        file_name = Path(file_path).name if file_path != "Unknown" else "Unknown"
        
        lines.extend([
            f"{i}. {icon} {severity.upper()}: {message}",
            f"   📄 {file_name}:{line_num} ({issue_type})",
            ""
        ])
    
    if len(issues) > show_limit:
        lines.append(f"... and {len(issues) - show_limit} more issues")
    
    return "\n".join(lines)


def get_issue_statistics(issues: List[Any]) -> str:
    """Get issue summary statistics as formatted string."""
    if not issues:
        return "No issues to analyze"
    
    severity_icons = {
        "critical": "🔴", "high": "🟠", "error": "❌", "warning": "⚠️",
        "medium": "🟡", "info": "ℹ️", "low": "🔵"
    }
    
    # Count by severity
    by_severity = {}
    by_type = {}
    
    for issue in issues:
        severity = getattr(issue, "severity", "unknown")
        issue_type = getattr(issue, "issue_type", getattr(issue, "type", "unknown"))
        
        by_severity[severity] = by_severity.get(severity, 0) + 1
        by_type[issue_type] = by_type.get(issue_type, 0) + 1
    
    stats_parts = []
    
    # Severity breakdown
    if by_severity:
        severity_stats = []
        for severity in ["critical", "high", "error", "warning", "medium", "info", "low"]:
            count = by_severity.get(severity, 0)
            if count > 0:
                icon = severity_icons.get(severity, "⚪")
                severity_stats.append(f"{icon} {severity}: {count}")
        
        if severity_stats:
            stats_parts.append(" | ".join(severity_stats))
    
    # Top issue types
    if by_type:
        top_types = sorted(by_type.items(), key=lambda x: x[1], reverse=True)[:3]
        type_stats = [f"{issue_type}: {count}" for issue_type, count in top_types]
        stats_parts.append(f"Top types: {', '.join(type_stats)}")
    
    return " • ".join(stats_parts) if stats_parts else "No detailed statistics available"


def _issue_matches_search(issue: Any, search_lower: str) -> bool:
    """Check if issue matches search term."""
    # Search in various fields
    searchable_text = " ".join([
        getattr(issue, "message", "").lower(),
        getattr(issue, "file_path", getattr(issue, "file", "")).lower(),
        getattr(issue, "issue_type", getattr(issue, "type", "")).lower()
    ])
    
    return search_lower in searchable_text