"""
Advent of Code 2025
Day 07: Laboratories
"""


def parse_input(file_name: str) -> list[str]:
    with open(file_name, "r", encoding="ascii") as data_file:
        return data_file.read().splitlines()


def day07_part1(data: list[str]) -> None:
    def step_beam(char, i, j):
        if char not in "S|":
            return 0
        below = grid[i + 1][j]
        if below == "|":
            return 0
        elif below == ".":
            grid[i + 1][j] = "|"
            return 0
        else:
            # below is "^"
            grid[i + 1][j - 1] = "|"
            grid[i + 1][j + 1] = "|"
            return 1

    count_splits = 0
    grid = [list(line) for line in data]
    for i, row in enumerate(grid[:-1]):
        for j, char in enumerate(row):
            count_splits += step_beam(char, i, j)
        print("\n")
        for row in grid:
            print("".join(row))

    return count_splits


def day07_part2(data: list[str]) -> None:
    pass


"""
@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day07_test.txt")


def test_day07_part1(test_data):
    assert day07_part1(test_data) == 21

def test_day07_part2(test_data):
    assert day07_part2(test_data)
"""

if __name__ == "__main__":
    input_data = parse_input("data/day07.txt")

    print("Day 07 Part 1:")
    print(day07_part1(input_data))

    print("Day 07 Part 2:")
    print(day07_part2(input_data))
