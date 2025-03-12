from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from apps.apis.serializers import MessageSerializer
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
        request=UserCreateInputSerializer, responses={201: UserCreateOutputSerializer}
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
            self.UserCreateOutputSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


class UserEmailVerifyApi(APIView):
    @extend_schema(
        responses=MessageSerializer
    )
    def get(self, request, token):
        service = UserService()
        service.verify_user_email(token=token)
        return Response(
            {"message": "Email confirmed successfully"},
            status=status.HTTP_200_OK,
        )


class UserResendVerificationApi(APIView):
    class ResendVerificationInputSerializer(serializers.Serializer):
        email = serializers.EmailField()

    @extend_schema(
        request=ResendVerificationInputSerializer, responses=MessageSerializer
    )
    def post(self, request):
        serializer = self.ResendVerificationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = UserService()
        service.resend_verification_email(email=serializer.validated_data["email"])
        return Response(
            {"message": "Verification email resent successfully", "data": None},
            status=status.HTTP_200_OK,
        )
