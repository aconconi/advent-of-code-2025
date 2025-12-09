"""
Advent of Code 2025
Day 09: Movie Theater
"""

from dataclasses import dataclass
from itertools import combinations, pairwise

import pytest


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __iter__(self):
        """Allow unpacking as (x, y) for compatibility."""
        return iter((self.x, self.y))


def parse_input(file_name: str) -> list[Point]:
    with open(file_name, "r", encoding="ascii") as data_file:
        return [
            Point(*map(int, line.split(","))) for line in data_file.read().splitlines()
        ]


def rect_area(a: Point, b: Point) -> int:
    return (abs(a.x - b.x) + 1) * (abs(a.y - b.y) + 1)


def rect_bounds(a: Point, b: Point) -> tuple[Point, Point]:
    """Convert pair of points to bounding box (min_corner, max_corner)."""
    return Point(min(a.x, b.x), min(a.y, b.y)), Point(max(a.x, b.x), max(a.y, b.y))


def polygon_edges_bounded(points: list[Point]) -> list[tuple[Point, Point]]:
    """Extract edges from polygon (closed chain of consecutive points)."""
    return [rect_bounds(a, b) for a, b in pairwise(points + [points[0]])]


def rects_overlap(rect1: tuple[Point, Point], rect2: tuple[Point, Point]) -> bool:
    """Check if two bounding rectangles overlap."""
    min_r1, max_r1 = rect1
    min_r2, max_r2 = rect2
    return (
        min_r2.x < max_r1.x
        and min_r2.y < max_r1.y
        and max_r2.x > min_r1.x
        and max_r2.y > min_r1.y
    )


def day09_part1(points: list[Point]) -> int:
    return max(rect_area(a, b) for a, b in combinations(points, 2))


def day09_part2(points: list[Point]) -> int:
    """Find largest rectangle entirely contained within polygon."""
    polygon_bounds = polygon_edges_bounded(points)

    def is_contained(rect: tuple[Point, Point]) -> bool:
        """Check if rectangle doesn't overlap any polygon edge."""
        return all(not rects_overlap(rect, edge) for edge in polygon_bounds)

    return max(
        (
            rect_area(*rect)
            for rect in (rect_bounds(a, b) for a, b in combinations(points, 2))
            if is_contained(rect)
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
