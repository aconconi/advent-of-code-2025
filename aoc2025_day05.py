"""
Advent of Code 2025
Day 05: Cafeteria
"""

import pytest
from itertools import pairwise


class IdRange:
    """Represents a range with start and end values."""
    
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
    
    def overlaps_with(self, other: "IdRange") -> bool:
        """Check if this range overlaps with another range."""
        return self.start <= other.start <= self.end or other.start <= self.start <= other.end
    
    def merge_with(self, other: "IdRange") -> "IdRange":
        """Merge this range with another range."""
        if not self.overlaps_with(other):
            raise ValueError("Ranges do not overlap and cannot be merged.")
        self.start = min(self.start, other.start)
        self.end = max(self.end, other.end)
    
    def contains_id(self, id: int) -> bool:
        return self.start <= id <= self.end
    
    def __len__(self) -> int:
        return self.end - self.start + 1
    
    def __lt__(self, other: "IdRange") -> bool:
        return self.start < other.start
    



def parse_input(file_name: str) -> tuple[list[tuple[int, int]], list[int]]:
     with open(file_name, "r", encoding="ascii") as data_file:
        fresh_ranges, available_ingredients = map(str.splitlines, data_file.read().strip().split("\n\n", 1))
        fresh_ranges = [IdRange(*map(int, line.split("-"))) for line in fresh_ranges]
        available_ingredients = [int(line) for line in available_ingredients]
        return fresh_ranges, available_ingredients



def day05_part1(data) -> int:
    fresh_ranges, available_ingredients = data
    return sum(
        any(id_range.contains_id(ingredient) for id_range in fresh_ranges)
        for ingredient in available_ingredients
    )


def day05_part2(data) -> int:
    fresh_ranges, _ = data
    fresh_ranges.sort()
    while True:
        overlapping_pair = next(
            (
                (a, b)
                for (a, b) in pairwise(fresh_ranges) if a.overlaps_with(b)
            ),
            None
        )
        if overlapping_pair is None:
            break
        a, b = overlapping_pair
        a.merge_with(b)
        fresh_ranges.remove(b)

    return sum(len(id_range) for id_range in fresh_ranges)



"""
@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day05_test.txt")


def test_day05_part1(test_data):
    assert day05_part1(test_data) == 3

def test_day05_part2(test_data):
    assert day05_part2(test_data) == 14
"""

if __name__ == "__main__":
    input_data = parse_input("data/day05.txt")

    print("Day 05 Part 1:")
    print(day05_part1(input_data))

    print("Day 05 Part 2:")
    print(day05_part2(input_data))
