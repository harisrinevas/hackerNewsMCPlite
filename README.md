# 🔶 HackerNews MCP Server

A minimal [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that exposes the public [HackerNews API](https://github.com/HackerNews/API) as tools for AI assistants like Claude.

---

## Features

| Tool | Description |
|------|-------------|
| `HN_get_top10_stories` | Fetch the current list of top stories on HackerNews |
| `HN_find_item_details` | Retrieve full details of any HackerNews item by ID |
| `HN_lastest_item` | Get the most recently submitted item on HackerNews |

---

## Requirements

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/) for dependency management

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/harisrinevas/hackerNewsMCPlite.git
cd hn-mcp-server
```

**2. Create a virtual environment and install dependencies**

```bash
uv sync
```

---

## Running the Server

```bash
uv run server.py
```

The server communicates over **stdio** by default, as expected by MCP clients.

---

## Connecting to Claude Desktop

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "hackernews": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/hn-mcp-server",
        "run",
        "server.py"
      ]
    }
  }
}
```

> **Config file location:**
> - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
> - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Restart Claude Desktop — the HackerNews tools will appear automatically.

---

## Tools Reference

### `HN_get_top10_stories`

Returns the top 10 story IDs and their details from the HackerNews front page.

**No input required.**

**Example response:**
```json
[
  12345, 12346, ...
]
```

---

### `HN_find_item_details`

Fetches the full details of a HackerNews item (story, comment, job, poll, etc.) by its ID.

**Input:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `item_id` | `integer` | ✅ | The HackerNews item ID |

**Example response:**
```json
{
  "id": 12345,
  "type": "story",
  "title": "An interesting article",
  "by": "author",
  "score": 256,
  "url": "https://example.com",
  "time": 1711234567,
  "descendants": 43
}
```

---

### `HN_lastest_item`

Returns the most recently submitted item on HackerNews. Useful for monitoring live activity.

**No input required.**

**Example response:**
```json
99999
```

---

## Project Structure

```
src/
├── main.py            # API wrapper on hackernews APIs
├── server.py          # MCP server entry point and tool definitions
├── pyproject.toml     # Project metadata and dependencies (uv)
├── uv.lock            # Locked dependency versions
├── .python-version    # Pinned Python version
├── .gitignore
└── README.md
```

---

## HackerNews API

This server is built on top of the official public HackerNews Firebase API:

- **Base URL:** `https://hacker-news.firebaseio.com/v0/`
- **Docs:** [github.com/HackerNews/API](https://github.com/HackerNews/API)
- No authentication required — completely free and open.

---

## Development

Open the project in VS Code:

```bash
code .
```

Run the server in development/inspector mode using the MCP CLI:

```bash
uv run mcp dev server.py
```

This launches the [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector) in your browser so you can test tools interactively without a full AI client.

---

## License

MIT