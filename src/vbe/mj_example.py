from collections import Counter
from vbe.mj import MajorityJudgement
from vbe.output import name
from vbe.errors import Ambiguous


def condorcet_winner(votes):
    if not (votes and votes[0]):
        raise Ambiguous()
    victories = Counter()
    n = len(votes[0])
    for v in votes:
        for i in range(n):
            for j in range(n):
                if v[i] > v[j]:
                    victories[(i, j)] += 1
    winner = [
        i for i in range(n)
        if all(victories[(i, j)] * 2 > len(votes) for j in range(n) if j != i)
    ]
    assert len(winner) <= 1
    if not winner:
        raise Ambiguous()
    return winner[0]


def mj_winner(votes):
    if not (votes and votes[0]):
        raise Ambiguous()
    max_score = max(c for v in votes for c in v)
    n_candidates = len(votes[0])
    tallies = [[0] * (max_score + 1) for _ in range(n_candidates)]
    for v in votes:
        for c, score in enumerate(v):
            tallies[c][score] += 1
    with_rankings = [(MajorityJudgement(t), i) for i, t in enumerate(tallies)]
    winning_score = max(c for c, _ in with_rankings)
    winner = [i for c, i in with_rankings if c == winning_score]
    if len(winner) != 1:
        raise Ambiguous()
    return winner[0]


def range_winner(votes):
    if not (votes and votes[0]):
        raise Ambiguous()
    scores = [0] * len(votes[0])
    for v in votes:
        for c, score in enumerate(v):
            scores[c] += score
    winning_score = max(scores)
    winner = [i for i, c in enumerate(scores) if c == winning_score]
    if len(winner) != 1:
        raise Ambiguous()
    return winner[0]


all_results_distinct = [[1, 2, 0], [2, 0, 3], [3, 4, 3], [3, 4, 3], [4, 0, 3]]
assert mj_winner(all_results_distinct) == 2
assert condorcet_winner(all_results_distinct) == 1
assert range_winner(all_results_distinct) == 0

disagree_with_condorcet = [[0, 1], [1, 2], [2, 0], [2, 0], [2, 3]]
assert mj_winner(disagree_with_condorcet) == 0
assert condorcet_winner(disagree_with_condorcet) == 1
assert range_winner(disagree_with_condorcet) == 0

range_beats_mj = [[3, 4], [3, 2], [0, 1]]
assert mj_winner(range_beats_mj) == 0
assert condorcet_winner(range_beats_mj) == 1
assert range_winner(range_beats_mj) == 1


mj_beats_range = [[0, 1], [3, 0], [0, 1]]
assert mj_winner(mj_beats_range) == 1
assert condorcet_winner(mj_beats_range) == 1
assert range_winner(mj_beats_range) == 0


def dump_vote(votes):
    counts = Counter(tuple(v) for v in votes)
    counts = list(counts.items())
    counts.sort(key=lambda x: (-x[1], x[0]))
    print("\\begin{itemize}")
    for vote, n in counts:
        grade = []
        k = len(vote)
        for i, c in enumerate(vote):
            base = "%s as %d" % (name(i), c)
            if i == k - 1:
                base = "and " + base
            grade.append(base)
        grade = ', '.join(grade)
        if n > 1:
            print("\item %d voters grade %s" % (
                n, grade
            ))
        else:
            print("\item 1 voter grades %s" % (
                grade,
            ))
    print("\\end{itemize}")

if __name__ == '__main__':
    print("The first one demonstrates all three approaches producing a "
          "different result:")

    dump_vote(all_results_distinct)
    print((
        "The Condorcet winner is %s, but the Majority Judgment winner is %s, "
        "and the range winner is %s."
    ) % (
        name(condorcet_winner(all_results_distinct)),
        name(mj_winner(all_results_distinct)),
        name(range_winner(all_results_distinct)),
    ))

    print(
        "It's also possible for any two of them to coincide and disagree "
        "with the third."
    )

    print()

    print(
        "The following shows an example where majority jugment and range "
        "voting agree on a candidate, but it's not the Condorcet winner."
    )

    dump_vote(disagree_with_condorcet)
    print((
        "The Condorcet winner is %s, but the Majority Judgment and range "
        "winner is %s."
    ) % (
        name(condorcet_winner(disagree_with_condorcet)),
        name(mj_winner(disagree_with_condorcet)),
    ))

    print(
        "While in the following election the Range Voting winner is preferred "
        "by the majority to the Majority Judgment winner:"
    )

    dump_vote(range_beats_mj)
    print((
        "The Condorcet and Range winner is %s, but the Majority Judgment "
        "winner is %s."
    ) % (
        name(condorcet_winner(range_beats_mj)),
        name(mj_winner(range_beats_mj)),
    ))

    dump_vote(mj_beats_range)
    print((
        "The Condorcet and Majority Judgment winner is %s, but the Range "
        "winner is %s."
    ) % (
        name(condorcet_winner(mj_beats_range)),
        name(range_winner(mj_beats_range)),
    ))
