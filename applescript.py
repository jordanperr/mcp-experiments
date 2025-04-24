from mcp.server.fastmcp import FastMCP
import subprocess
import shlex
import os

mcp = FastMCP()

async def execute_applescript(script: str) -> str:
    """
    Execute an AppleScript script and return the result.
    
    Args:
        script (str): The AppleScript command to execute
    """
    try:
        # Use osascript to run the AppleScript command
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error executing AppleScript: {e.stderr.strip()}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

@mcp.tool()
async def say(text: str) -> str:
    """
    Use AppleScript to say a given text.
    
    Args:
        text (str): The text to be spoken
    """
    # Sanitize the input text to prevent code injection
    text = shlex.quote(text)
    script = f'tell application "System Events" to say {text}'
    return await execute_applescript(script)

@mcp.tool()
async def whoami() -> str:
    """
    Get the name of the current user using AppleScript.
    
    Returns:
        str: The username of the current user
    """
    script = 'tell application "System Events" to return name of current user'
    return await execute_applescript(script)

# If arbitrary execution mode is enabled, we can expose the execute_applescript tool.
if os.getenv("MCP_EXECUTION_MODE", "restricted").lower() == "arbitrary":
    print("Warning: Arbitrary execution mode is enabled. Be careful with this option and only run it in a safe / sandboxed environment.")
    mcp.add_tool(execute_applescript)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')