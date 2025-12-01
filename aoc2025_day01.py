"""
Advent of Code 2025
Day 01: Secret Entrance
"""

import pytest


def parse_input(file_name: str) -> list[int]:
    def convert_rotation(line: str) -> int:
        direction = -1 if line[0] == "L" else 1
        distance = int(line[1:])
        return direction * distance

    with open(file_name, "r", encoding="ascii") as data_file:
        return [convert_rotation(line) for line in data_file.read().splitlines()]


def day01_part1(data: list[int]) -> int:
    dial = 50
    pointed_zero = 0
    for delta in data:
        dial = (dial + delta) % 100
        if dial == 0:
            pointed_zero += 1
    return pointed_zero


def day01_part2(data: list[int]) -> int:
    dial = 50
    pointed_zero = 0
    for delta in data:
        if delta > 0:
            pointed_zero += (dial + delta) // 100
        elif delta == 0:
            pointed_zero += 1
        else:
            pointed_zero += ((100 - dial) % 100 + abs(delta)) // 100
        dial = (dial + delta) % 100
    return pointed_zero


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day01_test.txt")


def test_day01_part1(test_data):
    assert day01_part1(test_data) == 3


def test_day01_part2(test_data):
    assert day01_part2(test_data) == 6


if __name__ == "__main__":
    input_data = parse_input("data/day01.txt")

    print("Day 01 Part 1:")
    print(day01_part1(input_data))

    print("Day 01 Part 2:")
    print(day01_part2(input_data))
