"""Define tests for MD GAme app."""
from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Game, Cell

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
        """Raise KeyError: if the cell does not exist.."""
        board = {}
        game = Game.objects.create(player=self.user, board=board)

        with self.assertRaises(KeyError):
            game[0, 0]

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


class CellTestCase(TestCase):
    """Test the Cell class and its attributes."""

    def test_cell_is_flagged(self):
        """When flagged, the is_flagged method return True."""
        cell = Cell({"flagged": True})
        self.assertTrue(cell.is_flagged)

    def test_cell_is_not_flagged(self):
        """When not flagged, the is_flagged method return False."""
        with self.subTest("marked as False"):
            cell = Cell({"flagged": False})
            self.assertFalse(cell.is_flagged)

        with self.subTest("marked as None"):
            cell = Cell({"flagged": None})
            self.assertFalse(cell.is_flagged)

        with self.subTest("no data about flagging"):
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
        cell = Cell({"flagged": True})
        self.assertTrue(cell.is_flagged)
        cell.unflag()
        self.assertFalse(cell.is_flagged)
