from enum import IntEnum, auto
import sys


class ReportState(IntEnum):
    Descending = auto()
    Undetermined = auto()
    Ascending = auto()


reports = []


def read_input(filename):
    with open(filename) as f:
        for report_raw in f.readlines():
            report_parsed = [int(level_raw) for level_raw in report_raw.split()]
            reports.append(report_parsed)


filename = sys.argv[1] if len(sys.argv) > 1 else "input"

read_input(filename)

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


num_safe = 0
for report in reports:
    previous_level = None
    previous_state = ReportState.Undetermined

    for current_level in report:
        # First level in report
        if previous_level is None:
            previous_level = current_level
            continue

        if not is_within_safe_range(current_level, previous_level):
            break

        if previous_level > current_level:
            current_state = ReportState.Descending
        elif previous_level < current_level:
            current_state = ReportState.Ascending
        else:
            # Not increasing or decreasing
            break

        if not has_consistent_direction(previous_state=previous_state, current_state=current_state):
            break

        previous_level = current_level
        previous_state = current_state

    else:
        # Safe Report
        num_safe += 1


print(num_safe)
