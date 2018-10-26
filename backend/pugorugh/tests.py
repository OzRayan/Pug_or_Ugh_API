from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from rest_framework.test import APIRequestFactory, force_authenticate
from . import models, views


class ViewTest(TestCase):
    def setUp(self):
        self.dog_data = {
            'name': 'Tomika',
            'image_filename': 'pugorugh/static/images/dogs/20.jpg',
            'breed': 'Belgian Malinois mix',
            'age': 51,
            'gender': 'm',
            'size': 'm'
        }
        # noinspection PyUnresolvedReferences
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@mail.com',
            password='testpassword'
        )
        # noinspection PyUnresolvedReferences
        self.user_pref = models.UserPref.objects.create(
            user=self.user,
            age='b,y,a,s',
            gender='m,f',
            size='s,m,l,xl'
        )
        # noinspection PyUnresolvedReferences
        self.dog = models.Dog.objects.create(
            name=self.dog_data['name'],
            image_filename=self.dog_data['image_filename'],
            breed=self.dog_data['breed'],
            age=self.dog_data['age'],
            gender=self.dog_data['gender'],
            size=self.dog_data['size']
        )
        # noinspection PyUnresolvedReferences
        models.UserDog.objects.create(
            user=self.user,
            dog=self.dog,
            status='u'
        )
