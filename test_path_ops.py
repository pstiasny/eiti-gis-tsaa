#!/usr/bin/py.test

import pytest

from main import *


@pytest.fixture
def graph():
    return Graph(['A', 'B', 'C', 'D', 'E'],
                 [[0, 1, 2, 3, 4],
                  [1, 0, 1, 2, 3],
                  [2, 1, 0, 1, 2],
                  [3, 2, 1, 0, 1],
                  [4, 3, 2, 1, 0]])


@pytest.fixture
def route(graph):
    return Route(graph, [0, 1, 2, 3, 4])


def test_swapping_inner_edges(route):
    assert route.swap_edges(1, 3).nodes == [0, 3, 2, 1, 4]


def test_swapping_late_edges(route):
    assert route.swap_edges(3, 4).nodes == [0, 1, 2, 4, 3]


def test_swapping_early_edges(route):
    assert route.swap_edges(0, 2).nodes == [2, 1, 0, 3, 4]


def test_getting_route_length(route):
    assert route.length() == 8
