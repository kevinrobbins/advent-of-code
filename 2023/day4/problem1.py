import dataclasses
import sys


@dataclasses.dataclass()
class Card:
    id: int
    winning_numbers: list[int]
    played_numbers: list[int]

    def score(self):
        matching_numbers = [
            played_num
            for played_num in self.played_numbers
            if played_num in self.winning_numbers
        ]

        if len(matching_numbers) == 0:
            return 0

        else:
            return 2 ** (len(matching_numbers) - 1)

    @staticmethod
    def parse(s):
        card_info, numbers = s.split(':')
        card_id = int(card_info[5:].strip())

        winning_number_str, played_number_str = numbers.split('|')
        winning_numbers = [int(num.strip()) for num in winning_number_str.strip().split(' ') if num]
        played_numbers = [int(num.strip()) for num in played_number_str.strip().split(' ') if num]

        return Card(card_id, winning_numbers, played_numbers)

    def __str__(self):
        winning_number_strings = []
        for num in self.winning_numbers:
            if num >= 10:
                winning_number_strings.append(str(num))
            else:
                winning_number_strings.append(" " + str(num))

        played_number_strings = []
        for num in self.played_numbers:
            if num >= 10:
                played_number_strings.append(str(num))
            else:
                played_number_strings.append(" " + str(num))

        if 10 <= self.id < 100:
            card_id_str = f" {self.id}"
        elif self.id < 10:
            card_id_str = f"  {self.id}"
        else:
            card_id_str = str(self.id)

        return f"Card {card_id_str}: {' '.join(winning_number_strings)} | {' '.join(played_number_strings)}"


filename = sys.argv[1]

cards = []
with open(filename, 'r') as f:
    while line := f.readline():
        cards.append(Card.parse(line.strip()))

sum = 0
for card in cards:
    sum += card.score()

print(int(sum))
