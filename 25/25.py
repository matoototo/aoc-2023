import sys
from collections import Counter
import random

class Node:
    def __init__(self, name):
        self.name = name
        self.neighbors = set()

class Edge:
    def __init__(self, node_1, node_2):
        self.node_1 = node_1
        self.node_2 = node_2

    def __eq__(self, other):
        return self.node_1 == other.node_1 and self.node_2 == other.node_2 or \
                self.node_1 == other.node_2 and self.node_2 == other.node_1
    
    def __hash__(self):
        return hash(self.node_1) + hash(self.node_2)
    
    def __repr__(self):
        return f'({self.node_1}, {self.node_2})'

def parse_nodes(lines):
    node_names = set()
    for line in lines:
        node_names.update(line.replace(':', '').split(' '))
    return {name: Node(name) for name in node_names}

def connect_nodes(lines, node_dict):
    for line in lines:
        source, destinations = line.split(': ')
        for destination in destinations.split(' '):
            node_dict[source].neighbors.add(node_dict[destination])
            node_dict[destination].neighbors.add(node_dict[source])

def expand_set(perimeter_set):
    new_set = set()
    for node in perimeter_set:
        new_set.update(node.neighbors)
    return new_set

def expand_full(node_set):
    while True:
        new_set = expand_set(node_set)
        if new_set == node_set: return new_set
        node_set.update(new_set)

def all_edges(node_dict):
    edges = set()
    for node in node_dict.values():
        for neighbor in node.neighbors:
            if (neighbor.name, node.name) in edges: continue
            edges.add((node.name, neighbor.name))
    return edges

def check_connected(start, end):
    return end in expand_full({start})

def disconnect(node_dict, edge):
    node_dict[edge.node_1].neighbors.remove(node_dict[edge.node_2])
    node_dict[edge.node_2].neighbors.remove(node_dict[edge.node_1])

def connect(node_dict, edge):
    node_dict[edge.node_1].neighbors.add(node_dict[edge.node_2])
    node_dict[edge.node_2].neighbors.add(node_dict[edge.node_1])

def connect_set(node_dict, edge_set):
    for edge in edge_set:
        connect(node_dict, edge)

def disconnect_set(node_dict, edge_set):
    for edge in edge_set:
        disconnect(node_dict, edge)

def random_edge_disjoint_path(start, end):
    visited_nodes = set()
    path = []
    current_node = start
    while current_node != end:
        candidates = list(current_node.neighbors.difference(visited_nodes))
        if not candidates: return random_edge_disjoint_path(start, end)
        next_node = random.choice(candidates)
        path.append(Edge(current_node.name, next_node.name))
        current_node = next_node
        visited_nodes.add(current_node)
    return path

def random_node(node_dict):
    return random.choice(list(node_dict.values()))

def part_1(lines):
    node_dict = parse_nodes(lines)
    connect_nodes(lines, node_dict)
    n_sample = int(1e3)
    while True:
        counter = Counter()
        for i in range(n_sample):
            path = random_edge_disjoint_path(random_node(node_dict), random_node(node_dict))
            for edge in path:
                counter[edge] += 1
        disconnect_edges = counter.most_common(3)
        disconnect_set(node_dict, [edge for edge, _ in disconnect_edges])
        sampled_node = random_node(node_dict)
        subgraph = expand_full({sampled_node})
        if len(subgraph) != len(node_dict):
            return len(subgraph) * (len(node_dict) - len(subgraph))
        connect_set(node_dict, [edge for edge, _ in disconnect_edges])

def part_2(lines):
    return -1

if __name__ == '__main__':
    lines = [line.rstrip('\n') for line in sys.stdin if line.rstrip('\n')]
    print(part_1(lines))
    print(part_2(lines))
