schematic = []
with open('input.txt') as f:
    while line := f.readline():
        schematic.append(line.strip())


def find_adjacent_symbols(schematic, symbol, min_y, max_y, min_x, max_x):
    adjacent_symbols = []
    y = min_y
    while y <= max_y:
        x = min_x
        while x <= max_x:
            if schematic[y][x] == symbol:
                adjacent_symbols.append((y, x))

            x += 1

        y += 1

    return adjacent_symbols


gear_candidates = {}
for i, line in enumerate(schematic):
    j = 0
    while j < len(line):
        num = ""
        pos = j
        while pos < len(line) and line[pos].isdigit():
            num += line[pos]
            pos += 1

        # Advance j to character after pos. This technically skips the first
        # non-digit symbol after a number, but at this point we only care about
        # digits, and it's not possible for pos to be a digit *unless* we
        # reached the end of the line, in which case pos + 1 will go past the
        # end of the line and the loop will exit.
        j = pos + 1

        # If we didn't find any digits, we don't need to search for adjacent
        # symbols.
        if not num:
            continue

        num_start_idx = pos - len(num)
        num_end_idx = pos - 1
        min_search_y = max(i - 1, 0)
        max_search_y = min(i + 1, len(schematic) - 1)
        min_search_x = max(num_start_idx - 1, 0)
        max_search_x = min(num_end_idx + 1, len(line) - 1)

        adjacent_symbols = find_adjacent_symbols(
            schematic,
            "*",
            min_search_y,
            max_search_y,
            min_search_x,
            max_search_x)

        for adjacent_symbol in adjacent_symbols:
            if adjacent_symbol not in gear_candidates:
                gear_candidates[adjacent_symbol] = []

            gear_candidates[adjacent_symbol].append(int(num))

sum = 0
for adjacent_part_numbers in gear_candidates.values():
    if len(adjacent_part_numbers) == 2:
        gear_ratio = adjacent_part_numbers[0] * adjacent_part_numbers[1]
        sum += gear_ratio

print(sum)
