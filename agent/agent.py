import asyncio
import json
import os
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
        command="python",
        args=["-m", "mcp_server.server"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Set up Gemini model with tools
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash",
                tools=get_gemini_tools(),
                system_instruction=SYSTEM_PROMPT
            )

            # Build chat with history
            chat = model.start_chat(history=chat_history)

            # Send user message to Gemini
            response = await asyncio.to_thread(chat.send_message, user_message)

            # Check if Gemini wants to call a tool
            final_response = ""

            for part in response.parts:
                # Gemini is calling a tool
                if hasattr(part, 'function_call') and part.function_call.name:
                    tool_name = part.function_call.name
                    tool_args = dict(part.function_call.args)

                    print(f"\n🔧 Calling MCP tool: {tool_name} with args: {tool_args}")

                    # Call the MCP server tool
                    mcp_result = await session.call_tool(tool_name, tool_args)

                    # Get the text result from MCP
                    tool_result_text = mcp_result.content[0].text

                    # Send tool result back to Gemini for final answer
                    tool_response = await asyncio.to_thread(
                        chat.send_message,
                        genai.protos.Content(
                            parts=[
                                genai.protos.Part(
                                    function_response=genai.protos.FunctionResponse(
                                        name=tool_name,
                                        response={"result": tool_result_text}
                                    )
                                )
                            ]
                        )
                    )

                    final_response = tool_response.text

                # Gemini responded directly without tool
                elif hasattr(part, 'text') and part.text:
                    final_response = part.text

            return final_response if final_response else "Sorry bro, I couldn't process that."


def ask(user_message: str, chat_history: list = []) -> str:
    """Sync wrapper so CLI and Streamlit can call this easily"""
    return asyncio.run(run_agent(user_message, chat_history))