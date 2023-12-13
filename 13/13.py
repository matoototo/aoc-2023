import sys
import numpy as np

def is_reflection(line, i):
    length = min(i, len(line) - i)
    return line[i-length:i] == line[i:i+length][::-1]

def find_reflection(pattern, skip_solution=-1):
    for i in range(1, len(pattern[0])):
        if all([is_reflection(line, i) for line in pattern]) and i != skip_solution:
            return i
    return False

def transpose_list_of_strings(pattern):
    return [''.join(line) for line in np.array([list(line) for line in pattern]).T]

def find_reflection_score(pattern, skip_solution=-1):
    reflection = find_reflection(pattern, skip_solution)
    if not reflection or reflection == skip_solution:
        reflection = find_reflection(transpose_list_of_strings(pattern), skip_solution // 100)
        reflection *= 100
    return reflection

def parse_patterns(lines):
    pattern = []
    patterns = []
    for line in lines:
        if not line:
            patterns.append(pattern)
            pattern = []
            continue
        pattern.append(line)
    patterns.append(pattern)
    return patterns

def part_1(lines):
    patterns = parse_patterns(lines)
    solution = 0
    for pattern in patterns:
        reflection = find_reflection_score(pattern)
        solution += reflection

    return solution

def desmudge_generator(pattern):
    for i in range(len(pattern)):
        for j in range(len(pattern[0])):
            copy_pattern = pattern.copy()
            if copy_pattern[i][j] == '.':
                copy_pattern[i] = copy_pattern[i][:j] + '#' + copy_pattern[i][j+1:]
            elif copy_pattern[i][j] == '#':
                copy_pattern[i] = copy_pattern[i][:j] + '.' + copy_pattern[i][j+1:]
            else:
                raise Exception("Invalid character")
            yield copy_pattern

def part_2(lines):
    patterns = parse_patterns(lines)
    solution = 0
    for pattern in patterns:
        original_score = find_reflection_score(pattern)
        for desmudged_pattern in desmudge_generator(pattern):
            reflection = find_reflection_score(desmudged_pattern, skip_solution=original_score)
            if not reflection or reflection == original_score:
                continue
            solution += reflection
            break
    return solution

if __name__ == '__main__':
    lines = [line.rstrip('\n') for line in sys.stdin]
    print(part_1(lines))
    print(part_2(lines))
