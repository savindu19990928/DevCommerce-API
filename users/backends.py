from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class EmailBackend(ModelBackend):
    """
    Authenticate against settings.AUTH_USER_MODEL using email.
    Falls back to username if no email matches.
    """
    def authenticate(self, request, username=None, password=None, email=None, **kwargs):
        lookup = email or username or kwargs.get('email')
        if not lookup or not password:
            return None
        try:
            user = UserModel.objects.filter(email__iexact=lookup).first()
            if not user:
                user = UserModel.objects.filter(username__iexact=lookup).first()
        except UserModel.DoesNotExist:
            return None

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
