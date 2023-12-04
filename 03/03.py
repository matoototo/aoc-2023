import sys
from collections import defaultdict

def extract_digits_and_neighbours(lines, include_neighbour_index):
    neighbour_locations = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1), (0, 1)]
    len_line = len(lines[0])
    for line_index, line in enumerate(lines):
        if line_index in [0, len(lines)-1]:
            continue
        digits = ""
        neighbours = []
        neighbour_indices = []
        for i, c in enumerate(line):
            if i in [0, len(line)-1]:
                continue
            if c.isdigit():
                for x, y in neighbour_locations:
                    neighbour = lines[line_index + x][i + y]
                    neighbours.append(neighbour)
                    if include_neighbour_index and neighbour == "*":
                        neighbour_indices.append((line_index + x) * len_line + (i + y))
                digits += c
            elif digits:
                yield digits, neighbours, set(neighbour_indices) if include_neighbour_index else None
                neighbours = []
                neighbour_indices = []
                digits = ""
        if digits:
            yield digits, neighbours, set(neighbour_indices) if include_neighbour_index else None

def is_valid(neighbours):
    not_symbols = ".0123456789"
    return any(c not in not_symbols for c in neighbours)

def extract_numbers(lines):
    numbers = []
    for digits, neighbours, _ in extract_digits_and_neighbours(lines, False):
        if is_valid(neighbours):
            numbers.append(int(digits))
    return sum(numbers)

def extract_numbers_2(lines):
    gears = defaultdict(list)
    for digits, _, neighbour_indices in extract_digits_and_neighbours(lines, True):
        for index in neighbour_indices:
            gears[index].append(int(digits))
    return sum(v[0] * v[1] for v in gears.values() if len(v) == 2)

def pad_lines(lines):
    line_length = len(lines[0])
    padded_lines = ["." * line_length] + lines + ["." * line_length]
    return ["." + line + "." for line in padded_lines]

def part_1(lines):
    padded_lines = pad_lines(lines)
    return extract_numbers(padded_lines)

def part_2(lines):
    padded_lines = pad_lines(lines)
    return extract_numbers_2(padded_lines)

if __name__ == '__main__':
    lines = [line.rstrip('\n') for line in sys.stdin]
    print(part_1(lines))
    print(part_2(lines))
