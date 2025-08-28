"""
Results Formatter
=================
Handles all result display formatting logic - separated from controller
"""

from pathlib import Path
from typing import Dict, List, Any
from functions.analysis_controller import AnalysisResults


def format_results_for_display(results: AnalysisResults) -> str:
    """Format results for display in GUI or CLI."""
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
    
    # Add recommendations
    lines.extend(_format_recommendations(results.issues))
    
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


def _format_recommendations(issues: List[Any]) -> List[str]:
    """Format recommendations based on issues found."""
    if len(issues) == 0:
        return [
            "",
            "🎉 CONGRATULATIONS!",
            "No issues were found in your codebase.",
            "Your code appears to be well-structured and follows good practices!",
        ]
    
    # Categorize issues by severity
    critical = sum(1 for issue in issues if getattr(issue, 'severity', '') == 'critical')
    high = sum(1 for issue in issues if getattr(issue, 'severity', '') == 'high')
    warnings = sum(1 for issue in issues if getattr(issue, 'severity', '') in ['warning', 'medium'])
    
    lines = ["", "💡 NEXT STEPS:"]
    if critical > 0:
        lines.append(f"  🔴 Address {critical} critical security issues immediately")
    if high > 0:
        lines.append(f"  🟠 Review {high} high-priority issues")  
    if warnings > 0:
        lines.append(f"  🟡 Consider fixing {warnings} warnings for better code quality")
    lines.append("  📊 Check the Issues tab for detailed information")
    
    return lines