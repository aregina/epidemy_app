from rest_framework.authentication import BaseAuthentication, get_authorization_header, BasicAuthentication
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import AnonymousUser
from epidemy.settings import DEFAULT_AUTHENTICATION_CREDENTIAL


class APIUser(AnonymousUser):
    def is_staff(self):
        return True


class DefaultBasicAuthentication(BasicAuthentication):
    def authenticate_credentials(self, login, password):
        default_login = DEFAULT_AUTHENTICATION_CREDENTIAL.get("login")
        default_password = DEFAULT_AUTHENTICATION_CREDENTIAL.get("password")

        if not default_login or (login, password) != (default_login, default_password):
            raise PermissionDenied

        return (APIUser(), None)

