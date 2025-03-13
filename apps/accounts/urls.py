from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .apis import UserCreateApi, UserEmailVerifyApi, UserResendVerificationApi, UserDataApi

urlpatterns = [
    path("register/", UserCreateApi.as_view(), name="user_register"),
    path('email/verify/<str:token>/', UserEmailVerifyApi.as_view(), name='email_verify'),
    path('email/resend/', UserResendVerificationApi.as_view(), name='email_resend'),
    
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    path("me/", UserDataApi.as_view(), name="user_data"),
]