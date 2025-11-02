from django.contrib.auth.backends import BaseBackend
from .models import LSCUser

class LSCAuthBackend(BaseBackend):
    def authenticate(self, request, lsc_number=None, password=None, **kwargs):
        try:
            user = LSCUser.objects.get(lsc_number=lsc_number)
            if user.check_password(password) and user.is_active:
                return user
        except LSCUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return LSCUser.objects.get(pk=user_id)
        except LSCUser.DoesNotExist:
            return None