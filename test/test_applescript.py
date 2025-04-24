import pytest
from unittest.mock import patch, MagicMock
import subprocess
import os
from applescript import execute_applescript, say, whoami

@pytest.fixture
def mock_subprocess_run():
    with patch('subprocess.run') as mock_run:
        yield mock_run

async def test_execute_applescript_success(mock_subprocess_run):
    mock_result = MagicMock()
    mock_result.stdout = "command output\n"
    mock_subprocess_run.return_value = mock_result
    
    result = await execute_applescript("test script")
    
    mock_subprocess_run.assert_called_once_with(
        ['osascript', '-e', "test script"],
        capture_output=True,
        text=True,
        check=True
    )
    assert result == "command output"

async def test_execute_applescript_error(mock_subprocess_run):
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(
        1, "cmd", stderr="script failed"
    )
    
    result = await execute_applescript("test script")
    assert result == "Error executing AppleScript: script failed"

async def test_say_command(mock_subprocess_run):
    mock_result = MagicMock()
    mock_result.stdout = ""
    mock_subprocess_run.return_value = mock_result
    
    await say("hello world")
    
    mock_subprocess_run.assert_called_once_with(
        ['osascript', '-e', "tell application \"System Events\" to say \'hello world\'"],
        capture_output=True,
        text=True,
        check=True
    )

async def test_whoami_command(mock_subprocess_run):
    mock_result = MagicMock()
    mock_result.stdout = "testuser\n"
    mock_subprocess_run.return_value = mock_result
    
    result = await whoami()
    
    mock_subprocess_run.assert_called_once_with(
        ['osascript', '-e', 'tell application "System Events" to return name of current user'],
        capture_output=True,
        text=True,
        check=True
    )
    assert result == "testuser"