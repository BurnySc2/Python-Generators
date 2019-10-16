import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from generators_2d.generators import generate_tuple

limit = 500

"""
This file can be run by using commands:

pipenv install --dev
pipenv run pytest test/benchmark_2d_grid_points.py
"""


def generator_function():
    for dist, x, y in generate_tuple(limit):
        pass


def list_comprehension_function():
    # Perhaps this function could be improved by only generating an 8th (triangle) and then yielding the other 7/8th of the square by using mirroring techniques like in the generator
    my_List = [(x ** 2 + y ** 2, x, y) for x in range(-limit, limit + 1) for y in range(-limit, limit + 1)]
    my_List.sort()


def test_generator_function(benchmark):
    result = benchmark(generator_function)


def test_list_comprehension_function(benchmark):
    result = benchmark(list_comprehension_function)
