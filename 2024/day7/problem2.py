import itertools
import math
import sys

def load_equations(filename):
    equations = []
    with open(filename) as f:
        while line := f.readline():
            # result: numbers
            # 123: 10 23 4
            result, numbers = line.split(":")
            result = int(result)
            equations.append([result] + [int(num.strip()) for num in numbers.split()])

    return equations

def count_digits(number):
    return int(math.log10(abs(number))) + 1

filename = sys.argv[1] if len(sys.argv) > 1 else "input"
equations = load_equations(filename)

OPERATORS = ("*", "+", "||")
operator_cache = {}
sum = 0
for equation in equations:
    target_result = equation[0]
    numbers = equation[1:]
    assert len(numbers) > 1, "Only one number in equation"

    num_operators = len(numbers) - 1
    if num_operators in operator_cache:
        operator_combos = operator_cache[num_operators]
    else:
        operator_combos = list(itertools.product(OPERATORS, repeat=num_operators))
        operator_cache[num_operators] = operator_combos

    for operator_combo in operator_combos:
        operator_index = 0
        curr_result = numbers[0]
        for number in numbers[1:]:
            operator = operator_combo[operator_index]
            if operator == "*":
                curr_result = curr_result * number
            elif operator == "+":
                curr_result = curr_result + number
            elif operator == "||":
                curr_result = curr_result * (10 ** count_digits(number)) + number
            else:
                raise ValueError(f"Invalid operator: {operator}")

            operator_index += 1

        if curr_result == target_result:
            sum += target_result
            break

print(sum)
