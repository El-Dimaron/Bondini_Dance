from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.status import (HTTP_200_OK, HTTP_401_UNAUTHORIZED,
                                   HTTP_403_FORBIDDEN)
from rest_framework.test import APIClient

from trainings.models import Group


class TestApi(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model()(first_name="Test name", last_name="Test surname", email="test_user@email.com")
        self.user.set_password("qwerty1234")
        self.user.save()

        self.group = Group.objects.create(name="Test", description="Group for API testing")
        self.group.users.add(self.user)

    def test_group_details_forbidden(self):
        self.client.force_authenticate(user=self.user)

        result = self.client.get(reverse("api:group_retreive", kwargs={"pk": self.group.pk}))

        self.assertEqual(result.status_code, HTTP_403_FORBIDDEN)

    def test_group_details_allowed(self):
        admin = get_user_model().objects.create_superuser(email="admin@admin.com", password="12345")
        self.client.force_authenticate(user=admin)

        result = self.client.get(reverse("api:group_retreive", kwargs={"pk": self.group.pk}))

        self.assertEqual(result.status_code, HTTP_200_OK)
        self.assertEqual(
            result.data,
            {
                "id": self.group.pk,
                "name": "Test",
                "plan_name": "Абонемент",
                "description": "Group for API testing",
                "price": None,
                "trainer": None,
                "users": [
                    {
                        "id": self.user.pk,
                        "first_name": self.user.first_name,
                        "last_name": self.user.last_name,
                        "email": self.user.email,
                        "is_staff": self.user.is_staff,
                    }
                ],
            },
        )

    def test_group_list_base_auth_restricted(self):
        result = self.client.get(reverse("api:group_retreive", kwargs={"pk": self.group.pk}))
        self.assertEqual(result.status_code, HTTP_401_UNAUTHORIZED)

    def test_group_list_superuser_restricted(self):
        self.client.force_authenticate(user=self.user)
        result = self.client.get(reverse("api:users-list"))
        self.assertEqual(result.status_code, HTTP_403_FORBIDDEN)

    def test_group_list_superuser_allowed(self):
        admin = get_user_model().objects.create_superuser(email="admin@admin.com", password="12345")
        self.client.force_authenticate(user=admin)
        result = self.client.get(reverse("api:users-list"))
        self.assertEqual(result.status_code, HTTP_200_OK)

    def test_group_list_trainer_allowed(self):
        self.user.is_staff = True
        self.client.force_authenticate(user=self.user)
        self.user.save()
        result = self.client.get(reverse("api:users-list"))
        self.assertEqual(result.status_code, HTTP_200_OK)
        self.assertEqual(
            result.data,
            [
                {
                    "id": 1,
                    "first_name": "Test name",
                    "last_name": "Test surname",
                    "email": "test_user@email.com",
                    "is_staff": True,
                }
            ],
        )
