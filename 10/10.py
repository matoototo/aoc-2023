
import sys
sys.setrecursionlimit(100000)
class Node:
    def __init__(self, type, pos):
        self.type = type
        self.pos = pos
        # left, right, up, down
        self.neighbours = []
        self.enclosed = None
        self.squeezable = False
        self.squeeze_entrance_exit = False

    def __hash__(self):
        return hash(self.pos)
    
    def __repr__(self):
        return self.type
        return f'Node({self.type}, {self.pos})'
    
    def __lt__(self, other):
        return self.type < other.type

    def flood(self, loop):
        for node in self.neighbours:
            if not node or node.enclosed is not None: continue
            if node in loop: continue
            node.enclosed = False
            node.flood(loop)

    def escape_flood(self, loop):
        for node in self.neighbours:
            if not node or node in loop or node.enclosed == False: continue
            node.enclosed = False
            node.escape_flood(loop)

    def next(self, trajectory):
        type_map = {
            '|': (2, 3),
            '-': (0, 1),
            'L': (2, 1),
            'J': (2, 0),
            '7': (0, 3),
            'F': (1, 3)
        }
        candidates = self.valid_neighbours()
        candidates = [node for node in candidates if node.type not in ['.'] and node not in trajectory]
        candidates_without_S = [node for node in candidates if node.type != 'S']
        if not candidates: return None
        # if len(trajectory) == 1:
        #     assert len(candidates_without_S) == 2
        return candidates_without_S[0] if candidates_without_S else candidates[0]

    def valid_neighbours(self):
        if self.type == '|':
            candidates = []
            if self.neighbours[2].type in "|7FS": candidates.append(self.neighbours[2])
            if self.neighbours[3].type in "|JLS": candidates.append(self.neighbours[3])
        elif self.type == '-':
            candidates = []
            if self.neighbours[0].type in "-FLS": candidates.append(self.neighbours[0])
            if self.neighbours[1].type in "-J7S": candidates.append(self.neighbours[1])
        elif self.type == 'L':
            candidates = []
            if self.neighbours[2].type in "|7FS": candidates.append(self.neighbours[2])
            if self.neighbours[1].type in "-J7S": candidates.append(self.neighbours[1])
        elif self.type == 'J':
            candidates = []
            if self.neighbours[2].type in "|7FS": candidates.append(self.neighbours[2])
            if self.neighbours[0].type in "-FLS": candidates.append(self.neighbours[0])
        elif self.type == '7':
            candidates = []
            if self.neighbours[3].type in "|JLS": candidates.append(self.neighbours[3])
            if self.neighbours[0].type in "-FLS": candidates.append(self.neighbours[0])
        elif self.type == 'F':
            candidates = []
            if self.neighbours[3].type in "|JLS": candidates.append(self.neighbours[3])
            if self.neighbours[1].type in "-J7S": candidates.append(self.neighbours[1])
        else:
            raise Exception("Unknown type", self.type)
        return candidates

    def is_squeeze_entrance(self, loop):
        if self not in loop and self.type != '.': return False
        if len([node for node in self.neighbours if node in loop or node and node.type == '.']) < 3: return False # Has to be a corner node
        direction = self.neighbours.index([node for node in self.neighbours if node not in loop][0])
        if direction in [0, 1]: return self.type not in ['|']
        if direction in [2, 3]: return self.type not in ['-']
        return True # TODO: Any other edgecases?
    
    def loop_neighbours(self, loop, with_ground = False):
        return [node for node in self.neighbours if node in loop] + ([node for node in self.neighbours if node and node.type == '.'] if with_ground else [])

def create_grid(lines):
    lines = ['.' + line + '.' for line in lines]
    lines = ['.' * len(lines[0])] + lines + ['.' * len(lines[0])]
    nodes = {}
    S_node = None
    for i, line in enumerate(lines[1:-1]):
        for j, type in enumerate(line[1:-1]):
            node = Node(type, (i, j))
            nodes[(i, j)] = node
            if type == 'S':
                assert S_node is None
                S_node = node
    attach_neighbours(nodes)
    return nodes, S_node

def part_1(lines):
    nodes, S_node = create_grid(lines)
    return len(find_loop_S(S_node)) // 2

def part_2(lines):
    nodes, S_node = create_grid(lines)
    loop = find_loop_S(S_node)
    loop_set = set(loop)
    edge_nodes = [node for node in nodes.values() if None in node.neighbours and node not in loop_set]
    for node in edge_nodes:
        node.enclosed = False
        node.flood(loop_set)
    not_enclosed = [node for node in nodes.values() if node.enclosed is False and node not in loop_set and node.type != 'S']
    enclosed = [node for node in nodes.values() if node not in not_enclosed and node not in loop_set and node.type != 'S']
    # print("Nodes:" , len(nodes))
    # print("Loop:" , len(loop))
    # print("Enclosed:" , len(enclosed))
    # print("Not enclosed:" , len(not_enclosed))
    last_squeeze_entrances = set()
    while True:
        new_squeeze_entrances = find_squeeze_entrances(not_enclosed, loop_set)
        print(sorted(list(new_squeeze_entrances)))
        if new_squeeze_entrances == last_squeeze_entrances: break
        last_squeeze_entrances = new_squeeze_entrances
        print("Marking...")
        for entrance in new_squeeze_entrances:
            entrance.squeezable = True
            entrance.squeeze_entrance_exit = True
            mark_squeeze_trail(entrance, loop)
        print("Flood...")
        squeezable = [node for node in nodes.values() if node.squeezable]
        # print("Squeezable:" , len(squeezable), squeezable)
        for squeeze_node in squeezable:
            if squeeze_node.squeeze_entrance_exit:
                non_loop_neighbour = [node for node in squeeze_node.neighbours if node not in loop_set and node][0]
                if not non_loop_neighbour.enclosed is False:
                    # This node can escape
                    non_loop_neighbour.enclosed = False
                    non_loop_neighbour.escape_flood(loop_set)
        new_not_enclosed = [node for node in nodes.values() if node.enclosed is False and node not in loop_set and node.type != 'S']
        enclosed = [node for node in nodes.values() if node not in new_not_enclosed and node not in loop_set and node.type != 'S']
        not_enclosed = new_not_enclosed
    print_grid(nodes, loop)
    return len(enclosed)

def mark_squeeze_trail(node, loop):
    start = loop.index(node)
    current_node = node
    flipped_loop = loop[::-1]
    next_node = loop[(start + 1)]
    previous_node = loop[(start - 1)]
    # TODO ground
    if len(next_node.loop_neighbours(loop)) >= 3:
        squeeze_trajectory = loop
        # assert len(previous_node.loop_neighbours(loop)) <= 2
    elif len(previous_node.loop_neighbours(loop)) >= 3:
        squeeze_trajectory = flipped_loop
        # assert len(next_node.loop_neighbours(loop)) <= 2
    else:
        print("Node:", node, node.neighbours)
        print("Next:", next_node, next_node.neighbours, len(next_node.loop_neighbours(loop)))
        print("Previous:", previous_node, previous_node.neighbours, len(previous_node.loop_neighbours(loop)))
        raise Exception("This shouldn't happen")
    
    start = squeeze_trajectory.index(node)
    for i in range(start, len(squeeze_trajectory)):
        index = i % len(squeeze_trajectory)
        next_node = squeeze_trajectory[index]
        if len(next_node.loop_neighbours(loop)) != 3:
            current_node.squeeze_entrance_exit = True
            break
        current_node = next_node
        current_node.squeezable = True
        # Mark all nodes until we reach a corner, including the corner
        # if len(loop[index].loop_neighbours(loop)) != 3: break

def print_grid(nodes, loop):
    max_i = max([node.pos[0] for node in nodes.values()])
    max_j = max([node.pos[1] for node in nodes.values()])
    for i in range(max_i + 1):
        for j in range(max_j + 1):
            if (i, j) in nodes:
                node = nodes[(i, j)]
                if node.squeeze_entrance_exit: print('E', end='')
                elif node in loop: print('L', end='')
                elif node.enclosed is False: print('O', end='')
                else: print('I', end='')
            else: print(' ', end='')
        print()

def all_neighbours(nodes):
    return sum([node.neighbours for node in nodes], [])

def find_squeeze_entrances(nodes, loop):
    not_enclosed = set([node for node in nodes if node.enclosed is False])
    squeeze_entrances = set()
    # JL , F7 are possible, TODO: S
    # ||, --, L-, J-, 7-, F-, -|, |- are not possible because disconnected loop 
    for node in all_neighbours(not_enclosed):
        if node and node.is_squeeze_entrance(loop): squeeze_entrances.add(node)
    return squeeze_entrances

def find_loop_S(S_node):
    types = ['|', '-', 'L', 'J', '7', 'F']
    max_len = 0
    best_loop = []
    for type in types:
        starting_node = Node(type, S_node.pos)
        starting_node.neighbours = S_node.neighbours
        try:
            loop = find_loop(starting_node)
            max_len = max(max_len, len(loop))
            if len(loop) == max_len: best_loop = loop
        except:
            pass
    return best_loop

def find_loop(node):
    visited = set()
    visited_list = []
    while True:
        if node.type == 'S':
            return visited_list
        visited.add(node)
        visited_list.append(node)
        node = node.next(visited)

def attach_neighbours(nodes):
    for node in nodes.values():
        i, j = node.pos
        # left, right, up, down
        neighbourhood = [(i, j-1), (i, j+1), (i-1, j), (i+1, j)]
        for pos in neighbourhood:
            if pos in nodes: node.neighbours.append(nodes[pos])
            else: node.neighbours.append(None)

if __name__ == '__main__':
    lines = [line.rstrip('\n') for line in sys.stdin if line.rstrip('\n')]
    print(part_1(lines))
    print(part_2(lines))
