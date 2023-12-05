import sys

class RangeMap:
    def __init__(self, start_input, start_output, length):
        self.start_input = start_input
        self.start_output = start_output
        self.length = length

    def __contains__(self, key):
        return key >= self.start_input and key < self.start_input + self.length

    def __getitem__(self, key):
        if key not in self:
            raise KeyError(key)
        return self.start_output + (key - self.start_input)

    def __lt__(self, other):
        return self.start_input < other.start_input
    
class Range:
    def __init__(self, start, length):
        self.start = start
        self.length = length
    
    def __contains__(self, key):
        return key >= self.start and key < self.start + self.length
    
    def skip(self, n):
        return Range(self.start + n, self.length - n)


def map_seed(seed, map_dict):
    current_state = "seed"
    while current_state != "location":
        seed, current_state = map_seed_iter(seed, current_state, map_dict)
    return seed

def map_seed_iter(seed, current_state, map_dict):
    maps, next_state = map_dict[current_state]
    for map in maps:
        if seed in map:
            seed = map[seed]
            break
    return seed, next_state

def map_range(seed_range, map_dict):
    current_state = "seed"
    seed_ranges = [seed_range]
    returned_state = ""
    while current_state != "location":
        next_seed_ranges = []
        for range in seed_ranges:
            returned_ranges, returned_state = map_range_iter(range, current_state, map_dict)
            next_seed_ranges.extend(returned_ranges)
        seed_ranges = next_seed_ranges
        current_state = returned_state
    return seed_ranges

def map_range_iter(seed_range, current_state, map_dict):
    maps, next_state = map_dict[current_state]
    sorted_maps = sorted(maps)
    mapped_seed_ranges = []
    ranges_todo = [seed_range]
    while ranges_todo:
        mapped = False
        range = ranges_todo.pop(0)
        for map in sorted_maps:
            if range.start in map:
                mapped_start = map[range.start]
                mapped_length = min(range.length, map.length - (mapped_start - map.start_output))
                mapped_seed_ranges.append(Range(mapped_start, mapped_length))
                if mapped_length != range.length:
                    ranges_todo.append(range.skip(mapped_length))
                mapped = True
                break
        if not mapped: mapped_seed_ranges.append(range)
    return mapped_seed_ranges, next_state

def create_map_dict(lines):
    current_maps = []
    map_dict = {}
    input, output = None, None
    for line in lines[1:] + ["end-to-end"]:
        if "map" in line or line == "end-to-end":
            line = line.split()
            if input: map_dict[input] = (current_maps, output)
            input, output = line[0].split("-to-")
            current_maps = []
            continue
        start_output, start_input, length = [int(x) for x in line.split()]
        current_maps.append(RangeMap(start_input, start_output, length))
    return map_dict

def part_1(lines):
    seeds = [int(seed) for seed in lines[0][6:].split()]
    map_dict = create_map_dict(lines)
    mapped_seeds = [map_seed(seed, map_dict) for seed in seeds]
    return min(mapped_seeds)

def part_2(lines):
    seed_ints = [int(seed) for seed in lines[0][6:].split()]
    seed_ranges = [Range(seed_ints[i], seed_ints[i+1]) for i in range(0, len(seed_ints), 2)]
    map_dict = create_map_dict(lines)
    mapped_seeds = sum([map_range(seed_range, map_dict) for seed_range in seed_ranges], [])
    return min(mapped_seeds, key=lambda x: x.start).start

if __name__ == '__main__':
    lines = [line.rstrip('\n') for line in sys.stdin if line.rstrip('\n')]
    print(part_1(lines))
    print(part_2(lines))
