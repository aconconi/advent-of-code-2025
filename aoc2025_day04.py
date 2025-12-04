"""
Advent of Code 2025
Day 04:
"""

# pylint: skip-file
import pytest
from itertools import product


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        rolls = set(
            (x, y)
            for y, row in enumerate(data_file.read().splitlines())
            for x, cell in enumerate(row)
            if cell == "@"
        )
        return rolls

def adjacent_positions(pos):
    for dx, dy in product([-1, 0, 1], repeat=2):
        if (dx, dy) != (0, 0):
            yield pos[0] + dx, pos[1] + dy

def count_neighbors(rolls, pos):
    return sum(
        other_pos in rolls
        for other_pos in adjacent_positions(pos)
    )


def day04_part1(rolls):
    return sum(count_neighbors(rolls, pos) < 4 for pos in rolls)


def day04_part2(data):
    pass


"""
@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day04_test.txt")


def test_day04_part1(test_data):
    assert day04_part1(test_data) == 13

def test_day04_part2(test_data):
    assert day04_part2(test_data)
"""

if __name__ == "__main__":
    input_data = parse_input("data/day04.txt")

    print("Day 04 Part 1:")
    print(day04_part1(input_data))

    print("Day 04 Part 2:")
    print(day04_part2(input_data))
