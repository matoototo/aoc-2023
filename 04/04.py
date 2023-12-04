import sys
from collections import defaultdict

def parse_card(line):
    numbers = line.split(":")[1]
    winning, mine = numbers.split("|")
    winning = [int(x) for x in winning.strip().split()]
    mine = [int(x) for x in mine.strip().split()]
    return winning, mine

def num_overlapping(card):
    winning, mine = card
    return len(set(winning).intersection(set(mine)))

def populate_winners(cards):
    dict = defaultdict(set)
    for i, (winning, mine) in cards.items():
        overlapping = num_overlapping((winning, mine))
        dict[i] = set(range(i+1, i+overlapping+1))
    return dict

def part_1(lines):
    scores = [int(2 ** (num_overlapping(parse_card(line)) - 1)) for line in lines]
    return sum(scores)
    
def part_2(lines):
    cards = {i : parse_card(line) for i, line in enumerate(lines)}
    winners = populate_winners(cards)
    current_cards = defaultdict(int)
    for i in range(len(cards)):
        current_cards[i] = 1

    used_cards = 0
    while True:
        for card, num in current_cards.items():
            for winner in winners[card]:
                current_cards[winner] += num
            current_cards[card] = 0
            used_cards += num
        if sum(current_cards.values()) == 0:
            break

    return used_cards

if __name__ == '__main__':
    lines = [line.rstrip('\n') for line in sys.stdin]
    print(part_1(lines))
    print(part_2(lines))
