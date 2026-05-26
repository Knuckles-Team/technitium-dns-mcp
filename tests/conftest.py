import pytest


@pytest.fixture
def mock_ctx():
    class MockCtx:
        async def info(self, msg):
            pass

        async def warn(self, msg):
            pass

        async def error(self, msg):
            pass

    return MockCtx()
