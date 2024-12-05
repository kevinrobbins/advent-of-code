import re
import sys

def load_memory(filename):
    with open(filename) as f:
        return f.read()

filename = sys.argv[1] if len(sys.argv) > 1 else "input"
memory = load_memory(filename)
operations = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', memory)

product_sum = 0
for operation in operations:
    assert len(operation) == 2
    product = int(operation[0]) * int(operation[1])
    product_sum += product

print(product_sum)
