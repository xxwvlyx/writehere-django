from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Спочатку пробуємо знайти користувача за email
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            # Якщо такого email немає, шукаємо за звичайним username
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None

        # Якщо користувача знайдено, перевіряємо пароль
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None