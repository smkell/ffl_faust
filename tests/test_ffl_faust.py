#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ffl_faust` package."""

import pytest
from unittest.mock import Mock, patch

import faust
from ffl_faust import ffl_faust

app = faust.App('example-test-agent-call')

@app.agent()
async def foo(stream):
    async for value in stream:
        await bar.send(value)
        yield value

@app.agent()
async def bar(stream):
    async for value in stream:
        yield value + 'YOLO'

@pytest.fixture()
def test_app():
    app.finalize()
    app.conf.store = 'memory://'
    app.flow_control.resume()
    return app

@pytest.mark.asyncio()
async def test_foo(test_app):
    with patch(__name__ + '.bar') as mocked_bar:
        mocked_bar.send = mock_coro()
        async with foo.test_context() as agent:
            await agent.put('hey')
            mocked_bar.send.assert_called_with('hey')

def mock_coro(return_value=None, **kwargs):
    """Create mock coroutine function."""
    async def wrapped(*args, **kwargs):
         return return_value
    return Mock(wraps=wrapped, **kwargs)

@pytest.mark.asyncio()
async def test_bar(test_app):
    async with bar.test_context() as agent:
        event = await agent.put('hey')
        print(event)
        assert agent.results[event.message.offset] == 'heyYOLO'
