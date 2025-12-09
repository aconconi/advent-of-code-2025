"""
Advent of Code 2025
Day 09: Movie Theater
"""

from itertools import combinations

import pytest
from shapely.geometry.polygon import Polygon


def parse_input(file_name: str) -> list[tuple]:
    with open(file_name, "r", encoding="ascii") as data_file:
        return [
            tuple(map(int, line.split(","))) for line in data_file.read().splitlines()
        ]


def rect_area(a, b):
    return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)


def get_rect_from_pair(a, b):
    x1, y1 = a
    x2, y2 = b
    return Polygon(
        [
            (min(x1, x2), min(y1, y2)),
            (max(x1, x2), min(y1, y2)),
            (max(x1, x2), max(y1, y2)),
            (min(x1, x2), max(y1, y2)),
        ]
    )


def day09_part1(points: list[tuple]) -> int:
    return max(rect_area(a, b) for a, b in combinations(points, 2))


def day09_part2(points: list[tuple]) -> int:
    region = Polygon(points)
    return max(
        rect_area(a, b)
        for a, b in combinations(points, 2)
        if region.contains(get_rect_from_pair(a, b))
    )


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day09_test.txt")


def test_day09_part1(test_data):
    assert day09_part1(test_data) == 50


def test_day09_part2(test_data):
    assert day09_part2(test_data) == 24


if __name__ == "__main__":
    input_data = parse_input("data/day09.txt")

    print("Day 09 Part 1:")
    print(day09_part1(input_data))

    print("Day 09 Part 2:")
    print(day09_part2(input_data))
