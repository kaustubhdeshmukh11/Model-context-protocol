### Architecture Overview

This project uses a split-architecture where the heavy lifting happens on a managed cloud server, while the client runs locally on your machine.

* **Local Client:** Your interface ( local llm ) which acts as the frontend.
* **Secure Bridge:** The client connects to the cloud via a secure **HTTPS/SSE (Server-Sent Events)** stream. This allows real-time communication without complex network configuration.
* **Remote Server:** The MCP logic is hosted on **FastMCP Cloud**, managing the database and processing requests.

**Connection Endpoint:**
`https://kaustubh-mcp.fastmcp.app/mcp`
