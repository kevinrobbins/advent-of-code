import enum
import sys

def load_word_search(filename):
    with open(filename) as f:
        return f.readlines()

def in_bounds(row, col, max_dim):
    if row < 0 or row >= max_dim:
        return False

    if col < 0 or col >= max_dim:
        return False

    return True

directions = [
    (-1, -1),
    (-1,  0),
    (-1,  1),
    (0,   1),
    (1,   1),
    (1,   0),
    (1,  -1),
    (0,  -1),
]


def search(word_search, word):
    num_found = 0
    for row in range(len(word_search)):
        for col in range(len(word_search[row])):
            for row_mod, col_mod in directions:
                candidate_word = ""
                curr_row, curr_col = row, col
                while (
                    word.startswith(candidate_word)
                    and in_bounds(curr_row, curr_col, len(word_search))
                ):
                    candidate_word += word_search[curr_row][curr_col]

                    if candidate_word == word:
                        num_found += 1
                        break

                    curr_row += row_mod
                    curr_col += col_mod
    return num_found


filename = sys.argv[1] if len(sys.argv) > 1 else "input"
word_search = load_word_search(filename)
matches = search(word_search, "XMAS")
print(matches)
