"""
Task Manager CLI - CLI Application
Day ? of 30-day Python challenge
"""

import sys
from typing import Optional

from .core import TaskManagerCli


def main():
    """Main CLI entry point"""
    print("🎯 Task Manager CLI")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("Usage: python -m task_manager_cli [command] [options]")
        print("Commands:")
        print("  help    - Show help information")
        print("  run     - Run the main functionality")
        return
    
    command = sys.argv[1].lower()
    
    try:
        app = TaskManagerCli()
        
        if command == "help":
            show_help()
        elif command == "run":
            app.run()
        else:
            print(f"Unknown command: {command}")
            show_help()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def show_help():
    """Show help information"""
    print("🎯 Task Manager CLI - Help")
    print()
    print("Description:")
    print("  SQLite-based task management with rich terminal UI")
    print()
    print("Commands:")
    print("  help    Show this help message")
    print("  run     Run the main application")
    print()
    print("Examples:")
    print("  python -m task_manager_cli run")
    print("  python -m task_manager_cli help")


if __name__ == "__main__":
    main()
