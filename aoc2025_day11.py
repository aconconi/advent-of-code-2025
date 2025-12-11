"""
Advent of Code 2025
Day 11: Reactor
"""

from functools import cache


def parse_input(file_name: str) -> dict[str, list[str]]:
    with open(file_name, "r", encoding="ascii") as data_file:
        lines = data_file.read().splitlines()
    devices = {"out": []}
    for line in lines:
        name, attached = line.split(":")
        devices[name] = attached.strip().split(" ")
    return devices


def count_paths_through_waypoints(graph: dict, waypoints: list) -> int:
    """Count all paths from source to dest passing through intermediate waypoints in order."""
    if len(waypoints) < 2:
        return 0

    source = waypoints[0]
    dest = waypoints[-1]

    @cache
    def dfs(current: str, waypoint_idx: int) -> int:
        # Base case: reached destination after all waypoints
        if waypoint_idx == len(waypoints) - 1:
            return 1 if current == dest else 0

        count = 0
        next_waypoint = waypoints[waypoint_idx + 1]

        # Explore neighbors
        for neighbor in graph[current]:
            # Advance waypoint_idx if we reach the next waypoint
            next_idx = waypoint_idx + 1 if neighbor == next_waypoint else waypoint_idx
            count += dfs(neighbor, next_idx)

        return count

    return dfs(source, 0)


def day11_part1(devices: dict[str, list[str]]) -> int:
    return count_paths_through_waypoints(devices, ["you", "out"])


def day11_part2(devices: dict[str, list[str]]) -> int:
    return count_paths_through_waypoints(devices, ["svr", "fft", "dac", "out"])


def test_day11_part1():
    test_data = parse_input("data/day11_test_part1.txt")
    assert day11_part1(test_data) == 5


def test_day11_part2():
    test_data = parse_input("data/day11_test_part2.txt")
    assert day11_part2(test_data) == 2


if __name__ == "__main__":
    input_data = parse_input("data/day11.txt")

    print("Day 11 Part 1:")
    print(day11_part1(input_data))

    print("Day 11 Part 2:")
    print(day11_part2(input_data))
