"""
Advent of Code 2025
Day 12: Christmas Tree Farm
"""

from dataclasses import dataclass


@dataclass
class Region:
    width: int
    height: int
    shape_counters: list[int]

    @property
    def size(self) -> int:
        return self.width * self.height


def parse_input(file_name: str) -> list[Region]:
    with open(file_name, "r", encoding="ascii") as data_file:
        lines = data_file.read().splitlines()
    regions = []
    for line in lines:
        if "x" not in line:
            continue
        line = line.replace("x", " ").replace(":", " ")
        numbers = [int(x) for x in line.split()]
        regions.append(Region(numbers[0], numbers[1], numbers[2:]))
    return regions


def day12_part1(regions: list[Region]) -> int:
    return sum(region.size >= 9 * sum(region.shape_counters) for region in regions)


if __name__ == "__main__":
    input_data = parse_input("data/day12.txt")

    print("Day 12 Part 1:")
    print(day12_part1(input_data))

    # There is no part 2 to be solved on this day :-)
