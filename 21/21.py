import sys
from collections import defaultdict

class Node:
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y
        self.neighbors = []
        self.left_grid = None
        self.right_grid = None
        self.above_grid = None
        self.below_grid = None

    def __repr__(self):
        return f'{self.type}({self.x}, {self.y})'

def connect_neighbours(nodes, part_2=False):
    neighbour_indices = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for node in nodes.values():
        x = node.x
        y = node.y
        for index in neighbour_indices:
            neighbour = nodes.get((x + index[0], y + index[1]))
            if neighbour:
                node.neighbors.append(neighbour)

    if part_2: # wrap around
        max_x = max([node.x for node in nodes.values()])
        max_y = max([node.y for node in nodes.values()])
        for node in nodes.values():
            x = node.x
            y = node.y
            if x == 0:
                # node.neighbors.append(nodes[(max_x, y)])
                node.left_grid = nodes[(max_x, y)]
            elif x == max_x:
                # node.neighbors.append(nodes[(0, y)])
                node.right_grid = nodes[(0, y)]
            if y == 0:
                # node.neighbors.append(nodes[(x, max_y)])
                node.above_grid = nodes[(x, max_y)]
            elif y == max_y:
                # node.neighbors.append(nodes[(x, 0)])
                node.below_grid = nodes[(x, 0)]


def step(node_set,):
    new_node_set = set()
    for node in node_set:
        for neighbour in node.neighbors:
            if neighbour.type in ['.', 'S']:
                new_node_set.add(neighbour)
    return new_node_set

def step_2(node_set, grid_coords):
    result = defaultdict(set)
    for node in node_set:
        for neighbour in node.neighbors:
            if neighbour.type in ['.', 'S']:
                result[grid_coords].add(neighbour)
        if node.left_grid:
            # print("entry:", node.left_grid)
            result[(grid_coords[0] - 1, grid_coords[1])].add(node.left_grid)
        if node.right_grid:
            # print("entry:", node.right_grid)
            result[(grid_coords[0] + 1, grid_coords[1])].add(node.right_grid)
        if node.above_grid:
            # print("entry:", node.above_grid)
            result[(grid_coords[0], grid_coords[1] - 1)].add(node.above_grid)
        if node.below_grid:
            # print("entry:", node.below_grid)
            result[(grid_coords[0], grid_coords[1] + 1)].add(node.below_grid)
    return result

def prepare_map(lines, part_2=False):
    nodes = {}
    start_node = None
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            nodes[(x, y)] = Node(char, x, y)
            if char == 'S': start_node = nodes[(x, y)]
    connect_neighbours(nodes, part_2)
    return nodes, start_node

def part_1(lines):
    nodes, start_node = prepare_map(lines)
    node_set = set([start_node])
    for i in range(64):
        node_set = step(node_set)
    return len(node_set)

def is_oscilating(prev_lens):
    if len(prev_lens) < 4: return False
    return prev_lens[-1] == prev_lens[-3] and prev_lens[-2] == prev_lens[-4]

def part_2(lines):
    nodes, start_node = prepare_map(lines, part_2=True)
    node_set = defaultdict(set)
    node_set[(0, 0)].add(start_node)
    lens = defaultdict(list)
    lens[(0, 0)].append(1)
    oscilating = set()
    oscilating_coords = set()
    oscilating_step = None
    for i in range(1000):
        new_node_set = defaultdict(set)
        for grid_coords, nodes in node_set.items():
            if grid_coords in oscilating_coords: continue
            result = step_2(nodes, grid_coords)
            if is_oscilating(lens[grid_coords]) and grid_coords not in oscilating_coords:
                oscilating.add((grid_coords, i))
                oscilating_coords.add(grid_coords)
                if not oscilating_step: oscilating_step = i - 1
                print(f'oscilating at {grid_coords} at {i}')
                break
            for grid_coords_result, nodes_result in result.items():
                new_node_set[grid_coords_result] = new_node_set[grid_coords_result].union(nodes_result)
        for grid_coords, nodes in new_node_set.items():
            lens[grid_coords].append(len(nodes))
        node_set = new_node_set
    n_oscilating = 1
    n_oscilating_even = 1 if oscilating_step % 2 == 0 else 0
    n_oscilating_odd = 1 if oscilating_step % 2 == 1 else 0
    current_n = 0
    target_step = 26501365
    target_step = 5000
    grid_coords_set = set([(0, 0)])
    for i in range(oscilating_step + 1, target_step+1, oscilating_step):
        # new_grid_coords = set()
        # for grid_coords in grid_coords_set:
        #     for x, y in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        #         new_coords = (x + grid_coords[0], y + grid_coords[1])
        #         if abs(new_coords[0]) + abs(new_coords[1]) != i // oscilating_step: continue
        #         new_grid_coords.add((x + grid_coords[0], y + grid_coords[1]))
        # grid_coords_set = new_grid_coords
        # manhattan = [abs(x) + abs(y) for x, y in grid_coords_set]
        # print(i // oscilating_step, manhattan[0])
        # assert all(manhattan[0] == m for m in manhattan)
        n_oscilating += current_n
        n_oscilating_even += current_n if i % 2 == 0 else 0
        n_oscilating_odd += current_n if i % 2 == 1 else 0
        current_n += 4 if i != 1 else 3
        print(i // oscilating_step, current_n, n_oscilating)
    to_simulate_steps = target_step % oscilating_step
    print(n_oscilating_even, n_oscilating_odd, n_oscilating_even*lens[(0, 0)][-2] + n_oscilating_odd*lens[(0, 0)][-1])
    print(oscilating_step, n_oscilating, n_oscilating * lens[(0, 0)][-1], to_simulate_steps)#, len(grid_coords_set))
    return sum([len(nodes) for nodes in node_set.values()])

if __name__ == '__main__':
    lines = [line.rstrip('\n') for line in sys.stdin if line.rstrip('\n')]
    print(part_1(lines))
    print(part_2(lines))
