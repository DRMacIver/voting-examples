from collections import Counter


def joined_list(ls):
    if len(ls) > 1:
        return '%s and %s' % (
            ', '.join(name(t) for t in ls[:-1]), name(ls[-1])
        )
    else:
        return name(ls[0])


CANDIDATE_NAMES = list("ABCDEFGHIJK")


def name(i):
    return CANDIDATE_NAMES[i]


def output_election(election, n_winners):
    assert n_winners == 1

    print("%d voters are electing a winner from %d candidates: %s." % (
        len(election), len(election[0]), joined_list(sorted(election[0]))
    ))
    print()

    output_votes(election)


def output_votes(election):
    counts = Counter(tuple(v) for v in election)
    counts = list(counts.items())
    counts.sort(key=lambda x: (-x[1], x[0]))
    print("\\begin{itemize}")
    for v, n in counts:
        vote = ", ".join(map(name, v))
        if n > 1:
            print("\item %d votes of %s" % (n, vote))
        else:
            print("\item A single vote of %s" % (vote,))
    print("\\end{itemize}")
