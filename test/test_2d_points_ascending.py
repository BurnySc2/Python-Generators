import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from hypothesis import given, settings, strategies as st

from generators_2d.generators import generate_tuple


@given(st.integers(min_value=0, max_value=100))
@settings(max_examples=20)
def test_2d_points_ascending(limit: int):
    list1 = list(generate_tuple(limit))
    list1.sort()

    # This list comprehension creates slightly more results than the generator, but the generator returns them ordered by distance squared, so this list needs to be sorted by distance which turns out to be about 3 times slower than the full generator run
    list2 = [(x ** 2 + y ** 2, x, y) for x in range(-limit, limit + 1) for y in range(-limit, limit + 1)]
    list2.sort()

    # The generator is supposed to have less or equal amount of elements as the list comprehension
    assert len(list1) <= len(list2)
    # Loop until the end of the shortest list is reached
    for i, j in zip(list1, list2):
        assert i == j
