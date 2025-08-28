"""
Results Tab Component - Fixed Import Issues
==========================================
Complete file with all necessary imports and classes properly defined
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
from typing import Dict, List, Any, Optional

from functions.analysis_controller import AnalysisResults


class SimpleScrollableText(ttk.Frame):
    """Simple scrollable text widget without external dependencies."""
    
    def __init__(self, parent: tk.Widget, font=("Consolas", 10), **kwargs):
        super().__init__(parent)
        
        # Default styling
        default_kwargs = {
            'font': font,
            'wrap': 'word',
            'bg': '#fafafa',
            'fg': '#2c3e50',
            'selectbackground': '#3498db',
            'selectforeground': 'white',
            'insertbackground': '#2c3e50',
            'relief': 'flat',
            'borderwidth': 1
        }
        default_kwargs.update(kwargs)
        
        # Create the scrolled text widget
        self.text_widget = scrolledtext.ScrolledText(self, **default_kwargs)
        self.text_widget.pack(fill="both", expand=True)
        
        # Add context menu
        self._setup_context_menu()
    
    def _setup_context_menu(self):
        """Setup right-click context menu."""
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Copy", command=self._copy_text)
        self.context_menu.add_command(label="Select All", command=self._select_all)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Clear", command=self.clear)
        
        # Bind right-click
        self.text_widget.bind("<Button-3>", self._show_context_menu)
    
    def _show_context_menu(self, event):
        """Show context menu."""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def _copy_text(self):
        """Copy selected text to clipboard."""
        try:
            selected_text = self.text_widget.selection_get()
            self.clipboard_clear()
            self.clipboard_append(selected_text)
        except tk.TclError:
            pass
    
    def _select_all(self):
        """Select all text."""
        self.text_widget.tag_add("sel", "1.0", "end")
    
    def set_content(self, content: str):
        """Set text content, clearing previous content."""
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(1.0, content)
        self.text_widget.see(1.0)
    
    def get_content(self) -> str:
        """Get all text content."""
        return self.text_widget.get(1.0, tk.END)
    
    def clear(self):
        """Clear all content."""
        self.text_widget.delete(1.0, tk.END)


class SimpleButtonToolbar(ttk.Frame):
    """Simple toolbar without external dependencies."""
    
    def __init__(self, parent: tk.Widget, buttons: List[tuple]):
        super().__init__(parent)
        
        for button_info in buttons:
            text = button_info[0]
            command = button_info[1]
            side = button_info[2] if len(button_info) > 2 else "left"
            
            btn = ttk.Button(self, text=text, command=command)
            btn.pack(side=side, padx=2)


class ResultsFormatter:
    """Formats analysis results for display - refactored into smaller functions."""
    
    def format_comprehensive_results(self, results: Dict[str, Any], issues: List[Any]) -> str:
        """Main formatting method - now delegated to smaller functions."""
        lines = []
        
        # Header section
        lines.extend(self._format_header(results, issues))
        
        # Analysis sections
        sections_added = 0
        sections_added += self._add_code_analysis_section(lines, results)
        sections_added += self._add_security_section(lines, results)
        sections_added += self._add_dependency_section(lines, results)
        sections_added += self._add_discovery_section(lines, results)
        sections_added += self._add_git_section(lines, results)
        
        # Footer section
        lines.extend(self._format_footer(sections_added, issues))
        
        return "\n".join(lines)
    
    def _format_header(self, results: Dict[str, Any], issues: List[Any]) -> List[str]:
        """Format the report header."""
        metadata = results.get('analysis_metadata', {})
        return [
            "🎯 CODE ANALYSIS RESULTS",
            "=" * 60,
            f"📁 Project: {metadata.get('project_path', 'Unknown')}",
            f"📊 Total Issues: {len(issues)}",
            f"🔧 Modules Used: {', '.join(metadata.get('modules_used', []))}",
            f"⏰ Analysis Time: {metadata.get('timestamp', 'Unknown')}",
            "",
        ]
    
    def _add_code_analysis_section(self, lines: List[str], results: Dict[str, Any]) -> int:
        """Add code analysis section if available."""
        if "total_files" in results:
            lines.extend(self._format_code_analysis_section(results))
            return 1
        return 0
    
    def _add_security_section(self, lines: List[str], results: Dict[str, Any]) -> int:
        """Add security section if available."""
        if "security_scan" in results:
            lines.extend(self._format_security_section(results["security_scan"]))
            return 1
        return 0
    
    def _add_dependency_section(self, lines: List[str], results: Dict[str, Any]) -> int:
        """Add dependency section if available."""
        if "dependencies" in results:
            lines.extend(self._format_dependency_section(results["dependencies"]))
            return 1
        return 0
    
    def _add_discovery_section(self, lines: List[str], results: Dict[str, Any]) -> int:
        """Add discovery section if available."""
        if "legacy_analysis" in results:
            lines.extend(self._format_discovery_section(results["legacy_analysis"]))
            return 1
        return 0
    
    def _add_git_section(self, lines: List[str], results: Dict[str, Any]) -> int:
        """Add git section if available."""
        if "git_info" in results:
            lines.extend(self._format_git_section(results["git_info"]))
            return 1
        return 0
    
    def _format_footer(self, sections_added: int, issues: List[Any]) -> List[str]:
        """Format the report footer with summary and recommendations."""
        lines = [
            "=" * 60,
            f"📋 Analysis Complete - {sections_added} modules analyzed",
            f"🐛 Total Issues Found: {len(issues)}",
        ]
        
        if len(issues) == 0:
            lines.extend(self._format_success_message())
        else:
            lines.extend(self._format_issue_summary(issues))
        
        return lines
    
    def _format_success_message(self) -> List[str]:
        """Format success message when no issues found."""
        return [
            "",
            "🎉 CONGRATULATIONS!",
            "No issues were found in your codebase.",
            "Your code appears to be well-structured and follows good practices!",
        ]
    
    def _format_issue_summary(self, issues: List[Any]) -> List[str]:
        """Format issue summary and next steps."""
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
    
    def _format_code_analysis_section(self, results: Dict) -> List[str]:
        """Format code analysis section."""
        return [
            "📋 CODE ANALYSIS",
            "-" * 30,
            f"📄 Files: {results.get('total_files', 0)}",
            f"🔧 Functions: {results.get('total_functions', 0)}",
            f"🗂️ Classes: {results.get('total_classes', 0)}",
            f"📏 Lines of Code: {results.get('total_lines', 0)}",
            ""
        ]
    
    def _format_security_section(self, security_results: Dict) -> List[str]:
        """Format security analysis section."""
        severity_icons = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵"}
        
        lines = [
            "🔍 SECURITY ANALYSIS",
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
    
    def _format_dependency_section(self, dependency_results: Dict) -> List[str]:
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
        
        # Show detailed dependency breakdown
        self._add_dependency_details(lines, dependency_results)
        
        lines.append("")
        return lines
    
    def _add_dependency_details(self, lines: List[str], dependency_results: Dict):
        """Add detailed dependency information."""
        
        # Show unused imports if available
        unused = dependency_results.get("unused_imports", [])
        if unused:
            lines.append(f"\n🗑️ UNUSED IMPORTS ({len(unused)} found):")
            for i, unused_import in enumerate(unused[:10], 1):
                if isinstance(unused_import, dict):
                    module_name = unused_import.get("module_name", "Unknown")
                    file_path = unused_import.get("file_path", "")
                    line_number = unused_import.get("line_number", 0)
                    file_name = Path(file_path).name if file_path else "Unknown"
                    lines.append(f"  {i}. {module_name} in {file_name}:{line_number}")
                else:
                    lines.append(f"  {i}. {unused_import}")
            
            if len(unused) > 10:
                lines.append(f"  ... and {len(unused) - 10} more")
    
    def _format_discovery_section(self, discovery_results: Dict) -> List[str]:
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
    
    def _format_git_section(self, git_results: Dict) -> List[str]:
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


class ResultsTab(ttk.Frame):
    """Self-contained results tab without external GUI dependencies."""
    
    def __init__(self, parent: tk.Widget, status_bar):
        super().__init__(parent)
        
        self.status_bar = status_bar
        self.current_results: Optional[AnalysisResults] = None
        self.formatter = ResultsFormatter()
        
        self._build_interface()
    
    def _build_interface(self):
        """Build the results interface."""
        # Toolbar
        toolbar_buttons = [
            ("💾 Save Report", self._save_results, "left"),
            ("📋 Copy to Clipboard", self._copy_results, "left"), 
            ("🗑️ Clear Results", self._clear_results, "right")
        ]
        
        toolbar = SimpleButtonToolbar(self, toolbar_buttons)
        toolbar.pack(fill="x", pady=(0, 10))
        
        # Title
        title_label = ttk.Label(self, text="📊 Analysis Results", 
                               font=("TkDefaultFont", 12, "bold"))
        title_label.pack(anchor="w", pady=(0, 10))
        
        # Results display
        self.results_display = SimpleScrollableText(
            self, 
            font=("Consolas", 10),
            wrap="word"
        )
        self.results_display.pack(fill="both", expand=True)
    
    def display_results(self, results: AnalysisResults):
        """Display analysis results."""
        self.current_results = results
        
        if not results or not results.success:
            self.results_display.set_content("❌ No results to display or analysis failed.")
            return
        
        # Format and display results
        formatted_results = self.formatter.format_comprehensive_results(
            results.results,
            results.issues
        )
        
        self.results_display.set_content(formatted_results)
    
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
                ("Markdown files", "*.md"),
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            try:
                if filename.lower().endswith('.json'):
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(self.current_results.to_json())
                else:
                    content = self.results_display.get_content()
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(content)
                
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


# Ensure proper module exports
__all__ = ['ResultsTab', 'ResultsFormatter', 'SimpleScrollableText', 'SimpleButtonToolbar']


if __name__ == "__main__":
    # Test the component in isolation
    root = tk.Tk()
    root.title("Results Tab Test")
    root.geometry("800x600")
    
    # Create a mock status bar
    class MockStatusBar:
        """Mock status bar for testing the ResultsTab component."""
        
        def set_text(self, text):
            """Set status text - prints to console for testing."""
            print(f"Status: {text}")
    
    status_bar = MockStatusBar()
    
    # Create the results tab
    results_tab = ResultsTab(root, status_bar)
    results_tab.pack(fill="both", expand=True)
    
    print("ResultsTab test window created successfully!")
    root.mainloop()