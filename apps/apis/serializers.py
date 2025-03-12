from rest_framework.serializers import Serializer, CharField


class MessageSerializer(Serializer):
    message = CharField(max_length=255)
