#!/usr/bin/env python3
"""
Claude Code Environment Explorer
=================================
An interactive tool to understand and explore the Claude Code environment capabilities.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


class ClaudeEnvironmentExplorer:
    def __init__(self):
        self.cwd = Path.cwd()

    def print_header(self, text):
        print(f"\n{'='*60}")
        print(f"  {text}")
        print(f"{'='*60}\n")

    def show_system_info(self):
        """Display system and environment information"""
        self.print_header("System Information")

        info = {
            "Operating System": platform.system(),
            "OS Version": platform.release(),
            "Platform": platform.platform(),
            "Architecture": platform.machine(),
            "Python Version": platform.python_version(),
            "Current Directory": os.getcwd(),
            "Home Directory": os.path.expanduser("~"),
            "User": os.getenv("USER", "unknown"),
        }

        for key, value in info.items():
            print(f"  {key:20s}: {value}")

    def show_installed_tools(self):
        """Check and display installed development tools"""
        self.print_header("Development Tools Available")

        tools = [
            ("Python", "python3 --version"),
            ("Node.js", "node --version"),
            ("npm", "npm --version"),
            ("Git", "git --version"),
            ("pip", "pip --version"),
            ("curl", "curl --version | head -1"),
            ("wget", "wget --version | head -1"),
            ("docker", "docker --version"),
            ("gcc", "gcc --version | head -1"),
        ]

        for name, command in tools:
            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                if result.returncode == 0:
                    version = result.stdout.strip().split('\n')[0]
                    print(f"  ✓ {name:15s}: {version}")
                else:
                    print(f"  ✗ {name:15s}: Not installed")
            except Exception as e:
                print(f"  ✗ {name:15s}: Not available")

    def show_git_capabilities(self):
        """Demonstrate Git capabilities"""
        self.print_header("Git Repository Information")

        try:
            # Check if in git repo
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print("  ✓ Current directory is a Git repository\n")

                # Show current branch
                branch = subprocess.run(
                    ["git", "branch", "--show-current"],
                    capture_output=True,
                    text=True
                ).stdout.strip()
                print(f"  Current Branch: {branch}")

                # Show remote
                remote = subprocess.run(
                    ["git", "remote", "-v"],
                    capture_output=True,
                    text=True
                ).stdout.strip()
                if remote:
                    print(f"\n  Remotes:")
                    for line in remote.split('\n')[:2]:  # Show first 2 lines
                        print(f"    {line}")

                # Show recent commits
                commits = subprocess.run(
                    ["git", "log", "--oneline", "-5"],
                    capture_output=True,
                    text=True
                ).stdout.strip()

                if commits:
                    print(f"\n  Recent Commits:")
                    for commit in commits.split('\n'):
                        print(f"    {commit}")

                # Show status
                status = subprocess.run(
                    ["git", "status", "--short"],
                    capture_output=True,
                    text=True
                ).stdout.strip()

                print(f"\n  Git Status:")
                if status:
                    for line in status.split('\n'):
                        print(f"    {line}")
                else:
                    print("    Working tree clean")
            else:
                print("  ✗ Not a Git repository")
        except Exception as e:
            print(f"  Error checking Git: {e}")

    def show_file_operations(self):
        """Demonstrate file operation capabilities"""
        self.print_header("File System Capabilities")

        print("  Claude Code can perform various file operations:")
        print("  • Read files (any format: code, text, images, PDFs)")
        print("  • Write and create new files")
        print("  • Edit existing files with precise replacements")
        print("  • Search files using glob patterns")
        print("  • Search file contents using regex (grep)")
        print("  • Execute shell commands")
        print()

        # Show current directory structure
        print("  Current Directory Structure:")
        for item in sorted(self.cwd.iterdir()):
            if item.name.startswith('.'):
                continue
            prefix = "📁" if item.is_dir() else "📄"
            print(f"    {prefix} {item.name}")

    def show_code_capabilities(self):
        """Show code analysis and development capabilities"""
        self.print_header("Code Development Capabilities")

        capabilities = [
            ("Code Analysis", "Analyze code structure, find functions, classes, imports"),
            ("Debugging", "Help identify and fix bugs in your code"),
            ("Testing", "Write and run tests, analyze test coverage"),
            ("Refactoring", "Improve code structure while maintaining functionality"),
            ("Documentation", "Generate or improve code documentation"),
            ("Multi-language", "Support for Python, JavaScript, TypeScript, Go, Rust, etc."),
            ("Package Management", "Install dependencies using pip, npm, cargo, etc."),
            ("Build Systems", "Run builds, compile code, manage build configs"),
            ("Linting & Formatting", "Run linters, formatters, and fix style issues"),
            ("Version Control", "Git operations: commit, branch, merge, rebase"),
        ]

        for title, description in capabilities:
            print(f"  ✓ {title:20s}: {description}")

    def show_advanced_features(self):
        """Show advanced Claude Code features"""
        self.print_header("Advanced Features")

        features = [
            "Task Planning: Break down complex tasks into manageable steps",
            "Parallel Operations: Run multiple independent operations simultaneously",
            "Web Search: Search the web for current information",
            "Web Fetch: Fetch and analyze web content",
            "Background Jobs: Run long-running commands in the background",
            "Specialized Agents: Use specialized AI agents for specific tasks",
            "MCP Servers: Connect to Model Context Protocol servers",
            "Slash Commands: Custom commands defined in .claude/commands/",
            "Hooks: Execute commands in response to events",
            "Multi-step Workflows: Chain complex operations together",
        ]

        for feature in features:
            print(f"  • {feature}")

    def create_demo_project(self):
        """Create a simple demo project to show capabilities"""
        self.print_header("Creating Demo Project")

        demo_dir = self.cwd / "demo_project"
        demo_dir.mkdir(exist_ok=True)

        # Create a simple Python module
        (demo_dir / "calculator.py").write_text('''"""
Simple calculator module to demonstrate code analysis
"""

def add(a, b):
    """Add two numbers"""
    return a + b

def subtract(a, b):
    """Subtract b from a"""
    return a - b

def multiply(a, b):
    """Multiply two numbers"""
    return a * b

def divide(a, b):
    """Divide a by b"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

if __name__ == "__main__":
    print(f"2 + 3 = {add(2, 3)}")
    print(f"5 - 2 = {subtract(5, 2)}")
    print(f"4 * 3 = {multiply(4, 3)}")
    print(f"10 / 2 = {divide(10, 2)}")
''')

        # Create a test file
        (demo_dir / "test_calculator.py").write_text('''"""
Tests for calculator module
"""
import pytest
from calculator import add, subtract, multiply, divide

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5

def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(-2, 3) == -6

def test_divide():
    assert divide(10, 2) == 5
    with pytest.raises(ValueError):
        divide(10, 0)
''')

        # Create package.json for Node demo
        (demo_dir / "package.json").write_text('''{
  "name": "demo-project",
  "version": "1.0.0",
  "description": "Demo project to explore Claude Code capabilities",
  "main": "index.js",
  "scripts": {
    "test": "echo \\"Running tests...\\"",
    "start": "node index.js"
  },
  "keywords": ["demo", "claude"],
  "author": "Claude",
  "license": "MIT"
}
''')

        # Create README
        (demo_dir / "README.md").write_text('''# Demo Project

This is a demonstration project created by Claude Code Environment Explorer.

## Contents

- `calculator.py` - Simple calculator module
- `test_calculator.py` - Unit tests for calculator
- `package.json` - Node.js project configuration

## Usage

Run the calculator:
```bash
python calculator.py
```

Run tests (requires pytest):
```bash
pytest test_calculator.py
```
''')

        print(f"  ✓ Created demo project in: {demo_dir}")
        print(f"  ✓ Files created:")
        for file in demo_dir.iterdir():
            print(f"    • {file.name}")

    def show_tips(self):
        """Show helpful tips for using Claude Code"""
        self.print_header("Tips for Using Claude Code")

        tips = [
            "Ask Claude to analyze your codebase structure",
            "Request code reviews and improvement suggestions",
            "Have Claude write tests for your code",
            "Ask for debugging help by showing error messages",
            "Request refactoring for better code organization",
            "Use Claude to understand unfamiliar code",
            "Ask Claude to add features or fix bugs",
            "Request documentation generation",
            "Have Claude help with git operations",
            "Ask Claude to search for specific code patterns",
            "Request performance optimization suggestions",
            "Use Claude to convert code between languages",
        ]

        for i, tip in enumerate(tips, 1):
            print(f"  {i:2d}. {tip}")

    def run_interactive(self):
        """Run interactive menu"""
        while True:
            print("\n" + "="*60)
            print("  Claude Code Environment Explorer")
            print("="*60)
            print("\n  What would you like to explore?")
            print()
            print("  1. System Information")
            print("  2. Installed Development Tools")
            print("  3. Git Capabilities")
            print("  4. File Operation Capabilities")
            print("  5. Code Development Capabilities")
            print("  6. Advanced Features")
            print("  7. Create Demo Project")
            print("  8. Usage Tips")
            print("  9. Show Everything")
            print("  0. Exit")
            print()

            try:
                choice = input("  Enter your choice (0-9): ").strip()

                if choice == "1":
                    self.show_system_info()
                elif choice == "2":
                    self.show_installed_tools()
                elif choice == "3":
                    self.show_git_capabilities()
                elif choice == "4":
                    self.show_file_operations()
                elif choice == "5":
                    self.show_code_capabilities()
                elif choice == "6":
                    self.show_advanced_features()
                elif choice == "7":
                    self.create_demo_project()
                elif choice == "8":
                    self.show_tips()
                elif choice == "9":
                    self.show_system_info()
                    self.show_installed_tools()
                    self.show_git_capabilities()
                    self.show_file_operations()
                    self.show_code_capabilities()
                    self.show_advanced_features()
                    self.show_tips()
                elif choice == "0":
                    print("\n  Goodbye! Happy coding with Claude!\n")
                    break
                else:
                    print("\n  Invalid choice. Please try again.")

                input("\n  Press Enter to continue...")

            except KeyboardInterrupt:
                print("\n\n  Goodbye! Happy coding with Claude!\n")
                break
            except EOFError:
                break

    def run_all(self):
        """Run all demonstrations non-interactively"""
        self.show_system_info()
        self.show_installed_tools()
        self.show_git_capabilities()
        self.show_file_operations()
        self.show_code_capabilities()
        self.show_advanced_features()
        self.show_tips()


if __name__ == "__main__":
    explorer = ClaudeEnvironmentExplorer()

    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        explorer.run_all()
    elif len(sys.argv) > 1 and sys.argv[1] == "--demo":
        explorer.create_demo_project()
    else:
        explorer.run_interactive()
