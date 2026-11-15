"""Check the controlled eight-well mixer on every physical input column."""
from itertools import permutations, product

PORTS = range(0, 8, 2)
BASIS = tuple(product(range(8), (1, -1)))


def propagate(a, b, source, ticks=16, gate='H'):
    """After the one balanced tick, store its 1/sqrt(2) factor symbolically."""
    state = {source: (1, False)}
    delay = ((b - a) % 8) // 2
    meeting = (a + delay) % 8
    for tick in range(ticks):
        after = {}
        for (x, rail), (sign, balanced) in state.items():
            if x == meeting and tick == delay and gate == 'H':
                assert not balanced
                exits = [(1, sign, True), (-1, sign * rail, True)]
            else:
                turn = (x == b and tick in (0, 8)) or (gate == 'X' and x == meeting and tick == delay)
                exits = [(-rail if turn else rail, sign, balanced)]
            for direction, coefficient, has_factor in exits:
                cell = ((x + direction) % 8, direction)
                assert cell not in after
                after[cell] = coefficient, has_factor
        state = after
    return state


if __name__ == "__main__":
    for a, b in permutations(PORTS, 2):
        for cell in BASIS:
            expected = {cell: (1, False)}
            if cell in ((a, 1), (b, 1)):
                expected = {(a, 1): (1, True), (b, 1): (1 if cell == (a, 1) else -1, True)}
            assert propagate(a, b, cell) == expected, (a, b, cell)

            swap = {(a, 1): (b, 1), (b, 1): (a, 1)}
            assert propagate(a, b, cell, gate='X') == {swap.get(cell, cell): (1, False)}
    for a in PORTS:
        b = (a-2) % 8
        for gate in ('I', 'H'):
            for x in PORTS:
                dest = ((x+4) % 8, -1 if x == b else 1)
                expected = {dest: (1, False)}
                if gate == 'H' and x in (a, b):
                    expected = {((a+4)%8, 1): (1, True), ((b+4)%8, -1): (1 if x == a else -1, True)}
                if x not in (a, b):
                    delta = (dest[0] - (a+3)) % 8
                    assert min(delta, 8-delta) == 3
                assert propagate(a, b, (x,1), ticks=4, gate=gate) == expected
    print("Swap columns, early panels and both protected distances agree.")
