"""
FastMCP quickstart example.

cd to the `examples/snippets/clients` directory and run:
    uv run server fastmcp_quickstart stdio
"""

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field


# Create an MCP server
mcp = FastMCP("Demo", host="0.0.0.0", port=3001)


class AddParams(BaseModel):
    a: int = Field(description="The first number to add.")
    b: int = Field(description="The second number to add.")


# Add an addition tool
@mcp.tool()
def add(params: AddParams) -> int:
    """
    Add two numbers
    
    Args:
        params (AddParams): The parameters for the addition.
    
    Returns:
        int: The sum of a and b.

    """
    return params.a + params.b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# Add a prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
