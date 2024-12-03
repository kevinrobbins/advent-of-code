import sys

occurrences_left = {}
occurrences_right = {}
list_right = []


def read_input(filename):
    with open(filename) as f:
        lines = f.readlines()

    for line in lines:
        left, right = [int(num) for num in line.split("   ")]

        if left not in occurrences_left:
            occurrences_left[left] = 0

        occurrences_left[left] += 1

        list_right.append(right)


filename = sys.argv[1] if len(sys.argv) > 1 else "input"

read_input(filename)

for num_right in list_right:
    if num_right not in occurrences_right:
        occurrences_right[num_right] = 0
    occurrences_right[num_right] += 1

similarity_score = 0
for number in occurrences_left:
    if number not in occurrences_right:
        continue

    similarity_score += number * occurrences_right[number] * occurrences_left[number]
print(similarity_score)
