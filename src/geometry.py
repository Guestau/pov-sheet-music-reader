__author__ = 'Marek'


class Rectangle:
    def __init__(self, x, y, width, height):
        """
        Coordinate system, top left of screen is 0,0, bottom right of screen is screen_with, screen_height (like in css)
        :param x:
        :param y:
        :param width:
        :param height:
        """
        self.height = height
        self.width = width
        self.y = y
        self.x = x

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.width

    @property
    def bottom(self):
        return self.y

    @property
    def top(self):
        return self.y + self.height

    @property
    def bottom_left(self):
        return self.left, self.bottom

    @property
    def top_left(self):
        return self.left, self.top

    @property
    def bottom_right(self):
        return self.right, self.bottom

    @property
    def top_right(self):
        return self.right, self.top

    def to_tuple(self):
        return self.x, self.y, self.width, self.height

    def contains_point(self, point):
        x, y = point
        return self.left <= x <= self.right and self.bottom <= y <= self.top

    def is_inside(self, b):
        return b.contains_point(self.bottom_left) and \
               b.contains_point(self.bottom_right) and \
               b.contains_point(self.top_left) and \
               b.contains_point(self.top_right)

    def is_overlaying(self, b):
        return b.is_inside(self)

    @staticmethod
    def _is_colliding_with(a, b):
        return b.contains_point(a.bottom_left) or \
               b.contains_point(a.bottom_right) or \
               b.contains_point(a.top_left) or \
               b.contains_point(a.top_right)

    def is_colliding_with(self, b):
        return self._is_colliding_with(self, b) or self._is_colliding_with(b, self)

    @staticmethod
    def maximal_overlaying_rectangle(rectangle_list):
        left = min(rectangle_list, key=lambda r: r.left).left
        bottom = min(rectangle_list, key=lambda r: r.bottom).bottom
        right = max(rectangle_list, key=lambda r: r.right).right
        top = max(rectangle_list, key=lambda r: r.top).top

        return Rectangle(left, bottom, right-left, top-bottom)

    def __repr__(self):
        return "<Rectangle x:%s, y:%s, w:%s, h:%s>" % (self.x, self.y, self.width, self.height)


def tuples2rectangles(list_of_tuples):
    """

    :param list_of_tuples: list of tuples(x, y, width, height)
    """
    for item in list_of_tuples:
        yield Rectangle(*item)


def group_rectangles(rectangle_list, condition=None):
    """

    :param rectangle_list:
    :param condition: function (group_item, rectangle) -> True/False, if returns True rectangles are grouped
        default lambda group_item, rectangle: rectangle.is_inside(group_item) or group_item.is_inside(rectangle)
    :return: list groups (list) of rectangles e.g. [[r], [r1, r2]] sorted by area
    """
    if condition is None:
        condition = lambda group_item, rectangle: rectangle.is_inside(group_item) or group_item.is_inside(rectangle)

    grouped_rectangles = []
    for rectangle in rectangle_list:
        in_group = -1
        for group_index, group in enumerate(grouped_rectangles):
            if any(group_item for group_item in group if condition(group_item, rectangle)):
                in_group = group_index
                break
        if in_group >= 0:
            grouped_rectangles[in_group].append(rectangle)
        else:
            grouped_rectangles.append([rectangle])
    return [sorted(group, key=lambda r: r.width*r.height, reverse=True) for group in grouped_rectangles]


def add_overlaying_rectangles(rectangle_group):
    """
    Adds overlaying rectangle to start of group which has more than one rectangle
    :param rectangle_group: [[r], [r1, r2]] similar to group_rectangles return value
    """
    new_rectangle_group = []
    for group in rectangle_group:
        if len(group) > 1:
            overlaying_rectangle = Rectangle.maximal_overlaying_rectangle(group)
            new_rectangle_group.append([overlaying_rectangle] + group)
        else:
            new_rectangle_group.append(group)
    return new_rectangle_group