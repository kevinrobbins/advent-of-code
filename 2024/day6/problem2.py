from copy import deepcopy
from dataclasses import dataclass, field
import enum
import sys


class Direction(enum.Enum):
    North = (-1, 0)
    South = (1, 0)
    East = (0, 1)
    West = (0, -1)


@dataclass
class Guard:
    y: int
    x: int
    direction: Direction = Direction.North

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


class CellState(enum.Enum):
    Obstacle = "#"
    NewObstacle = "O"
    Guard = "^"
    Visited = "X"
    Empty = "."


@dataclass
class Cell:
    state: CellState
    visits: set[Direction] = field(default_factory=set)


def load_room(filename) -> list[list[Cell]]:
    room = []
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            row = []
            for c in line:
                state = CellState(c)
                cell = Cell(state=state)
                row.append(cell)

            room.append(row)

    return room

def print_room(room: list[list[Cell]]):
    for row in room:
        for cell in row:
            print(cell.state.value, end=" ")
        print()

def is_loop(room: list[list[Cell]], guard: Guard):
    while True:
        # print_room(room)
        # print("- " * 10)
        # import pdb; pdb.set_trace()
        next_y = guard.y + guard.direction.value[0]
        next_x = guard.x + guard.direction.value[1]

        # Out of bounds
        if (
            next_y < 0 or next_y >= len(room) or
            next_x < 0 or next_x >= len(room)
        ):
            # print_room(room)
            return False

        while room[next_y][next_x].state in [CellState.Obstacle, CellState.NewObstacle]:
            guard.rotate()
            next_y = guard.y + guard.direction.value[0]
            next_x = guard.x + guard.direction.value[1]
            # print("After: ", guard.y, guard.x, guard.direction)

        # Check for loop after rotating the guard to avoid needing to make two
        # loops in some cases
        cell = room[guard.y][guard.x]
        if cell.state == CellState.Visited and guard.direction in cell.visits:
            return True

        cell.state = CellState.Visited
        cell.visits.add(guard.direction)
        guard.y, guard.x = next_y, next_x


def find_loops(room, default_route, guard_starting_y, guard_starting_x):
    num_loops = 0
    import time
    total_elapsed = 0
    total_elapsed_timer = time.perf_counter()
    for y, row in enumerate(room):
        for x, cell in enumerate(row):
            # print_room(default_route)
            # print()
            # print("- " * 10)
            # print()
            # Can't put obstacles where the guard starts
            if y == guard_starting_y and x == guard_starting_x:
                continue

            # Don't need to test cells the guard doesn't visit
            elif default_route[y][x].state != CellState.Visited:
                continue

            candidate_room = deepcopy(room)
            candidate_room[y][x].state = CellState.NewObstacle
            guard = Guard(guard_starting_y, guard_starting_x)

            if is_loop(candidate_room, guard):
                num_loops += 1

            # Reset guard position
            guard = Guard(guard_starting_y, guard_starting_x)

        print(time.perf_counter() - total_elapsed_timer)

    return num_loops

def test():
    room = load_room("test_input")
    guard = Guard(6, 4)
    obstacles = [
        (6, 3),
        (7, 6),
        (7, 7),
        (8, 1),
        (8, 3),
        (9, 7),
    ]
    for y, x in obstacles:
        new_room = room.copy()
        new_room[y][x].state = CellState.NewObstacle
        print_room(new_room)
        print(f"({y}, {x}): {is_loop(new_room, guard)}")

def simulate_route(room: list[list[Cell]], guard: Guard, depth: int = 0):
    if depth > 0:
        cell = room[guard.y][guard.x]
        cell.state = CellState.Visited
        cell.visits.add(guard.direction)

        next_y = guard.y + guard.direction.value[0]
        next_x = guard.x + guard.direction.value[1]

        # Out of bounds
        if (
            next_y < 0 or next_y >= len(room) or
            next_x < 0 or next_x >= len(room)
        ):
            return False

        while room[next_y][next_x].state in [CellState.Obstacle, CellState.NewObstacle]:
            guard.rotate()
            next_y = guard.y + guard.direction.value[0]
            next_x = guard.x + guard.direction.value[1]


        original_cell = room[next_y][next_x]
        guard.y, guard.x = next_y, next_x
    if depth == 0:
        while True:
            next_y = guard.y + guard.direction.value[0]
            next_x = guard.x + guard.direction.value[1]

            # Out of bounds
            if (
                next_y < 0 or next_y >= len(room) or
                next_x < 0 or next_x >= len(room)
            ):
                return False

            while room[next_y][next_x].state == CellState.Obstacle:
                guard.rotate()
                next_y = guard.y + guard.direction.value[0]
                next_x = guard.x + guard.direction.value[1]

            original_cell = room[next_y][next_x]
            room[next_y][next_x] = Cell(state=CellState.NewObstacle, visits=set())
            is_loop = simulate_route(room, guard, depth+1)
            # TODO

            # restore cell to original value
            room[next_y][next_x] = original_cell


    return room

def main(room):
    # Find guard starting position
    guard_starting_y = -1
    guard_starting_x = -1
    for y, row in enumerate(room):
        for x, cell in enumerate(row):
            if cell.state == CellState.Guard:
                guard_starting_y = y
                guard_starting_x = x

    assert guard_starting_y > -1 and guard_starting_x > -1, "No guard found."
    assert guard_starting_y < len(room) and guard_starting_x < len(room), "Guard out of bounds."

    default_route = simulate_route(deepcopy(room), guard_starting_y, guard_starting_x)
    num_loops = find_loops(room, default_route, guard_starting_y, guard_starting_x)
    print(num_loops)

if len(sys.argv) > 1 and sys.argv[1] == "test":
    test()

else:
    filename = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != "test" else "input"
    room = load_room(filename)
    main(room)
