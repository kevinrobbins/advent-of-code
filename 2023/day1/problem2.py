import sys
from typing import Dict, Optional, Tuple

NUM_WORDS: Dict[str, str] = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}


def find_first_digit(s: str) -> Tuple[int, Optional[str]]:
    for i, c in enumerate(s):
        if c.isdigit():
            return i, c

    return -1, None


def find_first_digit_backwards(s: str) -> Tuple[int, Optional[str]]:
    for i in range(len(s)-1, -1, -1):
        if s[i].isdigit():
            return i, s[i]

    return -1, None


def find_first_num_word(s: str) -> Tuple[int, Optional[str]]:
    first_num_word_index = len(s)
    first_num = None

    for num_word, num in NUM_WORDS.items():
        i = s.find(num_word)

        # Didn't find this num word
        if i < 0:
            continue

        if i < first_num_word_index:
            first_num_word_index = i
            first_num = num

    if first_num is None:
        first_num_word_index = -1

    return first_num_word_index, first_num


def find_first_num_word_backwards(s: str) -> Tuple[int, Optional[str]]:
    first_num_word_index = -1
    first_num = None

    for num_word, num in NUM_WORDS.items():
        i = s.rfind(num_word)

        # Didn't find this num word
        if i < 0:
            continue

        if i > first_num_word_index:
            first_num_word_index = i
            first_num = num

    if first_num is None:
        first_num_word_index = -1

    return first_num_word_index, first_num


def find_first_number(s: str) -> str:
    first_digit_index, digit = find_first_digit(s)
    first_num_word_index, num = find_first_num_word(s)

    if digit is None and num is None:
        raise RuntimeError("No number found")

    elif not digit:
        return num

    elif not num:
        return digit

    elif first_digit_index < first_num_word_index:
        return digit

    else:
        return num


def find_first_number_backwards(s: str) -> str:
    first_digit_index, digit = find_first_digit_backwards(s)
    first_num_word_index, num = find_first_num_word_backwards(s)

    if digit is None and num is None:
        raise RuntimeError("No number found")

    elif not digit:
        return num

    elif not num:
        return digit

    elif first_digit_index > first_num_word_index:
        return digit

    else:
        return num


def get_number_in_line(line):
    first_num_beginning = find_first_number(line)
    first_num_end = find_first_number_backwards(line)

    return int(first_num_beginning + first_num_end)


def main():
    calibration_file = '../inputs/calibration_values.txt'
    with open(calibration_file, 'r') as f:
        lines = f.readlines()

    sum = 0
    for line in lines:
        sum += get_number_in_line(line)

    print(sum)


# Tests
def assert_equal(x, y):
    if x != y:
        raise AssertionError(f"{x} not equal to {y}")


def test_find_first_digit():
    cases = {
        '12345': (0, '1'),
        'a12345': (1, '1'),
        'abc123': (3, '1'),
    }

    for test_input, expected_result in cases.items():
        result = find_first_digit(test_input)
        assert_equal(result, expected_result)


def test_find_first_digit_backwards():
    cases = {
        '12345': (4, '5'),
        'a12345': (5, '5'),
        'abc123': (5, '3'),
    }

    for test_input, expected_result in cases.items():
        result = find_first_digit_backwards(test_input)
        assert_equal(result, expected_result)


def test_find_first_num_word():
    cases = {
        'onetwo': (0, '1'),
        '3onetwo': (1, '1'),
        'abconetwo': (3, '1')
    }

    for test_input, expected_result in cases.items():
        result = find_first_num_word(test_input)
        assert_equal(result, expected_result)


def test_find_first_num_word_backwards():
    cases = {
        'onetwo': (3, '2'),
        'onetwo1': (3, '2'),
        'onetwoabc': (3, '2')
    }

    for test_input, expected_result in cases.items():
        result = find_first_num_word_backwards(test_input)
        assert_equal(result, expected_result)


def test_find_first_number():
    cases = {
        'one': '1',
        'onetwo': '1',
        'one2': '1',
        '2one': '2',
        'abc2one': '2',
        'abcone2': '1'
    }

    for test_input, expected_result in cases.items():
        result = find_first_number(test_input)
        assert_equal(result, expected_result)


def test_find_first_number_backwards():
    cases = {
        'one': '1',
        'onetwo': '2',
        'one2': '2',
        '2one': '1',
        'abc2one': '1',
        'abcone2': '2'
    }

    for test_input, expected_result in cases.items():
        result = find_first_number_backwards(test_input)
        assert_equal(result, expected_result)


def test_get_number_in_line():
    cases = {
        'two1nine': 29,
        'eightwothree': 83,
        'abcone2threexyz': 13,
        'xtwone3four': 24,
        '4nineeightseven2': 42,
        'zoneight234': 14,
        '7pqrstsixteen': 76,
    }

    for test_input, expected_result in cases.items():
        result = get_number_in_line(test_input)
        assert_equal(result, expected_result)


def test():
    tests = [
        test_find_first_digit,
        test_find_first_digit_backwards,
        test_find_first_num_word,
        test_find_first_num_word_backwards,
        test_get_number_in_line
    ]

    all_tests_passed = True
    for test in tests:
        try:
            test()

        except Exception as e:
            print(f"{test.__name__}: {str(e)}")
            all_tests_passed = False

    if all_tests_passed:
        print("All tests passed!")


if len(sys.argv) > 1 and sys.argv[1] == 'test':
    test()

else:
    main()
