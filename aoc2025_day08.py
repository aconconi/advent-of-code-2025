"""
Advent of Code 2025
Day 08:
"""

# pylint: skip-file
from math import sqrt

import pytest


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __lt__(self, other):
        return (self.x, self.y, self.z) < (other.x, other.y, other.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def distance(self, other):
        return sqrt(
            (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
        )

    def __repr__(self):
        return f"P({self.x}, {self.y}, {self.z})"

    def __hash__(self):
        return hash((self.x, self.y, self.z))


def parse_input(file_name: str) -> list:
    with open(file_name, "r", encoding="ascii") as data_file:
        return [
            Point(*map(int, line.split(","))) for line in data_file.read().splitlines()
        ]


from itertools import combinations
from math import prod


class UnionFind:
    """Disjoint Union Find (Union-Find) data structure."""

    def __init__(self):
        self.parent = {}
        self.rank = {}

    def find(self, x):
        """Find the root representative of the set containing x."""
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0

        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression

        return self.parent[x]

    def union(self, x, y):
        """Merge the sets containing x and y."""
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False  # Already in same set

        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        return True  # Sets were merged

    def get_components(self):
        """Return a list of sets representing connected components."""
        components = {}
        for element in self.parent:
            root = self.find(element)
            if root not in components:
                components[root] = set()
            components[root].add(element)
        return list(components.values())


def union_find_components(pairs):
    """Build connected components using Union-Find algorithm on all pairs."""
    uf = UnionFind()
    for p1, p2 in pairs:
        uf.union(p1, p2)
    return uf.get_components()


def day08_part1(points: list[Point], max_connections) -> int:
    pairs = sorted(combinations(points, 2), key=lambda pair: pair[0].distance(pair[1]))
    sorted_circuits = sorted(
        union_find_components(pairs[:max_connections]), key=len, reverse=True
    )
    return prod(len(component) for component in sorted_circuits[:3])


def day08_part2(data: list[str]) -> None:
    pass


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day08_test.txt")


def test_day08_part1(test_data):
    assert day08_part1(test_data, 10) == 40


def test_day08_part2(test_data):
    assert day08_part2(test_data)


if __name__ == "__main__":
    input_data = parse_input("data/day08.txt")

    print("Day 08 Part 1:")
    print(day08_part1(input_data, 1000))

    print("Day 08 Part 2:")
    print(day08_part2(input_data))
