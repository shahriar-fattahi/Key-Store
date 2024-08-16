from django.urls import include, path

app_name = "api"
urlpatterns = [
    path("users/", include("key_value.users.urls"), name="users"),
]
