"""
quadrants are rectangular boxes delimiting a set of items.
they are used in display to compute image sizes.
"""

class Quadrant:
    """
    enclosing rectangles.
    """
    def __init__(self, min_coordinates, max_coordinates):
        self.min_coordinates = list(min_coordinates)
        self.max_coordinates = list(max_coordinates)

    def copy(self):
        """
        return deepcopy of given quadrant.
        """
        return Quadrant(
            list(self.min_coordinates), list(self.max_coordinates))

    @classmethod
    def empty_quadrant(cls, dimension):
        """
        return an empty quadrant in space of given dimension
        """
        min_coordinates = []
        max_coordinates = []
        for _ in range(dimension):
            min_coordinates.append(float('+inf'))
            max_coordinates.append(float('-inf'))
        return cls(min_coordinates, max_coordinates)

    def add_point(self, added_point):
        """
        register a point inside the quadrant.
        update limits if needed.
        """
        for i, added_coordinate in enumerate(added_point.coordinates):
            if added_coordinate < self.min_coordinates[i]:
                self.min_coordinates[i] = added_coordinate
            if added_coordinate > self.max_coordinates[i]:
                self.max_coordinates[i] = added_coordinate

    def update(self, other):
        """
        expands self quadrant by taking constraints from other quadrant into account.
        the new one will have the minimal size needed to contain both initial ones.
        """
        assert len(self.min_coordinates) == len(other.min_coordinates), \
            'merge in different spaces'
        for i, coordinate in enumerate(other.min_coordinates):
            if self.min_coordinates[i] > coordinate:
                self.min_coordinates[i] = coordinate
        for i, coordinate in enumerate(other.max_coordinates):
            if self.max_coordinates[i] < coordinate:
                self.max_coordinates[i] = coordinate

    def limits(self, index):
        """
        returns array of limits for a given coordinate index
        """
        return (self.min_coordinates[index], self.max_coordinates[index])

    def inflate(self, distance):
        """
        get bigger quadrant containing original one + any point outside
        original at distance less than given
        """
        self.min_coordinates = [c - distance for c in self.min_coordinates]
        self.max_coordinates = [c + distance for c in self.max_coordinates]

    def get_arrays(self):
        """
        returns arrays of limits
        """
        return (self.min_coordinates, self.max_coordinates)

    def divide(self):
        """
        returns 4 sub quadrants of a 2D quadrant
        """
        tmin = [self.min_coordinates[0], self.min_coordinates[1]]
        tmax = [self.max_coordinates[0]/2, self.max_coordinates[1]/2]
        top_left_quadrant = Quadrant(tmin, tmax)

        tmin = [self.max_coordinates[0]/2, self.min_coordinates[1]]
        tmax = [self.max_coordinates[0], self.max_coordinates[1]/2]
        top_right_quadrant = Quadrant(tmin, tmax)

        tmin = [self.min_coordinates[0], self.max_coordinates[1]/2]
        tmax = [self.max_coordinates[0]/2, self.max_coordinates[1]]
        bot_left_quadrant = Quadrant(tmin, tmax)

        tmin = [self.max_coordinates[0]/2, self.max_coordinates[1]/2]
        tmax = [self.max_coordinates[0], self.max_coordinates[1]]
        bot_right_quadrant = Quadrant(tmin, tmax)

        return top_left_quadrant, top_right_quadrant, bot_left_quadrant, bot_right_quadrant

    def contains(self, point):
        """
        verify the point is inside the quadrant
        """
        for i in range(len(self.min_coordinates)):
            if not self.min_coordinates[i] <= point.coordinates[i] <= self.max_coordinates[i]:
                return False
        return True

    def contains_potentially(self, point, threshold):
        """
        verify the point is inside the quadrant
        """
        for i in range(len(self.min_coordinates)):
            if not self.min_coordinates[i] - threshold <= point.coordinates[i] <= self.max_coordinates[i] + threshold:
                return False
        return True
