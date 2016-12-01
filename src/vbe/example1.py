from vbe.irv_example import key_irv_example
from vbe.stv_splitting import is_splitting_example


example = [
    [0, 1, 2], [0, 1, 2], [0, 1, 2], [0, 1, 2], [0, 1, 2],
    [1, 0, 2], [1, 0, 2],
    [2, 1, 0], [2, 1, 0], [2, 1, 0], [2, 1, 0], [2, 1, 0], [2, 1, 0]
]


assert key_irv_example(example)
assert not is_splitting_example(example)
