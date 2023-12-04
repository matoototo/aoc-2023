import sys

def is_valid(line):
    colours = count_max_per_colour(line)
    if colours["red"] > 12 or colours["green"] > 13 or colours["blue"] > 14:
        return 0
    return 1

def count_max_per_colour(line):
    colours = {}
    _, record = line.split(":")
    sets = record.split(";")
    colour_counts = [set.split(",") for set in sets]
    for colour_count_list in colour_counts:
        for colour_count in colour_count_list:
            count, colour = colour_count.split()
            if colour not in colours:
                colours[colour] = int(count)
            else:
                colours[colour] = max(colours[colour], int(count))
    return colours

def part_1(lines):
    return sum([(i+1)*is_valid(line) for i, line in enumerate(lines)])

def part_2(lines):
    max = [count_max_per_colour(line) for line in lines]
    powers = [max[i]["red"]*max[i]["green"]*max[i]["blue"] for i in range(len(max))]
    return sum(powers)

if __name__ == '__main__':
    lines = [line.rstrip('\n') for line in sys.stdin]
    print(part_1(lines))
    print(part_2(lines))
