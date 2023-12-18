import sys
import random

class Command:
    def __init__(self, line, part_2 = False):
        self.direction, self.arg, self.colour = line.split(' ')
        if part_2:
            direction_map = { "0": "R", "1": "D", "2": "L", "3": "U" }
            self.colour = self.colour.strip()[2:-1]
            arg_hex = self.colour[:5]
            self.direction = direction_map[self.colour[5]]
            self.arg = int(arg_hex, 16)
        else:
            self.arg = int(self.arg)

    def draw(self, grid, position):
        direction_map = { "U": (1, 0), "D": (-1, 0), "R": (0, 1), "L": (0, -1) }
        index = direction_map[self.direction]
        for i in range(self.arg):
            position[0] += index[0]
            position[1] += index[1]
            grid[position[0]][position[1]] = "#"
        return grid, position
    
    def apply(self, position, boundary):
        direction_map = { "R": (1, 0), "D": (0, 1), "L": (-1, 0), "U": (0, -1) }
        index = direction_map[self.direction]
        position[0] += index[0] * self.arg
        position[1] += index[1] * self.arg
        boundary += self.arg
        return position, boundary

def trim_grid(grid):
    min_x, max_x, min_y, max_y = 1000, 0, 1000, 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "#":
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)
    grid = [line[min_x:max_x+1] for line in grid[min_y:max_y+1]]
    # Add padding
    grid = [["." for _ in range(len(grid[0]))]] + grid + [["." for _ in range(len(grid[0]))]]
    grid = [["."] + line + ["."] for line in grid]
    return grid

def flood(grid, position):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for direction in directions:
        new_position = [position[0] + direction[0], position[1] + direction[1]]
        if new_position[0] < 0 or new_position[0] >= len(grid) or new_position[1] < 0 or new_position[1] >= len(grid[0]):
            continue
        if grid[new_position[0]][new_position[1]] != "#":
            grid[new_position[0]][new_position[1]] = "#"
            flood(grid, new_position)

def fill_grid(grid):
    sys.setrecursionlimit(1000000)
    edges = [(0, 0), (len(grid)-1, 0), (0, len(grid[0])-1), (len(grid)-1, len(grid[0])-1)]
    while True:
        grid_copy = [line[:] for line in grid]
        random_point = [random.randint(0, len(grid)-1), random.randint(0, len(grid[0])-1)]
        if grid[random_point[0]][random_point[1]] == "#": continue
        flood(grid_copy, random_point)
        if all([grid_copy[edge[0]][edge[1]] == "#" for edge in edges]):
            continue
        grid = grid_copy
        break
    return grid

# def part_1(lines):
#     commands = [Command(line) for line in lines]
#     grid = [["." for _ in range(1000)] for _ in range(1000)]
#     position = [500, 500]
#     for command in commands:
#         grid, position = command.draw(grid, position)
#     grid = trim_grid(grid)
#     grid = fill_grid(grid)
#     return sum([line.count("#") for line in grid])

def part_1(lines):
    commands = [Command(line, part_2 = False) for line in lines]
    position = [0, 0]
    points = []
    boundary = 0
    for command in commands:
        position, boundary = command.apply(position, boundary)
        points.append(tuple(position))
    return int(shoelace(points) + boundary // 2 + 1)

def shoelace(points):
    n = len(points)
    area = 0
    for i in range(n - 1):
        area += points[i][0] * points[i+1][1]
        area -= points[i][1] * points[i+1][0]
    area += points[n-1][0] * points[0][1]
    area -= points[n-1][1] * points[0][0]
    return abs(area) / 2

def part_2(lines):
    commands = [Command(line, part_2 = True) for line in lines]
    position = [0, 0]
    points = []
    boundary = 0
    for command in commands:
        position, boundary = command.apply(position, boundary)
        points.append(tuple(position))
    return int(shoelace(points) + boundary // 2 + 1)

if __name__ == '__main__':
    lines = [line.rstrip('\n') for line in sys.stdin if line.rstrip('\n')]
    print(part_1(lines))
    print(part_2(lines))
