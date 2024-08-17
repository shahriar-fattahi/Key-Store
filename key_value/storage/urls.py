from django.urls import path

from .apis import GetKeyValueListApi, GetValueApi, SetKeyApi

app_name = "storage"

urlpatterns = [
    path("set", SetKeyApi.as_view(), name="set-key"),
    path("get", GetKeyValueListApi.as_view(), name="get-values"),
    path("get/<str:key_name>", GetValueApi.as_view(), name="get-value"),
]
