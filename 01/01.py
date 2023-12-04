import sys

def extract_number(line):
    numbers = [int(c) for c in line if c.isdigit()]
    return numbers[0] * 10 + numbers[-1]

def extract_number_alpha(line):
    number_map = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9
    }
    for number in number_map:
        line = line.replace(number, number+str(number_map[number])+number)

    return extract_number(line)

def part_1(lines):
    return sum([extract_number(line) for line in lines])

def part_2(lines):
    return sum([extract_number_alpha(line) for line in lines])

if __name__ == '__main__':
    lines = [line.rstrip('\n') for line in sys.stdin]
    print(part_1(lines))
    print(part_2(lines))
