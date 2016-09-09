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


