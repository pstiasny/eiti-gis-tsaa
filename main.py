#!/usr/bin/python

from itertools import chain, islice
from math import exp, log
from random import randrange, random


class Graph:
    def __init__(self, node_names, adjacency):
        self.nodes = node_names
        self.adjacency = adjacency

    def make_initial_route(self):
        return Route(self, range(len(self.adjacency)))

    @classmethod
    def load(cls, file_):
        nodes = file_.readline().strip().split(',')
        adjacency = [[float(s.strip() or '0') for s in l.split(',')] for l in file_]
        return cls(nodes, adjacency)


class Route:
    def __init__(self, graph, nodes):
        self.nodes = list(nodes)
        self.graph = graph

    def __str__(self):
        node_names = self.graph.nodes
        return ', '.join([node_names[i] for i in self.nodes])

    def length(self):
        adjacency = self.graph.adjacency

        # circular shift of the route list by one item left
        shifted = chain(islice(self.nodes, 1, None), [self.nodes[0]])
        edges = zip(self.nodes, shifted)
        edge_lengths = (adjacency[i][j] for i, j in edges)
        return sum(edge_lengths)

    def swap_edges(self, i, k):
        "Performs a 2-opt swap"
        new_nodes = self.nodes[:i] + \
                    list(reversed(self.nodes[i:k+1])) + \
                    self.nodes[k+1:]
        return Route(self.graph, new_nodes)

    def swap_random_edges(self):
        i = randrange(0, len(self.nodes))
        j = randrange(0, len(self.nodes))
        return self.swap_edges(min(i, j), max(i, j))


def annealing_temp(n):
    return 1 / log(n+2)


def annealing_accept_probability(current, candidate, n):
    return exp((current - candidate) / annealing_temp(n))


def find_route(graph):
    route = graph.make_initial_route()
    cur_route_length = route.length()

    for n in range(1, 500000):
        route_candidate = route.swap_random_edges()
        route_candidate_length = route_candidate.length()

        accept = False
        if route_candidate_length < cur_route_length:
            # if the new length is shorter, accept unconditionally
            accept = True
        else:
            # if the new route is longer, it can still be accepted according
            # to the simulated annealing method
            accept_probability = annealing_accept_probability(cur_route_length, route_candidate_length, n)
            accept = random() < accept_probability

        if accept:
            route = route_candidate
            cur_route_length = route_candidate_length

    return route


if __name__ == '__main__':
    graph = Graph.load(open('odleglosci.csv'))
    route = find_route(graph)
    print(route)
    print(route.length())
