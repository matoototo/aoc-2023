import sys
from itertools import cycle
import math

class Node:
    def __init__(self, line):
        line = line.split(' = ')
        self.name = line[0]
        self.left = line[1].split(',')[0][1:].strip()
        self.right = line[1].split(',')[1][:-1].strip()

    def transition(self, move, node_map):
        if move == 'L':
            return node_map[self.left]
        elif move == 'R':
            return node_map[self.right]

def length(current_node, node_map, movelist, part_2=False):
    step = 0
    for move in cycle(movelist):
        if not part_2 and (current_node.name == 'ZZZ'): break
        if part_2 and (current_node.name[-1] == 'Z'): break
        step += 1
        current_node = current_node.transition(move, node_map)
    assert step % len(movelist) == 0
    return step

def part_1(lines):
    nodes = [Node(line) for line in lines[1:]]
    node_map = {node.name: node for node in nodes}
    current_node = node_map['AAA']
    return length(current_node, node_map, lines[0])

def part_2(lines):
    nodes = [Node(line) for line in lines[1:]]
    node_map = {node.name: node for node in nodes}
    current_nodes = [node_map[x] for x in node_map.keys() if x[-1] == 'A']
    lengths = [length(current_node, node_map, lines[0], True) for current_node in current_nodes]
    return math.lcm(*lengths)

if __name__ == '__main__':
    lines = [line.rstrip('\n') for line in sys.stdin if line.rstrip('\n')]
    print(part_1(lines))
    print(part_2(lines))
