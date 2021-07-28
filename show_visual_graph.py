#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Example to visualize the example files
"""
from sys import argv

from geo.tycat import tycat
from geo.segment import Segment

from main_bruteforce import load_instance
from main_bruteforce import print_components_sizes, are_close

def main():
    """
    Use of tycat to display the sub graphes
    """
    for instance in argv[1:]:
        distance, points = load_instance(instance)
        subgraphes = print_components_sizes(distance, points, True)
        segments = []
        for subgraph in subgraphes:
            for point in subgraph:
                for other_point in subgraph:
                    if point is not other_point and are_close(point, other_point, distance):
                        segments.append(Segment([point, other_point]))
        tycat(points, segments)

if __name__ == "__main__":
    main()
