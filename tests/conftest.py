import pytest


@pytest.fixture
def mock_ctx():
    class MockCtx:
        """Mock MCP Context that records emitted log messages for assertions."""

        def __init__(self):
            self.messages: list[tuple[str, str]] = []

        async def info(self, msg):
            self.messages.append(("info", msg))

        async def warn(self, msg):
            self.messages.append(("warn", msg))

        async def error(self, msg):
            self.messages.append(("error", msg))

    return MockCtx()
