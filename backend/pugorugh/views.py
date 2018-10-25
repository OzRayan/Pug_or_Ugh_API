from django.contrib.auth import get_user_model
# from django.core.exceptions import ObjectDoesNotExist

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
    # noinspection PyUnresolvedReferences
    queryset = UserPref.objects.all()
    serializer_class = UserPrefSerializer

    def get_object(self):
        """get_object method
        :return - user preferences object
        """
        queries = self.get_queryset().get(user=self.request.user)
        # print('############')
        # print(queries.age)
        # print(queries.gender)
        # print(queries.size)
        # print('############')
        return queries


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
        age_list = []

        user = self.request.user
        # noinspection PyUnresolvedReferences
        user_preferences = UserPref.objects.get(user=user)

        pref_age = user_preferences.age.split(',')
        if 'b' in pref_age:
            age_list.extend(list(range(0, 4)))
        if 'y' in pref_age:
            age_list.extend(list(range(4, 12)))
        if 'a' in pref_age:
            age_list.extend(list(range(12, 61)))
        if 's' in pref_age:
            age_list.extend(list(range(61, 121)))

        # noinspection PyUnresolvedReferences
        queries = Dog.objects.filter(
            age__in=age_list,
            gender__in=user_preferences.gender.split(','),
            size__in=user_preferences.size.split(','))

        # 
        for dog in queries:
            # noinspection PyUnresolvedReferences
            obj, exists = UserDog.objects.get_or_create(
                user=self.request.user,
                dog=dog,
                defaults={'user': self.request.user, 'dog': dog, 'status': 'u'})
            obj.save()

        status = self.kwargs['status'][0]

        queryset = queries.filter(userdog__user_id=user.id,
                                  userdog__status=status).order_by('pk')
        return queryset

    def get_object(self):
        """get_object method
        :return - if there id s queryset:
                    -first dog object filtered by pk
                  else
                    -first dog object
        """
        pk = self.kwargs['pk']

        query = self.get_queryset().filter(id__gt=int(pk)).first()

        if query:
            return query
        return self.get_queryset().first()


class StatusDogView(UpdateAPIView):
    # noinspection PyUnresolvedReferences
    queryset = Dog.objects.all()
    serializer_class = DogSerializer

    def get_object(self):

        pk = self.kwargs['pk']

        query = self.get_queryset().get(pk=pk)

        if query:
            return query
        return Response(status=404)

    def put(self, *args, **kwargs):

        query = self.get_object()

        status = self.kwargs['status'][0]

        # noinspection PyUnresolvedReferences
        obj, exists = UserDog.objects.get_or_create(
            user=self.request.user,
            dog=query,
            defaults={'user': self.request.user, 'dog': query, 'status': status})

        obj.status = status
        obj.save()

        serializer = DogSerializer(query)
        return Response(serializer.data)
