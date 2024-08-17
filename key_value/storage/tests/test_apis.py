import json

from django.test import Client, TestCase
from django.urls import reverse

from key_value.users.models import User


class TestSetKeyApi(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.valid_data = {"data": {"key": "test-key", "value": 100}}
        self.user = User.objects.create(
            username="username",
            password="password",
            first_name="firstname",
            last_name="lastname",
        )
        self.jwt = self.client.post(
            reverse("api:users:token_obtain_pair"),
            data={
                "username": "username",
                "password": "password",
            },
        )
        self.jwt = json.loads(self.jwt.content)["access"]
        self.header = {"Authorization": f"Bearer {self.jwt}"}
        return super().setUp()

    def test_api_permmisions(self):
        response = self.client.post(
            reverse("api:storage:set-key"), data=self.valid_data
        )
        self.assertEqual(response.status_code, 401)

    def test_valid_data(self):
        response = self.client.post(
            path=reverse("api:storage:set-key"),
            data=self.valid_data,
            content_type="application/json",
            headers=self.header,
        )
        self.assertEqual(response.status_code, 201)
        response = json.loads(response.content)
        self.assertEqual(response["data"]["key"], self.valid_data["data"]["key"])
        self.assertEqual(response["data"]["value"], self.valid_data["data"]["value"])

    def test_duplicate_key_name(self):
        self.client.post(
            path=reverse("api:storage:set-key"),
            data=self.valid_data,
            content_type="application/json",
            headers=self.header,
        )
        response = self.client.post(
            path=reverse("api:storage:set-key"),
            data=self.valid_data,
            content_type="application/json",
            headers=self.header,
        )
        self.assertEqual(response.status_code, 400)
        response = json.loads(response.content)
        self.assertEqual(response["data"]["key"], "this key name already exists.")

    def test_invalid_data(self):
        self.valid_data["data"]["key"] = "a" * 30
        response = self.client.post(
            path=reverse("api:storage:set-key"),
            data=self.valid_data,
            content_type="application/json",
            headers=self.header,
        )
        self.assertEqual(response.status_code, 400)
        response = json.loads(response.content)
        self.assertEqual(
            response["data"]["key"], "key name should be less than 20 chars."
        )

        self.valid_data["data"]["key"] = ""
        response = self.client.post(
            path=reverse("api:storage:set-key"),
            data=self.valid_data,
            content_type="application/json",
            headers=self.header,
        )
        self.assertEqual(response.status_code, 400)
        response = json.loads(response.content)
        self.assertEqual(
            response["data"]["key"], "key name should contain at least 1 char."
        )

        del self.valid_data["data"]["key"]
        response = self.client.post(
            path=reverse("api:storage:set-key"),
            data=self.valid_data,
            content_type="application/json",
            headers=self.header,
        )
        self.assertEqual(response.status_code, 400)
        response = json.loads(response.content)
        self.assertEqual(response["data"]["key"], "data must include a key name.")

        self.valid_data["data"]["key"] = "key-name"
        del self.valid_data["data"]["value"]
        response = self.client.post(
            path=reverse("api:storage:set-key"),
            data=self.valid_data,
            content_type="application/json",
            headers=self.header,
        )
        self.assertEqual(response.status_code, 400)
        response = json.loads(response.content)
        self.assertEqual(response["data"]["value"], "data must include a value.")


class TestGetValueApi(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.valid_data = {"data": {"key": "test-key", "value": 100}}
        self.user = User.objects.create(
            username="username",
            password="password",
            first_name="firstname",
            last_name="lastname",
        )
        self.jwt = self.client.post(
            reverse("api:users:token_obtain_pair"),
            data={
                "username": "username",
                "password": "password",
            },
        )
        self.jwt = json.loads(self.jwt.content)["access"]
        self.header = {"Authorization": f"Bearer {self.jwt}"}
        self.client.post(
            path=reverse("api:storage:set-key"),
            data=self.valid_data,
            content_type="application/json",
            headers=self.header,
        )
        return super().setUp()

    def test_api_permmisions(self):
        response = self.client.post(
            reverse("api:storage:set-key"), data=self.valid_data
        )
        self.assertEqual(response.status_code, 401)

    def test_retrieve_existent_key(self):
        response = self.client.get(
            path=reverse(
                "api:storage:get-value",
                kwargs={"key_name": self.valid_data["data"]["key"]},
            ),
            content_type="application/json",
            headers=self.header,
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            json.loads(response.content),
            {self.valid_data["data"]["key"]: self.valid_data["data"]["value"]},
        )

    def test_retrieve_nonexistent_key(self):
        response = self.client.get(
            path=reverse(
                "api:storage:get-value",
                kwargs={"key_name": "nonexistent-key"},
            ),
            content_type="application/json",
            headers=self.header,
        )
        self.assertEqual(response.status_code, 404)
        self.assertDictEqual(
            json.loads(response.content),
            {"detail": "No Storage matches the given query."},
        )


class TestGetKeyValueListApi(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.valid_data = {"data": {"key": "test-key", "value": 100}}
        self.user = User.objects.create(
            username="username",
            password="password",
            first_name="firstname",
            last_name="lastname",
        )
        self.jwt = self.client.post(
            reverse("api:users:token_obtain_pair"),
            data={
                "username": "username",
                "password": "password",
            },
        )
        self.jwt = json.loads(self.jwt.content)["access"]
        self.header = {"Authorization": f"Bearer {self.jwt}"}
        self.client.post(
            path=reverse("api:storage:set-key"),
            data=self.valid_data,
            content_type="application/json",
            headers=self.header,
        )
        self.valid_data["data"]["key"] = "test-key2"
        self.client.post(
            path=reverse("api:storage:set-key"),
            data=self.valid_data,
            content_type="application/json",
            headers=self.header,
        )
        return super().setUp()

    def test_api_permmisions(self):
        response = self.client.post(
            reverse("api:storage:set-key"), data=self.valid_data
        )
        self.assertEqual(response.status_code, 401)

    def test_key_values_list(self):
        response = self.client.get(
            path=reverse("api:storage:get-values"),
            content_type="application/json",
            headers=self.header,
        )
        response = json.loads(response.content)
        self.assertEqual(response["count"], 2)
        self.assertIn({"test-key": 100}, response["results"])
        self.assertIn({"test-key2": 100}, response["results"])
