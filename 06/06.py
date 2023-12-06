import sys
from functools import reduce

def part_1(lines):
    times = [int(time) for time in lines[0].split(": ")[1].split()]
    distances = [int(time) for time in lines[1].split(": ")[1].split()]
    winners_overall = []
    for time, distance in zip(times, distances):
        winners = 0
        for i in range(time):
            start_velocity = i
            distance_travelled = start_velocity * (time - i)
            winners += distance_travelled > distance
        winners_overall.append(winners)

    return reduce(lambda x, y: x * y, winners_overall)

def part_2(lines):
    time = int("".join([time for time in lines[0].split(": ")[1].split()]))
    distance = int("".join([time for time in lines[1].split(": ")[1].split()]))
    winners = 0
    for i in range(time):
        start_velocity = i
        distance_travelled = start_velocity * (time - i)
        winners += distance_travelled > distance
    return winners

if __name__ == '__main__':
    lines = [line.rstrip('\n') for line in sys.stdin if line.rstrip('\n')]
    print(part_1(lines))
    print(part_2(lines))
