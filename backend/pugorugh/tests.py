# NOTE: # noinspection - prefixed comments are for pycharm editor only
# for ignoring PEP 8 style highlights

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from .models import Dog, UserDog, UserPref
from .views import NextDogView, StatusDogView, UserPrefView, UserRegisterView


class BaseTest(TestCase):
    """BaseTest class for all tests
    :inherit: -TestCase from django.test
    dog_data: - dog info(json or dict) for testing
    :method: - setUp()
    """
    dog_data = {'name': 'Tomika',
                'image_filename': 'pugorugh/static/images/dogs/20.jpg',
                'breed': 'Belgian Malinois mix',
                'age': 51,
                'gender': 'm',
                'size': 'm'}

    def setUp(self):
        """setUp method
        self.user: - User object
        self.user_pref: - UserPref object
        self.dog: - Dog object created from dog_data
        UserDog object
        """
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
    """UserView test
    All test uses APIRequestFactory() class from rest_framework.test
    :inherit: - BaseTest
    response_data - userpref data (json or dict)
    :methods: - test_user_register()
              - test_getUserPrefView()
              - test_putUserPrefView()
    """
    response_data = {'age': 'b', 'gender': 'm', 'size': 'm'}

    def test_user_register(self):
        """Test_user_register
        :request: - post using factory
        :test: - status code 201
               - response data
        """
        factory = APIRequestFactory()
        request = factory.post(
            reverse('register-user'),
            {'username': 'testuser2', 'password': 'password2'})
        view = UserRegisterView.as_view()

        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('username'), 'testuser2')

    def test_getUserPrefView(self):
        """Test_getUserPrefView
        :request: - get using factory
        :test: - status code 200
               - response data
        """
        factory = APIRequestFactory()
        request = factory.get(reverse('preferences'))
        force_authenticate(request, user=self.user)
        view = UserPrefView.as_view()

        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('age'), 'b,y,a,s')
        self.assertEqual(response.data.get('gender'), 'm,f')
        self.assertEqual(response.data.get('size'), 's,m,l,xl')

    def test_putUserPrefView(self):
        """Test_putUserPrefView
        :request: - put using factory
        :test: - status code 200
               - response data == self.response_data(defined in class)
        """
        factory = APIRequestFactory()
        request = factory.put(reverse('preferences'), self.response_data)
        force_authenticate(request, user=self.user)
        view = UserPrefView.as_view()

        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.response_data)


class NextDogViewTest(BaseTest):
    """NextDogView test
    Test uses APIRequestFactory() class from rest_framework.test
    :inherit: - BaseTest
    :methods: - test_getNextDogView()
    """
    def test_getNextDogView(self):
        """Test_getNextDogView
        :request: - get using factory
        :test: - status code 200
               - response data
        """
        factory = APIRequestFactory()
        request = factory.get(reverse('next', kwargs={'pk': -1, 'status': 'liked'}))
        force_authenticate(request, user=self.user)
        view = NextDogView.as_view()

        response = view(request, pk=-1, status='undecided')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('name'), 'Tomika')


class StatusDogViewTest(BaseTest):
    """StatusDogView test
    Test uses APIRequestFactory() class from rest_framework.test
    :inherit: - BaseTest
    :methods: - test_getDogView()
    """
    def test_getDogView(self):
        """Test_getDogView
        :request: - put using factory
        :test: - status code 200
               - response data
        """
        factory = APIRequestFactory()
        request = factory.put(reverse('status', kwargs={'pk': 1, 'status': 'liked'}))
        force_authenticate(request, user=self.user)
        view = StatusDogView.as_view()

        response = view(request, pk=1, status='liked')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('name'), 'Tomika')
