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
