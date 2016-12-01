from vbe.stv import stv, Ambiguous
from vbe.irv_example import condorcet_winner


def is_splitting_example(election):
    try:
        for options in [
            {}, {'wright_restart': True}
        ]:
            if stv(election, 1, **options).issubset(
                stv(election, 2, **options)
            ):
                return False
        return True
    except Ambiguous:
        return False


non_condorcet_splitter = [
    [0, 1, 2], [0, 1, 2], [0, 1, 2], [0, 1, 2], [0, 1, 2], [0, 1, 2],
    [1, 0, 2], [1, 0, 2], [1, 0, 2], [1, 0, 2], [1, 0, 2],
    [2, 1, 0], [2, 1, 0], [2, 1, 0], [2, 1, 0], [2, 1, 0], [2, 1, 0],
    [2, 1, 0], [2, 1, 0], [2, 1, 0]]

assert is_splitting_example(non_condorcet_splitter)


if __name__ == '__main__':
    from vbe.output import output_votes, name, joined_list

    result = non_condorcet_splitter

    winner = list(stv(result, 1))[0]
    house = sorted(stv(result, 2))
    assert len(house) == 2

    assert winner != condorcet_winner(non_condorcet_splitter)

    print("\n------------\n")
    print(result)
    print("\n------------\n")

    print("%d voters are choosing between %d candidates: %s." % (
        len(result), len(result[0]), joined_list(sorted(result[0]))
    ))
    print()

    output_votes(result)

    print()

    print((
        "The IRV winner is %s, but when electing two candidates "
        "we elect %s and %s") % (
        name(winner), name(house[0]), name(house[1])))

    print()

    print("Note that despite this the Condorcet winner is %s, not %s." % (
        name(condorcet_winner(result)), name(winner)
    ))
