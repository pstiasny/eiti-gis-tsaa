#!/usr/bin/python3

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


class NullAnnealingLogger:
    def log_iteration(self, iteration, temperature, length):
        pass


class FileAnnealingLogger:
    def __init__(self, file):
        self.file = file

    def log_iteration(self, iteration, temperature, length):
        self.file.write('{} {} {}\n'.format(iteration, temperature, length))


class AnnealingResult:
    def __init__(self, route, length, iterations):
        self.route = route
        self.length = length
        self.iterations = iterations


def temperatures(t0, a):
    t = t0
    while True:
        yield t
        t *= a
        if t <= 0: t = 0


def annealing_accept_probability(current, candidate, temp):
    if temp > 0:
        return exp((current - candidate) / temp)
    else:
        return 0


def find_route(logger, temps, graph):
    route = graph.make_initial_route()
    cur_route_length = route.length()
    last_improvement = 0

    for n, temp in enumerate(temps):
        route_candidate = route.swap_random_edges()
        route_candidate_length = route_candidate.length()

        accept = False
        if route_candidate_length < cur_route_length:
            # if the new length is shorter, accept unconditionally
            accept = True
            last_improvement = n
        else:
            # if the new route is longer, it can still be accepted according
            # to the simulated annealing method
            accept_probability = annealing_accept_probability(
                cur_route_length, route_candidate_length, temp)
            accept = random() < accept_probability

        if accept:
            route = route_candidate
            cur_route_length = route_candidate_length

        logger.log_iteration(n, temp, cur_route_length)
        if n >= 500000 or n - last_improvement >= 2000:
            return AnnealingResult(route, cur_route_length, n)

    return AnnealingResult(route, cur_route_length, n)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Wyszukiwanie najkrótszego cyklu w problemie komiwojażera')
    parser.add_argument('graphfile', type=str, help='plik CSV z danymi grafu')
    parser.add_argument('-t', dest="starttemp", type=int, default=10000, help='temperatura początkowa')
    parser.add_argument('-d', dest="tempdrop", type=float, default=0.999985, help='współczynnik spadku temperatury')
    parser.add_argument('-s', dest='stats', action='store_true', help='wyświetl tylko skrócone statystyki')
    parser.add_argument('-l', dest="logfile", type=str, help='logowanie do pliku')
    args = parser.parse_args()

    graph = Graph.load(open(args.graphfile))
    result = find_route(
        FileAnnealingLogger(open(args.logfile, 'w')) if args.logfile else NullAnnealingLogger(),
        temperatures(args.starttemp, args.tempdrop),
        graph)

    if args.stats:
        print(args.starttemp, result.length, result.iterations)
    else:
        print(result.route)
        print(result.length)
