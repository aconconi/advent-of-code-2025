"""
Advent of Code 2025
Day 04:
"""

from itertools import product

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        rolls = set(
            (x, y)
            for y, row in enumerate(data_file.read().splitlines())
            for x, cell in enumerate(row)
            if cell == "@"
        )
        return rolls


def neighbors(rolls, pos):
    for dx, dy in product([-1, 0, 1], repeat=2):
        if (dx, dy) != (0, 0):
            other_pos = (pos[0] + dx, pos[1] + dy)
            if other_pos in rolls:
                yield other_pos


def count_neighbors(rolls, pos):
    return sum(1 for _ in neighbors(rolls, pos))


def day04_part1(rolls):
    return sum(count_neighbors(rolls, roll) < 4 for roll in rolls)


def day04_part2(rolls):
    rolls_neigh_count = {pos: count_neighbors(rolls, pos) for pos in rolls}
    count_removed = 0
    while True:
        to_be_removed = []
        for roll, num_neighbors in rolls_neigh_count.items():
            if num_neighbors < 4:
                to_be_removed.append(roll)
                for neighbor in neighbors(rolls, roll):
                    rolls_neigh_count[neighbor] -= 1
        if not to_be_removed:
            break
        for roll in to_be_removed:
            count_removed += 1
            rolls.remove(roll)
            rolls_neigh_count.pop(roll)
    return count_removed


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day04_test.txt")


def test_day04_part1(test_data):
    assert day04_part1(test_data) == 13


def test_day04_part2(test_data):
    assert day04_part2(test_data) == 43


if __name__ == "__main__":
    input_data = parse_input("data/day04.txt")

    print("Day 04 Part 1:")
    print(day04_part1(input_data))

    print("Day 04 Part 2:")
    print(day04_part2(input_data))
