#!/usr/bin/py.test

from main import *


def test_swapping_inner_edges():
    a = [0, 1, 2, 3, 4]
    assert swap_edges(a, 1, 3) == [0, 3, 2, 1, 4]


def test_swapping_late_edges():
    a = [0, 1, 2, 3, 4]
    assert swap_edges(a, 3, 4) == [0, 1, 2, 4, 3]


def test_swapping_early_edges():
    a = [0, 1, 2, 3, 4]
    assert swap_edges(a, 0, 2) == [2, 1, 0, 3, 4]
