import sys

import copy

class Tile:
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y
        self.neighbours = []

class Beam:
    def __init__(self, x, y, direction_str):
        self.x = x
        self.y = y
        self.direction_str = direction_str

    def step(self, tiles, start = False):
        direction_map = {
            "up": (0, -1),
            "right": (1, 0),
            "down": (0, 1),
            "left": (-1, 0)
        }
        if not start:
            direction = direction_map[self.direction_str]
            self.x += direction[0]
            self.y += direction[1]
        if (self.x, self.y) not in tiles: return set()

        beams = set([self])

        tile_type = tiles[(self.x, self.y)].type
        if self.direction_str in ["left", "right"] and tile_type == "|":
            self.direction_str = "up"
            beams.add(Beam(self.x, self.y, "down"))
        elif self.direction_str in ["up", "down"] and tile_type == "-":
            self.direction_str = "left"
            beams.add(Beam(self.x, self.y, "right"))
        elif tile_type == "\\":
            reflection_map = {"up": "left", "right": "down", "down": "right", "left": "up"}
            self.direction_str = reflection_map[self.direction_str]
        elif tile_type == "/":
            reflection_map = {"up": "right", "right": "up", "down": "left", "left": "down"}
            self.direction_str = reflection_map[self.direction_str]

        return beams
    
    def __hash__(self):
        return "".join([str(self.x), str(self.y), self.direction_str]).__hash__()
    
    def __repr__(self):
        return f"({self.x}, {self.y}, {self.direction_str})"
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.direction_str == other.direction_str

def create_tiles(lines):
    tiles = {}
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            tiles[(j, i)] = Tile(char, j, i)

    for tile in tiles.values():
        neighbours = [(tile.x - 1, tile.y), (tile.x + 1, tile.y), (tile.x, tile.y - 1), (tile.x, tile.y + 1)]
        for neighbour in neighbours:
            if neighbour in tiles:
                tile.neighbours.append(tiles[neighbour])
    
    return tiles

def shoot_beam(tiles, x, y, direction_str):
    beams = set([Beam(x, y, direction_str)])
    energized = set()
    i = 0
    while True:
        i += 1
        new_beams = set()
        if not beams: break
        for beam in beams:
            energized.add(copy.deepcopy(beam))
            new_beams = new_beams.union(beam.step(tiles, start = (i == 1)))
        beams = set([beam for beam in new_beams if beam not in energized or i == 1])
    return len(set([(beam.x, beam.y) for beam in energized]))

def part_1(lines):
    tiles = create_tiles(lines)
    return shoot_beam(tiles, 0, 0, "right")

def part_2(lines):
    current_max = 0
    tiles = create_tiles(lines)
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if any([i == 0 or i == len(lines) - 1, j == 0 or j == len(lines[0]) - 1]):
                for direction in ["up", "right", "down", "left"]:
                    current_max = max(current_max, shoot_beam(tiles, j, i, direction))

    return current_max
            

if __name__ == '__main__':
    lines = [line.rstrip('\n') for line in sys.stdin if line.rstrip('\n')]
    print(part_1(lines))
    print(part_2(lines))
