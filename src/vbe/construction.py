import hypothesis
import hypothesis.strategies as st
from hypothesis.errors import NoSuchExample, UnsatisfiedAssumption


@st.composite
def permutations(draw, elements):
    elements = list(elements)
    if draw(st.booleans()):
        elements.reverse()
    elements = draw(st.permutations(elements))
    return draw(st.permutations(elements))


@st.composite
def elections(draw, n_candidates=None):
    n_candidates = draw(st.integers(3, n_candidates or 10))
    votes = draw(
        st.lists(
            permutations(range(n_candidates)),
            average_size=50, min_size=2),)
    result = []
    for v in votes:
        for _ in range(draw(st.integers(1, 10))):
            result.append(v)
    result.sort()
    return result


def smaller_elections(election):
    votes = election

    candidates = sorted(votes[0])
    for c in candidates:
        drop_out_vote = [
            [d for d in v if d != c] for v in votes
        ]
        yield drop_out_vote
    for i in range(len(votes)):
        w = list(votes)
        del w[i]
        yield w
    for i in range(len(votes)):
        t = list(reversed(votes[i]))
        if t < votes[i]:
            w = list(votes)
            w[i] = t
            yield w

    for i in range(len(votes)):
        v = votes[i]
        u = sorted(candidates)
        if u != v:
            yield [
                u if s == v else s
                for s in votes
            ]
    for i in range(len(votes)):
        v = votes[i]
        for j in range(len(v)):
            for k in range(j + 1, len(v)):
                if v[j] > v[k]:
                    u = list(v)
                    u[j], u[k] = u[k], u[j]
                    yield [
                        u if s == v else s
                        for s in votes
                    ]

    for i in range(len(votes)):
        for j in range(len(votes)):
            if votes[i] > votes[j]:
                w = list(votes)
                w[i] = w[j]
                yield w


def minimize_election(election, predicate):
    election = list(map(list, election))
    changed = True
    seen = set()
    while changed:
        changed = False
        election.sort()
        for s in smaller_elections(election):
            if s != election and predicate(s):
                track = tuple(map(tuple, election))
                assert track not in seen
                seen.add(track)
                changed = True
                election = s
                break
    return election


def normalize_election(election):
    election = list(map(list, election))
    

def find_election(predicate, n=10):
    best = hypothesis.find(
        elections(n), predicate,
        settings=hypothesis.settings(
            max_examples=10**6, max_iterations=10**6, timeout=-1,
            verbosity=hypothesis.Verbosity.debug, max_shrinks=10**6,
        ))

    hi = len(best[0])
    lo = 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        try:
            best = hypothesis.find(elections(mid), predicate)
            hi = mid
        except NoSuchExample:
            lo = mid

    def wrapped_predicate(election):
        try:
            if predicate(election):
                print("Shrunk", election)
                return True
            return False
        except UnsatisfiedAssumption:
            return False
    return minimize_election(best, wrapped_predicate)
