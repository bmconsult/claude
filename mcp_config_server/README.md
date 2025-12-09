# MCP Config Server

Persistent configuration storage for Claude Code sessions. Runs on **your machine** so config survives Claude Code session resets.

## The Problem

Claude Code's filesystem resets between sessions. API keys stored in `.env` disappear.

## The Solution

This MCP server runs on your machine and stores config persistently at `~/.claude_config/config.json`. Claude Code connects to it and retrieves keys at session start.

```
Your PC (persistent) → MCP Server → Claude Code (ephemeral)
         ↓
   ~/.claude_config/
       config.json
```

## Setup

### 1. Install dependencies

```bash
cd mcp_config_server
pip install -r requirements.txt
```

### 2. Store your API key

Run the server once to set your key:

```bash
python -c "
from server import set_config
set_config('ANTHROPIC_API_KEY', 'your-key-here')
print('Key saved!')
"
```

Or manually create `~/.claude_config/config.json`:

```json
{
  "ANTHROPIC_API_KEY": "sk-ant-..."
}
```

### 3. Run the server

```bash
python server.py
```

The server runs on stdio by default (for Claude Desktop integration) or can use HTTP.

### 4. Configure Claude Code

Add to your Claude Code MCP config (location varies by platform):

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "config-server": {
      "command": "python",
      "args": ["/path/to/mcp_config_server/server.py"]
    }
  }
}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `get_config(key)` | Get a config value |
| `set_config(key, value)` | Store a config value |
| `list_config_keys()` | List stored keys (not values) |
| `delete_config(key)` | Remove a config entry |
| `get_env_file()` | Get all API keys as .env format |

## Session Start Workflow

When Claude Code starts a new session:

1. Call `get_env_file()` to get all API keys
2. Write to `/home/user/claude/.env`
3. Keys available for the session

This happens automatically if configured in CLAUDE.md.

## Security Notes

- Config stored in your home directory, not in Claude's environment
- Keys never committed to git
- Only you have access to `~/.claude_config/`
