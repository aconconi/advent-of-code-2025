"""
Advent of Code 2025
Day 03: Lobby
"""

import pytest


def parse_input(file_name: str) -> list[list[int]]:
     with open(file_name, "r", encoding="ascii") as data_file:
         return [list(map(int, line)) for line in data_file.read().splitlines()]


def largest_joltage(bank: list[int], turn_on: int) -> int:
     digits = [0] * turn_on
     first_idx = 0
     for i, battery in enumerate(bank):
         update_idx = next(
             (
                 idx
                 for idx in range(first_idx, turn_on)
                 if battery > digits[idx] and i <= len(bank) - turn_on + idx
             ),
             None,
         )

         if update_idx is not None:
             digits[update_idx] = battery
             digits[update_idx + 1 :] = [0] * (turn_on - update_idx - 1)
             if battery == 9:
                 first_idx = update_idx + 1

     result = int("".join(map(str, digits)))
     return result


def day03_part1(banks: list[list[int]]) -> int:
     return sum(largest_joltage(bank, 2) for bank in banks)


def day03_part2(banks: list[list[int]]) -> int:
     return sum(largest_joltage(bank, 12) for bank in banks)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data() -> list[list[int]]:
     return parse_input("data/day03_test.txt")


def test_day03_part1(test_data: list[list[int]]) -> None:
     assert day03_part1(test_data) == 357


def test_day03_part2(test_data: list[list[int]]) -> None:
     assert day03_part2(test_data) == 3121910778619


if __name__ == "__main__":
    input_data = parse_input("data/day03.txt")

    print("Day 03 Part 1:")
    print(day03_part1(input_data))

    print("Day 03 Part 2:")
    print(day03_part2(input_data))
