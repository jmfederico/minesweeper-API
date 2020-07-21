"""Models for MS Api app."""
import uuid
from dataclasses import dataclass

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Status(models.TextChoices):
    """Define possible status for a cell."""

    FLAGGED = "F"
    UNCOVERED = "U"


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
        cell_data = self.board[f"{c},{r}"]

        if key not in self._cells:
            self._cells[key] = Cell(cell_data)

        return self._cells[key]

    class Meta:
        """Define properties for Game model."""

        verbose_name = "Game"
        verbose_name_plural = "Games"

    def _get_neighbors_keys(self, c, r):
        for cc in range(c - 1, c + 2):
            for rr in range(r - 1, r + 2):
                if c != cc or r != rr:
                    yield cc, rr

    def get_neighbors(self, cell_key):
        """Yield tuples of the neighbors of a cell key."""
        for cell_key in self._get_neighbors_keys(*cell_key):
            try:
                yield cell_key, self[cell_key]
            except KeyError:
                pass


@dataclass
class Cell:
    """Represent a cell in a Game."""

    _data: dict

    @property
    def is_flagged(self):
        """Return True if the cell is flagged, False otherwise."""
        return self._data.get("status", None) == Status.FLAGGED

    @property
    def is_covered(self):
        """Return True if the cell is covered, False otherwise."""
        return self._data.get("status", None) != Status.UNCOVERED

    @property
    def has_bomb(self):
        """Return True if the cell has a bomb, False otherwise."""
        return self._data.get("bomb", None) is True

    def flag(self):
        """Set the cell as flagged."""
        self._data["status"] = Status.FLAGGED.value

    def unflag(self):
        """Set the cell as not flagged."""
        if self.is_flagged:
            del self._data["status"]

    def uncover(self):
        """Set the cell as uncovered."""
        self._data["status"] = Status.UNCOVERED.value
