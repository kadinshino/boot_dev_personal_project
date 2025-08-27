"""
Fixed CLI Command Handler - All Import Issues Resolved
====================================================
Matches exactly with the actual function names in the analyzer modules
"""

import argparse
from pathlib import Path
from typing import Dict, Any
import json


class CLIHandler:
    """Handles CLI commands and routes to appropriate analyzers."""
    
    def execute(self, args) -> int:
        """Main CLI execution - simple routing."""
        parser = self._create_parser()
        
        try:
            parsed = parser.parse_args(args)
            return self._route_command(parsed)
        except Exception as e:
            print(f"❌ Error: {e}")
            return 1
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the argument parser."""
        parser = argparse.ArgumentParser(
            description="Enhanced Code Analyzer CLI",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        # Analysis modes (mutually exclusive)
        mode_group = parser.add_mutually_exclusive_group()
        mode_group.add_argument("--analyze", metavar="PATH", help="Basic code analysis")
        mode_group.add_argument("--security", metavar="PATH", help="Security scan")
        mode_group.add_argument("--comprehensive", metavar="PATH", help="Full analysis")
        mode_group.add_argument("--legacy", metavar="PATH", help="Legacy codebase analysis")
        mode_group.add_argument("--team", metavar="PATH", help="Team collaboration check")
        mode_group.add_argument("--install-hooks", metavar="PATH", help="Install git hooks")
        mode_group.add_argument("--pre-commit", metavar="PATH", help="Pre-commit hook analysis (internal)")
        
        # Output options
        parser.add_argument("--json", action="store_true", help="JSON output")
        parser.add_argument("--save", metavar="FILE", help="Save to file")
        parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
        
        return parser
    
    def _route_command(self, args) -> int:
        """Route to the appropriate command handler."""
        if args.analyze:
            return BasicAnalysisCommand().execute(args)
        elif args.security:
            return SecurityAnalysisCommand().execute(args)
        elif args.comprehensive:
            return ComprehensiveAnalysisCommand().execute(args)
        elif args.legacy:
            return LegacyAnalysisCommand().execute(args)
        elif args.team:
            return TeamAnalysisCommand().execute(args)
        elif args.install_hooks:
            return InstallHooksCommand().execute(args)
        elif args.pre_commit:
            return PreCommitCommand().execute(args)
        else:
            print("❌ No command specified. Use --help for options.")
            return 1


class BaseCommand:
    """Base class for all CLI commands."""
    
    def validate_path(self, path: str) -> Path:
        """Validate and return Path object."""
        path_obj = Path(path)
        if not path_obj.exists():
            raise ValueError(f"Directory '{path}' does not exist")
        return path_obj
    
    def save_results(self, content: str, save_path: str) -> None:
        """Save results to file."""
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"💾 Report saved to: {save_path}")
        except Exception as e:
            print(f"❌ Save failed: {e}")


class BasicAnalysisCommand(BaseCommand):
    """Handles basic code analysis - FIXED IMPORTS."""
    
    def execute(self, args) -> int:
        """Execute basic analysis."""
        try:
            project_path = self.validate_path(args.analyze)
            print(f"🔍 Running basic analysis on: {project_path}")
            
            # FIXED: Use the correct function names from code_analyzer.py
            from functions.code_analyzer import analyze_project, format_summary
            
            results = analyze_project(str(project_path))
            
            if args.json:
                # Convert issues to dict for JSON serialization
                json_results = {
                    'issues': [
                        {
                            'file': issue.file,
                            'line': issue.line,
                            'type': issue.type,
                            'message': issue.message,
                            'severity': issue.severity
                        } for issue in results.get('issues', [])
                    ],
                    'stats': results.get('stats', {}),
                    'project_path': results.get('project_path', ''),
                    'files_analyzed': results.get('files_analyzed', 0)
                }
                output = json.dumps(json_results, indent=2)
            else:
                # FIXED: Use format_summary instead of summarize_results
                output = format_summary(results)
            
            print(output)
            
            if args.save:
                self.save_results(output, args.save)
            
            # Return exit code based on issues
            issues = results.get('issues', [])
            errors = [i for i in issues if getattr(i, 'severity', 'info') == 'error']
            return 1 if errors else 0
            
        except ImportError as e:
            print(f"❌ Code analyzer module not available: {e}")
            return 1
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            return 1


class SecurityAnalysisCommand(BaseCommand):
    """Handles security analysis - FIXED IMPORTS."""
    
    def execute(self, args) -> int:
        """Execute security analysis."""
        try:
            project_path = self.validate_path(args.security)
            print(f"🔒 Running security analysis on: {project_path}")
            
            # FIXED: Use correct imports from security_scanner.py
            from functions.security_scanner import SecurityScanner, create_security_report
            
            scanner = SecurityScanner()
            results = scanner.scan_project(str(project_path))
            
            if args.json:
                # Convert SecurityIssue objects to dicts for JSON
                json_results = dict(results)
                json_results['security_issues'] = [
                    {
                        'file': issue.file,
                        'line': issue.line,
                        'type': issue.type,
                        'message': issue.message,
                        'severity': issue.severity,
                        'cwe_id': issue.cwe_id
                    } for issue in results.get('security_issues', [])
                ]
                output = json.dumps(json_results, indent=2)
            else:
                output = create_security_report(results)
            
            print(output)
            
            if args.save:
                self.save_results(output, args.save)
            
            # Exit code based on security findings
            critical_count = results.get('vulnerability_counts', {}).get('critical', 0)
            high_count = results.get('vulnerability_counts', {}).get('high', 0)
            
            if critical_count > 0:
                return 2
            elif high_count > 0:
                return 1
            else:
                return 0
                
        except ImportError as e:
            print(f"❌ Security scanner not available: {e}")
            return 1
        except Exception as e:
            print(f"❌ Security analysis failed: {e}")
            return 1


class ComprehensiveAnalysisCommand(BaseCommand):
    """Handles comprehensive analysis - FIXED IMPORTS."""
    
    def execute(self, args) -> int:
        """Execute comprehensive analysis."""
        try:
            project_path = self.validate_path(args.comprehensive)
            print(f"🚀 Running comprehensive analysis on: {project_path}")
            
            # FIXED: Use the analysis controller instead of direct imports
            from functions.analysis_controller import AnalysisController
            
            controller = AnalysisController()
            
            # Define enabled modules for comprehensive analysis
            enabled_modules = {
                'code_analyzer': True,
                'security_scanner': True,
                'dependency_analyzer': True,
                'codebase_discovery': False,  # Optional
                'git_integration': False      # Optional
            }
            
            # Run analysis
            results = controller.run_analysis_sync(str(project_path), enabled_modules)
            
            if args.json:
                output = results.to_json()
            else:
                output = self._format_comprehensive_report(results)
            
            print(output)
            
            if args.save:
                self.save_results(output, args.save)
            
            return self._calculate_exit_code(results)
            
        except ImportError as e:
            print(f"❌ Module not available: {e}")
            return 1
        except Exception as e:
            print(f"❌ Comprehensive analysis failed: {e}")
            return 1
    
    def _format_comprehensive_report(self, results) -> str:
        """Format comprehensive results."""
        lines = []
        lines.append("🚀 COMPREHENSIVE ANALYSIS REPORT")
        lines.append("=" * 50)
        
        if not results.success:
            lines.append(f"❌ Analysis failed: {results.error_message}")
            return "\n".join(lines)
        
        # Summary
        lines.append(f"📊 Total Issues: {len(results.issues)}")
        lines.append(f"🔧 Modules Used: {', '.join(results.modules_used or [])}")
        lines.append("")
        
        # Issue breakdown by severity
        if results.issues:
            severity_counts = {}
            for issue in results.issues:
                severity = getattr(issue, 'severity', 'unknown')
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            lines.append("📋 ISSUE BREAKDOWN:")
            for severity, count in severity_counts.items():
                lines.append(f"  • {severity.title()}: {count}")
        else:
            lines.append("🎉 No issues found!")
        
        return "\n".join(lines)
    
    def _calculate_exit_code(self, results) -> int:
        """Calculate exit code based on all results."""
        if not results.success:
            return 1
        
        # Check for critical issues
        for issue in results.issues:
            severity = getattr(issue, 'severity', 'info')
            if severity == 'critical':
                return 2
            elif severity == 'error':
                return 1
                
        return 0


class LegacyAnalysisCommand(BaseCommand):
    """Handles codebase discovery analysis - FIXED IMPORTS."""
    
    def execute(self, args) -> int:
        """Execute codebase discovery analysis."""
        try:
            project_path = self.validate_path(args.legacy)
            print(f"🗺️ Running codebase discovery on: {project_path}")
            
            # FIXED: Use correct imports from codebase_discovery.py
            from functions.codebase_discovery import analyze_codebase, create_discovery_report
            
            results = analyze_codebase(str(project_path))
            
            if args.json:
                from dataclasses import asdict
                output = json.dumps(asdict(results), indent=2, default=str)
            else:
                output = create_discovery_report(results)
            
            print(output)
            
            if args.save:
                self.save_results(output, args.save)
            
            return 0  # Discovery analysis doesn't have error conditions
            
        except ImportError as e:
            print(f"❌ Codebase discovery not available: {e}")
            return 1
        except Exception as e:
            print(f"❌ Codebase discovery failed: {e}")
            return 1


class TeamAnalysisCommand(BaseCommand):
    """Handles team collaboration analysis - FIXED IMPORTS."""
    
    def execute(self, args) -> int:
        """Execute team analysis."""
        try:
            project_path = self.validate_path(args.team)
            
            from functions.git_integration import GitAnalyzer, TeamReportGenerator
            
            # Validate git repo
            git_analyzer = GitAnalyzer(str(project_path))
            if not git_analyzer.is_git_repo():
                print("❌ Not a git repository")
                return 1
            
            print(f"👥 Running team analysis on: {project_path}")
            
            # Generate team report
            team_reporter = TeamReportGenerator(str(project_path))
            basic_results = {"issues": []}  # Minimal for team report
            team_report = team_reporter.generate_team_report(basic_results)
            
            if args.json:
                output = json.dumps(team_report, indent=2, default=str)
            else:
                output = self._format_team_report(team_report)
            
            print(output)
            
            if args.save:
                self.save_results(output, args.save)
            
            # Exit code based on commit readiness
            status = team_report.get("commit_readiness", {}).get("status")
            return {"blocked": 2, "caution": 1}.get(status, 0)
            
        except ImportError as e:
            print(f"❌ Git integration not available: {e}")
            return 1
        except Exception as e:
            print(f"❌ Team analysis failed: {e}")
            return 1
    
    def _format_team_report(self, report: Dict[str, Any]) -> str:
        """Format team report for display."""
        lines = []
        lines.append("👥 TEAM COLLABORATION REPORT")
        lines.append("=" * 40)
        
        readiness = report.get("commit_readiness", {})
        status = readiness.get("status", "unknown")
        reason = readiness.get("reason", "No reason")
        action = readiness.get("action", "No action")
        
        status_icons = {"ready": "✅", "caution": "⚠️", "blocked": "🚫"}
        icon = status_icons.get(status, "❓")
        
        lines.append(f"{icon} COMMIT STATUS: {status.upper()}")
        lines.append(f"Reason: {reason}")
        lines.append(f"Action: {action}")
        
        # Add recommendations
        recommendations = report.get("team_recommendations", [])
        if recommendations:
            lines.append("")
            lines.append("📋 RECOMMENDATIONS:")
            for rec in recommendations:
                lines.append(f"  • {rec}")
        
        return "\n".join(lines)


class InstallHooksCommand(BaseCommand):
    """Handles git hook installation - FIXED IMPORTS."""
    
    def execute(self, args) -> int:
        """Execute hook installation."""
        try:
            project_path = self.validate_path(args.install_hooks)
            
            from functions.git_integration import GitAnalyzer
            
            git_analyzer = GitAnalyzer(str(project_path))
            if not git_analyzer.is_git_repo():
                print("❌ Not a git repository")
                return 1
            
            print(f"🔧 Installing git hooks for: {project_path}")
            
            hook_config = {
                "security_enabled": True,
                "block_on_errors": True
            }
            
            if git_analyzer.install_simple_pre_commit_hook(hook_config):
                print("✅ Pre-commit hooks installed!")
                return 0
            else:
                print("❌ Hook installation failed")
                return 1
                
        except ImportError as e:
            print(f"❌ Git integration not available: {e}")
            return 1
        except Exception as e:
            print(f"❌ Hook installation failed: {e}")
            return 1


class PreCommitCommand(BaseCommand):
    """Handles pre-commit hook analysis - NEW COMMAND."""
    
    def execute(self, args) -> int:
        """Execute pre-commit analysis (called by git hooks)."""
        try:
            project_path = self.validate_path(args.pre_commit)
            
            from functions.git_integration import analyze_for_commit
            
            # Run pre-commit analysis with default config
            config = {
                "security_enabled": True,
                "block_on_errors": False  # Don't block on regular errors in hooks
            }
            
            return analyze_for_commit(str(project_path), config)
                
        except ImportError as e:
            print(f"⚠️ Pre-commit analysis not available: {e}")
            return 0  # Don't block commits on import errors
        except Exception as e:
            print(f"⚠️ Pre-commit analysis failed: {e}")
            return 0  # Don't block commits on analysis failures