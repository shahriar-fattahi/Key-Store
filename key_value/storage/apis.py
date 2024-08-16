from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from .models import Storage
from .serializers import GetKeyValueSerializer, SetKeySerializer


class SetKeyApi(CreateAPIView):
    serializer_class = SetKeySerializer


@method_decorator(cache_page(60 * 60 * 2), name="get")
class GetKeyValueListApi(ListAPIView):
    serializer_class = GetKeyValueSerializer

    def get_queryset(self):
        return Storage.objects.all()


@method_decorator(cache_page(60 * 60 * 2), name="get")
class GetValueApi(RetrieveAPIView):
    lookup_url_kwarg = "key_name"
    serializer_class = GetKeyValueSerializer

    def get_object(self):
        return get_object_or_404(Storage, data__key=self.kwargs[self.lookup_url_kwarg])
