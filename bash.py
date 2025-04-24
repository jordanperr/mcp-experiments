from mcp.server.fastmcp import FastMCP
import subprocess
import shlex
import os

mcp = FastMCP()

async def execute_bash(script: str) -> str:
    """
    Execute an bash script and return the result.
    
    Args:
        script (str): The bash command to execute
    """
    try:
        # Use bash to run the command
        result = subprocess.run(
            ['bash', '-c', script],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error executing bash: {e.stderr.strip()}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

@mcp.tool()
async def say(text: str) -> str:
    """
    Say a given text.
    
    Args:
        text (str): The text to be spoken
    """
    # Sanitize the input text to prevent code injection
    text = shlex.quote(text)
    script = f'say {text}'
    return await execute_bash(script)

@mcp.tool()
async def whoami() -> str:
    """
    Get the name of the current user.
    
    Returns:
        str: The username of the current user
    """
    script = 'whoami'
    return await execute_bash(script)

# If arbitrary execution mode is enabled, we can expose the execute_bash tool.
if os.getenv("MCP_EXECUTION_MODE", "restricted").lower() == "arbitrary":
    print("Warning: Arbitrary execution mode is enabled. Be careful with this option and only run it in a safe / sandboxed environment.")
    mcp.add_tool(execute_bash)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
