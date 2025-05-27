import unittest
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class TestAuthUser(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model()(email="testuser@email.com")
        self.user.set_password("12345")
        self.user.save()

        self.admin_user = get_user_model()(email="admin@email.com", is_staff=True)
        self.admin_user.set_password("admin")
        self.admin_user.save()

    def test_user_login_wrong_email(self):
        user_login = self.client.login(email="admon@email.com", password="admin")
        self.assertFalse(user_login)

    def test_user_login_wrong_password(self):
        user_login = self.client.login(email="admin@email.com", password="admiral")
        self.assertFalse(user_login)

    def test_user_login_to_admin_panel(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_admin_login_to_admin_panel(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @unittest.skip("'Index' page is not created yet. Will be available later")
    def test_user_login_to_index_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @unittest.expectedFailure
    def test_admin_login_to_index_page(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
