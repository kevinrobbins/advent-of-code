import enum
import sys

def load_word_search(filename):
    with open(filename) as f:
        return f.readlines()


def search(word_search, word):
    num_found = 0
    reverse_word = word[::-1]
    for row_num, row in enumerate(word_search):
        # An X can't have its middle in the first or last row
        if row_num == 0 or row_num == len(word_search) - 1:
            continue

        for col_num, cell in enumerate(row):
            # An X can't have its middle in the first or last col
            if col_num == 0 or col_num == len(word_search) - 1:
                continue

            # Searching for Xs from the middle is way easier so don't evaluate
            # anything other than A
            if cell != "A":
                continue

            southwest = word_search[row_num-1][col_num-1] + cell + word_search[row_num+1][col_num+1]
            if southwest != word and southwest != reverse_word:
                continue

            northeast = word_search[row_num-1][col_num+1] + cell + word_search[row_num+1][col_num-1]
            if northeast != word and northeast != reverse_word:
                continue

            num_found += 1

    return num_found


filename = sys.argv[1] if len(sys.argv) > 1 else "input"
word_search = load_word_search(filename)
matches = search(word_search, "MAS")
print(matches)
