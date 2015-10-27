#!/usr/bin/python

from itertools import chain, islice
from math import exp, log
from random import randrange, random


def load(file_):
    nodes = file_.readline().strip().split(',')
    incidence = [[float(s.strip() or '0') for s in l.split(',')] for l in file_]
    return nodes, incidence


def make_initial_path(incidence):
    return list(range(len(incidence)))


def print_path(nodes, path):
    print(', '.join([nodes[i] for i in path]))


def path_length(incidence, path):
    # circular shift of the path list by one item left
    shifted = chain(islice(path, 1, None), [path[0]])
    edges = zip(path, shifted)
    edge_lengths = (incidence[i][j] for i, j in edges)
    return sum(edge_lengths)


def swap_edges(path, i, k):
    "Performs a 2-opt swap"
    return path[:i] + list(reversed(path[i:k+1])) + path[k+1:]


def swap_random_edges(path):
    i = randrange(0, len(path))
    j = randrange(0, len(path))
    return swap_edges(path, min(i, j), max(i, j))


def annealing_temp(n):
    return 1 / log(n+2)


def annealing_accept_probability(current, candidate, n):
    return exp((current - candidate) / annealing_temp(n))


if __name__ == '__main__':
    nodes, incidence = load(open('odleglosci.csv'))
    path = make_initial_path(incidence)

    cur_path_length = path_length(incidence, path)

    for n in range(1, 500000):
        path_candidate = swap_random_edges(path)
        path_candidate_length = path_length(incidence, path_candidate)

        accept = False
        if path_candidate_length < cur_path_length:
            # if the new length is shorter, accept unconditionally
            accept = True
        else:
            # if the new path is longer, it can still be accepted according
            # to the simulated annealing method
            accept_probability = annealing_accept_probability(cur_path_length, path_candidate_length, n)
            accept = random() < accept_probability

        if accept:
            path = path_candidate
            cur_path_length = path_candidate_length

    print_path(nodes, path)
    print(cur_path_length)
