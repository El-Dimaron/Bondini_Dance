def user_photo_path(instance, filename):
    return f"user_photos/user_{instance.pk}/{filename}"
