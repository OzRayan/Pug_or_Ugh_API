from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.generics import (CreateAPIView, RetrieveAPIView,
                                     UpdateAPIView, RetrieveUpdateAPIView)

from .serializers import UserSerializer, DogSerializer, UserPrefSerializer
from .models import Dog, UserDog, UserPref


class UserRegisterView(CreateAPIView):
    """UserRegister View
    :inherit: - CreateAPIView from rest_framework.generics
    :variables: - permission_classes - AllowAny from rest_framework.permissions
                - model - get_user_model() from django.contrib.auth
                - serializer_class - UserSerializer
    """
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = UserSerializer


class UserPrefView(RetrieveUpdateAPIView):
    """UserPref View
    :inherit: - RetrieveUpdateAPIView from rest_framework.generics
    :variables: - queryset - UserPref objects
                - serializer_class - UserPrefSerializer
    :method: - get_object()
    """
    queryset = UserPref.objects.all()
    serializer_class = UserPrefSerializer

    def get_object(self):
        """get_object method
        :return - user preferences object
        """
        return self.get_queryset().get(user=self.request.user)


class NextDogView(RetrieveAPIView):
    """NextDog View
    :inherit: - RetrieveAPIView from rest_framework.generics
    :variables: - serializer_class - DogSerializer
    :method: - get_queryset()
             - get_object()
    """
    serializer_class = DogSerializer

    def get_queryset(self):
        """get_queryset method
        :return - dog queryset
        """
        user = self.request.user
        user_preferences = UserPref.objects.get(user=user)
        age_list = []
        pref_age = user_preferences.age.split(',')

        if 'b' in pref_age:
            age_list.extend(list(range(0, 3)))
        if 'y' in pref_age:
            age_list.extend(list(range(3, 11)))
        if 'a' in pref_age:
            age_list.extend(list(range(11, 60)))
        if 's' in pref_age:
            age_list.extend(list(range(60, 120)))

        query = Dog.objects.filter(
            age__in=age_list,
            gender__in=user_preferences.gender.split(','),
            size__in=user_preferences.size.split(',')
        ).order_by('pk')

        [UserDog(user=user, dog=dog, status='u').save() for dog in query]
        status = self.kwargs['status'][0]
        # print('############')
        # print(self.kwargs['status'][0])
        # print('############')
        queryset = query.filter(userdog__user_id=user.id,
                                userdog__status=status)
        return queryset

    def get_object(self):
        """get_object method
        :return - if there id s queryset:
                    -first dog object filtered by pk
                  else
                    -first dog object
        """
        pk = int(self.kwargs['pk'])
        queryset = self.get_queryset().filter(id__gt=pk)[0]
        if queryset:
            return queryset
        else:
            return self.get_queryset()[0]


class StatusDogView(UpdateAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer

    def put(self, *args, **kwargs):
        pk = self.kwargs['pk']
        status = self.kwargs['status'][0]
        dog_query = self.get_object().get(pk=pk)
        UserDog.objects.get_or_create(
            user=self.request.user,
            dog=dog_query,
            status=status
        ).save()
        serializer = DogSerializer(dog_query)
        return Response(serializer.data)

