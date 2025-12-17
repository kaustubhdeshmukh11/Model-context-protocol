graph LR
    %% Define styles for the nodes
    classDef local fill:#e1f5fe,stroke:#0288d1,stroke-width:2px,color:#01579b,rx:10,ry:10;
    classDef cloud fill:#fff3e0,stroke:#f57c00,stroke-width:2px,color:#e65100,rx:10,ry:10;
    classDef urlNote fill:#fff,stroke:#f57c00,stroke-width:1px,stroke-dasharray: 5 5,color:#e65100;

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