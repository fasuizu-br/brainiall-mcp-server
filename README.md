# Brainiall Speech AI - MCP Server

MCP server providing AI-powered pronunciation assessment, speech-to-text, and text-to-speech tools via [Brainiall](https://brainiall.com) Speech AI APIs.

<a href="https://glama.ai/mcp/servers/fasuizu-br/brainiall-mcp-server">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/fasuizu-br/brainiall-mcp-server/badge" alt="brainiall-mcp-server MCP server" />
</a>

## Tools

| Tool | Description |
|------|-------------|
| `assess_pronunciation` | Score how accurately a speaker pronounced a given text (0-100), with per-word and phoneme-level feedback |
| `transcribe_speech` | Transcribe speech audio into text with automatic language detection |
| `synthesize_speech` | Convert text to natural-sounding speech audio (MP3) |
| `list_voices` | List all available text-to-speech voices |

## Prerequisites

Get your free API key at **[app.brainiall.com](https://app.brainiall.com)**.

## Installation

### Using pip

```bash
pip install fastmcp httpx
```

### Using Docker

```bash
docker build -t brainiall-mcp .
docker run -e BRAINIALL_API_KEY=your-key -p 8000:8000 brainiall-mcp
```

## Configuration

Set the `BRAINIALL_API_KEY` environment variable:

```bash
export BRAINIALL_API_KEY=your-api-key
```

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "brainiall-speech-ai": {
      "command": "fastmcp",
      "args": ["run", "server.py"],
      "env": {
        "BRAINIALL_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Cursor / VS Code

Add to your MCP settings:

```json
{
  "mcpServers": {
    "brainiall-speech-ai": {
      "command": "fastmcp",
      "args": ["run", "/path/to/server.py"],
      "env": {
        "BRAINIALL_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Streamable HTTP (Docker / Remote)

```bash
docker run -e BRAINIALL_API_KEY=your-key -p 8000:8000 brainiall-mcp
```

Connect your MCP client to `http://localhost:8000/mcp`.

## Running Locally

```bash
# stdio (default for Claude Desktop / Cursor)
BRAINIALL_API_KEY=your-key fastmcp run server.py

# streamable-http
BRAINIALL_API_KEY=your-key fastmcp run server.py --transport streamable-http --port 8000
```

## API Reference

All tools communicate with the Brainiall Speech AI API at `https://api.brainiall.com`. Full API documentation is available at [app.brainiall.com](https://app.brainiall.com).

### assess_pronunciation

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `text` | string | Yes | Reference text the user should have read |
| `audio_base64` | string | Yes | Base64-encoded audio (WAV or MP3) |
| `language` | string | No | Language code, default `en-US` |

### transcribe_speech

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `audio_base64` | string | Yes | Base64-encoded audio (WAV, MP3, WEBM, OGG) |
| `language` | string | No | Language hint for transcription |

### synthesize_speech

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `text` | string | Yes | Text to convert to speech |
| `voice` | string | No | Voice ID, default `alloy` |
| `speed` | float | No | Speed multiplier (0.5-2.0), default `1.0` |

### list_voices

No parameters. Returns available voice options with IDs and supported languages.

## License

MIT

## Links

- [Brainiall](https://brainiall.com) - AI model provider
- [Get API Key](https://app.brainiall.com) - Sign up and get your free API key