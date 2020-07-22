"""Models for MS Api app."""
import uuid
from dataclasses import dataclass

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.fields import DateTimeField

User = get_user_model()


class Status(models.TextChoices):
    """Define possible status for a cell."""

    FLAGGED = "F"
    UNCOVERED = "U"


class Game(models.Model):
    """
    Represent a board/game of Minesweeper.

    A board is composed of Cells, each cell referenced by a tuple
    of its (column, row) number.

    A Game is Subscriptable, and the cells can be retrieved using the
    tuple of (column, row) for the cell:
        - `board[1, 2]`
    """

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    board = JSONField(_("Board"))
    player = models.ForeignKey(User, verbose_name=_("Player"), on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("created"), auto_now_add=True)
    finished_at = models.DateTimeField(_("finished"), null=True)

    _cells = None

    @property
    def cols(self):
        """Return the number of columns of the board."""
        return len(self.board)

    @property
    def rows(self):
        """Return the number of rows of the board."""
        return len(self.board[0]) if self.cols else 0

    @property
    def size(self):
        """Return the number of cells in the board."""
        return self.rows * self.cols

    @property
    def bombs(self):
        """Return the number of bombs in the board."""
        return sum(1 for _, cell in self.cells if cell.has_bomb)

    @property
    def uncovered(self):
        """Return the number of uncovered cells in the board."""
        return sum(1 for _, cell in self.cells if not cell.is_covered)

    @property
    def uncovered_bombs(self):
        """Return the number of uncovered bombs in the board."""
        return sum(1 for _, cell in self.cells if not cell.is_covered and cell.has_bomb)

    @property
    def finished(self):
        """
        Return True if the game has finished.

        A game is finished when a bomb has been uncovered or
        when only bombs are left to be uncovered.
        """
        return bool((self.size - self.uncovered == self.bombs) or self.uncovered_bombs)

    @property
    def won(self):
        """
        Return True if the game has finished ans the user won.

        A user wins when there are no uncovered bombs.
        """
        return self.finished and (self.size - self.uncovered == self.bombs)

    def __getitem__(self, key):
        """Return the requested game cell."""
        try:
            c, r = key
        except (ValueError, TypeError):
            raise TypeError("Invalid cell index.")

        if c < 0 or r < 0:
            raise IndexError("Cell does not exist.")

        try:
            cell_data = self.board[c][r]
        except IndexError:
            raise IndexError("Cell does not exist.")

        if self._cells is None:
            self._cells = {}

        if key not in self._cells:
            self._cells[key] = Cell(cell_data)

        return self._cells[key]

    class Meta:
        """Define properties for Game model."""

        verbose_name = "Game"
        verbose_name_plural = "Games"

    def _get_neighbors_keys(self, c, r):
        for rr in range(r - 1, r + 2):
            for cc in range(c - 1, c + 2):
                if c != cc or r != rr:
                    yield cc, rr

    def get_neighbors(self, cell_key):
        """Yield tuples of `(key: neighbor)` for the passed cell key."""
        for cell_key in self._get_neighbors_keys(*cell_key):
            try:
                yield cell_key, self[cell_key]
            except IndexError:
                pass

    @property
    def cells(self):
        """Yield all the cells for the current game."""
        for r in range(0, self.rows):
            for c in range(0, self.cols):
                yield (c, r), self[c, r]


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
