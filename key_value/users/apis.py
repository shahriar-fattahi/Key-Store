from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from key_value.users.models import User

from .serializers import RegisterUserSerializer, UserSerializer


class RegisterApi(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.instance
        refresh = RefreshToken.for_user(user)

        response_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return Response(
            data=response_data,
            status=status.HTTP_200_OK,
        )
