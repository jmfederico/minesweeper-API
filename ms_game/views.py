"""Define views for MS Game app."""
from django.http import Http404
from django.utils import timezone
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework import status as http_status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ms_game.authorization import IsPlayer

from .models import Game
from .serializers import CellSerializer, GameSerializer


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Retreive the games for the requesting user."
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="Create a new game for the requesting user."
    ),
)
class GameViewset(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Viewset for Game model.

    Through this Viewset it is possible to create and retrieve instances.
    """

    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsPlayer]

    def filter_queryset(self, queryset):
        """Limit the list querysets to the ones the user can access."""
        if not self.detail:
            queryset = queryset.filter(player=self.request.user)[:15]
        return queryset

    @swagger_auto_schema(responses={204: "Empty response."})
    @action(
        detail=True,
        methods=["PATCH"],
        url_path=r"cells/(?P<col>[0-9]*),(?P<row>[0-9]*)",
        serializer_class=CellSerializer,
    )
    def update_cell(self, request, pk, col, row):
        """Allow changing the status of a cell."""
        col, row = int(col), int(row)
        game = self.get_object()
        try:
            cell = game[(col, row)]
        except IndexError:
            raise Http404

        # Force a Game validation.
        # This checks that the game has not been finished.
        GameSerializer(game, {}, partial=True).is_valid(raise_exception=True)

        serializer = self.get_serializer(cell, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.recursive_uncover_neighbors(game, (col, row))
        if game.finished:
            game.finished_at = timezone.now()
        game.save()

        return Response(status=http_status.HTTP_204_NO_CONTENT)

    @staticmethod
    def recursive_uncover_neighbors(game, cell_key):
        """Recursively uncover neighbors for uncovered cells with no adjacent bombs."""
        cell = game[cell_key]

        if cell.is_covered or cell.has_bomb:
            return

        keys_to_check = {cell_key}

        while keys_to_check:
            current_cell_key = keys_to_check.pop()
            current_cell = game[current_cell_key]

            neighbor_has_bomb = False
            neighbor_keys = []
            neighbors = []

            # First pass checks if the current cell has neighbors with bombs.
            for neighbor_key, neighbor in game.get_neighbors((current_cell_key)):
                neighbors.append(neighbor)
                if neighbor.has_bomb:
                    neighbor_has_bomb = True

                if neighbor.is_covered:
                    neighbor_keys.append(neighbor_key)

            if not neighbor_has_bomb:
                [cell.uncover() for cell in neighbors]
                current_cell.uncover()
                keys_to_check.update(neighbor_keys)
