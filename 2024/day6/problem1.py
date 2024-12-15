from dataclasses import dataclass
import enum
import sys

OBSTACLE = "#"
GUARD = "^"
VISITED = "X"

class Direction(enum.Enum):
    North = (-1, 0)
    South = (1, 0)
    East = (0, 1)
    West = (0, -1)

@dataclass
class Guard:
    y: int
    x: int
    direction = Direction.North

    def rotate(self):
        match self.direction:
            case Direction.North:
                self.direction = Direction.East
            case Direction.East:
                self.direction = Direction.South
            case Direction.South:
                self.direction = Direction.West
            case Direction.West:
                self.direction = Direction.North


def load_room(filename) -> list[list[str]]:
    room = []
    with open(filename) as f:
        for line in f.readlines():
            row = [c for c in line]
            room.append(row)
    return room

def print_room(room):
    for row in room:
        for cell in row:
            print(cell, end=" ")
        print()

filename = sys.argv[1] if len(sys.argv) > 1 else "input"

room = load_room(filename)

# Find guard starting position
guard_y = -1
guard_x = -1
for y, row in enumerate(room):
    for x, cell in enumerate(row):
        if cell == GUARD:
            guard_y = y
            guard_x = x

guard = Guard(guard_y, guard_x)

while True:
    room[guard.y][guard.x] = VISITED

    next_y = guard.y + guard.direction.value[0]
    next_x = guard.x + guard.direction.value[1]

    # Out of bounds
    if (
        next_y < 0 or next_y >= len(room) or
        next_x < 0 or next_x >= len(room)
    ):
        break

    if room[next_y][next_x] == OBSTACLE:
        guard.rotate()
        next_y = guard.y + guard.direction.value[0]
        next_x = guard.x + guard.direction.value[1]

    guard.y, guard.x = next_y, next_x
    room[guard.y][guard.x] = GUARD

num_visited = 0
for row in room:
    num_visited += row.count("X")
print(num_visited)
