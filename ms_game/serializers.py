"""Define serializers for MS Game app."""
from random import random

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
    def _get_new_covered_board(cols, rows):
        board = []
        for _ in range(cols):
            row = []
            for _ in range(rows):
                row.append("c")
            board.append(row)
        return board

    @staticmethod
    def _get_new_data_board(cols, rows):
        board = []
        for _ in range(cols):
            row = []
            for _ in range(rows):
                row.append({})
            board.append(row)
        return board

    @staticmethod
    def _populate_board_with_bombs(board, bombs):
        size = len(board) * len(board[0])
        probability = bombs / size
        bombs = min(size, bombs)
        # Loop until we fill all the needed bombs.
        while bombs:
            for row in board:
                for cell in row:
                    if bombs and not cell.get("bomb", False) and random() < probability:
                        cell["bomb"] = True
                        bombs -= 1

        return board

    def get_board(self, obj):
        """
        Represent the board as a 2 level nested list.

        Each cell has a unique value that indicates its state.
        """
        board = self._get_new_covered_board(obj.cols, obj.rows)
        for cell_key, cell in obj.cells:
            c, r = cell_key
            if cell.is_flagged:
                board[c][r] = "f"
                continue

            if not cell.is_covered:
                board[c][r] = self._count_bombs(obj.get_neighbors(cell_key))
                continue

        return board

    def create(self, validated_data):
        """Create a new Game populating the board with the requested number of bombs."""
        # Extract validated data.
        cols = validated_data.pop("cols")
        rows = validated_data.pop("rows")
        bombs = validated_data.pop("bombs")

        # Generate board with bombs.
        board = self._get_new_data_board(cols, rows)
        self._populate_board_with_bombs(board, bombs)
        validated_data["board"] = board

        # Assign the player.
        validated_data["player"] = self._context["request"].user

        return super().create(validated_data)
