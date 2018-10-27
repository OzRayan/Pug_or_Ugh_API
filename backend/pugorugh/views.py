# NOTE: # noinspection - prefixed comments are for pycharm editor only
# for ignoring PEP 8 style highlights

from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.generics import (CreateAPIView, RetrieveAPIView,
                                     UpdateAPIView, RetrieveUpdateAPIView)

from .serializers import UserSerializer, DogSerializer, UserPrefSerializer
from .models import Dog, UserDog, UserPref


class UserRegisterView(CreateAPIView):
    """UserRegister View
    :url: - api/user/

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
    :url: - api/user/preferences/

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
        :return: - user preferences object
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
    :url: - api/dog/<pk>/<status>undecided|liked|disliked/next/

    :inherit: - RetrieveAPIView from rest_framework.generics
    :variables: - serializer_class - DogSerializer
    :method: - get_queryset()
             - get_object()
    """
    serializer_class = DogSerializer

    def get_queryset(self):
        """get_queryset method
        :return: - dog queryset
        """
        age_list = []

        user = self.request.user

        # Retrieving user preferences
        # noinspection PyUnresolvedReferences
        user_preferences = UserPref.objects.get(user=user)

        # user preference dog age: 'b,y,a,s'.split(',')
        pref_age = user_preferences.age.split(',')

        # age_list extended with age in months based on the user preferences
        if 'b' in pref_age:
            age_list.extend(list(range(0, 4)))
        if 'y' in pref_age:
            age_list.extend(list(range(4, 12)))
        if 'a' in pref_age:
            age_list.extend(list(range(12, 61)))
        if 's' in pref_age:
            age_list.extend(list(range(61, 121)))

        # All Dog objects filtered by the user preference (age, gender and size)
        # age filter - age_list populated above
        # gender - user preference dog gender: 'm,f'.split(',')
        # size - user preference dog size: 's,m,l,xl'.split(',')
        # noinspection PyUnresolvedReferences
        queries = Dog.objects.filter(
            age__in=age_list,
            gender__in=user_preferences.gender.split(','),
            size__in=user_preferences.size.split(','))

        # Retrieves or creates an UserDog object and saves object
        # This call requires a tuple of variable: object, exists
        # -- exists must be given otherwise will trow an error
        for dog in queries:
            # noinspection PyUnresolvedReferences
            obj, exists = UserDog.objects.get_or_create(
                user=self.request.user,
                dog=dog,
                defaults={'user': self.request.user, 'dog': dog, 'status': 'u'})
            obj.save()

        # Status first letter from url
        status = self.kwargs['status'][0]

        # queryset filtered by user id and user_dog status, ordered by pk
        queryset = queries.filter(userdog__user_id=user.id,
                                  userdog__status=status).order_by('pk')
        return queryset

    def get_object(self):
        """get_object method
        :return: - if there is a queryset:
                     - first dog object filtered by grater than pk
                   else
                     - first dog object
        """
        # pk from url
        pk = self.kwargs['pk']

        # First Dog object returned by get_queryset() method
        # filtered by pk grater than the pk defined above
        query = self.get_queryset().filter(id__gt=int(pk)).first()

        # Return Dog if there is, get_queryset first object
        if query:
            return query
        return self.get_queryset().first()


class StatusDogView(UpdateAPIView):
    """StatusDog View
    :url: - api/dog/<pk>/<status>undecided|liked|disliked/

    :inherit: - UpdateAPIView from rest_framework.generics
    :variables: - queryset - Dog objects
                - serializer_class - DogSerializer
    :method: - get_object()
             - put()
    """
    # noinspection PyUnresolvedReferences
    queryset = Dog.objects.all()
    serializer_class = DogSerializer

    def get_object(self):
        """get_object method by pk
        :return: - if there is a query(Dog):
                     - query
                   else
                     - status code 404
        """
        # pk from url
        pk = self.kwargs['pk']

        # Dog object from get_queryset
        query = self.get_queryset().get(pk=pk)

        # Return Dog if there is, otherwise 404
        if query:
            return query
        return Response(status=404)

    def put(self, *args, **kwargs):
        """put method
        Get a Dog object if does exists and sets status
        if object doesn't exists, creates and sets status.
        :param: - *args - any argument
                - **kwargs - any key pair argument
        :returns: - Response with Dog serialized data
        """
        # Dog object returned by get_object() method
        query = self.get_object()

        # Status first letter from url
        status = self.kwargs['status'][0]

        # Retrieves or creates an UserDog object and sets the status
        # to the first letter of the status defined above
        # This call requires a tuple of variable: object, exists
        # -- exists must be given otherwise will trow an error

        # noinspection PyUnresolvedReferences
        obj, exists = UserDog.objects.get_or_create(
            user=self.request.user,
            dog=query,
            defaults={'user': self.request.user, 'dog': query, 'status': status})
        obj.status = status
        obj.save()

        # Serialized Dog object
        serializer = DogSerializer(query)
        return Response(serializer.data)
