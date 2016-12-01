from vbe.irv_example import plurality_winner, irv_winner, condorcet_winner
from vbe.errors import Ambiguous


def irv_works(votes):
    try:
        iv = irv_winner(votes)
        if condorcet_winner(votes) != iv:
            return False
        if plurality_winner(votes) != iv:
            print(votes)
            return True
    except Ambiguous:
        return False

if __name__ == '__main__':
    from vbe.construction import find_election
    from vbe.output import output_election, name
    result = find_election(irv_works, 3)

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
