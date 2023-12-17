import sys
import heapq

class Node:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        # left, right, up, down
        self.neighbours = []
        self.neighbours_str = ["l", "r", "u", "d"]
        # 123left, 123right, 123up, 123down
        self.distances = {f"{i}{d}": float('inf') for i in range(1, 4) for d in ['l', 'r', 'u', 'd']}

    def __repr__(self):
        return f'({self.x}, {self.y}):{self.value}'
    
    def __lt__(self, other):
        return self.value < other.value

    def moves(self, crucible_state):
        potential = set()
        move_map = {'l': [0, 2, 3], 'r': [1, 2, 3], 'u': [0, 1, 2], 'd': [0, 1, 3]}
        for move in move_map[crucible_state[-1]]:
            n_steps = int(crucible_state[0])
            next_direction = self.neighbours_str[move]
            if next_direction == crucible_state[-1]:
                if "3" in crucible_state: continue
                n_steps += 1
            else:
                n_steps = 1
            next_state = f"{n_steps}{next_direction}"
            if self.neighbours[move]:
                potential.add((next_state, self.neighbours[move]))
        return potential

class UltraNode:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        # left, right, up, down
        self.neighbours = []
        self.neighbours_str = ["l", "r", "u", "d"]
        # 123left, 123right, 123up, 123down
        self.distances = {f"{i}{d}": float('inf') for i in range(1, 11) for d in ['l', 'r', 'u', 'd']}

    def __repr__(self):
        return f'({self.x}, {self.y}):{self.value}'
    
    def __lt__(self, other):
        return self.value < other.value

    def moves(self, crucible_state):
        potential = set()
        move_map = {'l': [0, 2, 3], 'r': [1, 2, 3], 'u': [0, 1, 2], 'd': [0, 1, 3]}
        for move in move_map[crucible_state[-1]]:
            n_steps = int(crucible_state[0]) if len(crucible_state) == 2 else int(crucible_state[:2])
            next_direction = self.neighbours_str[move]
            if next_direction == crucible_state[-1]:
                if "10" in crucible_state: continue
                n_steps += 1
            elif n_steps < 4:
                continue
            else:
                n_steps = 1
            next_state = f"{n_steps}{next_direction}"
            if self.neighbours[move]:
                potential.add((next_state, self.neighbours[move]))
        return potential

def create_graph(lines, part_2=False):
    graph = {}
    for y, line in enumerate(lines):
        for x, value in enumerate(line):
            graph[(x, y)] = Node(x, y, int(value)) if not part_2 else UltraNode(x, y, int(value))
    for y, line in enumerate(lines):
        for x, _ in enumerate(line):
            for nidx, neighbour in enumerate([(x-1, y), (x+1, y), (x, y+1), (x, y-1)]):
                if neighbour in graph:
                    graph[(x, y)].neighbours.append(graph[neighbour])
                else:
                    graph[(x, y)].neighbours.append(None)
    return graph

def construct_unvisited_set(graph, current_node, part_2=False):
    unvisited_set = set()
    unvisited_queue = []
    max_steps = 10 if part_2 else 3
    states = set([f"{i}{d}" for i in range(1, max_steps+1) for d in ['l', 'r', 'u', 'd']])
    for node in graph.values():
        # if node == current_node: continue
        unvisited_set.update(set([(state, node) for state in states]))
        for state in states:
            heapq.heappush(unvisited_queue, (node.distances[state], (state, node)))
    return unvisited_set, unvisited_queue

def count_unvisited(unvisited_set, node):
    return sum([1 for state, n in unvisited_set if n == node])

def part_1(lines):
    graph = create_graph(lines)
    current_node = graph[(0, 0)]
    current_node.distances = {f"{i}{d}": 0 for i in range(1, 4) for d in ['l', 'r', 'u', 'd']}
    target_node = graph[max(graph.keys())]
    crucible_state = "1r" # Also try "1d"
    unvisited_set, unvisited_queue = construct_unvisited_set(graph, current_node)
    start = True
    while unvisited_set:
        # print(len(unvisited_set))
        for next_state, neighbour in current_node.moves(crucible_state):
            if (next_state, neighbour) in unvisited_set:
                distance = current_node.distances[crucible_state] + neighbour.value
                if distance < neighbour.distances[next_state]:
                    neighbour.distances[next_state] = distance
                    heapq.heappush(unvisited_queue, (distance, (next_state, neighbour)))
        if not start: unvisited_set.remove((crucible_state, current_node))
        start = False
        if not unvisited_set:# or count_unvisited(unvisited_set, target_node) == 6:
            break
        while (crucible_state, current_node) not in unvisited_set:
            crucible_state, current_node = heapq.heappop(unvisited_queue)[1]
    return min([target_node.distances[state] for state in target_node.distances])

def ultra_can_stop(state):
    return len(state) == 3 or int(state[0]) > 3

def part_2(lines):
    graph = create_graph(lines, part_2=True)
    current_node = graph[(0, 0)]
    current_node.distances = {f"{i}{d}": 0 for i in range(1, 11) for d in ['l', 'r', 'u', 'd']}
    target_node = graph[max(graph.keys())]
    # crucible_state = "1r" # Also try "1d"
    crucible_state = "1r"
    unvisited_set, unvisited_queue = construct_unvisited_set(graph, current_node, part_2=True)
    start = True
    while unvisited_set:
        # print(len(unvisited_set))
        for next_state, neighbour in current_node.moves(crucible_state):
            if (next_state, neighbour) in unvisited_set:
                distance = current_node.distances[crucible_state] + neighbour.value
                if distance < neighbour.distances[next_state]:
                    neighbour.distances[next_state] = distance
                    heapq.heappush(unvisited_queue, (distance, (next_state, neighbour)))
        if not start: unvisited_set.remove((crucible_state, current_node))
        start = False
        if not unvisited_set:
            break
        while (crucible_state, current_node) not in unvisited_set:
            crucible_state, current_node = heapq.heappop(unvisited_queue)[1]
    return min([target_node.distances[state] for state in target_node.distances if ultra_can_stop(state)])

if __name__ == '__main__':
    lines = [line.rstrip('\n') for line in sys.stdin if line.rstrip('\n')]
    print(part_1(lines))
    print(part_2(lines))
