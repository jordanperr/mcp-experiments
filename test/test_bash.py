import pytest
from unittest.mock import patch, MagicMock
import subprocess
import os
from bash import execute_bash, say, whoami

@pytest.fixture
def mock_subprocess_run():
    with patch('subprocess.run') as mock_run:
        yield mock_run

async def test_execute_bash_success(mock_subprocess_run):
    mock_result = MagicMock()
    mock_result.stdout = "command output\n"
    mock_subprocess_run.return_value = mock_result
    
    result = await execute_bash("test command")
    
    mock_subprocess_run.assert_called_once_with(
        ['bash', '-c', "test command"],
        capture_output=True,
        text=True,
        check=True
    )
    assert result == "command output"

async def test_execute_bash_error(mock_subprocess_run):
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(
        1, "cmd", stderr="command failed"
    )
    
    result = await execute_bash("test command")
    assert result == "Error executing bash: command failed"

async def test_say_command(mock_subprocess_run):
    mock_result = MagicMock()
    mock_result.stdout = ""
    mock_subprocess_run.return_value = mock_result
    
    await say("hello world")
    
    mock_subprocess_run.assert_called_once_with(
        ['bash', '-c', "say 'hello world'"],
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
        ['bash', '-c', 'whoami'],
        capture_output=True,
        text=True,
        check=True
    )
    assert result == "testuser"