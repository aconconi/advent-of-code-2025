"""
Advent of Code 2025
Day 06:
"""

# pylint: skip-file
from math import prod

import pytest

OPS = {"*": prod, "+": sum}


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return data_file.read().splitlines()


def day06_part1(data: list[str]) -> int:
    columns = zip(*(map(int, line.split()) for line in data[:-1]))
    operations = data[-1].split()
    return sum(OPS[op](map(int, values)) for values, op in zip(columns, operations))


def day06_part2(data: list[str]) -> int:
    lines = [line.ljust(max(map(len, data))) for line in data]
    columns = (
        "".join(line[i] for line in lines) for i in reversed(range(len(lines[0])))
    )

    def process_columns(columns):
        nums = []
        for col in columns:
            if not col.strip():
                continue
            nums.append(int(col[:-1]))
            if op := OPS.get(col[-1]):
                yield op(nums)
                nums = []

    return sum(process_columns(columns))


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day06_test.txt")


def test_day06_part1(test_data):
    assert day06_part1(test_data) == 4277556


def test_day06_part2(test_data):
    assert day06_part2(test_data) == 3263827


if __name__ == "__main__":
    input_data = parse_input("data/day06.txt")

    print("Day 06 Part 1:")
    print(day06_part1(input_data))

    print("Day 06 Part 2:")
    print(day06_part2(input_data))
