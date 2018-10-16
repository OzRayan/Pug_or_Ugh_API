from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView

from .serializers import UserSerializer, DogSerializer
from .models import Dog


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = UserSerializer

#
# class ListDogView(ListAPIView):
#     queryset = Dog.objects().all()
#     serializer_class = DogSerializer
