import sys

list_left = []
list_right = []


def read_input(filename):
    with open(filename) as f:
        lines = f.readlines()

    for line in lines:
        left, right = line.split("   ")
        list_left.append(int(left))
        list_right.append(int(right))


filename = sys.argv[1] if len(sys.argv) > 1 else "input"

read_input(filename)

list_left = sorted(list_left)
list_right = sorted(list_right)

distance_sum = 0
for i in range(len(list_left)):
    distance_sum += abs(list_left[i] - list_right[i])

print(distance_sum)
