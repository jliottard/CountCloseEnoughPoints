#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to make a log file of a benchmark

# 1 FUNCTIONS
how to use it for one function:
$python3 -u ./test_analyse.py | tee fct.log
$gnuplot
>plot "fct.log" with lines

# COMPARE 2 FUNCTIONS

how to use it for one function:
$python3 -u ./test_analyse.py | tee compare.log
$gnuplot
>plot "compare.log" using 1:2 with lines, "compare.log" using 1:3 with lines
"""

from timeit import timeit
from random import random

from geo.point import Point

from main import print_components_sizes as print1
from main_square_id import print_components_sizes as print2

DISTANCE = 0.1
END = 50000
STEP = 100
REPETITIONS = 5

def generate_example(n_points):
    """ Return a list of n Points [0,1]"""
    points = list()
    for _ in range(0, n_points):
        points.append(Point([random(), random()]))
    return points

def test():
    """ Print time performance of the function """
    list_of_points = list()
    for size in range(1, END, STEP):
        list_of_points.append(generate_example(size))
    for points in list_of_points:
        duration_square = timeit(lambda: print1(DISTANCE, points), number=REPETITIONS)
        duration_brute = timeit(lambda: print2(DISTANCE, points), number=REPETITIONS)
        print(len(points), duration_square, duration_brute)

if __name__ == "__main__":
    test()
