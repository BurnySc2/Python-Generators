import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import math

from hypothesis import given, settings, strategies as st

from generators_2d.generators import generate_line


@given(
    st.integers(min_value=-10 ** 5, max_value=10 ** 5),
    st.integers(min_value=-10 ** 5, max_value=10 ** 5),
    st.integers(min_value=100, max_value=10 ** 5),
    st.integers(min_value=-100, max_value=100),
)
def test_lines_towards_east(x0, y0, east, north):
    x1, y1 = x0 + east, y0 + north
    correct_result = []
    m = (y1 - y0) / abs(x1 - x0)
    y_new = y0
    for x in range(x0, x1 + 1):
        correct_result.append((x, math.floor(y_new)))
        y_new += m

    function_result = list(generate_line(x0, y0, x1, y1))

    assert correct_result == function_result


@given(
    st.integers(min_value=-10 ** 5, max_value=10 ** 5),
    st.integers(min_value=-10 ** 5, max_value=10 ** 5),
    st.integers(min_value=-10 ** 5, max_value=-100),
    st.integers(min_value=-100, max_value=100),
)
def test_lines_towards_west(x0, y0, east, north):
    x1, y1 = x0 + east, y0 + north
    correct_result = []
    m = (y1 - y0) / abs(x1 - x0)
    y_new = y0
    for x in range(x0, x1 - 1, -1):
        correct_result.append((x, math.floor(y_new)))
        y_new += m

    function_result = list(generate_line(x0, y0, x1, y1))

    assert correct_result == function_result


@given(
    st.integers(min_value=-10 ** 5, max_value=10 ** 5),
    st.integers(min_value=-10 ** 5, max_value=10 ** 5),
    st.integers(min_value=-100, max_value=-100),
    st.integers(min_value=101, max_value=10 ** 5),
)
def test_lines_towards_north(x0, y0, east, north):
    x1, y1 = x0 + east, y0 + north
    correct_result = []
    m = (x1 - x0) / abs(y1 - y0)
    x_new = x0
    for y in range(y0, y1 + 1):
        correct_result.append((math.floor(x_new), y))
        x_new += m

    function_result = list(generate_line(x0, y0, x1, y1))

    assert correct_result == function_result


@given(
    st.integers(min_value=-10 ** 5, max_value=10 ** 5),
    st.integers(min_value=-10 ** 5, max_value=10 ** 5),
    st.integers(min_value=-100, max_value=-100),
    st.integers(min_value=-10 ** 5, max_value=-101),
)
def test_lines_towards_south(x0, y0, east, north):
    x1, y1 = x0 + east, y0 + north
    correct_result = []
    m = (x1 - x0) / abs(y1 - y0)
    x_new = x0
    for y in range(y0, y1 - 1, -1):
        correct_result.append((math.floor(x_new), y))
        x_new += m

    function_result = list(generate_line(x0, y0, x1, y1))

    assert correct_result == function_result


def test_simple_line_examples():
    # No line, start and end point are identical, dont divide by zero
    a = list(generate_line(0, 0, 0, 0))
    assert a == [(0, 0)]
    # 2 examples to check vertical and horizontal

    a = list(generate_line(0, 0, 1, 0))
    assert a == [(0, 0), (1, 0)]

    a = list(generate_line(0, 0, 0, 1))
    assert a == [(0, 0), (0, 1)]

    # 3 examples to check diagonal
    a = list(generate_line(0, 0, 1, 1))
    assert a == [(0, 0), (1, 1)]

    a = list(generate_line(-1, -1, 1, 1))
    assert a == [(-1, -1), (0, 0), (1, 1)]

    a = list(generate_line(-1, 1, 1, -1))
    assert a == [(-1, 1), (0, 0), (1, -1)]

    # Point2 is mostly to the right of point1
    a = list(generate_line(0, 0, 4, 2))
    b = [(0, 0), (1, 0), (2, 1), (3, 1), (4, 2)]
    assert a == b, f"{a}\n{b}"

    # Point2 is mostly to the left of point1
    a = list(generate_line(4, 2, 0, 0))
    b = [(4, 2), (3, 1), (2, 1), (1, 0), (0, 0)]
    assert a == b, f"{a}\n{b}"

    # Point2 is mostly to the top of point1
    a = list(generate_line(0, 0, 2, 4))
    b = [(0, 0), (0, 1), (1, 2), (1, 3), (2, 4)]
    assert a == b, f"{a}\n{b}"

    # Point2 is mostly to the bottom of point1
    a = list(generate_line(2, 4, 0, 0))
    b = [(2, 4), (1, 3), (1, 2), (0, 1), (0, 0)]
    assert a == b, f"{a}\n{b}"
