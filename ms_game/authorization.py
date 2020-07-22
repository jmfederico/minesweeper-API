"""Define authorization classes compatible with DRF."""
from rest_framework import permissions


class IsPlayer(permissions.IsAuthenticated):
    """
    Allow access if the user is the player of the game.

    For non object_level permission, being authenticated grants access.
    """

    def has_object_permission(self, request, view, obj):
        """If the current user is the player, allowe access."""
        return obj.player == request.user
