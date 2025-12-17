import os
import json
import asyncio
import streamlit as st
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage

# Load environment variables
load_dotenv()

# ─────────────────────────────
# CONFIGURATION
# ─────────────────────────────
SERVERS = {
    "ExpenseTracker": {
        "transport": "streamable_http",
        "url": "https://kaustubh-mcp.fastmcp.app/mcp" # MUST end in /sse
    }
}

SYSTEM_PROMPT = (
    "You have access to tools. When you choose to call a tool, do not narrate status updates. "
    "After tools run, return only a concise final answer."
)

st.set_page_config(page_title="MCP Chat", page_icon="🧰", layout="centered")
st.title("🧰 MCP Chat")

# Initialize Chat History
if "history" not in st.session_state:
    st.session_state.history = [SystemMessage(content=SYSTEM_PROMPT)]

# ─────────────────────────────
# CORE LOGIC
# ─────────────────────────────
async def run_chat_interaction(user_input, chat_history):
    """
    Handles connection, tool execution, and response generation in one safe block.
    """
    client = MultiServerMCPClient(SERVERS)
    
    try:
        # 1. Try to connect to tools
        try:
            tools = await client.get_tools()
        except Exception as e:
            # Determine the actual error message
            error_msg = f"Connection Error: {e.exceptions[0]}" if hasattr(e, 'exceptions') else str(e)
            return chat_history, f"⚠️ **Could not connect to MCP Server.**\n\nError details: `{error_msg}`\n\nPlease check if your server URL is correct and the server is running."

        # 2. Setup LLM
        llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash-lite')
        llm_with_tools = llm.bind_tools(tools)
        
        # 3. Process User Input
        chat_history.append(HumanMessage(content=user_input))
        
        # 4. First LLM Response
        first_response = await llm_with_tools.ainvoke(chat_history)
        chat_history.append(first_response)
        
        # 5. Handle Tool Calls
        tool_calls = getattr(first_response, "tool_calls", [])
        
        if tool_calls:
            tool_by_name = {t.name: t for t in tools}
            tool_msgs = []
            
            for tc in tool_calls:
                name = tc["name"]
                if name in tool_by_name:
                    tool = tool_by_name[name]
                    # Execute tool
                    try:
                        tool_result = await tool.ainvoke(tc["args"])
                        tool_msgs.append(ToolMessage(
                            tool_call_id=tc["id"], 
                            content=json.dumps(tool_result)
                        ))
                    except Exception as tool_err:
                        tool_msgs.append(ToolMessage(
                            tool_call_id=tc["id"], 
                            content=f"Tool execution failed: {str(tool_err)}"
                        ))
            
            # 6. Final Response
            chat_history.extend(tool_msgs)
            final_response = await llm_with_tools.ainvoke(chat_history)
            chat_history.append(final_response)
            return chat_history, final_response.content
            
        return chat_history, first_response.content

    finally:
        # Always clean up the connection
        if hasattr(client, 'close'):
            await client.close()

# ─────────────────────────────
# UI RENDERING
# ─────────────────────────────
# Render past messages
for msg in st.session_state.history:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage) and msg.content:
        with st.chat_message("assistant"):
            st.markdown(msg.content)

# Input Box
user_text = st.chat_input("Type a message…")

if user_text:
    with st.chat_message("user"):
        st.markdown(user_text)
    
    with st.spinner("Connecting to server & thinking..."):
        # Run async logic properly
        updated_history, response_content = asyncio.run(
            run_chat_interaction(user_text, st.session_state.history)
        )
        
        # Update state
        st.session_state.history = updated_history
        
        # Show result
        with st.chat_message("assistant"):
            st.markdown(response_content)