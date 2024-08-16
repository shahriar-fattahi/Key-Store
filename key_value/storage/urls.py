from django.urls import path

from .apis import SetKeyApi

app_name = "storage"

urlpatterns = [
    path("set", SetKeyApi.as_view(), name="set"),
]
