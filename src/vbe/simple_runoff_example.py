from vbe.errors import Ambiguous
from vbe.irv_example import irv_winner, plurality_winner, condorcet_winner
from collections import Counter


def simple_irv_winner(votes):
    candidates = set(c for v in votes for c in v)
    if not candidates:
        raise Ambiguous()
    if len(candidates) == 1:
        return list(candidates)[0]

    if len(candidates) > 2:
        scores = Counter()
        for v in votes:
            for c in v:
                if c in candidates:
                    scores[c] += 1
                    break
        t = list(candidates)
        t.sort(key=scores.__getitem__)
        threshold = scores[t[-2]]
        remainder = [c for c in candidates if scores[c] >= threshold]
        assert len(remainder) >= 2
        if len(remainder) > 2:
            raise Ambiguous()
        candidates = set(remainder)

    new_scores = Counter()
    for v in votes:
        for c in v:
            if c in candidates:
                new_scores[c] += 1
                break

    a, b = candidates
    n = len(votes)
    assert new_scores[a] + new_scores[b] == n
    if new_scores[a] == new_scores[b]:
        raise Ambiguous()
    return max((a, b), key=new_scores.__getitem__)


def distinct(votes):
    try:
        s = simple_irv_winner(votes)
        irv = irv_winner(votes)
        p = plurality_winner(votes)
        return (
            (p != irv) and (p != s) and (s != irv)
        )
    except Ambiguous:
        return False


def distinct_from_condorcet(votes):
    try:
        p = plurality_winner(votes)
        c = condorcet_winner(votes)
        if c == p:
            return False
        s = simple_irv_winner(votes)
        if s == c:
            return False
        irv = irv_winner(votes)
        return (
            (p != irv) and (p != s) and (s != irv)
        )
    except Ambiguous:
        return False


example = [
    [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3],
    [0, 1, 2, 3],
    [1, 2, 0, 3], [1, 2, 0, 3], [1, 2, 0, 3], [1, 2, 0, 3], [1, 2, 0, 3],
    [2, 1, 0, 3], [2, 1, 0, 3], [2, 1, 0, 3], [2, 1, 0, 3],
    [3, 2, 0, 1], [3, 2, 0, 1]
]

example2 = [
    [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [1, 0, 2, 3],
    [1, 0, 2, 3], [1, 0, 2, 3],
    [2, 1, 0, 3], [2, 1, 0, 3],
    [3, 1, 0, 2], [3, 1, 0, 2], [3, 1, 0, 2], [3, 1, 0, 2], [3, 1, 0, 2]]

if __name__ == '__main__':
    from vbe.output import output_election, name

    result = example2

    print("\n------------\n")
    print(result)
    print("\n------------\n")

    output_election(result, 1)

    print()
    print("The Plurality winner is %s." % (name(plurality_winner(result)),))
    print()
    print("The IRV winner is %s." % (name(irv_winner(result)),))
    print()
    print("The Simple IRV winner is %s." % (name(simple_irv_winner(result)),))
    print()
    print("The Condorcet winner is %s." % (name(condorcet_winner(result)),))
