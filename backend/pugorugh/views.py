from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from .serializers import UserSerializer


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = UserSerializer
