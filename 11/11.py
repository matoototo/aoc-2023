import sys
import numpy as np
from itertools import product

class Galaxy:
    def __init__(self, pos):
        self.pos = pos

    def __repr__(self):
        return f"Galaxy({self.pos})"
    
    def distance(self, other):
        return abs(self.pos[0] - other.pos[0]) + abs(self.pos[1] - other.pos[1])

def populate_galaxies(lines, gap=1):
    empty_row_indices = empty_rows(lines)
    empty_col_indices = empty_cols(lines)
    galaxies = []
    for row_i, line in enumerate(lines):
        for col_i, char in enumerate(line):
            if char != "#": continue
            pos_row = row_i + sum([gap for i in empty_row_indices if i < row_i])
            pos_col = col_i + sum([gap for i in empty_col_indices if i < col_i])
            galaxies.append(Galaxy((pos_row, pos_col)))
    return galaxies

def empty_rows(lines):
    indices = []
    for i, line in enumerate(lines):
        if "#" not in line: indices.append(i)
    return indices

def empty_cols(lines):
    return empty_rows(np.array([list(line) for line in lines]).T)

def part_1(lines):
    galaxies = populate_galaxies(lines)
    distances = 0
    for g1, g2 in product(galaxies, galaxies):
        if g1 == g2: continue
        distances += g1.distance(g2)
    return int(distances / 2)

def part_2(lines):
    galaxies = populate_galaxies(lines, gap=1e6-1)
    distances = 0
    for g1, g2 in product(galaxies, galaxies):
        if g1 == g2: continue
        distances += g1.distance(g2)
    return int(distances / 2)

if __name__ == '__main__':
    lines = [line.rstrip('\n') for line in sys.stdin if line.rstrip('\n')]
    print(part_1(lines))
    print(part_2(lines))
