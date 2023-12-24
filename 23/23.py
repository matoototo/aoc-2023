import sys

sys.setrecursionlimit(10000)

class Node:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.neighbors = []
        self.visited = False
        self.distance = 1
        self.straight_line_neighbours = False

def parse_nodes(lines, part_2=False):
    nodes = []
    for y, line in enumerate(lines):
        for x, type in enumerate(line):
            new_type = type
            node = Node(x, y, new_type)
            nodes.append(node)

    node_dict = {(node.x, node.y): node for node in nodes}
    for node in nodes:
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for direction in directions:
            other = node_dict.get((node.x + direction[0], node.y + direction[1]))
            if not other: continue
            if node == other or other.type == '#': continue
            if node.x == other.x and abs(node.y - other.y) == 1:
                if not part_2:
                    if other.type in ['>', '<']: continue
                    if other.type == '^' and node.y - other.y == -1: continue
                    if other.type == 'v' and node.y - other.y == 1: continue
                node.neighbors.append(other)
            if node.y == other.y and abs(node.x - other.x) == 1:
                if not part_2:
                    if other.type in ['^', 'v']: continue
                    if other.type == '>' and node.x - other.x == 1: continue
                    if other.type == '<' and node.x - other.x == -1: continue
                node.neighbors.append(other)
    return collapse_nodes(nodes)

def collapse_nodes(nodes):
    did_change = False
    while True:
        for node in nodes:
            if node.type == "." and len(node.neighbors) == 2 and all([neighbor.type == '.' for neighbor in node.neighbors]):
                for neighbor in node.neighbors:
                    neighbor.neighbors.remove(node)
                node.neighbors[0].neighbors.append(node.neighbors[1])
                node.neighbors[1].neighbors.append(node.neighbors[0])
                node.neighbors[0].distance += node.distance
                node.neighbors = []
                did_change = True
        if not did_change: break
        did_change = False
    return [node for node in nodes if node.neighbors and node.type != '#']

def all_paths(start, end):
    if start == end:
        return [[start]]
    paths = []
    for neighbor in start.neighbors:
        if neighbor.visited: continue
        neighbor.visited = True
        for path in all_paths(neighbor, end):
            paths.append([start] + path)
        neighbor.visited = False
    return paths

def part_1(lines):
    nodes = parse_nodes(lines)
    start_node = [node for node in nodes if node.type == '.' and node.y == 0][0]
    end_node = [node for node in nodes if node.type == '.' and node.y == len(lines)-1][0]
    paths = all_paths(start_node, end_node)
    return max(sum([p.distance for p in path]) for path in paths) - 1

def part_2(lines):
    nodes = parse_nodes(lines, part_2=True)
    start_node = [node for node in nodes if node.type == '.' and node.y == 0][0]
    end_node = [node for node in nodes if node.type == '.' and node.y == len(lines)-1][0]
    paths = all_paths(start_node, end_node)
    return max(sum([p.distance for p in path]) for path in paths) - 1

if __name__ == '__main__':
    lines = [line.rstrip('\n') for line in sys.stdin if line.rstrip('\n')]
    print(part_1(lines))
    print(part_2(lines))
