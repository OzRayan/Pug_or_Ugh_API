from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.generics import (CreateAPIView, RetrieveAPIView, UpdateAPIView,
                                     RetrieveUpdateAPIView)

from .serializers import (UserSerializer, DogSerializer, UserPrefSerializer,
                          UserDogSerializer)
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


class NextDogView(RetrieveAPIView):
    serializer_class = DogSerializer

    @staticmethod
    def age_range(user_preferences):
        age_list = []
        if 'b' in user_preferences:
            age_list.extend(list(range(0, 3)))
        if 'y' in user_preferences:
            age_list.extend(list(range(3, 11)))
        if 'a' in user_preferences:
            age_list.extend(list(range(11, 60)))
        if 's' in user_preferences:
            age_list.extend(list(range(60, 120)))
        return age_list

    def get_queryset(self):
        user_preferences = UserPref.objects.get(
            user=self.request.user)

        age_list = self.age_range(user_preferences.age.split(','))
        query = Dog.objects.filter(
            age__in=age_list,
            gender__in=user_preferences.gender.split(','),
            size__in=user_preferences.size.split(',')
        ).order_by('pk')

        for dog in query:
            UserDog(
                user=self.request.user,
                dog=dog,
                status='u'
            ).save()

        status = ''
        if self.kwargs['status'] == 'liked':
            status = 'l'
        if self.kwargs['status'] == 'disliked':
            status = 'd'
        if self.kwargs['status'] == 'undecided':
            status = 'u'

        return query.filter(userdog__user_id=self.request.user.id,
                            userdog__status=status)

    def get_object(self):

        pk = int(self.kwargs['pk'])
        queryset = self.get_queryset().filter(id__gt=pk).first()
        if queryset:
            return queryset
        else:
            return self.get_queryset().first()


class StatusDogView(UpdateAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer

