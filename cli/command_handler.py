"""
CLI Command Handler - Extracted from main.py

Handles all CLI operations in a clean, organized way.
Each analysis type has its own focused handler.
"""

import argparse
from pathlib import Path
from typing import Dict, Any


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
    """Handles basic code analysis."""
    
    def execute(self, args) -> int:
        """Execute basic analysis."""
        try:
            project_path = self.validate_path(args.analyze)
            print(f"🔍 Running basic analysis on: {project_path}")
            
            from functions.code_analyzer import analyze_project, summarize_results
            
            results = analyze_project(str(project_path))
            
            if args.json:
                import json
                output = json.dumps(results, indent=2, default=str)
            else:
                output = summarize_results(results)
            
            print(output)
            
            if args.save:
                self.save_results(output, args.save)
            
            # Return exit code based on issues
            issues = results.get('issues', [])
            errors = [i for i in issues if getattr(i, 'severity', 'info') == 'error']
            return 1 if errors else 0
            
        except ImportError:
            print("❌ Code analyzer module not available")
            return 1
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            return 1


class SecurityAnalysisCommand(BaseCommand):
    """Handles security analysis."""
    
    def execute(self, args) -> int:
        """Execute security analysis."""
        try:
            project_path = self.validate_path(args.security)
            print(f"🔒 Running security analysis on: {project_path}")
            
            from functions.security_scanner import SecurityScanner, create_security_report
            
            scanner = SecurityScanner()
            results = scanner.scan_project(project_path)
            
            if args.json:
                import json
                output = json.dumps(results, indent=2, default=str)
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
                
        except ImportError:
            print("❌ Security scanner not available")
            return 1
        except Exception as e:
            print(f"❌ Security analysis failed: {e}")
            return 1


class ComprehensiveAnalysisCommand(BaseCommand):
    """Handles comprehensive analysis."""
    
    def execute(self, args) -> int:
        """Execute comprehensive analysis."""
        try:
            project_path = self.validate_path(args.comprehensive)
            print(f"🚀 Running comprehensive analysis on: {project_path}")
            
            # Import all analyzers
            from functions.code_analyzer import analyze_project
            from functions.security_scanner import SecurityScanner
            from functions.dependency_analyzer import DependencyAnalyzer
            
            # Run all analyses
            results = {"comprehensive": True}
            
            # Code quality
            print("📋 Code quality...")
            code_results = analyze_project(str(project_path))
            results.update(code_results)
            
            # Security
            print("🔒 Security scan...")
            security_results = SecurityScanner().scan_project(project_path)
            results["security"] = security_results
            
            # Dependencies
            print("📦 Dependencies...")
            dep_results = DependencyAnalyzer(project_path).analyze_dependencies()
            results["dependencies"] = dep_results
            
            # Format output
            if args.json:
                import json
                output = json.dumps(results, indent=2, default=str)
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
    
    def _format_comprehensive_report(self, results: Dict[str, Any]) -> str:
        """Format comprehensive results."""
        lines = []
        lines.append("🚀 COMPREHENSIVE ANALYSIS REPORT")
        lines.append("=" * 50)
        
        # Code quality summary
        issues = results.get('issues', [])
        lines.append(f"📊 Code Issues: {len(issues)}")
        
        # Security summary
        security = results.get('security', {})
        vuln_count = security.get('total_vulnerabilities', 0)
        lines.append(f"🔒 Security Vulnerabilities: {vuln_count}")
        
        # Dependency summary
        deps = results.get('dependencies', {})
        dep_count = len(deps.get('all_dependencies', {}))
        lines.append(f"📦 Dependencies: {dep_count}")
        
        return "\n".join(lines)
    
    def _calculate_exit_code(self, results: Dict[str, Any]) -> int:
        """Calculate exit code based on all results."""
        # Check for critical security issues
        security = results.get('security', {})
        critical = security.get('vulnerability_counts', {}).get('critical', 0)
        if critical > 0:
            return 2
        
        # Check for code errors
        issues = results.get('issues', [])
        errors = [i for i in issues if getattr(i, 'severity', 'info') == 'error']
        if errors:
            return 1
            
        return 0


class LegacyAnalysisCommand(BaseCommand):
    """Handles codebase discovery analysis."""
    
    def execute(self, args) -> int:
        """Execute codebase discovery analysis."""
        try:
            project_path = self.validate_path(args.legacy)
            print(f"🗺️ Running codebase discovery on: {project_path}")
            
            # Use the new simplified API
            from functions.codebase_discovery import analyze_codebase, create_discovery_report
            
            results = analyze_codebase(str(project_path))
            
            if args.json:
                import json
                from dataclasses import asdict
                output = json.dumps(asdict(results), indent=2, default=str)
            else:
                output = create_discovery_report(results)
            
            print(output)
            
            if args.save:
                self.save_results(output, args.save)
            
            # Exit code based on analysis success (no more "risk areas" concept)
            return 0  # Success - discovery doesn't have "critical risks"
            
        except ImportError:
            print("❌ Codebase discovery not available")
            return 1
        except Exception as e:
            print(f"❌ Codebase discovery failed: {e}")
            return 1

class TeamAnalysisCommand(BaseCommand):
    """Handles team collaboration analysis."""
    
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
                import json
                output = json.dumps(team_report, indent=2, default=str)
            else:
                output = self._format_team_report(team_report)
            
            print(output)
            
            if args.save:
                self.save_results(output, args.save)
            
            # Exit code based on commit readiness
            status = team_report.get("commit_readiness", {}).get("status")
            return {"blocked": 2, "caution": 1}.get(status, 0)
            
        except ImportError:
            print("❌ Git integration not available")
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
        
        status_icons = {"ready": "✅", "caution": "⚠️", "blocked": "🚫"}
        icon = status_icons.get(status, "❓")
        
        lines.append(f"{icon} COMMIT STATUS: {status.upper()}")
        lines.append(f"Reason: {reason}")
        
        return "\n".join(lines)


class InstallHooksCommand(BaseCommand):
    """Handles git hook installation."""
    
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
                
        except ImportError:
            print("❌ Git integration not available")
            return 1
        except Exception as e:
            print(f"❌ Hook installation failed: {e}")
            return 1