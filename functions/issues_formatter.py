"""
Issues Formatter
================
Handles all issues display and filtering logic
"""

from pathlib import Path
from typing import List, Any


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