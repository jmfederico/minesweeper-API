"""Define authentication backends compatible with DRF."""
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import BasicAuthentication

User = get_user_model()


class EmailAuth(BasicAuthentication):
    """A very insecure authenticator that authenticates just with email!."""

    def authenticate_credentials(self, userid, password, request=None):
        """Authenticate userid as email. Create user if does not exist."""
        try:
            validate_email(userid)
        except ValidationError:
            raise exceptions.AuthenticationFailed(_("Invalid username/password."))

        user, __ = User.objects.get_or_create(username=userid.lower())

        return (user, None)
