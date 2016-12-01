from vbe.errors import Ambiguous
from collections import Counter
from vbe.simple_runoff_example import simple_irv_winner

def supplementary_winner(votes):
    candidates = set(c for v in votes for c in v)
    if not candidates:
        raise Ambiguous()
    if len(candidates) == 1:
        return list(candidates)[0]

    if len(candidates) > 2:
        scores = Counter()
        for v in votes:
            scores[v[0]] += 1
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
        for c in v[:2]:
            if c in candidates:
                new_scores[c] += 1
                break

    a, b = candidates
    if new_scores[a] == new_scores[b]:
        raise Ambiguous()
    return max((a, b), key=new_scores.__getitem__)


def is_not_two_round(votes):
    try:
        return supplementary_winner(votes) != simple_irv_winner(votes)
    except Ambiguous:
        return False


if __name__ == '__main__':
    from vbe.output import output_election, name
    from vbe.construction import find_election

    result = find_election(is_not_two_round)

    print("\n------------\n")
    print(result)
    print("\n------------\n")

    output_election(result, 1)

    print()
    print("The Simple IRV winner is %s." % (name(simple_irv_winner(result)),))
    print()
    print("The Supplementary winner is %s." % (name(supplementary_winner(result)),))
