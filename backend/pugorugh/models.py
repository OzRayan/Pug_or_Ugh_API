from django.contrib.auth.models import User
from django.db import models


CHOICES = {
    'age': (('b', 'baby'),
            ('y', 'young'),
            ('a', 'adult'),
            ('s', 'senior')),
    'gender': (('m', 'male'),
               ('f', 'female')),
    'size': (('s', 'small'),
             ('m', 'medium'),
             ('l', 'large'),
             ('xl', 'extra large'))
}


class Dog(models.Model):
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1, help_text='[L]iked [D]isliked',
        default='u')

    def __str__(self):
        return 'Dog: {}, User: {}'.format(self.dog.name.title(),
                                          self.user.username.title())


class UserPref(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='preferences')
    age = models.CharField(
        default='b,y,a,s',
        # choices=CHOICES['age'],
        max_length=7,
        help_text='[B]aby [Y]oung [A]dult [S]enior')
    gender = models.CharField(
        default='m,f',
        # choices=CHOICES['gender'],
        max_length=3,
        help_text='"[M]ale [F]emale')
    size = models.CharField(
        default='s,m,l,xl',
        # choices=CHOICES['size'],
        max_length=8,
        help_text='[S]mall [M]edium [L]arge [XL]arge')

    def __str__(self):
        return "{}'s dog preferences".format(self.user.username.title())
