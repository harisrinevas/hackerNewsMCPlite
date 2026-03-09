# 🔶 HackerNews MCP Server

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that exposes the public [HackerNews API](https://github.com/HackerNews/API) as tools for AI assistants like Claude.

---

## Features

| Tool | Description |
|------|-------------|
| `HN_latest_item` | Get the most recently submitted item ID on HackerNews |
| `HN_get_top_stories` | Fetch top story IDs (configurable limit, default 10) |
| `HN_get_new_stories` | Fetch newest story IDs (configurable limit, default 10) |
| `HN_get_best_stories` | Fetch best story IDs (configurable limit, default 10) |
| `HN_get_ask_stories` | Fetch Ask HN story IDs (configurable limit, default 10) |
| `HN_get_show_stories` | Fetch Show HN story IDs (configurable limit, default 10) |
| `HN_get_job_stories` | Fetch job posting IDs (configurable limit, default 10) |
| `HN_find_item_details` | Retrieve full details of any HackerNews item by ID |
| `HN_get_stories_with_details` | Fetch full details for a list of item IDs concurrently |

---

## Requirements

- Python 3.12+
- [`uv`](https://docs.astral.sh/uv/) for dependency management

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/harisrinevas/hackerNewsMCPlite.git
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
        "/absolute/path/to/domain_mcp",
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

### `HN_latest_item`

Returns the ID of the most recently submitted item on HackerNews.

**No input required.**

**Example response:**
```json
43821456
```

---

### `HN_get_top_stories` / `HN_get_new_stories` / `HN_get_best_stories`
### `HN_get_ask_stories` / `HN_get_show_stories` / `HN_get_job_stories`

Returns a list of item IDs from the respective HackerNews category.

**Input:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit` | `integer` | ❌ | `10` | Number of item IDs to return (max 500 for stories, 200 for ask/show/job) |

**Example response:**
```json
[43821456, 43821123, 43820987]
```

---

### `HN_find_item_details`

Fetches full details of a HackerNews item (story, comment, job, poll, etc.) by its ID. Returns `null` for deleted or non-existent items.

**Input:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `item_id` | `integer` | ✅ | The HackerNews item ID |

**Example response:**
```json
{
  "id": 43821456,
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

### `HN_get_stories_with_details`

Fetches full details for multiple item IDs **concurrently** — significantly faster than calling `HN_find_item_details` one at a time. Returns `null` for deleted or non-existent items.

**Input:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `item_ids` | `List[integer]` | ✅ | List of HackerNews item IDs |

**Example response:**
```json
[
  {"id": 43821456, "type": "story", "title": "...", "url": "...", "score": 256},
  {"id": 43821123, "type": "story", "title": "...", "url": "...", "score": 134}
]
```

---

## Project Structure

```
domain_mcp/
├── main.py            # Async HackerNews API client with Pydantic models
├── server.py          # MCP server — tool definitions and lifespan management
├── pyproject.toml     # Project metadata and dependencies (uv)
├── uv.lock            # Locked dependency versions
├── .python-version    # Pinned Python version
├── .gitignore
└── README.md
```

---

## Architecture

- **`main.py`** — pure async API layer using `httpx.AsyncClient`. All functions accept a shared client instance. Errors are caught and raised as descriptive `RuntimeError`s.
- **`server.py`** — FastMCP server with a lifespan context manager that opens one `httpx.AsyncClient` on startup and closes it cleanly on shutdown. Tools access the shared client via `Context`.

---

## HackerNews API

Built on top of the official public HackerNews Firebase API:

- **Base URL:** `https://hacker-news.firebaseio.com/v0/`
- **Docs:** [github.com/HackerNews/API](https://github.com/HackerNews/API)
- No authentication required — completely free and open.

---

## Development

Run the server in inspector mode using the MCP CLI:

```bash
uv run mcp dev server.py
```

This launches the [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector) in your browser so you can test tools interactively without a full AI client.

---

## License

MIT
