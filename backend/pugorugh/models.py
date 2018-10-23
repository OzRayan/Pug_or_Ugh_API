from django.contrib.auth.models import User
from django.db import models


class Dog(models.Model):
    """Dog model
    :inherit: - Model from django.db.models
    :fields: - name - CharField
             - image_filename - CharField
             - breed - CharField
             - age - IntegerField
             - gender - CharField
             - size - CharField
    """
    name = models.CharField(max_length=100)
    image_filename = models.CharField(max_length=100)
    breed = models.CharField(max_length=100,
                             default='unknown')
    age = models.IntegerField(help_text='Months in number')
    gender = models.CharField(
        max_length=1,
        help_text='[M]ale [F]emale [U]nknown')
    size = models.CharField(
        max_length=2,
        help_text='[S]mall [M]edium [L]arge [XL]arge [U]nknown')

    def __str__(self):
        return self.name


class UserDog(models.Model):
    """UserDog model
    :inherit: - Model from django.db.models
    :fields: - user - ForeignKey(User)
             - dog - ForeignKey(Dog)
             - status - CharField
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1, help_text='[L]iked [D]isliked',
        default='u')

    def __str__(self):
        return 'Dog: {}, User: {}'.format(self.dog.name.title(),
                                          self.user.username.title())


class UserPref(models.Model):
    """UserPref model
    :inherit: - Model from django.db.models
    :fields: - user - OneToOneField(User)
             - age - CharField
             - gender - CharField
             - size - CharField
    """
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='preferences')
    age = models.CharField(
        default='b,y,a,s',
        max_length=7,
        help_text='[B]aby [Y]oung [A]dult [S]enior')
    gender = models.CharField(
        default='m,f',
        max_length=3,
        help_text='"[M]ale [F]emale')
    size = models.CharField(
        default='s,m,l,xl',
        max_length=8,
        help_text='[S]mall [M]edium [L]arge [XL]arge')

    def __str__(self):
        return "{}'s dog preferences".format(self.user.username.title())
