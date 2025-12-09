"""
Advent of Code 2025
Day 08: Playground
"""

# pylint: skip-file
from dataclasses import dataclass
from itertools import combinations
from math import prod, sqrt

import pytest


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def distance(self, other: "Point") -> float:
        """Calculate Euclidean distance to another point."""
        return sqrt(
            (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
        )


def parse_input(file_name: str) -> list[tuple[Point, Point]]:
    """Parse input file and return sorted pairs."""
    with open(file_name, "r", encoding="ascii") as data_file:
        points = [
            Point(*map(int, line.split(","))) for line in data_file.read().splitlines()
        ]
    return sorted(combinations(points, 2), key=lambda pair: pair[0].distance(pair[1]))


class UnionFind:
    """Disjoint Union Find (Union-Find) data structure."""

    def __init__(self):
        self.parent = {}
        self.rank = {}

    def find(self, point):
        """Find the root representative of the set containing x."""
        if point not in self.parent:
            self.parent[point] = point
            self.rank[point] = 0

        if self.parent[point] != point:
            self.parent[point] = self.find(self.parent[point])  # Path compression

        return self.parent[point]

    def union(self, a, b):
        """Merge the sets containing points a and b."""
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:
            return False  # Already in same set

        # Union by rank
        if self.rank[root_a] < self.rank[root_b]:
            self.parent[root_a] = root_b
        elif self.rank[root_a] > self.rank[root_b]:
            self.parent[root_b] = root_a
        else:
            self.parent[root_b] = root_a
            self.rank[root_a] += 1

        return True  # Sets were merged

    def get_connected_sets(self):
        """Return a list of sets representing connected components."""
        connected_sets = {}
        for element in self.parent:
            root = self.find(element)
            if root not in connected_sets:
                connected_sets[root] = set()
            connected_sets[root].add(element)
        return list(connected_sets.values())


def union_find_sets(pairs):
    """Union-Find to build connected components.
    Args: pairs: List of (element1, element2) tuples.
    Returns: List of connected component sets.
    """
    uf = UnionFind()
    for pair in pairs:
        uf.union(*pair)
    return uf.get_connected_sets()


def kruskal_mst_edges(pairs):
    """Kruskal's algorithm: find Minimum Spanning Tree (MST).
    Assumes pairs are sorted by weight (distance).
    Args: pairs: List of (element1, element2) tuples.
    Returns: List of edges in the MST.
    """
    uf = UnionFind()
    mst_edges = []
    max_edges = len(set(p for pair in pairs for p in pair)) - 1

    for pair in pairs:
        if uf.union(*pair):
            mst_edges.append(pair)
            if len(mst_edges) == max_edges:
                break

    return mst_edges


def day08_part1(sorted_pairs: list[tuple[Point, Point]], max_connections) -> int:
    disjoint_sets = union_find_sets(sorted_pairs[:max_connections])
    three_largest = sorted(disjoint_sets, key=len, reverse=True)[:3]
    return prod(len(component) for component in three_largest)


def day08_part2(sorted_pairs: list[tuple[Point, Point]]) -> int:
    mst_edges = kruskal_mst_edges(sorted_pairs)
    last_a, last_b = mst_edges[-1]
    return last_a.x * last_b.x


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day08_test.txt")


def test_day08_part1(test_data):
    assert day08_part1(test_data, 10) == 40


def test_day08_part2(test_data):
    assert day08_part2(test_data) == 25272


if __name__ == "__main__":
    pairs = parse_input("data/day08.txt")

    print("Day 08 Part 1:")
    print(day08_part1(pairs, 1000))

    print("Day 08 Part 2:")
    print(day08_part2(pairs))
