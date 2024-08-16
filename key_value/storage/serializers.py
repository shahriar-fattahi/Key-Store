from django.db.models.query import QuerySet
from rest_framework import serializers

from .models import Storage


class SetKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = [
            "data",
        ]

    def validate_data(self, data):
        if "key" not in data:
            raise serializers.ValidationError({"key": "data must include a key name."})

        if len(data["key"]) > 20:
            raise serializers.ValidationError(
                {"key": "key name should be less than 20 chars."}
            )
        if len(data["key"]) < 1:
            raise serializers.ValidationError(
                {"key": "key name should contain at least 1 char."}
            )

        if Storage.objects.filter(data__key=data["key"]).exists():
            raise serializers.ValidationError({"key": "this key name already exists."})

        if "value" not in data:
            raise serializers.ValidationError({"value": "data must include a value."})

        keys_to_keep = {
            "key",
            "value",
        }
        filtered_dict = {k: data[k] for k in keys_to_keep if k in data}
        return filtered_dict


class GetKeyValueSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        if not isinstance(instance, QuerySet):
            return {instance.data["key"]: instance.data["value"]}

        OUTPUT = dict()
        for storage in instance:
            OUTPUT[storage.id] = {storage.data["key"]: storage.data["value"]}

        return OUTPUT
