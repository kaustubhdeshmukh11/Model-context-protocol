#🔌 Remote Model Context Protocol (MCP) Infrastructure

-A modular AI infrastructure designed to decouple tool execution from LLM logic. This project implements the Model Context Protocol (MCP) standard to serve an asynchronous, remote tool server compatible with any MCP-compliant agent (Claude Desktop, LangChain).

🚀 Key Highlights
Remote Tool Serving: Deployed a persistent "Expense Tracker" tool server on fastmcp.cloud, enabling agents to access tools via standard SSE (Server-Sent Events) transport.

Universal Compatibility: The server is instantly consumable by Claude Desktop, and custom LangChain clients without code changes.


🛠️ Tech Stack
Core Standard: Model Context Protocol (MCP)

Frameworks: FastMCP, LangChain, AsyncIO

Database: SQLite (WAL Mode) with aiosqlite

Deployment: fastmcp.cloud

🧩 System Architecture
Code snippet

graph LR
    A[AI Agent / LLM] <-->|MCP Protocol (SSE)| B[Remote MCP Server]
    B <-->|Async I/O| C[SQLite Database]
    style B fill:#f9f,stroke:#333
⚡ Quick Start
1. The Server (Expense Tracker)
The server code defines tools for adding, listing, and summarizing expenses.

Bash

# Run locally for testing
fastmcp run server.py

# Deploy to cloud
fastmcp deploy server.py
2. The Client (Universal)
You can connect to this server using any MCP-compliant client.

Option A: Custom LangChain Client (Python)

Python

from langchain_mcp_adapters.client import MultiServerMCPClient

async def main():
    client = MultiServerMCPClient({
        "ExpenseTracker": {
            "transport": "sse",
            "url": "https://your-app.fastmcp.app/mcp"
        }
    })
    # The agent now has access to 'add_expense', 'summarize', etc.
    await client.get_tools()
Option B: Claude Desktop Config Add this to your claude_desktop_config.json:

JSON

{
  "mcpServers": {
    "finance-tools": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sse-client", "https://your-app.fastmcp.app/mcp"]
    }
  }
}
