import sys
from itertools import product

class Hailstone:
    def __init__(self, line):
        self.x, self.y, self.z = line.split(" @ ")[0].split(", ")
        self.vx, self.vy, self.vz = line.split(" @ ")[1].split(", ")
        self.x, self.y, self.z = float(self.x), float(self.y), float(self.z)
        self.vx, self.vy, self.vz = float(self.vx), float(self.vy), float(self.vz)

    def intersects(self, other, bbox=[7, 27]):
        # x_1 + vx_1 * t_1 = x_2 + vx_2 * t_2
        # y_1 + vy_1 * t_1 = y_2 + vy_2 * t_2
        # (x_1 - x_2) = vx_2 * t_2 - vx_1 * t_1
        # (y_1 - y_2) = vy_2 * t_2 - vy_1 * t_1
        # -> t_2 = (x_1 - x_2 + vx_1 * t_1) / vx_2
        # -> t_2 = (y_1 - y_2 + vy_1 * t_1) / vy_2
        # -> (x_1 - x_2 + vx_1 * t_1) * vy_2 = (y_1 - y_2 + vy_1 * t_1) * vx_2
        # -> (x_1 - x_2) * vy_2 + vx_1 * vy_2 * t_1 = (y_1 - y_2) * vx_2 + vy_1 * vx_2 * t_1
        # -> t_1 = ((y_1 - y_2) * vx_2 - (x_1 - x_2) * vy_2) / (vx_1 * vy_2 - vy_1 * vx_2)
        if self.vx * other.vy == self.vy * other.vx: return False
        t_1 = ((self.y - other.y) * other.vx - (self.x - other.x) * other.vy) / (self.vx * other.vy - self.vy * other.vx)
        t_2 = (self.x - other.x + self.vx * t_1) / other.vx
        return t_1 >= 0 and t_2 >= 0 and self.at(t_1).close(other.at(t_2)) and self.at(t_1).in_bbox(bbox)
    
    def __mul__(self, t):
        return Hailstone(f"{self.x + self.vx * t}, {self.y + self.vy * t}, {self.z + self.vz * t} @ {self.vx}, {self.vy}, {self.vz}")
    
    def __rmul__(self, t):
        return self * t

    def close(self, other):
        eps = 1e1 # why so large lol
        return abs(self.x - other.x) <= eps and abs(self.y - other.y) <= eps #and abs(self.z - other.z) < 1e-6

    def in_bbox(self, bbox=[7, 27]):
        eps = 1e-5
        return self.x - bbox[0] >= eps and bbox[1] - self.x >= eps and self.y - bbox[0] >= eps and bbox[1] - self.y >= eps #and self.z - bbox[0] >= eps and bbox[1] - self.z >= eps

    def at(self, t):
        return self * t
        # return (self.x + self.vx * t, self.y + self.vy * t, self.z + self.vz * t)

from z3 import *

def solve_hailstone_collision(hailstones):
    rx, ry, rz = Ints('rx ry rz')
    rvx, rvy, rvz = Ints('rvx rvy rvz')
    s = Solver()
    hailstones = hailstones[:3]

    for hailstone in hailstones:
        hx, hy, hz = int(hailstone.x), int(hailstone.y), int(hailstone.z)
        hvx, hvy, hvz = int(hailstone.vx), int(hailstone.vy), int(hailstone.vz)

        t = Int(f't_{hx}_{hy}_{hz}')
        s.add(t >= 0)

        hailstone_pos_x = hx + t * hvx
        hailstone_pos_y = hy + t * hvy
        hailstone_pos_z = hz + t * hvz

        rock_pos_x = rx + t * rvx
        rock_pos_y = ry + t * rvy
        rock_pos_z = rz + t * rvz

        s.add(rock_pos_x == hailstone_pos_x, rock_pos_y == hailstone_pos_y, rock_pos_z == hailstone_pos_z)

        if s.check() == unsat:
            return None  # No solution exists with these constraints

    if s.check() == sat:
        m = s.model()
        return sum((m[rx].as_long(), m[ry].as_long(), m[rz].as_long()))
    else: 
        return None

def part_1(lines):
    hailstones = [Hailstone(line) for line in lines]
    bbox = [200000000000000, 400000000000000]
    if len(hailstones) == 5: bbox = [7, 27]
    intersect_count = 0
    for a, b in product(hailstones, hailstones):
        if a == b: continue
        if a.intersects(b, bbox):
            intersect_count += 1
    return intersect_count // 2

def part_2(lines):
    hails = [Hailstone(line) for line in lines]
    return solve_hailstone_collision(hails)

if __name__ == '__main__':
    lines = [line.rstrip('\n') for line in sys.stdin if line.rstrip('\n')]
    print(part_1(lines))
    print(part_2(lines))
