from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from .models import Storage
from .serializers import GetKeyValueSerializer, SetKeySerializer


class SetKeyApi(CreateAPIView):
    serializer_class = SetKeySerializer


class GetKeyValueListApi(ListAPIView):
    serializer_class = GetKeyValueSerializer

    def get_queryset(self):
        return Storage.objects.all()


class GetValueApi(RetrieveAPIView):
    lookup_url_kwarg = "key_name"
    serializer_class = GetKeyValueSerializer

    def get_object(self):
        return get_object_or_404(Storage, data__key=self.kwargs[self.lookup_url_kwarg])
