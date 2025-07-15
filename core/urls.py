from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

def health_check(request):
    return JsonResponse({"status": "Healthy"})

urlpatterns = [
    path("", health_check),
    path("admin/", admin.site.urls),
    path("api/", include(
        [
            path("users/", include("user.urls")),
            path('schema/', SpectacularAPIView.as_view(), name='schema'),
            path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
            path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
        ]
    ))
]
