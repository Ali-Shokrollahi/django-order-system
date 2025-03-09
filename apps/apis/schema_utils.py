from rest_framework import serializers
from drf_spectacular.utils import inline_serializer


def get_success_response(
    serializer_name: str,
    data_serializer: type[serializers.Serializer] | None = None,
) -> type[serializers.Serializer]:
    """
    Factory function to create a unique response serializer for each endpoint.
    """

    fields = {
        "message": serializers.CharField(max_length=255),
        "data": data_serializer()
        if data_serializer
        else serializers.DictField(allow_null=True, required=False)
    }

    return inline_serializer(name=serializer_name, fields=fields)
