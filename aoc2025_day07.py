"""
Advent of Code 2025
Day 07: Laboratories
"""

import pytest


def parse_input(file_name: str) -> list[str]:
    with open(file_name, "r", encoding="ascii") as data_file:
        return data_file.read().splitlines()


def day07_part1(grid: list[str]) -> int:
    # Beams at time i are represented by their column position j
    beams = {grid[0].find("S")}
    splits = 0
    for i in range(len(grid) - 1):
        new_beams = set()
        for j in beams:
            if grid[i + 1][j] == "^":
                new_beams.update([j - 1, j + 1])
                splits += 1
            else:
                new_beams.add(j)
        beams = new_beams
    return splits


def day07_part2(grid: list[str]) -> int:
    # beam_counts[j] is the number of timelines for a beam
    # in column j at time i
    beam_counts = {grid[0].find("S"): 1}
    for i in range(len(grid) - 1):
        new_counts = {}
        for col, count in beam_counts.items():
            if grid[i + 1][col] == "^":
                new_counts[col - 1] = new_counts.get(col - 1, 0) + count
                new_counts[col + 1] = new_counts.get(col + 1, 0) + count
            else:
                new_counts[col] = new_counts.get(col, 0) + count
        beam_counts = new_counts

    return sum(beam_counts.values())


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day07_test.txt")


def test_day07_part1(test_data):
    assert day07_part1(test_data) == 21


def test_day07_part2(test_data):
    assert day07_part2(test_data) == 40


if __name__ == "__main__":
    input_data = parse_input("data/day07.txt")

    print("Day 07 Part 1:")
    print(day07_part1(input_data))

    print("Day 07 Part 2:")
    print(day07_part2(input_data))
