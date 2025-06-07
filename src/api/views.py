from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.serializers import (GroupCreateSerializer, GroupSerializer,
                             GroupUpdateSerializer, UserSerializer)
from trainings.models import Group


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class GroupListApiView(APIView):
    def get(self, request):
        group = Group.objects.all()
        serializer = GroupSerializer(group, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GroupCreateApiView(APIView):
    def post(self, request):
        serializer = GroupCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        serializer.create(validated_data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GroupRetreiveUpdateDeleteApiView(APIView):
    def get(self, request, pk):
        group = Group.objects.get(id=pk)
        serializer = GroupSerializer(group)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        group = Group.objects.get(id=pk)
        serializer = GroupUpdateSerializer(group, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        group = Group.objects.get(id=pk)
        serializer = GroupCreateSerializer(group, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        Group.objects.filter(id=pk).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
