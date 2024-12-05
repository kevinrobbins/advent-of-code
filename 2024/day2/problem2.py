from enum import IntEnum, auto
import sys


class ReportState(IntEnum):
    Descending = auto()
    Undetermined = auto()
    Ascending = auto()


def load_reports(filename):
    reports = []
    with open(filename) as f:
        for report_raw in f.readlines():
            report_parsed = [int(level_raw) for level_raw in report_raw.split()]
            reports.append(report_parsed)

    return reports

def has_consistent_direction(previous_state, current_state):
    if previous_state == ReportState.Undetermined:
        return True

    if previous_state == current_state:
        return True

    return False

def is_within_safe_range(level, previous_level):
    difference = abs(level - previous_level)
    if difference >= 1 and difference <= 3:
        return True

    else:
        return False

def is_safe(previous_level, current_level, previous_state, current_state):
    if not is_within_safe_range(current_level, previous_level):
        return False

    if not has_consistent_direction(previous_state=previous_state, current_state=current_state):
        return False

    return True

def evaluate_report(full_report):
    report_variations = [full_report]
    for i in range(len(full_report)):
        left = full_report[:i]
        right = full_report[i+1:]
        report_variations.append(left+right)

    for report in report_variations:
        previous_level = None
        previous_state = ReportState.Undetermined

        for current_level in report:
            # First level in report
            if previous_level is None:
                previous_level = current_level
                continue

            if previous_level > current_level:
                current_state = ReportState.Descending
            elif previous_level < current_level:
                current_state = ReportState.Ascending
            else:
                break

            if not is_safe(previous_level, current_level, previous_state, current_state):
                break

            previous_level = current_level
            previous_state = current_state

        else:
            return True

    return False


def main(reports):
    num_safe = 0
    for full_report in reports:
        if evaluate_report(full_report):
            num_safe += 1
    print(num_safe)


def test():
    test_reports = [
        ([7, 6, 4, 2, 1], True),
        ([1, 2, 7, 8, 9], False),
        ([9, 7, 6, 2, 1], False),
        ([1, 3, 2, 4, 5], True),
        ([1, 3, 6, 7, 9], True),
        ([7, 6, 10, 11, 13], True),
        ([1, 1, 2, 3, 4], True),
        ([1, 2, 2, 3, 4], True),
        ([1, 2, 3, 4, 4], True),
        ([1, 5, 2, 3, 4], True),
        ([1, 5, 6, 7, 8], True),
    ]

    for report, expected_safe in test_reports:
        actual_safe = evaluate_report(report)
        if expected_safe != actual_safe:
            print(f"FAIL: {report} was found {'SAFE' if actual_safe else 'UNSAFE'}, but expected {'SAFE' if expected_safe else 'UNSAFE'}")


if len(sys.argv) > 1 and sys.argv[1] == "test":
    test()

else:
    filename = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != "test" else "input"
    reports = load_reports(filename)
    main(reports)
