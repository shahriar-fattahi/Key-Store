import json

from django.test import Client, TestCase
from django.urls import reverse

from key_value.users.models import User


class TestRegisterApi(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.valid_data = {
            "username": "username",
            "first_name": "firstname",
            "last_name": "lastname",
            "password": "password",
        }
        return super().setUp()

    def test_valid_data(self):
        response = self.client.post(
            path=reverse("api:users:register"),
            data=self.valid_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

        user = User.objects.filter(username=self.valid_data["username"])
        self.assertEqual(user.count(), 1)
        self.assertEqual(user[0].first_name, self.valid_data["first_name"])
        self.assertEqual(user[0].last_name, self.valid_data["last_name"])
        response = json.loads(response.content)
        self.assertIn("refresh", response)
        self.assertIn("access", response)

    def test_duplicate_username(self):
        self.client.post(
            path=reverse("api:users:register"),
            data=self.valid_data,
            content_type="application/json",
        )
        response = self.client.post(
            path=reverse("api:users:register"),
            data=self.valid_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response = json.loads(response.content)
        self.assertDictEqual(
            response, {"username": ["user with this username already exists."]}
        )

    def test_invalid_data(self):
        self.valid_data["username"] = "a" * 51
        self.client.post(
            path=reverse("api:users:register"),
            data=self.valid_data,
            content_type="application/json",
        )
        response = self.client.post(
            path=reverse("api:users:register"),
            data=self.valid_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response = json.loads(response.content)
        self.assertDictEqual(
            response,
            {"username": ["Ensure this field has no more than 50 characters."]},
        )

        del self.valid_data["username"]
        response = self.client.post(
            path=reverse("api:users:register"),
            data=self.valid_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response = json.loads(response.content)

        self.assertDictEqual(
            response,
            {"username": ["This field is required."]},
        )

        self.valid_data["username"] = "username"
        del self.valid_data["password"]
        response = self.client.post(
            path=reverse("api:users:register"),
            data=self.valid_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response = json.loads(response.content)

        self.assertDictEqual(
            response,
            {"password": ["This field is required."]},
        )

        self.valid_data["password"] = "password"
        del self.valid_data["first_name"]
        response = self.client.post(
            path=reverse("api:users:register"),
            data=self.valid_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response = json.loads(response.content)

        self.assertDictEqual(
            response,
            {"first_name": ["This field is required."]},
        )

        self.valid_data["first_name"] = "first_name"
        del self.valid_data["last_name"]
        response = self.client.post(
            path=reverse("api:users:register"),
            data=self.valid_data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        response = json.loads(response.content)

        self.assertDictEqual(
            response,
            {"last_name": ["This field is required."]},
        )
