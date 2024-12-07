import sys

def load_update(filename):
    rules: dict[int, set[int]] = {}
    updates: list[list[int]] = []

    with open(filename) as f:
        while line := f.readline():
            line = line.strip()
            if not line:
                continue

            if "|" in line:
                rule = [int(part) for part in line.split("|")]
                if rule[0] not in rules:
                    rules[rule[0]] = set()
                rules[rule[0]].add(rule[1])

            elif "," in line:
                pages = line.split(",")
                updates.append(
                    [int(page) for page in pages]
                )

    return rules, updates

filename = sys.argv[1] if len(sys.argv) > 1 else "input"
rules, updates = load_update(filename)

correct_updates = []
for update in updates:
    pages_before = set()
    for page in update:
        required_pages_after = rules.get(page, set())
        pages_out_order = required_pages_after & pages_before
        if len(pages_out_order) > 0:
            break

        pages_before.add(page)

    else:
        correct_updates.append(update)

sum = 0
for correct_update in correct_updates:
    middle_pos = int(len(correct_update) / 2)
    middle = correct_update[middle_pos]
    sum += middle

print(sum)
