import google.generativeai as genai

# These are the tool definitions we pass to Gemini
# Gemini reads these and decides which one to call based on user input

github_tools = [
    {
        "name": "get_my_repos",
        "description": "Get a list of the authenticated user's GitHub repositories",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_repo_issues",
        "description": "Get issues for a specific GitHub repository",
        "parameters": {
            "type": "object",
            "properties": {
                "repo_name": {
                    "type": "string",
                    "description": "The name of the repository"
                },
                "state": {
                    "type": "string",
                    "description": "State of issues: open, closed, or all. Default is open"
                }
            },
            "required": ["repo_name"]
        }
    },
    {
        "name": "get_pull_requests",
        "description": "Get pull requests for a specific GitHub repository",
        "parameters": {
            "type": "object",
            "properties": {
                "repo_name": {
                    "type": "string",
                    "description": "The name of the repository"
                },
                "state": {
                    "type": "string",
                    "description": "State of PRs: open, closed, or all. Default is open"
                }
            },
            "required": ["repo_name"]
        }
    },
    {
        "name": "get_repo_summary",
        "description": "Get detailed summary and info about a specific GitHub repository",
        "parameters": {
            "type": "object",
            "properties": {
                "repo_name": {
                    "type": "string",
                    "description": "The name of the repository"
                }
            },
            "required": ["repo_name"]
        }
    },
    {
        "name": "get_user_profile",
        "description": "Get the authenticated GitHub user's profile information",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

def get_gemini_tools():
    """Convert our tool definitions into Gemini's expected format"""
    tools = []
    for tool in github_tools:
        tools.append(
            genai.protos.Tool(
                function_declarations=[
                    genai.protos.FunctionDeclaration(
                        name=tool["name"],
                        description=tool["description"],
                        parameters=genai.protos.Schema(
                            type=genai.protos.Type.OBJECT,
                            properties={
                                k: genai.protos.Schema(
                                    type=genai.protos.Type.STRING,
                                    description=v["description"]
                                )
                                for k, v in tool["parameters"]["properties"].items()
                            },
                            required=tool["parameters"].get("required", [])
                        )
                    )
                ]
            )
        )
    return tools