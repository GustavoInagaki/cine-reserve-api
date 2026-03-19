from rest_framework.test import APITestCase
from rest_framework import status
from .models import User


class UserAuthTests(APITestCase):
    def test_register_user(self):
        data = {
            "username": "gustavo",
            "email": "gustavo@email.com",
            "password": "12345678"
        }

        response = self.client.post("/api/users/register/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, "gustavo")

    def test_login_user(self):
        User.objects.create_user(
            username="gustavo",
            email="gustavo@email.com",
            password="12345678"
        )

        data = {
            "username": "gustavo",
            "password": "12345678"
        }

        response = self.client.post("/api/users/login/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
