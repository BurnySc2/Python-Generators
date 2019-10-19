import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import time

from hypothesis import given, settings, strategies as st

from generators_2d.generators import generate_2d_grid_points, generate_2d_ordered_grid_points


def test_grid():
    list1 = list(generate_2d_grid_points(max_distance=1))
    list2 = [(0, 0), (-1, 1), (-1, -1), (0, 1), (0, -1), (1, 1), (1, -1), (1, 0), (-1, 0)]
    print(list1)
    print(list2)

    assert list1 == list2


@given(st.integers(min_value=0, max_value=100), st.integers(min_value=0, max_value=100))
def test_grid_hypothesis(min_distance, max_distance):
    # TODO: test with variable step_size
    step_size = 1
    expected_amount = sum(max(1, value * 8) for value in range(min_distance, max_distance + 1, step_size))

    list1 = list(generate_2d_grid_points(min_distance=min_distance, max_distance=max_distance, step_size=step_size))
    actual_amount = len(list1)

    assert expected_amount == actual_amount


def test_performance():
    t0 = time.perf_counter()
    list1 = list(generate_2d_grid_points(max_distance=100))
    t1 = time.perf_counter()
    list2 = list(generate_2d_ordered_grid_points(limit=100))
    t2 = time.perf_counter()

    print(len(list1), len(list2))
    print(f"{t2-t1}\n{t1-t0}")
    assert t1 - t0 < (t2 - t1) * 2
