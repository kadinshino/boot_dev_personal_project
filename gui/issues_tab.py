"""
Lightweight Issues Tab Component
==============================
Much simpler - uses existing GUI components and delegates business logic
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Any

from gui.gui_components import ScrollableText, FilterFrame


class SearchFrame(ttk.Frame):
    """Simple search widget using existing patterns."""
    
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
        self.clear_button = ttk.Button(self, text="✖", command=self.clear_search, width=3)
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


class IssuesTab(ttk.Frame):
    """Lightweight issues tab - delegates business logic to controller."""
    
    def __init__(self, parent: tk.Widget, status_bar):
        super().__init__(parent)
        
        self.status_bar = status_bar
        self.all_issues: List[Any] = []
        self.filtered_issues: List[Any] = []
        
        self._build_interface()
    
    def _build_interface(self):
        """Build the simple interface."""
        # Header
        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", pady=(0, 10))
        
        title_label = ttk.Label(
            header_frame, 
            text="🐛 Issues", 
            font=("TkDefaultFont", 12, "bold")
        )
        title_label.pack(side="left")
        
        self.issue_count_var = tk.StringVar(value="No analysis run")
        count_label = ttk.Label(header_frame, textvariable=self.issue_count_var)
        count_label.pack(side="right")
        
        # Controls
        controls_frame = ttk.Frame(self)
        controls_frame.pack(fill="x", pady=(0, 10))
        
        # Severity filter using existing FilterFrame
        self.severity_filter = FilterFrame(
            controls_frame, 
            ["all"], 
            self._on_filter_change,
            default="all",
            label="Severity:"
        )
        self.severity_filter.pack(side="left")
        
        # Search box
        self.search_frame = SearchFrame(
            controls_frame,
            self._on_search_change,
            placeholder="Search issues..."
        )
        self.search_frame.pack(side="right", fill="x", expand=True, padx=(20, 0))
        
        # Issues display using existing ScrollableText
        self.issues_display = ScrollableText(
            self, 
            font=("Consolas", 9), 
            wrap="none"
        )
        self.issues_display.pack(fill="both", expand=True)
        
        # Statistics
        stats_frame = ttk.LabelFrame(self, text="📊 Issue Statistics", padding=5)
        stats_frame.pack(fill="x", pady=(10, 0))
        
        self.stats_text = tk.StringVar(value="No issues to analyze")
        stats_label = ttk.Label(
            stats_frame, 
            textvariable=self.stats_text, 
            font=("TkDefaultFont", 9)
        )
        stats_label.pack()
    
    def display_issues(self, issues: List[Any]):
        """Display new issues - delegates formatting to specialized formatter."""
        self.all_issues = issues or []
        
        # FIXED: Import from correct module  
        from functions.issues_formatter import get_severity_options
        severity_options = get_severity_options(self.all_issues)
        self.severity_filter.filter_combo.configure(values=severity_options)
        
        # Reset filters and display
        self.severity_filter.set_value("all")
        self.search_frame.clear_search()
        self._apply_filters()
        self._update_statistics()
    
    def _apply_filters(self):
        """Apply current filters - delegates to specialized formatter."""
        from functions.issues_formatter import filter_issues
        
        # Get current filter values
        severity = self.severity_filter.get_value()
        search_term = self.search_frame.get_search_text()
        
        # Delegate filtering to business logic
        self.filtered_issues = filter_issues(
            self.all_issues, 
            severity_filter=severity,
            search_term=search_term
        )
        
        self._display_filtered_issues()
    
    def _display_filtered_issues(self):
        """Display filtered issues - delegates formatting to specialized formatter."""
        from functions.issues_formatter import format_issues_for_display
        
        formatted = format_issues_for_display(self.filtered_issues)
        self.issues_display.set_content(formatted)
        
        # Update counter
        if not self.all_issues:
            self.issue_count_var.set("No analysis run")
        elif len(self.filtered_issues) == len(self.all_issues):
            self.issue_count_var.set(f"📊 {len(self.all_issues)} issues found")
        else:
            self.issue_count_var.set(f"📊 {len(self.filtered_issues)} of {len(self.all_issues)} issues")
    
    def _update_statistics(self):
        """Update statistics display - delegates to specialized formatter."""
        if not self.all_issues:
            self.stats_text.set("No issues to analyze")
            return
        
        from functions.issues_formatter import get_issue_statistics
        stats_text = get_issue_statistics(self.all_issues)
        self.stats_text.set(stats_text)
    
    def _on_filter_change(self, event=None):
        """Handle filter changes."""
        self._apply_filters()
    
    def _on_search_change(self, search_term: str):
        """Handle search changes."""
        self._apply_filters()
    
    def get_issue_count(self) -> int:
        """Get total issue count."""
        return len(self.all_issues)