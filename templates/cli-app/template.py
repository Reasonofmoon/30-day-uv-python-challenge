"""
CLI Application Template

This template provides a standard structure for CLI applications
using modern Python practices and the uv package manager.
"""

TEMPLATE_INFO = {
    "name": "CLI Application",
    "description": "Command-line interface application template",
    "type": "cli-app",
    "base_dependencies": ["typer", "rich", "pytest", "pytest-cov"],
    "python_version": ">=3.8"
}

DIRECTORY_STRUCTURE = [
    "src/{package_name}/__init__.py",
    "src/{package_name}/main.py",
    "src/{package_name}/core.py",
    "src/{package_name}/cli.py", 
    "src/{package_name}/utils.py",
    "tests/__init__.py",
    "tests/test_core.py",
    "tests/test_cli.py",
    "tests/conftest.py",
    "pyproject.toml",
    "README.md",
    ".gitignore"
]

TEMPLATE_FILES = {
    "src/{package_name}/cli.py": '''"""
CLI interface using Typer
"""

import typer
from typing import Optional
from rich.console import Console
from rich.table import Table

from .core import {class_name}

app = typer.Typer(help="{description}")
console = Console()


@app.command()
def run(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    config: Optional[str] = typer.Option(None, "--config", "-c", help="Configuration file path")
):
    """Run the main application functionality"""
    try:
        if verbose:
            console.print("🚀 Starting {project_name}...", style="bold green")
        
        # Initialize the main class
        instance = {class_name}()
        
        # Run the application
        result = instance.run()
        
        if result:
            console.print("✅ Completed successfully!", style="bold green")
        else:
            console.print("⚠️  Completed with warnings", style="bold yellow")
            
    except Exception as e:
        console.print(f"❌ Error: {{e}}", style="bold red")
        raise typer.Exit(1)


@app.command()
def status():
    """Show application status"""
    try:
        instance = {class_name}()
        status_info = instance.get_status()
        
        # Create status table
        table = Table(title="Application Status")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="magenta")
        
        for key, value in status_info.items():
            table.add_row(key.replace('_', ' ').title(), str(value))
        
        console.print(table)
        
    except Exception as e:
        console.print(f"❌ Error getting status: {{e}}", style="bold red")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
''',

    "tests/test_cli.py": '''"""
Tests for CLI interface
"""

import pytest
from typer.testing import CliRunner
from src.{package_name}.cli import app

runner = CliRunner()


def test_cli_run():
    """Test CLI run command"""
    result = runner.invoke(app, ["run"])
    assert result.exit_code == 0
    assert "Starting" in result.stdout or "Completed" in result.stdout


def test_cli_status():
    """Test CLI status command"""
    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0


def test_cli_verbose():
    """Test CLI with verbose flag"""
    result = runner.invoke(app, ["run", "--verbose"])
    assert result.exit_code == 0


def test_cli_help():
    """Test CLI help"""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.stdout
'''
}


def generate_template(package_name: str, class_name: str, project_name: str, description: str) -> dict:
    """Generate template files with substitutions"""
    files = {}
    
    for file_path, content in TEMPLATE_FILES.items():
        # Substitute template variables
        formatted_content = content.format(
            package_name=package_name,
            class_name=class_name,
            project_name=project_name,
            description=description
        )
        
        # Format file path
        formatted_path = file_path.format(package_name=package_name)
        
        files[formatted_path] = formatted_content
    
    return files