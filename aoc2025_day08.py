"""
Advent of Code 2025
Day 08:
"""

# pylint: skip-file
from math import sqrt

import pytest

Point = tuple[int, ...]


def distance(p1: Point, p2: Point) -> float:
    """Calculate Euclidean distance between two 3D points (tuples)."""
    return sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))


def parse_input(file_name: str) -> list[Point]:
    with open(file_name, "r", encoding="ascii") as data_file:
        return [
            tuple(map(int, line.split(","))) for line in data_file.read().splitlines()
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

    def get_connected_sets(self):
        """Return a list of sets representing connected components."""
        connected_sets = {}
        for element in self.parent:
            root = self.find(element)
            if root not in connected_sets:
                connected_sets[root] = set()
            connected_sets[root].add(element)
        return list(connected_sets.values())


def union_find_connected_sets(pairs):
    """Build connected components using Union-Find algorithm on all pairs."""
    uf = UnionFind()
    for p1, p2 in pairs:
        uf.union(p1, p2)
    return uf.get_connected_sets()


def kruskal_mst_edges(pairs):
    """Kruskal's algorithm: find Minimum Spanning Tree (MST).
    Assumes pairs are sorted by weight (distance).
    Returns list of edges in the MST.
    """
    uf = UnionFind()
    mst_edges = []
    num_elements = len(set(p for pair in pairs for p in pair))

    for pair in pairs:
        if len(mst_edges) == num_elements - 1:
            break
        p1, p2 = pair
        if uf.union(p1, p2):
            mst_edges.append(pair)

    return mst_edges


def day08_part1(points: list[tuple], max_connections) -> int:
    pairs = sorted(combinations(points, 2), key=lambda pair: distance(pair[0], pair[1]))
    sorted_circuits = sorted(
        union_find_connected_sets(pairs[:max_connections]), key=len, reverse=True
    )
    return prod(len(component) for component in sorted_circuits[:3])


def day08_part2(points: list[tuple]) -> int:
    pairs = sorted(combinations(points, 2), key=lambda pair: distance(pair[0], pair[1]))
    mst_edges = kruskal_mst_edges(pairs)
    last_a, last_b = mst_edges[-1]
    return last_a[0] * last_b[0]


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day08_test.txt")


def test_day08_part1(test_data):
    assert day08_part1(test_data, 10) == 40


def test_day08_part2(test_data):
    assert day08_part2(test_data) == 25272


if __name__ == "__main__":
    input_data = parse_input("data/day08.txt")

    print("Day 08 Part 1:")
    print(day08_part1(input_data, 1000))

    print("Day 08 Part 2:")
    print(day08_part2(input_data))
