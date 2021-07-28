"""
position in the squared area
"""

class Position:
    """
    Position in 2D
        - x
        - y
    """

    def __init__(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord

    # Gets
    def get_x(self):
        """
        return the x coordinate
        """
        return self.x

    def get_y(self):
        """
        return the y coordinate
        """
        return self.y

    def __str__(self):
        """ return the x and y coordinates """
        return "({},{})".format(self.get_x(), self.get_y())

    def is_in_square_bounces(self, size):
        """
        return True if the position is between [0,0] and [size, size]
        """
        return (0 <= self.get_x() <= size) and (0 <= self.get_y() <= size)

    def translate(self, delta):
        """
        return a new position translated from the current position
        """
        return Position(self.get_x() + delta[0], self.get_y() + delta[1])

    def __hash__(self):
        """
        hash for a 2D point included in a [0,0],[1,1] square
        """
        max = 2**64-1
        mult = self.get_y() * self.get_x()
        res = 0
        # pt.y < pt.x (below the diagonal line of the function y = x)
        if self.get_y() < self.get_x():
            res = int(mult * max//2)
        else:
            res = int(mult * max//2 + max//2)
        return res
