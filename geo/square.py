"""
square
"""


class Square:
    """
    Square containing points
    Attributs:
        - its position :    (0,0) ---> +x
                              |
                              v
                              +y
        - list of points
        - number of points in it
        - group id for gathering several squares
    """

    def __init__(self, pos):
        self.position = pos
        self.points = list()
        self.occupancy = 0
        self.group_id = None

    # Gets
    def get_position(self):
        """
        give the position of the square
        """
        return self.position

    def get_position(self):
        """
        give the square's position in a board depending of its position
        """
        return self.position

    def get_points(self):
        """ return the list of points """
        return self.points

    def get_occupancy(self):
        """ return the number of points stocked """
        return self.occupancy

    def get_group_id(self):
        """ return its group id """
        return self.group_id

    def add_point(self, point):
        """
        insert the point in the list of points
        and increase the occupancy counter
        """
        self.points.append(point)
        self.occupancy += 1

    def set_group_id(self, ide):
        """ set its group id """
        self.group_id = ide

    def get_neighbor(self, bounce_area):
        """
        return a list of position of the squares close enough to the current
        square according to the hypothenus
        """
        neighbor_positions = list()
        translations = [        (-1, -2),   (0, -2),  (1, -2),
                    (-2, -1),   (-1, -1),   (0, -1),  (1, -1),  (2, -1),
                    (-2, 0),    (-1, 0),              (1, 0),   (2, 0),
                    (-2, 1),    (-1, 1),    (0, 1),   (1, 1),   (2,1),
                                (-1, 2),    (0, 2),   (1, 2)]
        my_position = self.get_position()
        for translation in translations:
            new_position = my_position.translate(translation)
            if new_position.is_in_square_bounces(bounce_area):
                neighbor_positions.append(new_position)
        return neighbor_positions

    def __str__(self):
        """ return the attributs the square """
        res = "Position : {}, ".format(self.position)
        res += "Occupancy : {}, ".format(self.occupancy)
        res += "Group id: {}, ".format(self.group_id)
        res += " Points : \n["
        for point in self.points:
            res += "({})".format(point.__str__())
        res += "]"
        return res
