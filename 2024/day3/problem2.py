import re
import sys

def load_memory(filename):
    with open(filename) as f:
        return f.read()


def process_memory(memory):
    range_start = 0
    next_delim = "don't()"
    operations = []

    while range_start < len(memory):
        range_end = memory.find(next_delim, range_start)

        # Last range
        if range_end == -1:
            range_end = len(memory) # Can't set None or loop condition will never pop

        # If next is don't, we must be in a do
        if next_delim == "don't()":
            operations.extend(
                re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', memory[range_start:range_end])
            )

        range_start = range_end + len(next_delim)
        next_delim = "don't()" if next_delim == "do()" else "do()"

    product_sum = 0
    for operation in operations:
        assert len(operation) == 2
        product = int(operation[0]) * int(operation[1])
        product_sum += product

    return product_sum


def test():
    test_memories = [
        "mul(2,2)asdfmul(4,4)don't()mul(1,1)asdfmul(3,3)", # 4 + 16 = 20
        "mul(2,2)asdfmul(4,4)don't()mul(1,1)asdfmul(3,3)do()mul(6,6)", # 4 + 16 + 36 = 56
        "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))" # 48
    ]
    for memory in test_memories:
        print(process_memory(memory))


if len(sys.argv) > 1 and sys.argv[1] == "test":
    test()

else:
    filename = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != "test" else "input"
    memory = load_memory(filename)
    sum = process_memory(memory)
    print(sum)
