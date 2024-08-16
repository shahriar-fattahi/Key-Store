from django.urls import path

from .apis import RegisterApi

app_name = "users"
urlpatterns = [
    path("register", view=RegisterApi.as_view(), name="register"),
]
