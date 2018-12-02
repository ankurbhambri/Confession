from rest_framework import permissions
from rest_framework.authentication import get_authorization_header
from rest_framework_jwt.settings import api_settings

from blog.models import User

JWT_DECODE_HANDLER = api_settings.JWT_DECODE_HANDLER


class ChiefRequiredPermission(permissions.BasePermission):
    """
    check user type
    """

    def has_permission(self, request, view):
        auth_keyword, token = get_authorization_header(request).split()
        user = JWT_DECODE_HANDLER(token).get('user_id', None)
        if request.user.is_authenticated:
            if User.objects.filter(id=user, is_chief=True).exists():
                return True
        return False
