import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import math

from hypothesis import given, settings, strategies as st

from generators_2d.generators import generate_circle_points


@given(st.integers(min_value=1, max_value=10 ** 3), st.integers(min_value=2, max_value=10 ** 3))
# @settings(max_examples=20)
def test_circle_points(point_radius, circle_radius):
    if point_radius * 2 > circle_radius:
        assert list(generate_circle_points(point_radius, circle_radius)) == []
        return

    amount_of_points_on_circle: int = math.pi / (2 * math.asin(point_radius / (2 * circle_radius)))
    amount_of_points_on_circle_rounded = math.floor(amount_of_points_on_circle)

    points_above_x_axis = amount_of_points_on_circle // 2 + amount_of_points_on_circle_rounded % 2

    for point_index, (amount, current_angle, x, y) in enumerate(generate_circle_points(point_radius, circle_radius)):
        assert abs(amount - amount_of_points_on_circle) < 10e-10
        assert y >= 0 or point_index >= points_above_x_axis
        assert y < 0 or point_index <= points_above_x_axis
