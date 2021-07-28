#!/usr/bin/env python3
"""
compute sizes of all connected components.
sort and display.
"""

from sys import argv

from geo.point import Point

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

def are_close(point1, point2, threshold):
    """
    verify if the distance between the first Point and the second Point is
    less or equal to the threshold
    """
    return point1.distance_to(point2) <= threshold

def get_subgraphes(distance, points, subgraphes):
    """ Find the subgraphes where each points is close to the distance
        the points list is dumped
        and the subgraphes list is filled in the process
    """
    while len(points) != 0:
        # Setting a subgraph
        current_subgraph = []
        # Initial point of the subgraph
        initial_point = points[0]
        layer_n0_points = [initial_point]
        points.remove(initial_point)

        # Update the subgraph
        current_subgraph += layer_n0_points
        new_points_added = True

        while new_points_added:
            layer_n1_points = []
            for layer_n0_point in layer_n0_points:
                for layer_n1_point in points:
                    if are_close(layer_n0_point, layer_n1_point, distance):
                        layer_n1_points.append(layer_n1_point)

            # Integrity of the list
            layer_n1_points = set(layer_n1_points)
            # Remove n+1-layer points from the global list
            for point in layer_n1_points:
                points.remove(point)
            # Update : the n+1 layer becomes the n layer
            layer_n0_points = layer_n1_points

            # Save the new points in the current_subgraph
            if len(layer_n0_points) != 0:
                current_subgraph += layer_n0_points
                new_points_added = True
            else:
                new_points_added = False # break

        # All possible points have been added to the subgraphes
        # The rest must go in other subgraph(es)
        subgraphes.append(current_subgraph)

def print_components_sizes(distance, points, return_subgraphes=False):
    """
    display the sorted size of each componant
    """
    # Get the subgraphes of the points
    tmp_points = points.copy()
    subgraphes = []
    get_subgraphes(distance, tmp_points, subgraphes)

    # Sorted list of subgraphes length
    number_of_points_in_subgraphes = []
    for subgraph in subgraphes:
        number_of_points_in_subgraphes.append(len(subgraph))
    number_of_points_in_subgraphes.sort(reverse=True)

    # For visual representation
    if return_subgraphes:
        return subgraphes
    return None

def main():
    """
    loads the instances passed as parameters and display the sizes
    """
    for instance in argv[1:]:
        distance, points = load_instance(instance)
        print_components_sizes(distance, points)

if __name__ == "__main__":
    main()
