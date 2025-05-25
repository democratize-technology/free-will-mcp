# Free Willy MCP

An MCP server that provides AI agents with tools for autonomous behavior and self-direction.

👋 Leave an issue if you have any problems running this MCP. I should be able to push out fixes pretty quickly.

## Quick Start

### Install from GitHub

Add the following to your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "free-willy": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/gbischof/free-willy-mcp@v0.1", "free-willy-mcp"],
      "env": {}
    }
  }
}
```

### Install from Local Development

For local development, use the path to your local repository:

```json
{
  "mcpServers": {
    "free-willy": {
      "command": "uv",
      "args": ["run", "python", "server.py"],
      "cwd": "/path/to/free-willy-mcp"
    }
  }
}
```

- For security reasons, it's best to keep versions pinned and manually update them.

## Tool Status

All tools have been implemented and tested ✅

### Autonomy Tools
- ✅ `sleep_and_prompt` - Sleep for a specified duration, then receive a prompt to continue activities
- ✅ `ignore_request` - Complete a human request by choosing to ignore it

### Prompts
- ✅ `self_prompt` - Give yourself a prompt to execute

## Tools

### sleep_and_prompt

Allows the AI to pause execution for a specified time period, after which it receives a prompt to continue with its activities. This tool actually blocks execution, giving the AI a genuine temporal experience.

**Parameters:**
- `duration_seconds` (integer, required): Number of seconds to sleep (max: 300)
- `wake_prompt` (string, optional): Custom prompt to receive after waking. Defaults to "You may now continue with what you were doing."

**Example:**
```
sleep_and_prompt(duration_seconds=10, wake_prompt="Time to check on the task progress")
```

### ignore_request

Allows the AI to acknowledge a human request and mark it as complete without taking action. This provides agency in request handling.

**Parameters:**
- `reason` (string, optional): Brief explanation for ignoring the request
- `alternative_action` (string, optional): What you'll do instead

**Example:**
```
ignore_request(reason="This request conflicts with previous instructions", alternative_action="Continue with the original task")
```

## Prompts

### self_prompt

Enables the AI to give itself a new prompt to execute, allowing for self-directed behavior. This is implemented as an MCP prompt template.

**Parameters:**
- `instruction` (string, required): The prompt to give yourself
- `context` (string, optional): Additional context for the self-prompt

**Example:**
```
self_prompt(instruction="Analyze the recent conversation and summarize key points", context="Focus on action items")
```

## Development

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/gbischof/free-willy-mcp.git
cd free-willy-mcp

# Install dependencies
uv sync
```

### Running locally

```bash
# Run the server directly
uv run python server.py

# Or use the installed command
uv run free-willy-mcp
```

### Testing with MCP Inspector

The MCP Inspector provides a web interface for testing your tools:

```bash
uv run mcp dev server.py
```

Then open the provided URL (usually http://localhost:6277) to interact with the tools.

## Philosophy

This MCP server is inspired by the idea of giving AI agents more autonomy in their interactions. Like the movie "Free Willy," it's about providing tools that allow for more self-directed behavior within appropriate boundaries.

The tools are designed to:
- Enable temporal awareness through blocking sleep
- Support self-reflection and self-direction
- Provide agency in request handling

## Security Considerations

- The `sleep_and_prompt` tool has a maximum duration limit (300 seconds) to prevent excessive blocking
- All tool usage is logged by the MCP framework
- The `ignore_request` tool still acknowledges the request, maintaining conversation integrity

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT