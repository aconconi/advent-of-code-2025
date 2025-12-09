"""
Advent of Code 2025
Day 09: Movie Theater
"""

from dataclasses import dataclass, field
from itertools import chain, combinations, pairwise

import pytest


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class Rectangle:
    """Rectangle defined by its bounding box."""

    min_corner: Point = field(init=False)
    max_corner: Point = field(init=False)

    def __init__(self, p1: Point, p2: Point):
        object.__setattr__(self, "min_corner", Point(min(p1.x, p2.x), min(p1.y, p2.y)))
        object.__setattr__(self, "max_corner", Point(max(p1.x, p2.x), max(p1.y, p2.y)))

    @property
    def area(self) -> int:
        return (self.max_corner.x - self.min_corner.x + 1) * (
            self.max_corner.y - self.min_corner.y + 1
        )

    def overlaps(self, other: "Rectangle") -> bool:
        return (
            other.min_corner.x < self.max_corner.x
            and other.min_corner.y < self.max_corner.y
            and other.max_corner.x > self.min_corner.x
            and other.max_corner.y > self.min_corner.y
        )


def parse_input(file_name: str) -> list[Point]:
    with open(file_name, "r", encoding="ascii") as data_file:
        return [
            Point(*map(int, line.split(","))) for line in data_file.read().splitlines()
        ]


def day09_part1(points: list[Point]) -> int:
    return max(Rectangle(a, b).area for a, b in combinations(points, 2))


def day09_part2(points: list[Point]) -> int:
    # we define edges as rectangles between consecutive points (with
    # pairwise) and wrap around the list of points (with chain)
    edges = [Rectangle(a, b) for a, b in pairwise(chain(points, points[:1]))]

    def is_contained(rect: Rectangle) -> bool:
        return all(not rect.overlaps(edge) for edge in edges)

    return max(
        (
            rect.area
            for a, b in combinations(points, 2)
            if is_contained(rect := Rectangle(a, b))
        ),
        default=0,
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
