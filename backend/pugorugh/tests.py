# NOTE: # noinspection - prefixed comments are for pycharm editor only
# for ignoring PEP 8 style highlights

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from .models import Dog, UserDog, UserPref
from .views import NextDogView, StatusDogView, UserPrefView, UserRegisterView


class BaseTest(TestCase):
    dog_data = {'name': 'Tomika',
                'image_filename': 'pugorugh/static/images/dogs/20.jpg',
                'breed': 'Belgian Malinois mix',
                'age': 51,
                'gender': 'm',
                'size': 'm'}

    def setUp(self):

        # noinspection PyUnresolvedReferences
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@mail.com',
            password='testpassword'
        )
        # noinspection PyUnresolvedReferences
        self.user_pref = UserPref.objects.create(
            user=self.user,
            age='b,y,a,s',
            gender='m,f',
            size='s,m,l,xl'
        )
        # noinspection PyUnresolvedReferences
        self.dog = Dog.objects.create(
            name=self.dog_data['name'],
            image_filename=self.dog_data['image_filename'],
            breed=self.dog_data['breed'],
            age=self.dog_data['age'],
            gender=self.dog_data['gender'],
            size=self.dog_data['size']
        )
        # noinspection PyUnresolvedReferences
        UserDog.objects.create(
            user=self.user,
            dog=self.dog,
            status='u'
        )


class UserViewTest(BaseTest):

    response_data = {'age': 'b', 'gender': 'm', 'size': 'm'}

    def test_user_register(self):
        factory = APIRequestFactory()
        request = factory.post(
            reverse('register-user'),
            {'username': 'testuser2', 'password': 'password2'})
        view = UserRegisterView.as_view()

        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_getUserPrefView(self):
        factory = APIRequestFactory()
        request = factory.get(reverse('preferences'))
        force_authenticate(request, user=self.user)
        view = UserPrefView.as_view()

        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_putUserPrefView(self):
        factory = APIRequestFactory()
        request = factory.put(reverse('preferences'), self.response_data)
        force_authenticate(request, user=self.user)
        view = UserPrefView.as_view()

        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.response_data)


class NextDogViewTest(BaseTest):
    def test_getNextDogView(self):
        factory = APIRequestFactory()
        request = factory.get(reverse('next', kwargs={'pk': 1, 'status': 'liked'}))
        force_authenticate(request, user=self.user)
        view = NextDogView.as_view()

        response = view(request, pk=1, status='liked')
        self.assertEqual(response.status_code, 200)


class StatusDogViewTest(BaseTest):
    def test_getGetDogView(self):
        factory = APIRequestFactory()
        request = factory.put(reverse('status', kwargs={'pk': 1, 'status': 'undecided'}))
        force_authenticate(request, user=self.user)
        view = StatusDogView.as_view()

        response = view(request, pk=1, status='undecided')
        self.assertEqual(response.status_code, 200)
