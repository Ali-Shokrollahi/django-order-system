from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema


from .models import User
from .services import UserService


class UserCreateApi(APIView):
    class UserCreateInputSerializer(serializers.Serializer):
        email = serializers.EmailField()

        password = serializers.CharField(max_length=254, min_length=8)

        confirm_password = serializers.CharField(max_length=254)

        def validate(self, attrs):
            password = attrs.get("password")
            confirm_password = attrs.get("confirm_password")
            if password != confirm_password:
                raise serializers.ValidationError(
                    code="password_must_match", detail="Passwords must match"
                )

            return attrs

    class UserCreateOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ("email", "role", "created_at")

    @extend_schema(
        request=UserCreateInputSerializer, responses=UserCreateOutputSerializer
    )
    def post(self, request):
        serializer = self.UserCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = UserService()
        user = service.register_user(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        return Response(
            self.UserCreateOutputSerializer(user).data, status=status.HTTP_201_CREATED
        )
