"""Define tests for MD GAme app."""
from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Game, Cell, Status

User = get_user_model()


class GameModelTestCase(TestCase):
    """Test the functionality of the Game model."""

    def setUp(self):
        """Set up common test data."""
        self.user = User.objects.create_user("user@example.com")

    def test_game_has_cells(self):
        """A Game cell can be accessed as an index."""
        board = {"0,0": {}}
        game = Game.objects.create(player=self.user, board=board)

        self.assertIsInstance(game[0, 0], Cell)

    def test_non_existing_cell(self):
        """Raise KeyError: if the cell does not exist."""
        board = {}
        game = Game.objects.create(player=self.user, board=board)

        with self.assertRaises(KeyError):
            game[0, 0]

    def test_neighbors(self):
        """Neighbors is a generator that can be used as a mapping."""
        board = {}
        for c in range(0, 10):
            for r in range(0, 10):
                board[f"{c},{r}"] = {}
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
        board = {"0,0": {}}
        game = Game.objects.create(player=self.user, board=board)

        cell = game[0, 0]
        self.assertIs(cell._data, game.board["0,0"])


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
