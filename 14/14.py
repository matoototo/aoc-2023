import sys
from tqdm import tqdm

def drop_stone(lines, x, y):
    if lines[y][x] != 'O': return
    if y == 0: return
    if lines[y-1][x] == '.':
        lines[y-1] = lines[y-1][:x] + 'O' + lines[y-1][x+1:]
        lines[y] = lines[y][:x] + '.' + lines[y][x+1:]
        drop_stone(lines, x, y-1)

def rotate_lines(lines):
    new_lines = []
    for i in range(len(lines[0])):
        new_line = ''
        for line in lines:
            new_line += line[i]
        new_lines.append(new_line[::-1])
    return new_lines

def simulate_gravity(lines):
    for line_idx, line in enumerate(lines[:]):
        for char_idx, char in enumerate(line):
            drop_stone(lines, char_idx, line_idx)

def part_1(lines):
    simulate_gravity(lines)
    return calculate_load(lines)

def calculate_load(lines):
    load = 0
    for i, line in enumerate(lines):
        factor = len(line) - i
        load += line.count('O') * factor
    return load

def cycle(lines):
    for i in range(4):
        simulate_gravity(lines)
        lines = rotate_lines(lines)
    return lines

def hash_lines(lines):
    return ''.join(lines)

def part_2(lines):
    past_states = {}
    i = 0
    n_iters = 1000000000
    while i < n_iters - 1:
        lines = cycle(lines)
        h = hash_lines(lines)
        cycle_length = n_iters
        if h in past_states: cycle_length = i - past_states[h]
        if cycle_length < n_iters - i:
            i += cycle_length * ((n_iters - i) // cycle_length)
        else:
            past_states[h] = i
            i += 1
    return calculate_load(lines)

if __name__ == '__main__':
    lines = [line.rstrip('\n') for line in sys.stdin if line.rstrip('\n')]
    print(part_1(lines))
    print(part_2(lines))
