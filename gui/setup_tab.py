"""
Setup Tab Component
==========================================
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import Callable, Dict

# Import the controller directly
from functions.analysis_controller import AnalysisController


MODULE_CONFIG = {
    "code_analyzer": {
        "label": "📋 Code Quality Analysis",
        "description": "Analyze code quality, complexity, and structure",
        "default_enabled": True
    },
    "security_scanner": {
        "label": "🔐 Security Scan", 
        "description": "Scan for security vulnerabilities and issues",
        "default_enabled": True
    },
    "dependency_analyzer": {
        "label": "📦 Dependency Analysis",
        "description": "Analyze project dependencies and imports", 
        "default_enabled": True
    },
    "codebase_discovery": {
        "label": "🗺️ Codebase Discovery",
        "description": "Discover project structure and frameworks",
        "default_enabled": False
    },
    "git_integration": {
        "label": "📊 Git Integration",
        "description": "Analyze git repository information",
        "default_enabled": False
    }
}


class SimpleProgressFrame(ttk.Frame):
    """Simple progress display without external dependencies."""
    
    def __init__(self, parent: tk.Widget, show_progress_bar: bool = False):
        super().__init__(parent)
        
        # Progress text
        self.progress_var = tk.StringVar(value="Ready")
        self.progress_label = ttk.Label(self, textvariable=self.progress_var)
        self.progress_label.pack(anchor="w")
        
        # Optional progress bar
        self.progress_bar = None
        if show_progress_bar:
            self.progress_bar = ttk.Progressbar(
                self,
                mode="indeterminate",
                length=400
            )
            self.progress_bar.pack(fill="x", pady=(5, 0))
    
    def set_text(self, text: str):
        """Update progress text."""
        self.progress_var.set(text)
        self.update_idletasks()
    
    def start_progress(self):
        """Start animated progress bar."""
        if self.progress_bar:
            self.progress_bar.start(10)
    
    def stop_progress(self):
        """Stop animated progress bar."""
        if self.progress_bar:
            self.progress_bar.stop()


class SimpleModuleSelector(ttk.LabelFrame):
    """Simple module selection without external dependencies."""
    
    def __init__(self, parent: tk.Widget, modules: Dict[str, Dict], title: str = "Select Modules"):
        super().__init__(parent, text=title, padding=15)
        
        self.module_vars = {}
        self.module_widgets = {}
        
        for module_id, module_info in modules.items():
            self._create_module_row(module_id, module_info)
    
    def _create_module_row(self, module_id: str, module_info: Dict):
        """Create a row for a single module."""
        # Main frame for this module
        module_frame = ttk.Frame(self)
        module_frame.pack(fill="x", pady=3)
        
        # Extract module info
        label = module_info.get('label', module_id)
        description = module_info.get('description', '')
        available = module_info.get('available', True)
        default_enabled = module_info.get('default_enabled', False)
        
        # Create checkbox
        var = tk.BooleanVar(value=default_enabled and available)
        self.module_vars[module_id] = var
        
        cb = ttk.Checkbutton(
            module_frame, 
            text=label, 
            variable=var
        )
        cb.pack(side="left")
        
        # Status indicator
        if available:
            status_label = ttk.Label(
                module_frame, 
                text="✅ Ready", 
                foreground="#27ae60"
            )
            status_label.pack(side="right")
        else:
            status_label = ttk.Label(
                module_frame, 
                text="❌ Unavailable", 
                foreground="#e74c3c"
            )
            status_label.pack(side="right")
            
            # Disable checkbox
            cb.configure(state="disabled")
            var.set(False)
        
        # Store widgets for later access
        self.module_widgets[module_id] = {
            'frame': module_frame,
            'checkbox': cb,
            'status': status_label
        }
        
        # Description (if provided)
        if description:
            desc_label = ttk.Label(
                self, 
                text=f"   {description}",
                font=("TkDefaultFont", 8),
                foreground="#7f8c8d"
            )
            desc_label.pack(anchor="w", padx=(20, 0))
    
    def get_selected_modules(self) -> Dict[str, bool]:
        """Get dictionary of module_id: enabled status."""
        return {module_id: var.get() for module_id, var in self.module_vars.items()}
    
    def update_module_status(self, module_id: str, available: bool):
        """Update the availability status of a module."""
        if module_id in self.module_widgets:
            widgets = self.module_widgets[module_id]
            checkbox = widgets['checkbox']
            status = widgets['status']
            
            if available:
                status.configure(text="✅ Ready", foreground="#27ae60")
                checkbox.configure(state="normal")
            else:
                status.configure(text="❌ Unavailable", foreground="#e74c3c") 
                checkbox.configure(state="disabled")
                self.module_vars[module_id].set(False)


class SetupTab(ttk.Frame):
    """
    Specialized component for handling analysis setup.
    Self-contained with minimal external dependencies.
    """
    
    def __init__(self, parent: tk.Widget, controller: AnalysisController, 
                 status_bar, on_analysis_complete: Callable):
        super().__init__(parent)
        
        self.controller = controller
        self.status_bar = status_bar
        self.on_analysis_complete = on_analysis_complete
        self.current_project = Path.cwd()
        
        self._build_interface()
        self._update_module_availability()
    
    def _build_interface(self):
        """Build the setup interface."""
        # Project selection section
        self._build_project_section()
        
        # Module selection section  
        self._build_module_section()
        
        # Analysis controls section
        self._build_controls_section()
    
    def _build_project_section(self):
        """Build project selection section."""
        proj_frame = ttk.LabelFrame(self, text="📁 Project Selection", padding=15)
        proj_frame.pack(fill="x", pady=(0, 15))
        
        ttk.Label(proj_frame, text="Project Path:", 
                 font=("TkDefaultFont", 10, "bold")).pack(anchor="w")
        
        path_frame = ttk.Frame(proj_frame)
        path_frame.pack(fill="x", pady=(5, 0))
        
        self.path_var = tk.StringVar(value=str(self.current_project))
        self.path_entry = ttk.Entry(path_frame, textvariable=self.path_var, font=("Consolas", 10))
        self.path_entry.pack(side="left", fill="x", expand=True)
        
        ttk.Button(path_frame, text="📁 Browse...", 
                  command=self._browse_project).pack(side="left", padx=(8, 0))
    
    def _build_module_section(self):
        """Build module selection section."""
        # Get available modules and update config
        available_modules = self.controller.get_available_modules()
        
        module_config = MODULE_CONFIG.copy()
        for module_id, config in module_config.items():
            config['available'] = available_modules.get(module_id, False)
        
        self.module_selector = SimpleModuleSelector(
            self, 
            module_config, 
            title="🔧 Analysis Modules"
        )
        self.module_selector.pack(fill="x", pady=(0, 15))
    
    def _build_controls_section(self):
        """Build analysis controls section."""
        controls_frame = ttk.LabelFrame(self, text="🚀 Run Analysis", padding=15)
        controls_frame.pack(fill="x")
        
        # Progress display
        self.progress_frame = SimpleProgressFrame(controls_frame, show_progress_bar=True)
        self.progress_frame.pack(fill="x", pady=(0, 10))
        
        # Control buttons
        button_frame = ttk.Frame(controls_frame)
        button_frame.pack(fill="x")
        
        self.run_button = ttk.Button(
            button_frame, text="🚀 Run Analysis", 
            command=self._start_analysis
        )
        self.run_button.pack(side="left")
        
        ttk.Button(
            button_frame, text="🔄 Refresh Modules",
            command=self._refresh_modules
        ).pack(side="left", padx=(10, 0))
    
    def _browse_project(self):
        """Browse for project directory."""
        directory = filedialog.askdirectory(
            title="Select Project Directory",
            initialdir=str(self.current_project)
        )
        if directory:
            self.current_project = Path(directory)
            self.path_var.set(str(directory))
            self.status_bar.set_text(f"Selected: {Path(directory).name}")
    
    def _start_analysis(self):
        """Start analysis using the controller."""
        # Validate inputs
        project_path = self.path_var.get().strip()
        if not project_path or not Path(project_path).exists():
            messagebox.showerror("Invalid Path", "Please select a valid project directory.")
            return
        
        enabled_modules = self.module_selector.get_selected_modules()
        if not any(enabled_modules.values()):
            messagebox.showwarning("No Modules", "Please select at least one module.")
            return
        
        # Disable UI and start analysis
        self._set_analysis_state(True)
        
        # Use controller for async analysis
        self.controller.run_analysis_async(
            project_path=project_path,
            enabled_modules=enabled_modules,
            progress_callback=self._on_progress,
            completion_callback=self._on_analysis_complete_internal
        )
    
    def _on_progress(self, message: str):
        """Handle progress updates from controller."""
        self.progress_frame.set_text(message)
        self.status_bar.set_text(message)
        self.update()  # Force UI update
    
    def _on_analysis_complete_internal(self, results):
        """Handle analysis completion internally, then notify parent."""
        self._set_analysis_state(False)
        
        if results.success:
            # Notify parent component
            self.on_analysis_complete(results)
        else:
            messagebox.showerror("Analysis Failed", f"Analysis failed: {results.error_message}")
            self.status_bar.set_text("Analysis failed")
    
    def _set_analysis_state(self, analyzing: bool):
        """Enable/disable UI during analysis."""
        state = "disabled" if analyzing else "normal"
        text = "🔄 Analyzing..." if analyzing else "🚀 Run Analysis"
        
        self.run_button.configure(state=state, text=text)
        self.path_entry.configure(state=state)
        
        if analyzing:
            self.progress_frame.start_progress()
            self.progress_frame.set_text("Starting analysis...")
        else:
            self.progress_frame.stop_progress()
            self.progress_frame.set_text("Ready to analyze")
    
    def _refresh_modules(self):
        """Refresh module availability."""
        self._update_module_availability()
        self.status_bar.set_text("Module availability refreshed")
    
    def _update_module_availability(self):
        """Update which modules are available."""
        available_modules = self.controller.get_available_modules()
        
        # Update module selector
        for module_id, available in available_modules.items():
            self.module_selector.update_module_status(module_id, available)
        
        # Update status bar
        available_count = sum(1 for available in available_modules.values() if available)
        total_count = len(available_modules)
        self.status_bar.set_info(f"Modules: {available_count}/{total_count} available")
    
    def set_project_path(self, path: Path):
        """Set the project path externally."""
        self.current_project = path
        self.path_var.set(str(path))