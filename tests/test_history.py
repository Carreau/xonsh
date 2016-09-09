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
    h = History(filename='xonsh-HISTORY-TEST.json', here='yup', sessionid='SESSIONID', gc=False)
    yield h
    os.remove(h.filename)


CMDS = ['ls', 'cat hello kitty', 'abc', 'def', 'touch me', 'grep from me']

@pytest.mark.parametrize('inp, commands, offset', [
    ('', CMDS, (0, 1)),
    ('-r', list(reversed(CMDS)), (len(CMDS)- 1, -1)),
    ('0', CMDS[0:1], (0, 1)),
    ('1', CMDS[1:2], (1, 1)),
    ('-2', CMDS[-2:-1], (len(CMDS) -2 , 1)),
    ('1:3', CMDS[1:3], (1, 1)),
    ('1::2', CMDS[1::2], (1, 2)),
    ('-4:-2', CMDS[-4:-2], (len(CMDS) - 4, 1))
    ])
def test_show_cmd_numerate(inp, commands, offset, hist, xonsh_builtins, capsys):
    """Verify that CLI history commands work."""
    base_idx, step = offset
    xonsh_builtins.__xonsh_history__ = hist
    xonsh_builtins.__xonsh_env__['HISTCONTROL'] = set()
    for ts,cmd in enumerate(CMDS):  # populate the shell history
        hist.append({'inp': cmd, 'rtn': 0, 'ts':(ts+1, ts+1.5)})

    exp = ('{}: {}'.format(base_idx + idx * step, cmd)
           for idx, cmd in enumerate(list(commands)))
    exp = '\n'.join(exp)

    history.history_main(['show', '-n'] + shlex.split(inp))
    out, err = capsys.readouterr()
    assert out.rstrip() == exp


