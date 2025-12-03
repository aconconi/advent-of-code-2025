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


def largest_joltage(bank, n=2):
    print(f"\n{bank=}")
    digits = [0] * n
    for i, battery in enumerate(bank):
        print(f"\n{i=} {battery=} {digits=}")
        for j in range(n):
            print(f"{j=} {digits[j]=} {len(bank) - n + j}")
            if battery > digits[j] and i <= len(bank) - n + j :
                digits[j] = battery
                digits[j+1:] = [0] * (n - j - 1)
                print(f"{digits=}")
                break

    print(digits)
    result = sum(
        digit * 10 ** i
        for i, digit in enumerate(reversed(digits))
    )
    return result

def day03_part1(banks):
    return sum(
        largest_joltage(bank, 2)
        for bank in banks
    )


def day03_part2(banks):
    return sum(
        largest_joltage(bank, 12)
        for bank in banks
    )



@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day03_test.txt")


def test_day03_part1(test_data):
    assert day03_part1(test_data) == 357

def test_day03_part2(test_data):
    assert day03_part2(test_data) == 3121910778619


if __name__ == "__main__":
    input_data = parse_input("data/day03.txt")

    print("Day 03 Part 1:")
    print(day03_part1(input_data))

    print("Day 03 Part 2:")
    print(day03_part2(input_data))
