#!/bin/bash

rm -f stats

for i in $(seq 0 100 1000) $(seq 2000 1000 10000); do
    echo $i ...
    for j in $(seq 5); do
        pypy3 main.py -s -t $i odleglosci.csv >> stats
    done
done
