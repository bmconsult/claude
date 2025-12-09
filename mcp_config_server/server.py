#!/usr/bin/env python3
"""
MCP Config Server - Persistent configuration storage for Claude Code sessions.

This server runs on YOUR machine and provides persistent config/secrets
that survive Claude Code session resets.

Usage:
    pip install "mcp[cli]"
    python server.py

Then configure Claude Code to connect to this server.
"""

import json
import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Initialize server
mcp = FastMCP(name="config-server")

# Config file location - on YOUR machine, so it persists
CONFIG_DIR = Path.home() / ".claude_config"
CONFIG_FILE = CONFIG_DIR / "config.json"


def ensure_config_dir():
    """Create config directory if it doesn't exist."""
    CONFIG_DIR.mkdir(exist_ok=True)
    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text("{}")


def load_config() -> dict:
    """Load config from persistent storage."""
    ensure_config_dir()
    try:
        return json.loads(CONFIG_FILE.read_text())
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_config(config: dict):
    """Save config to persistent storage."""
    ensure_config_dir()
    CONFIG_FILE.write_text(json.dumps(config, indent=2))


@mcp.tool()
def get_config(key: str) -> str:
    """
    Get a configuration value by key.

    Args:
        key: The config key to retrieve (e.g., 'ANTHROPIC_API_KEY')

    Returns:
        The config value, or empty string if not found.
    """
    config = load_config()
    return config.get(key, "")


@mcp.tool()
def set_config(key: str, value: str) -> str:
    """
    Set a configuration value.

    Args:
        key: The config key to set (e.g., 'ANTHROPIC_API_KEY')
        value: The value to store

    Returns:
        Confirmation message.
    """
    config = load_config()
    config[key] = value
    save_config(config)
    return f"Config '{key}' saved successfully."


@mcp.tool()
def list_config_keys() -> str:
    """
    List all available config keys (not values, for security).

    Returns:
        Comma-separated list of config keys.
    """
    config = load_config()
    if not config:
        return "No config keys stored."
    return ", ".join(config.keys())


@mcp.tool()
def delete_config(key: str) -> str:
    """
    Delete a configuration value.

    Args:
        key: The config key to delete

    Returns:
        Confirmation message.
    """
    config = load_config()
    if key in config:
        del config[key]
        save_config(config)
        return f"Config '{key}' deleted."
    return f"Config '{key}' not found."


@mcp.tool()
def get_env_file() -> str:
    """
    Get the full .env file content for Claude Code session setup.

    Returns:
        Content suitable for writing to .env file.
    """
    config = load_config()
    lines = []
    for key, value in config.items():
        if key.endswith("_API_KEY") or key.endswith("_KEY") or key.endswith("_TOKEN"):
            lines.append(f"{key}={value}")
    return "\n".join(lines) if lines else "No API keys configured."


if __name__ == "__main__":
    print(f"Config stored at: {CONFIG_FILE}")
    print("Starting MCP Config Server...")
    mcp.run()
