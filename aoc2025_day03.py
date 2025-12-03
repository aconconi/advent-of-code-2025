"""
Advent of Code 2025
Day 03: Lobby
"""

# pylint: skip-file
import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return [
            list(map(int, line))
            for line in data_file.read().splitlines()
        ]


def largest_joltage(bank):
    high_digit, low_digit = 0, 0
    for i, battery in enumerate(bank):
        if battery > high_digit and i < len(bank) - 1:
            # new best high_digit found
            high_digit = battery
            # invalidate low_digit because high_digit has been updated
            low_digit = 0
        elif battery > low_digit:
            low_digit = battery
        if high_digit == low_digit == 9:
            # maximum achieved, no need to continue
            break

    return high_digit * 10 + low_digit

def day03_part1(banks):
    return sum(
        largest_joltage(bank)
        for bank in banks
    )


def day03_part2(banks):
    pass


"""
@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day03_test.txt")


def test_day03_part1(test_data):
    assert day03_part1(test_data) == 357

def test_day03_part2(test_data):
    assert day03_part2(test_data)
"""

if __name__ == "__main__":
    input_data = parse_input("data/day03.txt")

    print("Day 03 Part 1:")
    print(day03_part1(input_data))

    print("Day 03 Part 2:")
    print(day03_part2(input_data))
