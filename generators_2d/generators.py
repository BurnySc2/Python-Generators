import time
import math
import cmath
import itertools
from typing import Generator, Tuple, Set
import heapq


def generate_2d_offset_points(limit: int) -> Generator[Tuple[int, int, int], None, None]:
    """
    Imagine having a 2 dimensional grid of points, e.g.
    [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), ...]
    but you want to have them sorted by distance towards origin (0, 0)
    [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), ...]

    You can solve this by creating a list with infinite amount of points and sorting them afterwards.
    However, the problem for me was that I just want to loop over this list and eventually break out of the loop. Meaning, I do not know how many points I need, so I created this generator which actually creates the needed numbers around 3 to 4 times faster than using list comprehension with sorting it afterwards.

    Returnvalues:
    (distance_squared: int, x: int, y: int)
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


def generate_grid(
    min_distance: int = 0, max_distance: int = 1, step_size: int = 1
) -> Generator[Tuple[int, int], None, None]:
    """
    Generates a grid of points around (0, 0).

    Over time, this function will generate the same points as "generate_2d_offset_points" function, but faster because it does not do any sorting.

    generate_grid(max_Distance=1) returns a generator with values
    [(0, 0), (-1, 1), (-1, -1), (0, 1), (0, -1), (1, 1), (1, -1), (1, 0), (-1, 0)]

    :param min_distance:
    :param max_distance:
    :param step_size:
    :return:
    """
    if min_distance == 0:
        yield 0, 0
    for dist in range(min_distance, max_distance + 1, step_size):
        if dist == 0:
            continue
        for x in range(-dist, dist + 1, step_size):
            # Top row
            yield x, dist
            # Bottom row
            yield x, -dist
        for y in range(-dist + 1, dist, step_size):
            # Right column
            yield dist, y
            # Left column
            yield -dist, y
    return None


def generate_line(
    x0: int, y0: int, x1: int, y1: int, exclude_start: bool = False, exclude_end: bool = False
) -> Generator[Tuple[int, int], None, None]:
    """
    Generates a 2-dimensional line (list of points) from point1 towards point2.
    This does not use antialiasing, so the number of points will be
    amount = max(abs(x0-x1), abs(y0-y1)) + 1

    Returnvalues:
    (x: int, y: int)
    """
    if x0 == x1 and y0 == y1:
        if not (exclude_start or exclude_end):
            yield (x0, y0)
        return None
    x_diff = abs(x1 - x0)
    y_diff = abs(y1 - y0)

    start_offset = 1 if exclude_start else 0
    end_offset = 1 if exclude_end else 0

    if y_diff <= x_diff:

        m = (y1 - y0) / abs(x1 - x0)
        new_y = y0
        # Point2 lies mostly to the right of Point1
        if x1 > x0:
            for x in range(x0 + start_offset, x1 + 1 - end_offset):
                yield (x, math.floor(new_y))
                new_y += m

        # Point2 lies mostly to the left of Point1
        else:
            for x in range(x0 - start_offset, x1 - 1 + end_offset, -1):
                yield (x, math.floor(new_y))
                new_y += m
    else:
        m = (x1 - x0) / abs(y1 - y0)
        new_x = x0
        # Point2 lies mostly to the top of Point1
        if y1 > y0:
            for y in range(y0 + start_offset, y1 + 1 - end_offset):
                yield (math.floor(new_x), y)
                new_x += m

        # Point2 lies mostly to the bottom of Point1
        else:
            for y in range(y0 - start_offset, y1 - 1 + end_offset, -1):
                yield (math.floor(new_x), y)
                new_x += m
    return None


def generate_circle_points(
    point_radius: float = 1.0, circle_radius: float = 1.0
) -> Generator[Tuple[float, float, float, float], None, None]:
    """
    This function will attempt to pack points as tightly as possible on a circle line, starting with the initial point at coordinates
    (circle_radius, 0)
    and will continue to yield points anti-clockwise until an angle of 2pi is reached

    Returnvalues:
    (amount_of_points: float, current_angle_on_circle: float, x: float, y: float)
    """
    # https://math.stackexchange.com/questions/2092025/equally-spaced-points-on-a-circle
    if point_radius * 2 > circle_radius:
        return None

    amount_of_points_on_circle: int = math.pi / (2 * math.asin(point_radius / (2 * circle_radius)))
    # Remove math.floor to pack points as tightly as possible, but the last point on that circle will have some distance to the first point on the circle
    amount_of_points_on_circle_rounded = math.floor(amount_of_points_on_circle)

    angle_per_point: float = (2 * math.pi) / amount_of_points_on_circle_rounded

    # These 4 lines could replace the 2 lines below it, but the performance benefit is tiny
    # angle_limit = 2 * math.pi
    # for current_angle in itertools.count(0, angle_per_point):
    #     if current_angle > angle_limit:
    #         break
    for step in range(amount_of_points_on_circle_rounded):
        current_angle = step * angle_per_point
        X: complex = cmath.rect(circle_radius, current_angle)
        x, y = X.real, X.imag
        yield (amount_of_points_on_circle, current_angle, x, y)

    return None


def _get_colors_hex(amount: int = 1) -> Generator[Tuple[int, int, int], None, None]:
    """
    Returns hexadecimal values as string, e.g. (255, 255, 255)

    :param amount:
    :return:
    """
    limit = 256 ** 3 - 1
    assert amount < limit, "Too many points!"
    step_size = limit // amount

    for color_number in range(0, limit + 1, step_size):
        color_number, r = divmod(color_number, 256)
        color_number, g = divmod(color_number, 256)
        color_number, b = divmod(color_number, 256)
        yield (r, g, b)

    return None


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    def plot_squares(limit: int):
        fig, ax = plt.subplots()

        point_positions = []

        # Set the ranges of x and y axis
        xmin, ymin = -limit - 0.5, -limit - 0.5
        xmax, ymax = limit + 0.5, limit + 0.5
        ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))

        # Aspect ratio of 1:1 for x and y axis, don't stretch one axis
        ax.set_aspect(1.0)

        # Show vertical and horizontal line at (0, 0)
        ax.axhline(y=0, color="k")
        ax.axvline(x=0, color="k")

        for dist, x, y in generate_2d_offset_points(limit):
            point_positions.append((dist, x, y))

        colors = list(_get_colors_hex(len(point_positions)))
        # colors.sort()
        colors.sort(key=lambda c: c[0] ** 2 + c[1] ** 2 + c[2] ** 2, reverse=True)
        # colors.sort(key=lambda c: c[0] + c[1] + c[2], reverse=True)
        # colors.sort(key=lambda c: c[0] * c[1] * c[2], reverse=True)

        for (dist, x, y), color in zip(point_positions, colors):
            # print(dist, x, y)
            r, g, b = color
            hex_string = "#" + hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)
            square = plt.Rectangle((x - 0.5, y - 0.5), width=1, height=1, color=hex_string)
            ax.add_artist(square)

        if point_positions:
            fig.savefig(f"plot_square.png", dpi=1000)

    def plot_line(start: Tuple[int, int], end: Tuple[int, int]):
        fig, ax = plt.subplots()

        point_positions = []

        # Set the ranges of x and y axis
        xmin, ymin = start
        xmax, ymax = end
        ax.set(xlim=(xmin - 0.5, xmax + 0.5), ylim=(ymin - 0.5, ymax + 0.5))

        # Aspect ratio of 1:1 for x and y axis, don't stretch one axis
        ax.set_aspect(1.0)

        # Show vertical and horizontal line at (0, 0)
        ax.axhline(y=0, color="k")
        ax.axvline(x=0, color="k")

        for x, y in generate_line(*start, *end):
            point_positions.append((x, y))

        for (x, y), color in zip(point_positions, _get_colors_hex(len(point_positions))):
            r, g, b = color
            hex_string = "#" + hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)
            square = plt.Rectangle((x - 0.5, y - 0.5), width=1, height=1, color=hex_string)
            ax.add_artist(square)

        if point_positions:
            fig.savefig(f"plot_line.png", dpi=1000)

    def plot_circles(fill_circle: bool = False):
        # Set the radius of each point on the circle, and the circle radius
        limit = 100
        for point_radius in range(1, 10):
            fig, ax = plt.subplots()

            circle_positions = []

            if fill_circle:
                # Draw the center point
                circle_positions.append((0, 0))

            # Set the ranges of x and y axis
            xmin = ymin = -limit - point_radius
            xmax = ymax = limit + point_radius
            ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))

            # Aspect ratio of 1:1 for x and y axis, don't stretch one axis
            ax.set_aspect(1.0)

            # Hide axes
            # ax.get_xaxis().set_visible(False)
            # ax.get_yaxis().set_visible(False)

            # Show vertical and horizontal line at (0, 0)
            ax.axhline(y=0, color="k")
            ax.axvline(x=0, color="k")

            circles_added = 0

            for circle_radius in itertools.count(start=point_radius * 2, step=point_radius * 2):
                if circle_radius >= limit:
                    break

                if not fill_circle:
                    # Comment this out if you want to fill points inside the circle
                    if circle_radius < limit - point_radius * 2:
                        continue

                for amount, angle, x, y in generate_circle_points(
                    point_radius=point_radius, circle_radius=circle_radius
                ):
                    circle_positions.append((x, y))
                    circles_added += 1

            circle_positions.sort(key=lambda p: (round(p[0] ** 2 + p[1] ** 2, 3), p[0], p[1]), reverse=True)

            colors = list(_get_colors_hex(len(circle_positions)))
            # Sort by bright colors inside, dark colors outside
            # colors.sort(key=lambda c: c[0] + c[1] + c[2])
            # colors.sort(key=lambda c: c[0] * c[1] * c[2])
            # Sort by red colors inside, green colors outside
            colors.sort()

            # Draw circles
            for (x, y), color in zip(circle_positions, colors):
                r, g, b = color
                hex_string = "#" + hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)
                circle1 = plt.Circle((x, y), point_radius, color=hex_string, antialiased=True)
                ax.add_artist(circle1)

            # Check if the circles are too close to each other or only if the output .png file has those overlaps
            # for x0, y0 in circle_positions:
            #     for x1, y1 in circle_positions:
            #         if x0 == x1 and y0 == y1:
            #             continue
            #         dist = math.hypot(x0-x1, y0-y1)
            #         if dist + 10e-8 < point_radius * 2:
            #             print(f"({x0}, {y0}) and ({x1}, {y1}) have distance {dist} but should only have distance {point_radius * 2}")

            # fig.show()
            if circles_added:
                fig.savefig(f"plot_circles-{point_radius:02}-{limit:02}.png", dpi=100)

    t0 = time.perf_counter()
    plot_squares(limit=5)
    plot_line(start=(0, 0), end=(40, 30))
    plot_circles(fill_circle=True)
    t1 = time.perf_counter()
    print(t1 - t0)
