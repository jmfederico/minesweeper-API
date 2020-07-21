"""Define tests for MD GAme app."""
from .serializers import GameSerializer
from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Game, Cell, Status

User = get_user_model()


def create_data_board(cols, rows):
    """Return an empty data board of size cols * rows."""
    board = []
    for _ in range(cols):
        row = []
        for _ in range(rows):
            row.append({})
        board.append(row)
    return board


def create_covered_board(cols, rows):
    """Return an covered board of size cols * rows."""
    board = []
    for _ in range(cols):
        row = []
        for _ in range(rows):
            row.append("c")
        board.append(row)
    return board


class GameModelTestCase(TestCase):
    """Test the functionality of the Game model."""

    def setUp(self):
        """Set up common test data."""
        self.user = User.objects.create_user("user@example.com")

    def test_game_has_cells(self):
        """A Game cell can be accessed as an index."""
        board = [[dict()]]
        game = Game.objects.create(player=self.user, board=board)

        self.assertIsInstance(game[0, 0], Cell)

    def test_cells_generator(self):
        """It is possible to iterate over the cells of a game."""
        board = create_data_board(2, 2)
        game = Game.objects.create(player=self.user, board=board)

        cells = game.cells
        self.assertEqual(next(cells), ((0, 0), game[0, 0]))
        self.assertEqual(next(cells), ((1, 0), game[1, 0]))

    def test_non_existing_cell(self):
        """Raise KeyError: if the cell does not exist."""
        with self.subTest("empty board"):
            board = []
            game = Game.objects.create(player=self.user, board=board)

            with self.assertRaises(IndexError):
                game[0, 0]

        with self.subTest("out fo range"):
            board = [[{}, {}], [{}, {}]]
            game = Game.objects.create(player=self.user, board=board)

            with self.assertRaises(IndexError):
                game[3, 0]

    def test_neighbors(self):
        """Neighbors is a generator that can be used as a mapping."""
        board = create_data_board(10, 10)
        game = Game.objects.create(player=self.user, board=board)

        key = 0, 0
        with self.subTest(key):
            expected_neighbors = {
                (1, 0): game[1, 0],
                (0, 1): game[0, 1],
                (1, 1): game[1, 1],
            }
            self.assertEqual(dict(game.get_neighbors(key)), expected_neighbors)

        key = 9, 9
        with self.subTest(key):
            expected_neighbors = {
                (8, 8): game[8, 8],
                (9, 8): game[9, 8],
                (8, 9): game[8, 9],
            }
            self.assertEqual(dict(game.get_neighbors(key)), expected_neighbors)

        key = 4, 4
        with self.subTest(key):
            expected_neighbors = {
                (3, 3): game[3, 3],
                (4, 3): game[4, 3],
                (5, 3): game[5, 3],
                (3, 4): game[3, 4],
                (5, 4): game[5, 4],
                (3, 5): game[3, 5],
                (4, 5): game[4, 5],
                (5, 5): game[5, 5],
            }
            self.assertEqual(dict(game.get_neighbors(key)), expected_neighbors)

    def test_cell_references_game_board(self):
        """
        The dict references in a Cell, is the same dict as in the game board.

        This is important to ensure that modification at the Cell level are
        seen in the game board.
        """
        board = [[dict()]]
        game = Game.objects.create(player=self.user, board=board)

        cell = game[0, 0]
        self.assertIs(cell._data, game.board[0][0])


class CellFlagTestCase(TestCase):
    """Test the ability to flag Cells."""

    def test_cell_is_flagged(self):
        """When flagged, the is_flagged property is True."""
        cell = Cell({"status": Status.FLAGGED.value})
        self.assertTrue(cell.is_flagged)

    def test_cell_is_not_flagged(self):
        """When not flagged, the is_flagged property is False."""
        with self.subTest("marked as uncovered"):
            cell = Cell({"status": Status.UNCOVERED.value})
            self.assertFalse(cell.is_flagged)

        with self.subTest("marked as None"):
            cell = Cell({"status": None})
            self.assertFalse(cell.is_flagged)

        with self.subTest("no data about status"):
            cell = Cell({})
            self.assertFalse(cell.is_flagged)

    def test_flagging(self):
        """Calling `.flag()` marks the cell as flagged."""
        cell = Cell({})
        self.assertFalse(cell.is_flagged)
        cell.flag()
        self.assertTrue(cell.is_flagged)

    def test_unflagging(self):
        """Calling `.unflag()` marks the cell as flagged."""
        cell = Cell({"status": Status.FLAGGED.value})
        self.assertTrue(cell.is_flagged)
        cell.unflag()
        self.assertFalse(cell.is_flagged)


class CellCoveredTestCase(TestCase):
    """Test the ability to flag Cells."""

    def test_cell_is_covered(self):
        """By default cells are covered."""
        with self.subTest("no data about status"):
            cell = Cell({})
            self.assertTrue(cell.is_covered)

        with self.subTest("marked as None"):
            cell = Cell({"status": None})
            self.assertTrue(cell.is_covered)

        with self.subTest("marked as Flagged"):
            cell = Cell({"status": Status.FLAGGED.value})
            self.assertTrue(cell.is_covered)

    def test_cell_is_not_covered(self):
        """When uncovered, the is_covered property is False."""
        cell = Cell({"status": Status.UNCOVERED.value})
        self.assertFalse(cell.is_covered)

    def test_uncovering(self):
        """Calling `.uncover()` marks the cell as uncovered."""
        cell = Cell({})
        self.assertTrue(cell.is_covered)
        cell.uncover()
        self.assertFalse(cell.is_covered)


class CellBombTestCase(TestCase):
    """Test the ability of Cells to contain bombs."""

    def test_cell_has_bomb(self):
        """When has a bomb, the has_bomb property is True."""
        cell = Cell({"bomb": True})
        self.assertTrue(cell.has_bomb)

    def test_cell_has_no_bomb(self):
        """When does not have a bomb, the has_bomb property is False."""
        with self.subTest("marked as False"):
            cell = Cell({"bomb": False})
            self.assertFalse(cell.has_bomb)

        with self.subTest("marked as None"):
            cell = Cell({"bomb": None})
            self.assertFalse(cell.has_bomb)

        with self.subTest("no data about flagging"):
            cell = Cell({})
            self.assertFalse(cell.has_bomb)


class GameSerializerTestCase(TestCase):
    """Test the output of the Serializer."""

    def setUp(self):
        """Set up common test data."""
        board = create_data_board(8, 9)
        self.user = User.objects.create_user("user@example.com")
        self.game = Game.objects.create(player=self.user, board=board)

    def test_empty_board(self):
        """The serializer board is a 2 dimension list of cells of None."""
        expected_board = create_covered_board(8, 9)
        data = GameSerializer(self.game).data
        self.assertEqual(data["board"], expected_board)

    def test_board_uncovered_count(self):
        """Uncovered cells reveal number of adjacent bombs."""
        self.game.board[2][2]["bomb"] = True
        self.game.board[2][3]["status"] = Status.UNCOVERED.value
        self.game.board[2][4]["bomb"] = True
        expected_board = create_covered_board(8, 9)
        expected_board[2][3] = 2
        data = GameSerializer(self.game).data
        self.assertEqual(data["board"], expected_board)

    def test_flagged_bomb(self):
        """Flagged cells show as flagged, with and without bombs."""
        self.game.board[2][2]["bomb"] = True
        self.game.board[2][2]["status"] = Status.FLAGGED.value
        expected_board = create_covered_board(8, 9)
        expected_board[2][2] = "f"
        data = GameSerializer(self.game).data
        self.assertEqual(data["board"], expected_board)

    def test_cols(self):
        """Cols give the number of columns."""
        data = GameSerializer(self.game).data
        self.assertEqual(data["cols"], 8)

    def test_rows(self):
        """Rows give the number of rows."""
        data = GameSerializer(self.game).data
        self.assertEqual(data["rows"], 9)

    def test_bombs(self):
        """Gives the number of bombs in the board."""
        self.game.board[2][2]["bomb"] = True
        self.game.board[3][3]["bomb"] = True
        self.game.board[5][3]["bomb"] = True
        data = GameSerializer(self.game).data
        self.assertEqual(data["bombs"], 3)
