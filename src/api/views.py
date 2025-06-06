from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from api.serializers import GroupSerializer, UserSerializer
from trainings.models import Group


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
