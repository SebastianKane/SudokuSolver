"""Acceptance suite: solves the benchmark set, validates every solution
independently of the solver's own logic, and rejects contradictions."""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
sys.setrecursionlimit(10000)

from SudokuTools import SudokuSolver as st

EASY = ("530070000600195000098000060800060003"
        "400803001700020006060000280000419005000080079")
SEVENTEEN_CLUE = ("000000010400000000020000000000050407"
                  "008000300001090000300400200050100000000806000")
INKALA_2010 = ("005300000800000020070010500400005300"
               "010070006003200080060500009004000030000009700")
AL_ESCARGOT = ("100007090030020008009600500005300900"
               "010080002600004000300000010040000007007000300")
EMPTY = "0" * 81
CONTRADICTION = "55" + EASY[2:]   # two 5s adjacent in the top row


def solve(s):
    p = st.Puzzle()
    p.load_puzzle(s)
    return p.solve()


def assert_valid(sol, clues):
    assert sol is not None
    grid = [list(map(int, sol.split("\n")[r])) for r in range(9)]
    want = list(range(1, 10))
    for i in range(9):
        assert sorted(grid[i]) == want, f"row {i} invalid"
        assert sorted(grid[r][i] for r in range(9)) == want, f"col {i} invalid"
    for br in range(3):
        for bc in range(3):
            box = sorted(grid[br * 3 + r][bc * 3 + c]
                         for r in range(3) for c in range(3))
            assert box == want, f"box {br},{bc} invalid"
    flat = "".join(str(grid[r][c]) for r in range(9) for c in range(9))
    for i, ch in enumerate(clues):
        if ch != "0":
            assert flat[i] == ch, f"clue at {i} was overwritten"


def test_typical():
    assert_valid(solve(EASY), EASY)


def test_seventeen_clue_minimal():
    assert_valid(solve(SEVENTEEN_CLUE), SEVENTEEN_CLUE)


def test_inkala_worlds_hardest():
    assert_valid(solve(INKALA_2010), INKALA_2010)


def test_al_escargot():
    assert_valid(solve(AL_ESCARGOT), AL_ESCARGOT)


def test_empty_grid():
    assert_valid(solve(EMPTY), EMPTY)


def test_contradiction_returns_none():
    assert solve(CONTRADICTION) is None


def test_demo_copy_is_verbatim():
    """docs/SudokuSolver.py is a deployment copy for the Pages demo; it must
    never drift from the source of truth."""
    root = pathlib.Path(__file__).parent
    src = (root / "SudokuTools" / "SudokuSolver.py").read_text()
    demo = (root / "docs" / "SudokuSolver.py").read_text()
    assert src == demo, "docs/SudokuSolver.py drifted from SudokuTools/SudokuSolver.py"
