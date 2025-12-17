
   

    %% Local Client Block
    subgraph LocalMachine ["💻 Your Local Machine"]
        Client["MCP Client\n(e.g., Claude Desktop, Custom Python Script)"]:::local
    end

    %% Remote Server Block
    subgraph FastMCPCloud ["☁️ FastMCP Cloud Platform"]
        Server["Your Remote MCP Server\n(Expense Tracker Application)"]:::cloud
    end

    %% Connection and URL Annotation
    Client ==>|"🔒 Secure HTTPS / SSE Connection"| Server

    %% URL Note attached to the server block
    URLNote["Server Endpoint URL:\nhttps://kaustubh-mcp.fastmcp.app/mcp"]:::urlNote
    Server -.- URLNote

    %% Final layout adjustments
    linkStyle 0 stroke:#0288d1,stroke-width:3px,fill:none;
