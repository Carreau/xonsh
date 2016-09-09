# -*- coding: utf-8 -*-
"""Tests the xonsh history."""
# pylint: disable=protected-access
import os
import shlex

from xonsh.history import History
from xonsh import history

import pytest


@pytest.yield_fixture
def hist():
    #h = History(filename='xonsh-HISTORY-TEST.json', here='yup', sessionid='SESSIONID', gc=False)
    yield 1
    #os.remove(h.filename)


CMDS = ['ls', 'cat hello kitty', 'abc', 'def', 'touch me', 'grep from me']

@pytest.mark.parametrize('inp, commands, offset', [
    ('', CMDS, (0, 1)),
    ])
def test_show_cmd_numerate(inp, commands, offset, hist, xonsh_builtins, capsys):
    """Verify that CLI history commands work."""
    pass

