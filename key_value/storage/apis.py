from rest_framework.generics import CreateAPIView

from .serializers import SetKeySerializer


class SetKeyApi(CreateAPIView):
    serializer_class = SetKeySerializer
