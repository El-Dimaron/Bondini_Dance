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
    plan_name = CharField(source="get_plan_name_display")

    class Meta:
        model = Group
        fields = ["id", "name", "plan_name", "description", "price", "trainer", "users"]
