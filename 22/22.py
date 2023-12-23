import sys
from itertools import product
import copy
from tqdm import tqdm

sys.setrecursionlimit(10000)

class Brick:
    def __init__(self, line):
        self.line = line
        self.start, self.end = line.split("~")
        self.start = [int(i) for i in self.start.split(",")]
        self.end = [int(i) for i in self.end.split(",")]
        self.points = self.occupied_points()
        self.supported_bricks = set()
        self.supported_by = set()
        self.did_drop = False

    def drop(self, undo=False):
        self.start[2] += -1 if not undo else 1
        self.end[2] += -1 if not undo else 1
        self.points = self.occupied_points()

    def occupied_points(self):
        x, y, z = self.start
        x2, y2, z2 = self.end
        # return set([(i, j, k) for i in range(x, x2+1) for j in range(y, y2+1) for k in range(z, z2+1)])
        range_x = range(x, x2+1)
        range_y = range(y, y2+1)
        range_z = range(z, z2+1)
        return set(product(range_x, range_y, range_z))

    def populate_supported(self, bricks):
        for other in bricks:
            if self == other: continue
            if self.supports(other):
                self.supported_bricks.add(other)
                other.supported_by.add(self)

    def can_disintegrate(self):
        for other in self.supported_bricks:
            if len(other.supported_by) == 1:
                return True
        return False

    def n_fall(self, bricks):
        bricks_copy = copy.deepcopy([brick for brick in bricks if brick != self])
        for brick in bricks_copy:
            brick.did_drop = False
        # bricks_copy = sort_by_z(bricks_copy)
        drop_bricks(bricks_copy)
        return sum([1 if brick.did_drop else 0 for brick in bricks_copy])

    def supports(self, other):
        supporting_points = set([tuple([x, y, z+1]) for x, y, z in self.points])
        return supporting_points.intersection(other.points) != set()

    def intersects(self, other):
        return self.points.intersection(other.points) != set()
    
    def __repr__(self):
        return f"{self.start}~{self.end}"

def parse_bricks(lines):
    return [Brick(line) for line in lines]

def sort_by_z(bricks):
    return sorted(bricks, key=lambda brick: min(brick.start[2], brick.end[2]))

def drop_brick(brick, bricks):
    drop_count = 0
    while brick.start[2] > 0:
        brick.drop()
        drop_count += 1
        for other in bricks:
            if brick == other: continue
            if brick.intersects(other):
                brick.drop(undo=True)
                drop_count -= 1
                brick.did_drop = drop_count > 0
                return
    brick.did_drop = drop_count > 0

def drop_bricks(bricks):
    for brick in bricks:
        drop_brick(brick, bricks)

def disintegrate_bricks(bricks, part_2=False):
    for brick in bricks:
        brick.populate_supported(bricks)

    disintegrated = 0
    # for brick in bricks:
    for brick in tqdm(bricks):
        if not part_2:
            disintegrated += brick.can_disintegrate() == 0
        else:
            disintegrated += brick.n_fall(bricks)

    return disintegrated

def part_1(lines):
    bricks = parse_bricks(lines)
    bricks = sort_by_z(bricks)
    drop_bricks(bricks)
    return disintegrate_bricks(bricks)

def part_2(lines):
    bricks = parse_bricks(lines)
    bricks = sort_by_z(bricks)
    drop_bricks(bricks)
    return disintegrate_bricks(bricks, part_2=True)

if __name__ == '__main__':
    lines = [line.rstrip('\n') for line in sys.stdin if line.rstrip('\n')]
    print(part_1(lines))
    print(part_2(lines))
