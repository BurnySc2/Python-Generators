import time
import math
import cmath
from typing import Generator, Tuple, Set
import heapq


def generate_tuple(limit: int) -> Generator[Tuple[int, int, int], None, None]:
    """
    Imagine having a 2 dimensional grid of points, e.g.
    [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), ...]
    but you want to have them sorted by distance towards origin (0, 0)
    [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), ...]

    You can solve this by creating a list with infinite amount of points and sorting them afterwards.
    However, the problem for me was that I just want to loop over this list and eventually break out of the loop. Meaning, I do not know how many points I need, so I created this generator which actually creates the needed numbers around 3 to 4 times faster than using list comprehension with sorting it afterwards.

    :param limit:
    """
    sorted_list = [(0, 0, 0)]
    x_value = 1
    x_value_squared = 1

    def order_next_batch():
        nonlocal sorted_list, x_value, x_value_squared
        for y in range(x_value + 1):
            heapq.heappush(sorted_list, (x_value ** 2 + y ** 2, x_value, y))
        x_value += 1
        x_value_squared = x_value ** 2

    while sorted_list:
        next_value = heapq.heappop(sorted_list)
        # Generate new numbers if current distance value is larger than x_value_squared, e.g. generate (4, 0) before (3, 3) is returned because (4, 0) has squared distance 16 and (3, 3) has squared distance 18
        if x_value_squared < next_value[0]:
            # print(f"Putting back {next_value} because x_value_squared is {x_value_squared}")
            order_next_batch()
            next_value = heapq.heappushpop(sorted_list, next_value)
        dist, x_val, y_val = next_value

        # Exit generator once limit is reached
        if max(abs(x_val), abs(y_val)) > limit:
            return None

        yield next_value
        # Continue for x == 0 and y == 0, only yield one value
        if not x_val:
            order_next_batch()
            continue
        # Yield mirrors
        yield (dist, -x_val, -y_val)
        if y_val != 0:
            yield (dist, x_val, -y_val)
            yield (dist, -x_val, y_val)
        # If they are not same values, e.g. (1, 1), (2, 2), (3, 3)
        if x_val != y_val:
            yield (dist, y_val, x_val)
            yield (dist, -y_val, -x_val)
            if y_val != 0:
                yield (dist, y_val, -x_val)
                yield (dist, -y_val, x_val)
        # Generate new numbers if list is empty
        if not sorted_list:
            order_next_batch()


def generate_line(x0: int, y0: int, x1: int, y1: int) -> Generator[Tuple[int, int], None, None]:
    """ Generates a 2-dimensional line from point1 towards point2. """
    x_diff = abs(x1 - x0)
    y_diff = abs(y1 - y0)

    if y_diff <= x_diff:

        m = (y1 - y0) / abs(x1 - x0)
        new_y = y0
        # Point2 lies mostly to the right of Point1
        if x1 > x0:
            for x in range(x0, x1 + 1):
                yield (x, math.floor(new_y))
                new_y += m

        # Point2 lies mostly to the left of Point1
        else:
            for x in range(x0, x1 - 1, -1):
                yield (x, math.floor(new_y))
                new_y += m
    else:
        m = (x1 - x0) / abs(y1 - y0)
        new_x = x0
        # Point2 lies mostly to the top of Point1
        if y1 > y0:
            for y in range(y0, y1 + 1):
                yield (math.floor(new_x), y)
                new_x += m

        # Point2 lies mostly to the bottom of Point1
        else:
            for y in range(y0, y1 - 1, -1):
                yield (math.floor(new_x), y)
                new_x += m
    return None


