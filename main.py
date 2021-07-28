#!/usr/bin/env python3
"""
    Algorithmic projet : Count close enough points as graphes
For each file with a given distance and a list of points, this program finds the
points close enough according to the given distance and group them as graphes.
At the end, it returns the number of points in each graph in an descendant order
as lists.

Hypothesis : points' coordinates range from 0 to 1
"""
from sys import argv
from math import sqrt
from collections import defaultdict

from geo.point import Point

from geo.square import Square
from geo.position import Position

AREA_X_MAX = 1.0
AREA_Y_MAX = AREA_X_MAX

DISTANCE = None
NUMBER_OF_COLUMNS = None
NUMBER_OF_LINES = None

def load_instance(filename):
    """
    loads .pts file.
    returns distance limit and points.
    """
    with open(filename, "r") as instance_file:
        lines = iter(instance_file)
        distance = float(next(lines))
        points = [Point([float(f) for f in l.split(",")]) for l in lines]
    return distance, points

def get_square_position_from_point(point):
    """
    return position of the square where the point is located in
    """
    global DISTANCE
    if point.coordinates[0] == AREA_X_MAX:
        x_square = NUMBER_OF_COLUMNS - 1
    else:
        x_square = int(point.coordinates[0]//(DISTANCE/sqrt(2)))
    if point.coordinates[1] == AREA_Y_MAX:
        y_square = NUMBER_OF_LINES - 1
    else:
        y_square = int(point.coordinates[1]//(DISTANCE/sqrt(2)))
    return Position(x_square, y_square)

def get_square_id_from_position(position):
    """
    Returns the id associated to the position
    the id can be from 0 to (number of columns)*(number of rows)
    """
    return (position.get_y()*NUMBER_OF_COLUMNS) + position.get_x()

def get_square_id_from_point(point):
    """ Returns the id of the square which contains the point """
    if point.coordinates[0] == AREA_X_MAX:
        x_square = NUMBER_OF_COLUMNS - 1
    else:
        x_square = int(NUMBER_OF_COLUMNS*point.coordinates[0])
        if point.coordinates[1] == AREA_Y_MAX:
            y_square = NUMBER_OF_LINES - 1
        else:
            y_square = int(NUMBER_OF_LINES*point.coordinates[1])
    return (y_square*NUMBER_OF_COLUMNS + x_square)

def class_points(points):
    """
    Creates a dict containing all points, sorted by the squares they belong to.
    """
    directory = defaultdict(None)
    for point in points:
        square_position = get_square_position_from_point(point)
        square_id = get_square_id_from_position(square_position)
        if square_id in directory.keys():
            directory[square_id].add_point(point)
        else:
            new_square = Square(square_position)
            new_square.add_point(point)
            directory[square_id] = new_square
    return directory


def can_2_squares_be_fused(square_base, square_tested):
    """
    (brute-force algorithm)
    try to find point close enough in 2 between 2 squares
    returns :
        - bool : true if it exists at least one point in square_base close enough
                to a point in square_tested
    """
    global DISTANCE
    for point_base in square_base.get_points():
        for point_tested in square_tested.get_points():
            if point_base.distance_to(point_tested) <= DISTANCE:
                return True
    return False

def process(points):
    """
    return the list of the number of points of each connected components
    """
    # Initialisation of the global parameters
    global NUMBER_OF_COLUMNS
    global NUMBER_OF_LINES
    NUMBER_OF_COLUMNS = int(sqrt(2)*AREA_X_MAX/DISTANCE)+1
    NUMBER_OF_LINES = int(sqrt(2)*AREA_Y_MAX/DISTANCE)+1

    # Classifying the points in squares
    sqr_dict = class_points(points)

    # Going through all squares by counting their points
    nb_of_pts = list()
    nb_of_pts_index = 0

    while (sqr_dict):
        keys = list(sqr_dict.keys())
        current_square = sqr_dict.pop(keys.pop())
        nb_of_pts.append(current_square.get_occupancy())

        tmp_dict = sqr_dict.copy()
        new_squares_to_explore = [current_square]
        while(new_squares_to_explore):
            cur_explored_sqr = new_squares_to_explore.pop()
            pos_neighs = cur_explored_sqr.get_neighbor(NUMBER_OF_COLUMNS-1)
            for neigh_pos in pos_neighs:
                if get_square_id_from_position(neigh_pos) in tmp_dict.keys():
                    neigh_sqr = tmp_dict[get_square_id_from_position(neigh_pos)]
                    if can_2_squares_be_fused(cur_explored_sqr, neigh_sqr):
                        new_squares_to_explore.append(neigh_sqr)
                        nb_of_pts[nb_of_pts_index] += neigh_sqr.get_occupancy()
                        tmp_dict.pop(get_square_id_from_position(neigh_sqr.get_position()))
        sqr_dict = tmp_dict
        nb_of_pts_index += 1
    return nb_of_pts


def print_components_sizes(distance, points):
    """
    display the sorted size of each componant
    """
    global DISTANCE
    DISTANCE = float(distance)
    number_of_points = process(points)
    points = sorted(number_of_points, reverse=True)
    print(points)

def main():
    """
    loads the instances passed as parameters and display the sizes
    """
    for instance in argv[1:]:
        distance, points = load_instance(instance)
        print_components_sizes(distance, points)

"""
Tools for visualizing the duration of each function:

(For CentOs distribution)
Required :
$sudo yum install kdesdk valgrind graphviz
$pip install pyprof2calltree

Commands :
$python3 -m cProfile -o log.prof ./main.py exemple_1.pts
$pyprof2calltree -i log.prof -k
"""

'''
Input as argument of the Python scripts files' name formatted as examples files
For instance:
$ ./main.py example_1.pts example_2.pts
'''
if __name__ == "__main__":
    if len(argv) < 2:
        print("Command : ./main.py points_file1.pts points_file2.pts ...")
    else:
        main()
