import sys

solutions = {}

def is_valid(state, sizes):
    split_state = [group for group in state.split(".") if group]
    return len(split_state) == len(sizes) and all([len(group) == size for group, size in zip(split_state, sizes)])

def is_done(state, sizes):
    if not state and not sizes: return 1
    if not state and sum(sizes): return 0
    if "#" in state and not sizes: return 0
    return None

def solve_line_recurse(state, sizes):
    if state+repr(sizes) in solutions: return solutions[state+repr(sizes)]
    done = is_done(state, sizes)
    if done is not None:
        solutions[state+repr(sizes)] = done
        return done
 
    if state[0] == '#':
        if len(state) < sizes[0]: return 0
        next_n = state[:sizes[0]]
        if '.' in next_n: return 0
        state = state[sizes[0]:]
        sizes = sizes[1:]
            
        done = is_done(state, sizes)
        if done is not None:
            solutions[state+repr(sizes)] = done
            return done

        if state[0] == '#': return 0
        else: state = state[1:]
    elif state[0] == '?':
        solution = solve_line_recurse('.' + state[1:], sizes[:]) + solve_line_recurse('#' + state[1:], sizes[:])
        solutions[state+repr(sizes)] = solution
        return solution
    else:
        state = state[1:]
    solution = solve_line_recurse(state[:], sizes[:])
    solutions[state+repr(sizes)] = solution
    return solution

def parse_line(line, factor = 1):
    state, sizes = line.split(" ")
    sizes = [int(size) for size in sizes.split(",")]
    return "?".join(state for i in range(factor)), sizes * factor

def part_1(lines):
    return sum([solve_line_recurse(*parse_line(line)) for line in lines])

def part_2(lines):
    return sum([solve_line_recurse(*parse_line(line, 5)) for line in lines])

if __name__ == '__main__':
    lines = [line.rstrip('\n') for line in sys.stdin if line.rstrip('\n')]
    print(part_1(lines))
    print(part_2(lines))
