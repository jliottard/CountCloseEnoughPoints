#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sys import argv
from math import sqrt

from geo.point import Point
from geo.tycat import tycat
from geo.segment import Segment

from main import load_instance
from main_bruteforce import print_components_sizes, are_close

def main():
    """
    Visual representation of the solution used to sorted the points
    """
    for instance in argv[1:]:
        distance, points = load_instance(instance)
        segments_grid = list()
        square_size = sqrt(distance**2/2)
        col_nb = int(1/square_size)+1
        i = 0
        while(i < 1):
            segments_grid.append(Segment([Point([i,0]),Point([i,1])]))
            segments_grid.append(Segment([Point([0,i]),Point([1,i])]))
            i += square_size
        subgraphes = print_components_sizes(distance, points, True)
        segments = []
        for subgraph in subgraphes:
            for point in subgraph:
                for other_point in subgraph:
                    if point is not other_point and are_close(point, other_point, distance):
                        segments.append(Segment([point, other_point]))
        tycat(points, segments_grid, segments)

'''
To be able to use tycat, use a Terminalogy as the terminal console
'''
if __name__ == "__main__":
    if len(argv) < 2:
        print("Command : ./show_visual_explaination.py points_file1.pts points_file2.pts ...")
    else:
        main()
