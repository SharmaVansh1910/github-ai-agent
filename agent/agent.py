import asyncio
import json
import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from agent.tools import get_gemini_tools

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are a helpful GitHub assistant. You help users understand 
their GitHub repositories, issues, pull requests, and profile.
When a user asks something, use the available tools to fetch real data from GitHub
and give clear, helpful, well formatted answers.
Always be concise but informative."""

async def run_agent(user_message: str, chat_history: list = []) -> str:
    """
    Main agent function:
    1. Send user message to Gemini
    2. If Gemini wants to call a tool → call MCP server
    3. Send tool result back to Gemini
    4. Return final response
    """

    server_params = StdioServerParameters(
        command=sys.executable,          
        args=["-m", "mcp_server.server"],
        env={**os.environ},               
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Set up Gemini model with tools
            model = genai.GenerativeModel(
                model_name="gemini-3.5-flash-lite",
                tools=get_gemini_tools(),
                system_instruction=SYSTEM_PROMPT
            )

            # Build chat with history
            chat = model.start_chat(history=chat_history)


            # Send user message to Gemini
            response = await asyncio.to_thread(chat.send_message, user_message)

            final_response = ""

            # Keep handling tool calls until Gemini gives a text response
            while True:
                function_calls = []

                for part in response.parts:
                    if hasattr(part, 'function_call') and part.function_call.name:
                        function_calls.append(part.function_call)

                # If there are no more tool calls, get final text
                if not function_calls:
                    text_parts = []

                    for part in response.parts:
                        if hasattr(part, 'text') and part.text:
                            text_parts.append(part.text)

                    final_response = "\n".join(text_parts)
                    break

                function_response_parts = []

                # Execute every requested MCP tool
                for function_call in function_calls:
                    tool_name = function_call.name
                    tool_args = dict(function_call.args)

                    print(f"\nCalling MCP tool: {tool_name} with args: {tool_args}")

                    mcp_result = await session.call_tool(tool_name, tool_args)

                    tool_result_text = mcp_result.content[0].text

                    function_response_parts.append(
                        genai.protos.Part(
                            function_response=genai.protos.FunctionResponse(
                                name=tool_name,
                                response={"result": tool_result_text}
                            )
                        )
                    )

                # Send tool results back to Gemini
                response = await asyncio.to_thread(
                    chat.send_message,
                    genai.protos.Content(
                        parts=function_response_parts
                    )
                )

            return final_response if final_response else "Sorry bro, I couldn't process that."


def ask(user_message: str, chat_history: list = []) -> str:
    """Sync wrapper so CLI and Streamlit can call this easily"""
    return asyncio.run(run_agent(user_message, chat_history))
