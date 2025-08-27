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
    
    def save_results(self, results: AnalysisResults, output_path: Union[str, Path]) -> bool:
        """Save analysis results to a file."""
        try:
            output_path = Path(output_path)
            
            if output_path.suffix.lower() == '.json':
                # Save as JSON
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(results.to_json())
            else:
                # Save as text (default)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(f"Analysis Results\n")
                    f.write(f"================\n\n")
                    f.write(f"Project: {results.results.get('analysis_metadata', {}).get('project_path', 'Unknown')}\n")
                    f.write(f"Modules: {', '.join(results.modules_used or [])}\n")
                    f.write(f"Issues Found: {len(results.issues)}\n\n")
                    
                    # Add formatted results
                    f.write("Detailed Results:\n")
                    f.write("-" * 50 + "\n")
                    f.write(str(results.results))
            
            return True
        except Exception as e:
            print(f"Failed to save results: {e}")
            return False