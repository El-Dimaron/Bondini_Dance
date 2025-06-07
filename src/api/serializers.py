from django.contrib.auth import get_user_model
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from trainings.models import Group


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "first_name", "last_name", "email", "is_staff"]


class GroupSerializer(ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    plan_name = CharField(source="get_plan_name_display", read_only=True)

    class Meta:
        model = Group
        fields = ["id", "name", "plan_name", "description", "price", "trainer", "users"]


class GroupCreateSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name", "plan_name", "description", "price", "trainer"]


class GroupUpdateSerializer(GroupCreateSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.partial:
            for field in self.fields.values():
                field.required = True
