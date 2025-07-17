from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsSuperUser, IsTrainer
from api.serializers import (GroupCreateSerializer, GroupSerializer,
                             GroupUpdateSerializer, UserSerializer)
from trainings.models import Group


def tag_viewset(viewset_cls, tag="users"):
    """Provides UserViewSet's methods are placed under a separate 'users' section"""
    methods = ["list", "retrieve", "create", "update", "partial_update", "destroy"]
    for method in methods:
        viewset_cls = method_decorator(name=method, decorator=swagger_auto_schema(tags=[tag]))(viewset_cls)
    return viewset_cls


@tag_viewset
class UserViewSet(ModelViewSet):
    swagger_schema_fields = {"tags": ["users"]}
    permission_classes = [IsSuperUser | IsTrainer]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class GroupListApiView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=["groups"])
    def get(self, request):
        group = Group.objects.all()
        serializer = GroupSerializer(group, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GroupCreateApiView(APIView):
    permission_classes = [IsSuperUser]

    @swagger_auto_schema(tags=["groups"])
    def post(self, request):
        serializer = GroupCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        serializer.create(validated_data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GroupRetreiveUpdateDeleteApiView(APIView):
    permission_classes = [IsSuperUser]

    @swagger_auto_schema(tags=["groups"])
    def get(self, request, pk):
        group = Group.objects.get(id=pk)
        serializer = GroupSerializer(group)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=["groups"])
    def put(self, request, pk):
        group = Group.objects.get(id=pk)
        serializer = GroupUpdateSerializer(group, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=["groups"])
    def patch(self, request, pk):
        group = Group.objects.get(id=pk)
        serializer = GroupCreateSerializer(group, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=["groups"])
    def delete(self, request, pk):
        Group.objects.filter(id=pk).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
