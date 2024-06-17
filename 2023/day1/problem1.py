calibration_file = '../inputs/calibration_values.txt'

with open(calibration_file, 'r') as f:
    lines = f.readlines()

sum = 0

for line in lines:
    num = ''
    # Get first digit
    for c in line:
        if c.isdigit():
            num += c
            break

    for c in reversed(line):
        if c.isdigit():
            num += c
            break

    sum += int(num)

print(sum)
