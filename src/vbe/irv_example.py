from collections import Counter
from vbe.errors import Ambiguous


def irv_winner(votes):
    candidates = set(c for v in votes for c in v)
    n = len(votes)
    while candidates:
        scores = Counter()
        for v in votes:
            for c in v:
                if c in candidates:
                    scores[c] += 1
                    break
        best = max(scores.values())
        if best * 2 > n:
            winners = [c for c, v in scores.items() if v == best]
            assert len(winners) == 1
            return winners[0]
        worst = min(scores[c] for c in candidates)
        losers = [c for c in candidates if scores[c] == worst]
        assert len(losers) >= 1
        if len(losers) > 1:
            raise Ambiguous()
        candidates.remove(losers[0])
    raise Ambiguous()


def condorcet_winner(votes):
    victories = Counter()
    n = len(votes[0])
    for v in votes:
        for i, r in enumerate(v):
            for s in v[i+1:]:
                victories[(r, s)] += 1
    winners = [
        i for i in range(n)
        if all(victories[(i, j)] * 2 > len(votes) for j in range(n) if j != i)
    ]
    assert len(winners) <= 1
    if not winners:
        raise Ambiguous()
    return winners[0]


def plurality_winner(votes):
    scores = Counter(v[0] for v in votes)
    winning_score = max(scores.values())
    winners = [c for c, v in scores.items() if v == winning_score]
    assert winners
    if len(winners) > 1:
        raise Ambiguous()
    return winners[0]


def key_irv_example(votes):
    """This tests whether an example has unambiguous IRV, Condorcet and
    Plurality winners which are all different."""
    try:
        w1 = irv_winner(votes)
        w2 = plurality_winner(votes)
        if w1 == w2:
            return False
        w3 = condorcet_winner(votes)
        if (w1 != w3) and (w2 != w3):
            return True
    except Ambiguous:
        return False


def irv_sucks(votes):
    try:
        pl = plurality_winner(votes)
        if condorcet_winner(votes) != pl:
            return False
        return irv_winner(votes) != pl
    except Ambiguous:
        return False


if __name__ == '__main__':
    from vbe.construction import find_election
    print(find_election(irv_sucks))

    import sys; sys.exit(0)

    from vbe.construction import find_election
    from vbe.output import output_election, name

    result = find_election(key_irv_example, 4)

    print("\n------------\n")
    print(result)
    print("\n------------\n")

    output_election(result, 1)

    print()
    print("The Plurality winner is %s." % (name(plurality_winner(result)),))
    print()
    print("The IRV winner is %s." % (name(irv_winner(result)),))
    print()
    print("The Condorcet winner is %s." % (name(condorcet_winner(result)),))
