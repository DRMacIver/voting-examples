from vbe.irv_example import plurality_winner, irv_winner, condorcet_winner
from vbe.errors import Ambiguous


def irv_sucks(votes):
    try:
        pl = plurality_winner(votes)
        if condorcet_winner(votes) != pl:
            return False
        if irv_winner(votes) != pl:
            print(votes)
            return True
    except Ambiguous:
        return False

ex1 = [[0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [1, 0, 2, 3, 4], [1, 0, 2, 3, 4], [1, 0, 2, 3, 4], [2, 0, 1, 3, 4], [2, 0, 1, 3, 4], [2, 0, 1, 3, 4], [2, 0, 1, 3, 4], [2, 0, 1, 3, 4], [3, 4, 2, 0, 1], [3, 4, 2, 0, 1]
, [4, 2, 0, 1, 3], [4, 2, 0, 1, 3], [4, 2, 0, 1, 3], [4, 2, 0, 1, 3]]

ex2 = [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]
, [0, 1, 2, 3], [1, 0, 2, 3], [1, 0, 2, 3], [1, 0, 2, 3], [1, 0, 2, 3], [1, 0, 2, 3], [1, 0, 2, 3], [1, 0, 2, 3], [1, 0, 2, 3], [1, 0, 2, 3], [1, 0, 2, 3], [1, 0, 2, 3], [1, 0, 2, 3], [1, 0, 2, 3], [1, 0, 2, 3], [1, 0, 2, 3], [1, 0, 2, 3
], [1, 0, 2, 3], [1, 0, 2, 3], [1, 0, 2, 3], [2, 0, 1, 3], [2, 0, 1, 3], [2, 3, 0, 1], [2, 3, 0, 1], [2, 3, 0, 1], [2, 3, 0, 1], [2, 3, 0, 1], [2, 3, 0, 1], [2, 3, 0, 1], [2, 3, 0, 1], [3, 1, 0, 2], [3, 1, 0, 2], [3, 1, 0, 2], [3, 1, 0,
2], [3, 1, 0, 2], [3, 1, 0, 2], [3, 1, 0, 2], [3, 1, 0, 2], [3, 1, 0, 2], [3, 1, 0, 2], [3, 1, 0, 2], [3, 1, 0, 2]]

if __name__ == '__main__':
    from vbe.output import output_election, name
    result = ex2

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
    from vbe.simple_runoff_example import simple_irv_winner

    assert simple_irv_winner(result) == plurality_winner(result)
