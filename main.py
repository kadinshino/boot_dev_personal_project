#!/usr/bin/env python3
"""
Entry Point
"""

import sys
from pathlib import Path

BANNER = """
🚀 Enhanced Code Analyzer
A comprehensive Python development tool
=========================================
"""

def main() -> int:
    """Main entry point - simple routing only."""
    print(BANNER)
    
    # No arguments = GUI mode
    if len(sys.argv) == 1:
        return launch_gui()
    
    # Arguments = CLI mode
    return handle_cli()

def launch_gui() -> int:
    """Launch GUI Interface"""
    try:
        # Import the refactored GUI directly
        import gui.analyzer_gui as gui_module
        
        # Use the create_app function from our refactored GUI
        app = gui_module.create_app(Path("."))
        app.mainloop()
        return getattr(app, "exit_code", 0)
    except Exception as e:
        print(f"❌ GUI failed: {e}")
        print("💡 Make sure all GUI component files exist in gui/ directory")
        return 1

def handle_cli() -> int:
    """Handle CLI mode - delegate to CLI module."""
    try:
        from cli.command_handler import CLIHandler
        handler = CLIHandler()
        return handler.execute(sys.argv[1:])
    except ImportError:
        print("❌ CLI module not available")
        return 1
    except Exception as e:
        print(f"❌ CLI failed: {e}")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nℹ️ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)