"""Define views for MS Game app."""
from django.http import Http404
from rest_framework import mixins
from rest_framework import status as http_status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ms_game.authorization import IsPlayer

from .models import Game
from .serializers import CellSerializer, GameSerializer


class GameViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
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
            queryset = queryset.filter(player=self.request.user)
        return queryset

    @action(
        detail=True,
        methods=["PUT"],
        url_path=r"cells/(?P<col>[0-9]*),(?P<row>[0-9]*)",
        serializer_class=CellSerializer,
    )
    def update_cell(self, request, pk, col, row):
        """Allow changing the status of a cell."""
        game = self.get_object()
        try:
            cell = game[(int(col), int(row))]
        except IndexError:
            raise Http404

        # Force a Game validation.
        # This checks that the game has not been finished.
        GameSerializer(game, {}, partial=True).is_valid(raise_exception=True)

        serializer = self.get_serializer(cell, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        game.save()

        return Response(status=http_status.HTTP_204_NO_CONTENT)
