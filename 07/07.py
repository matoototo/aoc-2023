import sys
from collections import Counter
from functools import reduce

class Hand:
    def __init__(self, cards, bet, part_2=False):
        self.cards = cards
        self.bet = bet
        self.part_2 = part_2
        self.order = "AKQT98765432J" if part_2 else "AKQJT98765432"
        self.order_set = set(self.order)

    def strength(self):
        if self.part_2:
            permutations = set([self.cards])
            for i in range(5):
                new_permutations = set()
                for cards in permutations:
                    # Don't have to add all permutations for J, only those with overlapping cards plus ace
                    order_subset = self.order_set.intersection(set(cards + "A"))
                    new_permutations.add(cards)
                    if cards[i] == 'J':
                        new_permutations.update([cards[:i] + card + cards[i+1:] for card in order_subset])
                permutations = new_permutations
            return max(Hand(cards, 0).strength() for cards in permutations)

        counter = Counter(self.cards)
        counts = counter.most_common()
        # for 5oak -> 16, 4oak -> 8, fh -> 6, 3oak -> 4, 2p -> 2, 1p -> 1
        strength = sum(pow(10, count - 1) for card, count in counts)
        return strength

    def worse_order(self, other):
        for x, y in zip(self.cards, other.cards):
            if x == y: continue
            return self.order.index(x) > self.order.index(y)
        return False

    def __lt__(self, other):
        less_strength = self.strength() < other.strength()
        worse_order = self.worse_order(other)
        return less_strength or (self.strength() == other.strength() and worse_order)
    
    def __repr__(self):
        return f'Hand({self.cards}, {self.strength()})\n'

def part_1(lines):
    hands = [Hand(line.split(' ')[0], int(line.split(' ')[1])) for line in lines]
    sorted_hands = sorted(hands)
    return reduce(lambda bet, hand: bet + hand.bet * (sorted_hands.index(hand) + 1), sorted_hands, 0)

def part_2(lines):
    hands = [Hand(line.split(' ')[0], int(line.split(' ')[1]), part_2=True) for line in lines]
    sorted_hands = sorted(hands)
    return reduce(lambda bet, hand: bet + hand.bet * (sorted_hands.index(hand) + 1), sorted_hands, 0)

if __name__ == '__main__':
    lines = [line.rstrip('\n') for line in sys.stdin if line.rstrip('\n')]
    print(part_1(lines))
    print(part_2(lines))
