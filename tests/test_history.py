# -*- coding: utf-8 -*-
"""Tests the xonsh history."""
# pylint: disable=protected-access
import pytest


@pytest.yield_fixture
def hist():
    yield 1


CMDS = ['ls', 'cat hello kitty', 'abc', 'def', 'touch me', 'grep from me']

@pytest.mark.parametrize('inp', [ (1,)])
def test_show_cmd_numerate(inp, hist, xonsh_builtins, capsys):
    """Verify that CLI history commands work."""
    pass

