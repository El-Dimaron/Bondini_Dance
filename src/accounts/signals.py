from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def setup_groups_and_permissions(sender, **kwargs):
    admin_group, _ = Group.objects.get_or_create(name="Admin")
    coach_group, _ = Group.objects.get_or_create(name="Coach")
    dancer_group, _ = Group.objects.get_or_create(name="Dancer")

    admin_permissions = Permission.objects.all()
    coach_permissions = Permission.objects.filter(
        codename__in=[
            "view_item",
            "change_item",
            "view_user",
            "add_category",
            "change_category",
            "delete_category",
            "view_category",
            "add_favorite",
            "change_favorite",
            "delete_favorite",
            "view_favorite",
            "add_tag",
            "change_tag",
            "delete_tag",
            "view_tag",
            "view_group",
            "change_group",
            "add_schedule",
            "change_schedule",
            "delete_schedule",
            "view_schedule",
        ]
    )
    dancer_permissions = Permission.objects.filter(
        codename__in=[
            "view_item",
        ]
    )

    admin_group.permissions.set(admin_permissions)
    coach_group.permissions.set(coach_permissions)
    dancer_group.permissions.set(dancer_permissions)
