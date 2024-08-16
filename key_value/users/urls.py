from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .apis import ProfileApi, RegisterApi

app_name = "users"
urlpatterns = [
    path("register", view=RegisterApi.as_view(), name="register"),
    path("token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile", view=ProfileApi.as_view(), name="profile"),
]
