"""Models for MS Api app."""
import uuid
from dataclasses import dataclass

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Game(models.Model):
    """Represent a board/game of Minesweeper."""

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    board = JSONField(_("Board"))
    timelog = JSONField(_("Timelog"), default=list)
    player = models.ForeignKey(User, verbose_name=_("Player"), on_delete=models.CASCADE)

    _cells = {}

    def __getitem__(self, key):
        """Return the requested game cell."""
        try:
            c, r = key
        except (ValueError, TypeError):
            raise TypeError("Invalid cell index.")

        # Raise KeyError if cell does not exist.
        self.board[f"{c},{r}"]

        if key not in self._cells:
            self._cells[key] = Cell(self, c, r)

        return self._cells[key]

    class Meta:
        """Define properties for Game model."""

        verbose_name = "Game"
        verbose_name_plural = "Games"


@dataclass
class Cell:
    """Represent a cell in a Game."""

    game: Game
    column: int
    row: int
