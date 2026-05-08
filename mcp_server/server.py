import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types
from mcp_server.github_api import (
    get_my_repos,
    get_repo_issues,
    get_pull_requests,
    get_repo_summary,
    get_user_profile
)

app = Server("github-mcp-server")

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_my_repos",
            description="Get a list of the authenticated user's GitHub repositories",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="get_repo_issues",
            description="Get issues for a specific GitHub repository",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo_name": {
                        "type": "string",
                        "description": "The name of the repository"
                    },
                    "state": {
                        "type": "string",
                        "description": "State of issues: open, closed, or all",
                        "default": "open"
                    }
                },
                "required": ["repo_name"]
            }
        ),
        types.Tool(
            name="get_pull_requests",
            description="Get pull requests for a specific GitHub repository",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo_name": {
                        "type": "string",
                        "description": "The name of the repository"
                    },
                    "state": {
                        "type": "string",
                        "description": "State of PRs: open, closed, or all",
                        "default": "open"
                    }
                },
                "required": ["repo_name"]
            }
        ),
        types.Tool(
            name="get_repo_summary",
            description="Get detailed summary of a specific GitHub repository",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo_name": {
                        "type": "string",
                        "description": "The name of the repository"
                    }
                },
                "required": ["repo_name"]
            }
        ),
        types.Tool(
            name="get_user_profile",
            description="Get the authenticated GitHub user's profile information",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    try:
        if name == "get_my_repos":
            result = await get_my_repos()
        elif name == "get_repo_issues":
            result = await get_repo_issues(
                arguments["repo_name"],
                arguments.get("state", "open")
            )
        elif name == "get_pull_requests":
            result = await get_pull_requests(
                arguments["repo_name"],
                arguments.get("state", "open")
            )
        elif name == "get_repo_summary":
            result = await get_repo_summary(arguments["repo_name"])
        elif name == "get_user_profile":
            result = await get_user_profile()
        else:
            result = {"error": f"Unknown tool: {name}"}

        return [types.TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]

    except Exception as e:
        return [types.TextContent(
            type="text",
            text=json.dumps({"error": str(e)})
        )]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())