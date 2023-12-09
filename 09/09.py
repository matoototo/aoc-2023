import sys

def construct_difference(sequence):
    return [sequence[i+1] - sequence[i] for i in range(len(sequence) - 1)]

def predict_next(current_sequence):
    sequences = []
    while any([x != 0 for x in current_sequence]):
        sequences.append(current_sequence)
        current_sequence = construct_difference(current_sequence)
    return sum([sequence[-1] for sequence in sequences])

def predict_previous(current_sequence):
    sequences = []
    while any([x != 0 for x in current_sequence]):
        sequences.append(current_sequence)
        current_sequence = construct_difference(current_sequence)
    return sequences[0][0] - (predict_previous(sequences[1]) if len(sequences) > 1 else 0)

def part_1(lines):
    sequences = [[int(x) for x in line.split()] for line in lines]
    return sum([predict_next(sequence) for sequence in sequences])

def part_2(lines):
    sequences = [[int(x) for x in line.split()] for line in lines]
    return sum([predict_previous(sequence) for sequence in sequences])

if __name__ == '__main__':
    lines = [line.rstrip('\n') for line in sys.stdin if line.rstrip('\n')]
    print(part_1(lines))
    print(part_2(lines))
