"""Define serializers for MS Game app."""
from rest_framework import serializers

from .models import Game


class GameSerializer(serializers.ModelSerializer):
    """Serializer for Game model instances."""

    board = serializers.SerializerMethodField()
    cols = serializers.IntegerField()
    rows = serializers.IntegerField()
    bombs = serializers.IntegerField()

    class Meta:
        """Define options for GameSerializer."""

        model = Game
        fields = ["board", "cols", "rows", "bombs"]

    @staticmethod
    def _count_bombs(cells):
        return sum(1 for _, cell in cells if cell.has_bomb)

    @staticmethod
    def _get_new_board(cols, rows):
        board = []
        for _ in range(cols):
            row = []
            for _ in range(rows):
                row.append("c")
            board.append(row)
        return board

    def get_board(self, obj):
        """
        Represent the board as a 2 level nested list.

        Each cell has a unique value that indicates its state.
        """
        board = self._get_new_board(obj.cols, obj.rows)
        for cell_key, cell in obj.cells:
            c, r = cell_key
            if cell.is_flagged:
                board[c][r] = "f"
                continue

            if not cell.is_covered:
                board[c][r] = self._count_bombs(obj.get_neighbors(cell_key))
                continue

        return board
