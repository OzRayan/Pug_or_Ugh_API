from django.contrib.auth.models import User
from django.db import models


class Dog(models.Model):
    name = models.CharField(max_length=100)
    image_filename = models.CharField(max_length=100)
    breed = models.CharField(max_length=100,
                             default='unknown')
    age = models.IntegerField(help_text='Months in number')
    gender = models.CharField(
        max_length=20,
        help_text='"m" for male, "f" for female, "u" for unknown')
    size = models.CharField(
        max_length=20,
        help_text='"s" for small, "m" for medium, "l" for large, '
                  '"xl" for extra large, "u" for unknown')

    def __str__(self):
        return self.name


class UserDog(models.Model):
    user = models.ForeignKey(User)
    dog = models.ForeignKey(Dog)
    status = models.CharField(
        max_length=10, help_text='"l" for liked, "d" for disliked',
        default='u')

    def __str__(self):
        return 'Dog: {}, User: {}'.format(self.dog.name.title(),
                                          self.user.username.title())


class UserPref(models.Model):
    user = models.OneToOneField(User)
    age = models.CharField(
        max_length=20,
        help_text='"b" for baby, "y" for young, '
                  '"a" for adult, "s" for senior')
    gender = models.CharField(max_length=10,
                              help_text='"m" for male, "f" for female')
    size = models.CharField(max_length=10,
                            help_text='"s" for small, "m" for medium,'
                                      '"l" for large, "xl" for extra')

    def __str__(self):
        return "{}'s dog preferences".format(self.user.username.title())