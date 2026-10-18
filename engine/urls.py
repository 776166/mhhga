"""
URL configuration for mhhga project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from .api import CurrentUserView

from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path('admin/', admin.site.urls),

    path("accounts/", include("allauth.urls")),
]

urlpatterns += [
    path("candidates/", include("candidates.urls")),
    # path("r/<uuid:public_id>/", candidates.views.public_resume, name="public_resume"),
]

urlpatterns += [
    path(
        'api/schema/',
        SpectacularAPIView.as_view(
            permission_classes=[permissions.AllowAny],
        ),
        name='schema',
    ),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(
            url_name='schema',
            permission_classes=[permissions.AllowAny],
        ),
        name='swagger-ui',
    ),
    path(
        'api/redoc/',
        SpectacularRedocView.as_view(
            url_name='schema',
            permission_classes=[permissions.AllowAny],
        ),
        name='redoc',
    ),
    path('api/v1/me/', CurrentUserView.as_view(), name='api-me'),
]

