"""
Lightweight Results Tab Component
================================
Much simpler - uses existing GUI components and delegates formatting
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import Optional

from functions.analysis_controller import AnalysisResults
from gui.gui_components import ScrollableText, ButtonToolbar


class ResultsTab(ttk.Frame):
    """Lightweight results display tab."""
    
    def __init__(self, parent: tk.Widget, status_bar):
        super().__init__(parent)
        
        self.status_bar = status_bar
        self.current_results: Optional[AnalysisResults] = None
        
        self._build_interface()
    
    def _build_interface(self):
        """Build the simple interface."""
        # Title
        title_label = ttk.Label(
            self, 
            text="📊 Analysis Results", 
            font=("TkDefaultFont", 12, "bold")
        )
        title_label.pack(anchor="w", pady=(0, 10))
        
        # Simple toolbar using existing component
        toolbar_buttons = [
            ("💾 Save Report", self._save_results, "left"),
            ("📋 Copy to Clipboard", self._copy_results, "left"), 
            ("🗑️ Clear Results", self._clear_results, "right")
        ]
        
        toolbar = ButtonToolbar(self, toolbar_buttons)
        toolbar.pack(fill="x", pady=(0, 10))
        
        # Results display using existing component
        self.results_display = ScrollableText(
            self, 
            font=("Consolas", 10),
            wrap="word"
        )
        self.results_display.pack(fill="both", expand=True)
    
    def display_results(self, results: AnalysisResults):
        """Display analysis results - delegates formatting to specialized formatter."""
        self.current_results = results
        
        if not results or not results.success:
            self.results_display.set_content("❌ No results to display or analysis failed.")
            return
        
        # FIXED: Import from the correct module
        from functions.results_formatter import format_results_for_display
        formatted_text = format_results_for_display(results)
        
        self.results_display.set_content(formatted_text)
        self.status_bar.set_text(f"Results displayed - {len(results.issues)} issues found")
    
    def _save_results(self):
        """Save results to file."""
        if not self.current_results:
            messagebox.showwarning("No Results", "No results to save.")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save Analysis Results",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                # Delegate to formatter
                from functions.results_formatter import save_results_to_file
                save_results_to_file(self.current_results, filename)
                
                messagebox.showinfo("Saved", f"Results saved to {Path(filename).name}")
                self.status_bar.set_text(f"Results saved to {Path(filename).name}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save: {e}")
    
    def _copy_results(self):
        """Copy results to clipboard."""
        if not self.current_results:
            messagebox.showwarning("No Results", "No results to copy.")
            return
        
        try:
            content = self.results_display.get_content()
            self.clipboard_clear()
            self.clipboard_append(content)
            messagebox.showinfo("Copied", "Results copied to clipboard!")
            self.status_bar.set_text("Results copied to clipboard")
        except Exception as e:
            messagebox.showerror("Copy Error", f"Failed to copy: {e}")
    
    def _clear_results(self):
        """Clear all results."""
        if messagebox.askyesno("Clear Results", "Clear all analysis results?"):
            self.current_results = None
            self.results_display.clear()
            self.status_bar.set_text("Results cleared")
    
    def has_results(self) -> bool:
        """Check if there are results to display."""
        return self.current_results is not None and self.current_results.success