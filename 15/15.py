import sys
import re

from collections import defaultdict

def hash(string):
    value = 0
    for character in string:
        ascii = ord(character)
        value += ascii
        value *= 17
        value %= 256
    return value

def part_1(lines):
    steps = lines[0].split(",")
    value_sum = 0
    for step in steps:
        value_sum += hash(step)
    return value_sum

def part_2(lines):
    lenses = lines[0].split(",")
    boxes = defaultdict(list)
    for lens in lenses:
        if "-" in lens: dash_operation(boxes, lens)
        elif "=" in lens: equal_operation(boxes, lens)

    power = 0
    for box, lenses in boxes.items():
        for i, lens in enumerate(lenses):
            power += (box + 1) * (i + 1) * int(lens[-1])
        
    return power

def get_label(lens):
    return re.findall(r"^[a-z]+", lens)[0]

def dash_operation(boxes, lens):
    label = get_label(lens)
    label_hash = hash(label)
    boxes[label_hash] = list(filter(lambda x: get_label(x) != label, boxes[label_hash]))

def equal_operation(boxes, lens):
    label = get_label(lens)
    label_hash = hash(label)
    replace_idx = None
    for i, lens_in_box in enumerate(boxes[label_hash]):
        if get_label(lens_in_box) == label:
            replace_idx = i
            break
    if replace_idx is not None:
        boxes[label_hash][replace_idx] = lens
    else:
        boxes[label_hash].append(lens)


if __name__ == '__main__':
    lines = [line.rstrip('\n') for line in sys.stdin if line.rstrip('\n')]
    print(part_1(lines))
    print(part_2(lines))
