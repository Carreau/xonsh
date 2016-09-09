# -*- coding: utf-8 -*-
"""Tests the xonsh history."""
# pylint: disable=protected-access
import os

from xonsh.lazyjson import LazyJSON
from xonsh.history import History

import pytest


@pytest.yield_fixture
def hist():
    h = History(filename='xonsh-HISTORY-TEST.json', here='yup', sessionid='SESSIONID', gc=False)
    yield h
    os.remove(h.filename)


def test_hist_init(hist):
    """Test initialization of the shell history."""
    with LazyJSON(hist.filename) as lj:
        obs = lj['here']
    assert 'yup' == obs


def test_hist_append(hist, xonsh_builtins):
    """Verify appending to the history works."""
    xonsh_builtins.__xonsh_env__['HISTCONTROL'] = set()
    hf = hist.append({'joco': 'still alive'})
    assert hf is None
    assert 'still alive' == hist.buffer[0]['joco']


def test_hist_flush(hist, xonsh_builtins):
    """Verify explicit flushing of the history works."""
    hf = hist.flush()
    assert hf is None
    xonsh_builtins.__xonsh_env__['HISTCONTROL'] = set()
    hist.append({'joco': 'still alive'})
    hf = hist.flush()
    assert hf is not None
    while hf.is_alive():
        pass
    with LazyJSON(hist.filename) as lj:
        obs = lj['cmds'][0]['joco']
    assert 'still alive' == obs


def test_cmd_field(hist, xonsh_builtins):
    # in-memory
    xonsh_builtins.__xonsh_env__['HISTCONTROL'] = set()
    hf = hist.append({'rtn': 1})
    assert hf is None
    assert 1 == hist.rtns[0]
    assert 1 == hist.rtns[-1]
    assert None == hist.outs[-1]
    # slice
    assert [1] == hist.rtns[:]
    # on disk
    hf = hist.flush()
    assert hf is not None
    assert 1 == hist.rtns[0]
    assert 1 == hist.rtns[-1]
    assert None == hist.outs[-1]


CMDS = ['ls', 'cat hello kitty', 'abc', 'def', 'touch me', 'grep from me']

