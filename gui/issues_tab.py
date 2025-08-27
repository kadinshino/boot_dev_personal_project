"""
Issues Tab Component - Self-Contained Version
===========================================
No external dependencies to avoid circular imports
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from pathlib import Path
from typing import List, Any


SEVERITY_ICONS = {
    "critical": "🔴", "high": "🟠", "error": "❌", "warning": "⚠️",
    "medium": "🟡", "info": "ℹ️", "low": "🔵"
}


class SimpleScrollableText(ttk.Frame):
    """Simple scrollable text widget."""
    
    def __init__(self, parent: tk.Widget, font=("Consolas", 9), **kwargs):
        super().__init__(parent)
        
        default_kwargs = {
            'font': font,
            'wrap': 'none',
            'bg': '#fafafa',
            'fg': '#2c3e50'
        }
        default_kwargs.update(kwargs)
        
        self.text_widget = scrolledtext.ScrolledText(self, **default_kwargs)
        self.text_widget.pack(fill="both", expand=True)
    
    def set_content(self, content: str):
        """Set text content."""
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(1.0, content)
        self.text_widget.see(1.0)
    
    def clear(self):
        """Clear content."""
        self.text_widget.delete(1.0, tk.END)


class SimpleFilterFrame(ttk.Frame):
    """Simple filter frame without external dependencies."""
    
    def __init__(self, parent: tk.Widget, options: List[str], 
                 callback, default: str = "all", label: str = "Filter:"):
        super().__init__(parent)
        
        # Filter label
        filter_label = ttk.Label(self, text=label, font=("TkDefaultFont", 10, "bold"))
        filter_label.pack(side="left")
        
        # Filter dropdown
        self.filter_var = tk.StringVar(value=default)
        self.filter_combo = ttk.Combobox(
            self,
            textvariable=self.filter_var,
            values=options,
            state="readonly",
            width=15
        )
        self.filter_combo.pack(side="left", padx=(8, 0))
        self.filter_combo.bind("<<ComboboxSelected>>", callback)
        
        self.callback = callback
    
    def get_value(self) -> str:
        """Get current filter value."""
        return self.filter_var.get()
    
    def set_value(self, value: str):
        """Set filter value."""
        if value in self.filter_combo['values']:
            self.filter_var.set(value)


class SimpleSearchFrame(ttk.Frame):
    """Simple search widget."""
    
    def __init__(self, parent: tk.Widget, search_callback, placeholder: str = "Search..."):
        super().__init__(parent)
        
        self.search_callback = search_callback
        self.placeholder = placeholder
        self.is_placeholder_active = True
        
        # Search icon
        ttk.Label(self, text="🔍").pack(side="left", padx=(0, 5))
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self, textvariable=self.search_var)
        self.search_entry.pack(side="left", fill="x", expand=True)
        
        # Clear button
        self.clear_button = ttk.Button(self, text="✕", command=self.clear_search, width=3)
        self.clear_button.pack(side="left", padx=(5, 0))
        
        # Setup placeholder and bindings
        self._setup_placeholder()
        self.search_var.trace("w", self._on_search_change)
    
    def _setup_placeholder(self):
        """Setup placeholder behavior."""
        self.search_entry.bind("<FocusIn>", self._on_focus_in)
        self.search_entry.bind("<FocusOut>", self._on_focus_out)
        self._show_placeholder()
    
    def _show_placeholder(self):
        """Show placeholder text."""
        if not self.search_var.get() or self.is_placeholder_active:
            self.search_entry.configure(foreground='grey')
            self.search_var.set(self.placeholder)
            self.is_placeholder_active = True
    
    def _hide_placeholder(self):
        """Hide placeholder text."""
        if self.is_placeholder_active:
            self.search_entry.configure(foreground='black')
            self.search_var.set("")
            self.is_placeholder_active = False
    
    def _on_focus_in(self, event):
        """Handle focus in."""
        self._hide_placeholder()
    
    def _on_focus_out(self, event):
        """Handle focus out."""
        if not self.search_var.get():
            self._show_placeholder()
    
    def _on_search_change(self, *args):
        """Handle search changes."""
        if not self.is_placeholder_active:
            self.search_callback(self.get_search_text())
    
    def get_search_text(self) -> str:
        """Get search text."""
        return "" if self.is_placeholder_active else self.search_var.get()
    
    def clear_search(self):
        """Clear search."""
        self.is_placeholder_active = False
        self.search_var.set("")
        self.search_entry.focus()
        self.search_callback("")
        self._show_placeholder()


class IssueFormatter:
    """Formats issues for display."""
    
    def format_issues_list(self, issues: List[Any], show_limit: int = 100) -> str:
        """Format issues for display."""
        if not issues:
            return "🎉 No issues found! Your code looks great!"
        
        lines = [f"🐛 ISSUES FOUND ({len(issues)} total)", "=" * 60, ""]
        
        for i, issue in enumerate(issues[:show_limit], 1):
            severity = getattr(issue, "severity", "unknown")
            message = getattr(issue, "message", "No message")
            file_path = getattr(issue, "file_path", "Unknown")
            line_num = getattr(issue, "line_number", 0)
            issue_type = getattr(issue, "issue_type", "unknown")
            
            icon = SEVERITY_ICONS.get(severity, "❓")
            file_name = Path(file_path).name if file_path != "Unknown" else "Unknown"
            
            lines.extend([
                f"{i}. {icon} {severity.upper()}: {message}",
                f"   📄 {file_name}:{line_num} ({issue_type})",
                ""
            ])
        
        if len(issues) > show_limit:
            lines.append(f"... and {len(issues) - show_limit} more issues")
        
        return "\n".join(lines)
    
    def get_issue_summary(self, issues: List[Any]) -> dict:
        """Get issue summary statistics."""
        if not issues:
            return {"total": 0, "by_severity": {}, "by_type": {}}
        
        by_severity = {}
        by_type = {}
        
        for issue in issues:
            severity = getattr(issue, "severity", "unknown")
            issue_type = getattr(issue, "issue_type", "unknown")
            
            by_severity[severity] = by_severity.get(severity, 0) + 1
            by_type[issue_type] = by_type.get(issue_type, 0) + 1
        
        return {
            "total": len(issues),
            "by_severity": by_severity,
            "by_type": by_type
        }


class IssueFilter:
    """Handles issue filtering logic."""
    
    def filter_by_severity(self, issues: List[Any], severity: str) -> List[Any]:
        """Filter by severity."""
        if severity == "all":
            return issues
        
        return [issue for issue in issues
                if getattr(issue, "severity", "unknown") == severity]
    
    def filter_by_search(self, issues: List[Any], search_term: str) -> List[Any]:
        """Filter by search term."""
        if not search_term:
            return issues
        
        search_lower = search_term.lower()
        filtered = []
        
        for issue in issues:
            # Search in various fields
            searchable_text = " ".join([
                getattr(issue, "message", "").lower(),
                getattr(issue, "file_path", "").lower(),
                getattr(issue, "issue_type", "").lower()
            ])
            
            if search_lower in searchable_text:
                filtered.append(issue)
        
        return filtered
    
    def get_severity_options(self, issues: List[Any]) -> List[str]:
        """Get available severity options."""
        if not issues:
            return ["all"]
        
        severities = set(getattr(issue, "severity", "unknown") for issue in issues)
        return ["all"] + sorted(severities)


class IssuesTab(ttk.Frame):
    """Self-contained issues tab."""
    
    def __init__(self, parent: tk.Widget, status_bar):
        super().__init__(parent)
        
        self.status_bar = status_bar
        self.all_issues: List[Any] = []
        self.filtered_issues: List[Any] = []
        
        # Helper components
        self.formatter = IssueFormatter()
        self.issue_filter = IssueFilter()
        
        self._build_interface()
    
    def _build_interface(self):
        """Build the interface."""
        # Header
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", pady=(0, 10))
        
        title_label = ttk.Label(header_frame, text="🐛 Issues", 
                               font=("TkDefaultFont", 12, "bold"))
        title_label.pack(side="left")
        
        self.issue_count_var = tk.StringVar(value="No analysis run")
        count_label = ttk.Label(header_frame, textvariable=self.issue_count_var)
        count_label.pack(side="right")
        
        # Controls
        controls_frame = ttk.Frame(self)
        controls_frame.pack(fill="x", pady=(0, 10))
        
        # Severity filter
        self.severity_filter = SimpleFilterFrame(
            controls_frame, 
            ["all"], 
            self._on_filter_change,
            default="all",
            label="Severity:"
        )
        self.severity_filter.pack(side="left")
        
        # Search box
        self.search_frame = SimpleSearchFrame(
            controls_frame,
            self._on_search_change,
            placeholder="Search issues..."
        )
        self.search_frame.pack(side="right", fill="x", expand=True, padx=(20, 0))
        
        # Issues display
        self.issues_display = SimpleScrollableText(self, font=("Consolas", 9), wrap="none")
        self.issues_display.pack(fill="both", expand=True)
        
        # Statistics
        stats_frame = ttk.LabelFrame(self, text="📊 Issue Statistics", padding=5)
        stats_frame.pack(fill="x", pady=(10, 0))
        
        self.stats_text = tk.StringVar(value="No issues to analyze")
        stats_label = ttk.Label(stats_frame, textvariable=self.stats_text, 
                               font=("TkDefaultFont", 9))
        stats_label.pack()
    
    def display_issues(self, issues: List[Any]):
        """Display new issues."""
        self.all_issues = issues or []
        
        # Update filter options
        severity_options = self.issue_filter.get_severity_options(self.all_issues)
        self.severity_filter.filter_combo.configure(values=severity_options)
        
        # Reset filters and display
        self.severity_filter.set_value("all")
        self.search_frame.clear_search()
        self._apply_filters()
        self._update_statistics()
    
    def _apply_filters(self):
        """Apply current filters."""
        # Start with all issues
        filtered = self.all_issues
        
        # Apply severity filter
        severity = self.severity_filter.get_value()
        filtered = self.issue_filter.filter_by_severity(filtered, severity)
        
        # Apply search filter
        search_term = self.search_frame.get_search_text()
        filtered = self.issue_filter.filter_by_search(filtered, search_term)
        
        # Update display
        self.filtered_issues = filtered
        self._display_filtered_issues()
    
    def _display_filtered_issues(self):
        """Display filtered issues."""
        formatted = self.formatter.format_issues_list(self.filtered_issues)
        self.issues_display.set_content(formatted)
        
        # Update counter
        if not self.all_issues:
            self.issue_count_var.set("No analysis run")
        elif len(self.filtered_issues) == len(self.all_issues):
            self.issue_count_var.set(f"📊 {len(self.all_issues)} issues found")
        else:
            self.issue_count_var.set(f"📊 {len(self.filtered_issues)} of {len(self.all_issues)} issues")
    
    def _update_statistics(self):
        """Update statistics display."""
        if not self.all_issues:
            self.stats_text.set("No issues to analyze")
            return
        
        summary = self.formatter.get_issue_summary(self.all_issues)
        
        # Build stats text
        stats_parts = []
        
        # Severity breakdown
        by_severity = summary["by_severity"]
        if by_severity:
            severity_stats = []
            for severity in ["critical", "high", "error", "warning", "medium", "info", "low"]:
                count = by_severity.get(severity, 0)
                if count > 0:
                    icon = SEVERITY_ICONS.get(severity, "❓")
                    severity_stats.append(f"{icon} {severity}: {count}")
            
            if severity_stats:
                stats_parts.append(" | ".join(severity_stats))
        
        # Top issue types
        by_type = summary["by_type"]
        if by_type:
            top_types = sorted(by_type.items(), key=lambda x: x[1], reverse=True)[:3]
            type_stats = [f"{issue_type}: {count}" for issue_type, count in top_types]
            stats_parts.append(f"Top types: {', '.join(type_stats)}")
        
        final_stats = " • ".join(stats_parts) if stats_parts else "No detailed statistics available"
        self.stats_text.set(final_stats)
    
    def _on_filter_change(self, event=None):
        """Handle filter changes."""
        self._apply_filters()
    
    def _on_search_change(self, search_term: str):
        """Handle search changes."""
        self._apply_filters()
    
    def get_issue_count(self) -> int:
        """Get total issue count."""
        return len(self.all_issues)