from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.generics import (CreateAPIView, RetrieveAPIView, UpdateAPIView,
                                     RetrieveUpdateAPIView)

from .serializers import UserSerializer, DogSerializer, UserPrefSerializer
from .models import Dog, UserDog, UserPref


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = UserSerializer


class UserPrefView(RetrieveUpdateAPIView):
    queryset = UserPref.objects.all()
    serializer_class = UserPrefSerializer

    def get_object(self):
        return self.get_queryset().get(user=self.request.user)


class RetrieveNextDogView(RetrieveAPIView):
    queryset = UserDog.objects.all()
    serializer_class = DogSerializer


class UpdateDogView(UpdateAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer

