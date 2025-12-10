"""
Advent of Code 2025
Day 10:
"""

import re
from dataclasses import dataclass

import pytest

# Type aliases
Matrix = list[list[int]]
Vector = list[int]
PivotCols = list[int]


@dataclass
class Machine:
    lights: list[int]
    buttons: list[list[int]]
    joltage: list[int]

    @classmethod
    def from_line(cls, line: str) -> "Machine":
        """Parse a machine from a data line."""
        # Extract lights: [.##.]
        lights_match = re.search(r"\[([\\.#]+)\]", line)
        lights = (
            [1 if c == "#" else 0 for c in lights_match.group(1)]
            if lights_match
            else []
        )

        # Extract buttons: (2,3,4,5,6,7,8) (0,1,2,3,7) ...
        buttons_matches = re.findall(r"\(([0-9,]*)\)", line)
        buttons = []
        for match in buttons_matches:
            if match:
                buttons.append([int(x) for x in match.split(",")])
            else:
                buttons.append([])

        # Extract joltage: {13,30,32,41,36,25,29,24,45}
        joltage_match = re.search(r"\{([0-9,]+)\}", line)
        joltage = (
            [int(x) for x in joltage_match.group(1).split(",")] if joltage_match else []
        )

        return cls(lights=lights, buttons=buttons, joltage=joltage)

    def solve_turn_on(self) -> int | None:
        """Solve the lights puzzle using boolean linear algebra over GF(2).

        Returns the minimum number of buttons to press, or None if no solution exists.
        """
        # Build matrix a where a[i][j] = 1 if button j affects light i
        a = [
            [1 if i in button_indices else 0 for button_indices in self.buttons]
            for i in range(len(self.lights))
        ]
        solution = solve_system_gf2_minweight(a, self.lights)
        return solution.count(1) if solution else None


def parse_input(file_name: str) -> list[Machine]:
    with open(file_name, "r", encoding="ascii") as data_file:
        return [Machine.from_line(line) for line in data_file]


def gauss_jordan_gf2(augmented: Matrix) -> PivotCols | None:
    """Gaussian elimination in GF(2) on augmented matrix.

    Returns pivot column indices, or None if the system is inconsistent.
    """
    m = len(augmented)  # number of rows
    n = len(augmented[0])  # number of columns
    pivot_cols: PivotCols = []
    current_row = 0

    for col in range(n - 1):  # exclude the augmented column
        pivot = next((i2 for i2 in range(current_row, m) if augmented[i2][col]), None)
        if pivot is None:
            continue
        if current_row != pivot:
            augmented[current_row], augmented[pivot] = (
                augmented[pivot],
                augmented[current_row],
            )

        pivot_cols.append(col)

        for i2 in range(m):
            if i2 == current_row or not augmented[i2][col]:
                continue
            for j in range(n):
                augmented[i2][j] ^= augmented[current_row][j]

        current_row += 1

    # Check for inconsistency: row with all zeros in coefficient part but 1 in augmented column
    for row in augmented:
        if all(row[j] == 0 for j in range(n - 1)) and row[-1] == 1:
            return None

    return pivot_cols


def solve_system_gf2_minweight(a: Matrix, b: Vector) -> Vector | None:
    """Solve Ax=b in GF(2), returning the minimum-weight solution, or None if no solution exists."""
    m = len(a)  # number of rows (equations)
    n = len(a[0])  # number of columns (variables)

    # Augment matrix with b
    augmented: Matrix = [row + [item] for row, item in zip(a, b)]
    pivot_cols = gauss_jordan_gf2(augmented)

    # No solution if system is inconsistent
    if pivot_cols is None:
        return None

    # Free variables are those without a pivot
    free_cols = [i for i in range(n) if i not in pivot_cols]

    # Try all combinations of free variables
    min_solution: Vector | None = None
    min_weight = float("inf")

    for mask in range(1 << len(free_cols)):
        # Set free variables according to mask
        solution: Vector = [0] * n
        for i, col in enumerate(free_cols):
            solution[col] = (mask >> i) & 1

        # Back-substitute for dependent variables
        for row_idx, col in enumerate(pivot_cols):
            val = augmented[row_idx][-1]  # RHS
            for j in range(col + 1, n):
                if j not in pivot_cols:
                    val ^= augmented[row_idx][j] & solution[j]
            solution[col] = val

        # Count 1s
        weight = sum(solution)
        if weight < min_weight:
            min_weight = weight
            min_solution = solution

    return min_solution


def day10_part1(machines: list[Machine]) -> int:
    return sum(
        result
        for result in (machine.solve_turn_on() for machine in machines)
        if result is not None
    )


def day10_part2(machines: list[Machine]) -> int:
    pass


"""
@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day10_test.txt")


def test_day10_part1(test_data):
    assert day10_part1(test_data) == 7

def test_day10_part2(test_data):
    assert day10_part2(test_data)
"""

if __name__ == "__main__":
    input_data = parse_input("data/day10.txt")

    print("Day 10 Part 1:")
    print(day10_part1(input_data))

    print("Day 10 Part 2:")
    print(day10_part2(input_data))
