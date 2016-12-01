try:
    from gmpy2 import mpq as Fraction
except ImportError:
    from fractions import Fraction
from collections import defaultdict
import math
from random import Random
from vbe.errors import Ambiguous


def droop_quota(voters, winners):
    return Fraction(math.floor(voters / (winners + 1)) + 1)


def hare_quota(voters, winners):
    return Fraction(voters, winners)


def initial_weight_votes(votes):
    vote_weights = defaultdict(lambda: Fraction(0))
    for v in votes:
        vote_weights[tuple(v)] += Fraction(1)
    return vote_weights


def reweight_votes(original_vote_weights, candidates):
    vote_weights = defaultdict(lambda: Fraction(0))
    for v, w in original_vote_weights.items():
        if w > 0:
            vote_weights[tuple(w for w in v if w in candidates)] += w
    return vote_weights


class StandardCounting(object):

    def __init__(self, votes, winners, quota_type):
        self.winners = winners
        self.votes = votes
        self.quota = quota_type(len(votes), winners)
        candidates = sorted(set(votes[0]))
        for v in votes:
            assert sorted(v) == candidates
        self.candidates = set(candidates)
        self.elected = set()
        self.disqualified = set()
        self.vote_weights = initial_weight_votes(self.votes)

    def elect_winners(self):
        eligible = self.candidates - self.elected - self.disqualified
        self.vote_weights = reweight_votes(self.vote_weights, eligible)
        if not self.vote_weights:
            raise Ambiguous()

        current_scores = {c: Fraction(0) for c in eligible}
        voters = defaultdict(lambda: [])

        for v, w in self.vote_weights.items():
            c = v[0]
            assert c in eligible
            voters[c].append(v)
            current_scores[c] += w

        n_winners = 0
        for candidate, score in current_scores.items():
            if score >= self.quota:
                n_winners += 1
                self.elected.add(candidate)
                excess = score - self.quota
                reweight = excess / score
                assert 0 <= reweight < 1
                for v in voters[candidate]:
                    self.vote_weights[v] *= reweight

        assert len(self.elected) * self.quota + sum(
            self.vote_weights.values()) == len(self.votes)
        return current_scores

    def disqualify(self, candidate):
        self.disqualified.add(candidate)

    def restart(self):
        self.elected.clear()
        self.vote_weights = initial_weight_votes(self.votes)


MEEK_PRECISION = Fraction(1, 10 ** 5)
MEEK_ITERATIONS = 10 ** 3


class MeekCounting(object):

    def __init__(self, votes, winners, quota_type):
        self.winners = winners
        self.votes = votes
        self.quota_type = quota_type
        candidates = sorted(set(votes[0]))
        for v in votes:
            assert sorted(v) == candidates
        self.candidates = set(candidates)
        self.elected = set()
        self.disqualified = set()
        self.excess = 0

    def elect_winners(self):
        vote_retention = {
            c: Fraction(0) if c in self.disqualified else Fraction(1)
            for c in self.candidates
        }

        for _ in range(MEEK_ITERATIONS):
            excess = Fraction(0)
            candidate_scores = {
                c: Fraction(0) for c in self.candidates
            }
            for v in self.votes:
                remaining = Fraction(1)
                for c in v:
                    capture = vote_retention[c]
                    assert 0 <= capture <= 1
                    candidate_scores[c] += capture * remaining
                    remaining *= (1 - capture)
                assert remaining == 0

            quota = self.quota_type(len(self.votes) - excess, self.winners)
            precision = 0
            for v in candidate_scores.values():
                assert v >= 0
            assert sum(candidate_scores.values()) + excess == len(self.votes)

            for e in self.elected:
                score = candidate_scores[e]
                if score == 0:
                    reweight = 1
                else:
                    reweight = quota / score
                vote_retention[e] = min(
                    Fraction(1), vote_retention[e] * reweight)
                precision = max(precision, abs(1 - reweight))
            for e in self.disqualified:
                assert candidate_scores[e] == 0
            if precision <= MEEK_PRECISION:
                for candidate, score in candidate_scores.items():
                    if score >= quota:
                        self.elected.add(candidate)
                return candidate_scores
        assert False

    def disqualify(self, candidate):
        assert candidate not in self.disqualified
        self.disqualified.add(candidate)

    def restart(self):
        self.elected.clear()


def HareClark(seed):
    class HC(object):

        def __init__(self, votes, winners, quota_type):
            self.winners = winners
            self.votes = votes
            self.quota = quota_type(len(votes), winners)
            candidates = sorted(set(votes[0]))
            for v in votes:
                assert sorted(v) == candidates
            self.candidates = set(candidates)
            self.elected = set()
            self.disqualified = set()
            self.random = Random(seed)
            self.restart()

        def elect_winners(self):
            scores = {
                c: len(v) for c, v in self.allocated_votes.items()
            }
            for c, v in scores.items():
                if v >= self.quota:
                    self.elected.add(c)
            return scores

        def disqualify(self, candidate):
            assert candidate not in self.disqualified
            self.disqualified.add(candidate)
            self.__allocate_votes(self.allocated_votes.pop(candidate))

        def restart(self):
            self.elected.clear()
            self.allocated_votes = {
                c: [] for c in self.candidates
                if c not in self.disqualified
            }
            self.__allocate_votes(self.votes)

        def __allocate_votes(self, votes):
            votes = list(votes)
            self.random.shuffle(votes)
            for v in votes:
                for c in v:
                    if c not in self.disqualified:
                        pool = self.allocated_votes[c]
                        if len(pool) < self.quota:
                            assert c not in self.elected
                            pool.append(v)
                            break

    HC.__name__ = 'HareClark(%r)' % (seed,)
    return HC


def stv(
    votes, winners, quota_type=droop_quota, wright_restart=False,
    tally_method=StandardCounting, print_steps=False, break_ties=False,
):

    def note(*args, **kwargs):
        if print_steps:
            print(*args, **kwargs)

    count = tally_method(votes, winners, quota_type)

    if winners * quota_type(len(votes), winners) > len(votes):
        raise Ambiguous()

    while True:
        assert not (count.elected & count.disqualified)
        if (
            len(count.elected) + len(count.disqualified) ==
            len(count.candidates)
        ):
            raise Ambiguous()
        prev_winners = len(count.elected)
        xs = set(count.elected)
        current_scores = count.elect_winners()
        if xs != count.elected:
            note('Elected: %r' % (count.elected - xs,))
        else:
            note('Scores: %r' % (current_scores,))
        for c in count.disqualified:
            current_scores.pop(c, None)

        assert len(count.elected) <= winners
        if len(count.elected) == winners:
            return count.elected

        assert len(count.elected) >= prev_winners

        if prev_winners != len(count.elected):
            continue

        losing_score = min(current_scores.values())
        losers = [
            c for c, v in current_scores.items() if v == losing_score]
        assert losers
        if len(losers) > 1:
            if break_ties:
                losers = [min(losers)]
            else:
                raise Ambiguous()
        count.disqualify(losers[0])
        note('Disqualified:', losers[0])
        if wright_restart:
            note('Restarting count with %r eliminated' % (count.disqualified,))
            count.restart()
    return count.elected


def interesting_for_wright_reasons(election):
    try:
        votes, to_elect = election
        base_winners = stv(*election)
        wright_winners = stv(*election, wright_restart=True)
        if base_winners == wright_winners:
            return False
        all_winners = base_winners | wright_winners
        drop_out_vote = [
            [d for d in v if d in all_winners] for v in votes
        ]
        if stv(
            drop_out_vote, to_elect
        ) != stv(drop_out_vote, to_elect, wright_restart=True):
            return True
    except Ambiguous:
        return False
