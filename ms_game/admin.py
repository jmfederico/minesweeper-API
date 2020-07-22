"""Integrate MS Game models with Django admin."""
from django.contrib import admin

from .models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Configure Game integratino with Django admin."""

    list_display = ("__str__", "player", "finished", "won")
    list_select_related = ["player"]
