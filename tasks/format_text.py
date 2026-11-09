from itertools import combinations


def can_make_lucky(digits):
    if len(digits) != 6:
        return False

    total = sum(digits)

    if total % 2 != 0:
        return False

    half = total // 2

    for group in combinations(digits, 3):
        if sum(group) == half:
            return True

    return False


def main():
    tickets = [
        (1, 2, 3, 3, 2, 1),
        (1, 2, 3, 4, 5, 6),
        (1, 2, 3, 7, 8, 9),
        (0, 0, 0, 0, 0, 0),
        (1, 2, 4, 6, 8, 9),
    ]

    for digits in tickets:
        if can_make_lucky(digits):
            print(f"{digits} -> TRUE")
        else:
            print(f"{digits} -> FALSE")

if __name__ == "__main__":
    main()
