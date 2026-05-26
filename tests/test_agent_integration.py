import os
import pytest


@pytest.mark.concept("TDNS-007")
def test_agent_integration():
    prompt_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "prompts", "main_agent.md"
    )
    assert os.path.exists(prompt_path)
