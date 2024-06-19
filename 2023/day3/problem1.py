schematic = []
with open('input.txt') as f:
    while line := f.readline():
        schematic.append(line.strip())


def is_part_number(schematic, min_y, max_y, min_x, max_x):
    ret_val = False
    y = min_y

    search_space = ""
    while y <= max_y:
        x = min_x
        while x <= max_x:
            search_space += schematic[y][x]
            if not schematic[y][x].isdigit() and schematic[y][x] != ".":
                ret_val = True

            x += 1

        search_space += "\n"

        y += 1

    # if ret_val:
        # print(search_space)
        # print(f"Part Number: {ret_val}")
        # print()
    return ret_val


sum = 0
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
        # digits, and it's not possible for pos to be a digit at this point
        # *unless* we reached the end of the line, in which case pos + 1 will
        # go past the end of the line and the loop will exit.
        j = pos + 1

        # If we didn't find any digits, we don't need to search for adjacent
        # symbols.
        if not num:
            continue

        # print(num)
        num_start_idx = pos - len(num)
        num_end_idx = pos - 1
        min_search_y = max(i - 1, 0)
        max_search_y = min(i + 1, len(schematic) - 1)
        min_search_x = max(num_start_idx - 1, 0)
        max_search_x = min(num_end_idx + 1, len(line) - 1)
        # print(
        #     f"Searching in region ("
        #     f"{min_search_y}, {min_search_x}), "
        #     f"({min_search_y}, {max_search_x}), "
        #     f"({max_search_y}, {min_search_x}), "
        #     f"({max_search_y}, {max_search_x})")

        if is_part_number(schematic, min_search_y, max_search_y, min_search_x, max_search_x):
            sum += int(num)

print(sum)
