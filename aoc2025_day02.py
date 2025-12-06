"""
Advent of Code 2025
Day 02: Gift Shop
"""

import re

import pytest


def parse_input(file_name: str) -> list[tuple[int, int]]:
    with open(file_name, "r", encoding="ascii") as data_file:
        ranges: list[tuple[int, int]] = []
        for id_range in data_file.read().strip().split(","):
            low_str, high_str = id_range.split("-")
            ranges.append((int(low_str), int(high_str)))
        return ranges


def solve(id_ranges: list[tuple[int, int]], pattern: str) -> int:
    return sum(
        sum(id for id in range(low, high + 1) if re.fullmatch(pattern, str(id)))
        for low, high in id_ranges
    )


def day02_part1(id_ranges: list[tuple[int, int]]) -> int:
    return solve(id_ranges, r"(\d+)\1")


def day02_part2(id_ranges: list[tuple[int, int]]) -> int:
    return solve(id_ranges, r"(\d+)\1{1,}")


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data() -> list[tuple[int, int]]:
    return parse_input("data/day02_test.txt")


def test_day02_part1(test_data: list[tuple[int, int]]) -> None:
    assert day02_part1(test_data) == 1227775554


def test_day02_part2(test_data: list[tuple[int, int]]) -> None:
    assert day02_part2(test_data) == 4174379265


if __name__ == "__main__":
    input_data = parse_input("data/day02.txt")

    print("Day 02 Part 1:")
    print(day02_part1(input_data))

    print("Day 02 Part 2:")
    print(day02_part2(input_data))
