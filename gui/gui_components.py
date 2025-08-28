"""
GUI Components
==============================================
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import List, Dict, Callable, Tuple


class StatusBar(ttk.Frame):
    """Simple status bar."""
    
    def __init__(self, parent: tk.Widget):
        super().__init__(parent)
        self.pack(fill="x", side="bottom", pady=(5, 0))
        
        # Main status text
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(
            self, 
            textvariable=self.status_var,
            relief="sunken",
            anchor="w",
            padding=(5, 2)
        )
        self.status_label.pack(fill="x", side="left", expand=True)
        
        # Secondary info
        self.info_var = tk.StringVar(value="")
        self.info_label = ttk.Label(
            self,
            textvariable=self.info_var,
            relief="sunken",
            anchor="center",
            padding=(5, 2)
        )
    
    def set_text(self, text: str):
        """Set main status text."""
        self.status_var.set(text)
    
    def set_info(self, text: str):
        """Set secondary info text."""
        if text:
            self.info_var.set(text)
            self.info_label.pack(side="right", padx=(5, 0))
        else:
            self.info_label.pack_forget()


class StyleManager:
    """Simple style manager."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.style = ttk.Style(root)
        self._setup_styles()
    
    def _setup_styles(self):
        """Configure basic styles."""
        self.style.configure(
            "Title.TLabel",
            font=("TkDefaultFont", 12, "bold"),
            foreground="#2c3e50"
        )
        
        self.style.configure(
            "Section.TLabel",
            font=("TkDefaultFont", 10, "bold"),
            foreground="#34495e"
        )


class ProgressFrame(ttk.Frame):
    """Simple progress display."""
    
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


class ScrollableText(ttk.Frame):
    """Simple scrollable text widget."""
    
    def __init__(self, parent: tk.Widget, font=("Consolas", 10), **text_kwargs):
        super().__init__(parent)
        
        default_kwargs = {
            'font': font,
            'wrap': 'word',
            'bg': '#fafafa',
            'fg': '#2c3e50'
        }
        default_kwargs.update(text_kwargs)
        
        self.text_widget = scrolledtext.ScrolledText(self, **default_kwargs)
        self.text_widget.pack(fill="both", expand=True)
    
    def set_content(self, content: str):
        """Set text content."""
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(1.0, content)
        self.text_widget.see(1.0)
    
    def get_content(self) -> str:
        """Get all text content."""
        return self.text_widget.get(1.0, tk.END)
    
    def clear(self):
        """Clear all content."""
        self.text_widget.delete(1.0, tk.END)


class ButtonToolbar(ttk.Frame):
    """Simple button toolbar."""
    
    def __init__(self, parent: tk.Widget, buttons: List[Tuple]):
        super().__init__(parent)
        
        for button_info in buttons:
            text = button_info[0]
            command = button_info[1]
            side = button_info[2] if len(button_info) > 2 else "left"
            
            btn = ttk.Button(self, text=text, command=command)
            btn.pack(side=side, padx=2)


class ModuleSelector(ttk.LabelFrame):
    """Simple module selection."""
    
    def __init__(self, parent: tk.Widget, modules: Dict[str, Dict], title: str = "Select Modules"):
        super().__init__(parent, text=title, padding=15)
        
        self.module_vars = {}
        self.module_widgets = {}
        
        for module_id, module_info in modules.items():
            self._create_module_row(module_id, module_info)
    
    def _create_module_row(self, module_id: str, module_info: Dict):
        """Create a row for a single module."""
        module_frame = ttk.Frame(self)
        module_frame.pack(fill="x", pady=3)
        
        label = module_info.get('label', module_id)
        available = module_info.get('available', True)
        default_enabled = module_info.get('default_enabled', False)
        
        var = tk.BooleanVar(value=default_enabled and available)
        self.module_vars[module_id] = var
        
        cb = ttk.Checkbutton(module_frame, text=label, variable=var)
        cb.pack(side="left")
        
        if available:
            status_label = ttk.Label(module_frame, text="✅ Ready")
        else:
            status_label = ttk.Label(module_frame, text="❌ Unavailable")
            cb.configure(state="disabled")
            var.set(False)
        
        status_label.pack(side="right")
        
        self.module_widgets[module_id] = {
            'frame': module_frame,
            'checkbox': cb,
            'status': status_label
        }
    
    def get_selected_modules(self) -> Dict[str, bool]:
        """Get dictionary of module_id: enabled status."""
        return {module_id: var.get() for module_id, var in self.module_vars.items()}
    
    def update_module_status(self, module_id: str, available: bool):
        """Update module availability status."""
        if module_id in self.module_widgets:
            widgets = self.module_widgets[module_id]
            checkbox = widgets['checkbox']
            status = widgets['status']
            
            if available:
                status.configure(text="✅ Ready")
                checkbox.configure(state="normal")
            else:
                status.configure(text="❌ Unavailable")
                checkbox.configure(state="disabled")
                self.module_vars[module_id].set(False)


class FilterFrame(ttk.Frame):
    """Simple filter controls."""
    
    def __init__(self, parent: tk.Widget, options: List[str], 
                 callback: Callable, default: str = "all", label: str = "Filter:"):
        super().__init__(parent)
        
        ttk.Label(self, text=label).pack(side="left")
        
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