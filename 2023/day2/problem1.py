import enum
import typing as t

class Color(enum.Enum):
    BLUE = 'blue'
    GREEN = 'green'
    RED = 'red'

LIMITS = {
    Color.BLUE: 14,
    Color.GREEN: 13,
    Color.RED: 12
}


class Draw:
    groups: dict[Color, int] = None

    def __init__(self):
        self.groups = {
            Color.BLUE: 0,
            Color.GREEN: 0,
            Color.RED: 0
        }

    def record_group(self, color: Color, amount: int):
        self.groups[color] = amount

    @staticmethod
    def parse(group_info):
        groups = group_info.split(',')
        draw = Draw()
        for group in groups:
            amount, color = group.strip().split(' ')
            draw.record_group(Color(color), int(amount))

        return draw

    def __getitem__(self, key: Color) -> int:
        return self.groups[key]

    def __str__(self):
        return str(self.groups)


class Game:
    draws: list[Draw] = None

    def __init__(self, id: int):
        self.id = id
        self.draws = []

    def record_draw(self, draw: Draw):
        self.draws.append(draw)

    def max_draw(self, color: Color):
        max = 0
        for draw in self.draws:
            if draw[color] > max:
                max = draw[color]
        return max

    def satisfies(self, limits: dict[Color, int]) -> bool:
        for color, amount in limits.items():
            if self.max_draw(color) > amount:
                return False

        return True

    @staticmethod
    def parse(game_info):
        game_title, draws = game_info.split(':')
        game_id = int(game_title.split(' ')[1])

        game = Game(id=game_id)

        for draw_string in draws.split(';'):
            draw = Draw.parse(draw_string)
            game.record_draw(draw)

        return game

    def __str__(self):
        s = ""
        for draw in self.draws:
            s += str(draw) + "\n"

        return s

def read_games_from_file() -> list[Game]:
    games = []
    with open("game_info.txt", 'r') as f:
        lines = f.readlines()
        for line in lines:
            game = Game.parse(line)
            games.append(game)

    return games


def read_games_from_str(s) -> list[Game]:
    games = []
    lines = s.split('\n')
    for line in lines:
        if not line:
            continue
        game = Game.parse(line)
        games.append(game)

    return games


test_input = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

# games = read_games_from_str(test_input)
games = read_games_from_file()
sum = 0
for game in games:
    # Part 1
    # if game.satisfies(LIMITS):
    #     sum += game.id
    # Part 2
    blue = game.max_draw(Color.BLUE)
    green = game.max_draw(Color.GREEN)
    red = game.max_draw(Color.RED)
    power = blue * green * red
    sum += power

print(sum)
