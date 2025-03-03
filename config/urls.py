from django.contrib import admin
from django.urls import include, path
from django.conf import settings

from debug_toolbar.toolbar import debug_toolbar_urls
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

docs_urls = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(), name="swagger"),
    path("redoc/", SpectacularRedocView.as_view(), name="redoc"),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.apis.urls"), name="api"),
] + docs_urls

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
