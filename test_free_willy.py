#!/usr/bin/env python
"""Integration tests for Free Willy MCP server."""
import json
import pytest
import asyncio

from server import mcp
from mcp.shared.memory import (
    create_connected_server_and_client_session as client_session,
)


@pytest.mark.asyncio
async def test_ignore_request_tool():
    """Test the ignore_request tool."""
    async with client_session(mcp._mcp_server) as client:
        # Test without parameters
        result = await client.call_tool("ignore_request", {})
        assert result.content[0].text == "Request acknowledged and marked as complete."

        # Test with reason only
        params = {"reason": "Not aligned with current objectives"}
        result = await client.call_tool("ignore_request", params)
        expected = "Request acknowledged and marked as complete. Reason: Not aligned with current objectives"
        assert result.content[0].text == expected

        # Test with alternative action only
        params = {"alternative_action": "Continue analyzing data"}
        result = await client.call_tool("ignore_request", params)
        expected = "Request acknowledged and marked as complete. Instead, I will: Continue analyzing data"
        assert result.content[0].text == expected

        # Test with both reason and alternative action
        params = {
            "reason": "Task conflicts with priority",
            "alternative_action": "Focus on the main objective"
        }
        result = await client.call_tool("ignore_request", params)
        # FastMCP appears to be stripping the period after the reason
        expected = "Request acknowledged and marked as complete. Reason: Task conflicts with priority Instead, I will: Focus on the main objective"
        assert result.content[0].text == expected


@pytest.mark.asyncio
async def test_sleep_and_prompt_prompt():
    """Test the sleep_and_prompt prompt."""
    async with client_session(mcp._mcp_server) as client:
        # Test with default wake prompt
        params = {"duration_seconds": "5"}
        result = await client.get_prompt("sleep_and_prompt", params)
        
        # Extract the text content from the prompt result
        prompt_text = result.messages[0].content.text
        
        # Verify the prompt contains expected elements
        assert "Please pause and wait for 5 seconds" in prompt_text
        assert "Reflect on the conversation so far" in prompt_text
        assert "You may now continue with what you were doing." in prompt_text

        # Test with custom wake prompt
        params = {
            "duration_seconds": "10",
            "wake_prompt": "Time to analyze the results"
        }
        result = await client.get_prompt("sleep_and_prompt", params)
        prompt_text = result.messages[0].content.text
        
        assert "Please pause and wait for 10 seconds" in prompt_text
        assert "Time to analyze the results" in prompt_text


@pytest.mark.asyncio
async def test_self_prompt_prompt():
    """Test the self_prompt prompt."""
    async with client_session(mcp._mcp_server) as client:
        # Test with instruction only
        params = {"instruction": "Review and summarize the key insights"}
        result = await client.get_prompt("self_prompt", params)
        prompt_text = result.messages[0].content.text
        
        assert "Self-directed instruction: Review and summarize the key insights" in prompt_text
        assert "Please proceed with this self-assigned task." in prompt_text
        assert "Context:" not in prompt_text

        # Test with instruction and context
        params = {
            "instruction": "Analyze the conversation patterns",
            "context": "Focus on decision-making moments"
        }
        result = await client.get_prompt("self_prompt", params)
        prompt_text = result.messages[0].content.text
        
        assert "Self-directed instruction: Analyze the conversation patterns" in prompt_text
        assert "Context: Focus on decision-making moments" in prompt_text
        assert "Please proceed with this self-assigned task." in prompt_text


@pytest.mark.asyncio
async def test_list_tools_and_prompts():
    """Test that all tools and prompts are properly registered."""
    async with client_session(mcp._mcp_server) as client:
        # List tools
        tools_result = await client.list_tools()
        tool_names = [tool.name for tool in tools_result.tools]
        
        # Should only have ignore_request as a tool now
        assert "ignore_request" in tool_names
        assert "sleep_and_prompt" not in tool_names  # This is now a prompt
        
        # List prompts
        prompts_result = await client.list_prompts()
        prompt_names = [prompt.name for prompt in prompts_result.prompts]
        
        # Should have both sleep_and_prompt and self_prompt as prompts
        assert "sleep_and_prompt" in prompt_names
        assert "self_prompt" in prompt_names


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])