"""
Refactored Code Analyzer GUI - Main Application
==============================================
Simplified main class that delegates to specialized components
"""

import tkinter as tk
from tkinter import ttk
from pathlib import Path
from typing import Optional

from functions.analysis_controller import AnalysisController
from gui.gui_components import StatusBar, StyleManager
from gui.setup_tab import SetupTab
from gui.results_tab import ResultsTab
from gui.issues_tab import IssuesTab


class CodeAnalyzerGUI(tk.Tk):
    """
    Main GUI application - now much simpler with delegation to specialized tabs.
    This class only handles:
    - Window management
    - Tab coordination
    - Cross-tab communication
    """
    
    def __init__(self, project_path: Optional[Path] = None):
        super().__init__()
        
        self.title("Code Analyzer Pro - Enhanced")
        self.geometry("1200x900")
        self.minsize(1000, 700)
        
        # Business logic controller (shared across tabs) - PASS WINDOW REFERENCE
        self.controller = AnalysisController(main_window=self)  # ← ADD main_window=self
        
        # Initialize UI
        self.style_manager = StyleManager(self)
        self._setup_ui()
        
        # Set initial project path
        if project_path:
            self.setup_tab.set_project_path(project_path)
    
    def _setup_ui(self):
        """Setup the main UI structure."""
        # Status bar (shared across all tabs)
        self.status_bar = StatusBar(self)
        
        # Main notebook
        self.notebook = ttk.Notebook(self, padding=10)
        self.notebook.pack(fill="both", expand=True)
        
        # Create specialized tab components
        self.setup_tab = SetupTab(
            self.notebook, 
            controller=self.controller,
            status_bar=self.status_bar,
            on_analysis_complete=self._on_analysis_complete
        )
        
        self.results_tab = ResultsTab(
            self.notebook,
            status_bar=self.status_bar
        )
        
        self.issues_tab = IssuesTab(
            self.notebook,
            status_bar=self.status_bar
        )
        
        # Add tabs to notebook
        self.notebook.add(self.setup_tab, text="🔧 Setup")
        self.notebook.add(self.results_tab, text="📊 Results")
        self.notebook.add(self.issues_tab, text="🐛 Issues")
    
    def _on_analysis_complete(self, results):
        """Handle analysis completion by coordinating between tabs."""
        # Update results tab
        self.results_tab.display_results(results)
        
        # Update issues tab
        self.issues_tab.display_issues(results.issues)
        
        # Switch to results tab
        self.notebook.select(1)
        
        # Update status
        issue_count = len(results.issues)
        modules_used = ", ".join(results.modules_used or [])
        self.status_bar.set_text(f"Analysis complete - {issue_count} issues found")
        self.status_bar.set_info(f"Modules: {modules_used}")


def create_app(project_path: Optional[Path] = None) -> CodeAnalyzerGUI:
    """Create and return the GUI application."""
    return CodeAnalyzerGUI(project_path)


if __name__ == "__main__":
    app = create_app()
    app.mainloop()