__author__ = 'Marek'


def nparray2tuple(nparray):
    return tuple([tuple(row) for row in nparray])


def are_rect_colliding_with(a, b):
    left, bottom, width, height = b
    right = left + width
    top = bottom + height

    b_x1, b_y1, b_w, b_h = a
    b_x2 = b_x1 + b_w
    b_y2 = b_y1 + b_h

    return (left <= b_x1 <= right and bottom <= b_y1 <= top) or ( # bottom left
            left <= b_x2 <= right and bottom <= b_y1 <= top) or ( # bottom right
            left <= b_x2 <= right and bottom <= b_y2 <= top) or ( # top right
            left <= b_x1 <= right and bottom <= b_y2 <= top)      # top left


def any_rect_interaction(a, b):
    return are_rect_colliding_with(a, b) or are_rect_colliding_with(b, a)