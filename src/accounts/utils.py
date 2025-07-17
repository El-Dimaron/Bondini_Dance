from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


def user_photo_path(instance, filename):
    return f"user_photos/user_{instance.pk}/{filename}"


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp) -> str:
        return text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)
