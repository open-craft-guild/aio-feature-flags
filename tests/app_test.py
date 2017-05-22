"""Basic tests suite for aiohttp app."""

from unittest.mock import patch

from feature_api.app import build_application


@patch('aiomysql.sa.create_engine')  # temporarily mock DB connection
async def test_app(test_client, loop):
    """Check availability of the feature flags collection endpoint."""
    app = await build_application()
    client = await test_client(app)
    resp = await client.get('/api/v1/features/')
    assert resp.status == 200
    text = await resp.text()
    assert '{"content": "feature-flags-api"}' == text
