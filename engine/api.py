
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from allauth.account.models import EmailAddress


User = get_user_model()


class CurrentUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    email_verified = serializers.SerializerMethodField()

    def get_email_verified(self, obj):
        return EmailAddress.objects.filter(
            user=obj,
            email=obj.email,
            verified=True,
        ).exists()


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Текущий пользователь',
        description='Возвращает данные авторизованного пользователя.',
        responses=CurrentUserSerializer,
        tags=['Authentication'],
    )
    def get(self, request):
        serializer = CurrentUserSerializer(request.user)
        return Response(serializer.data)
