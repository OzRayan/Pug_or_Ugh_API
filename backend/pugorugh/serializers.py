from django.contrib.auth import get_user_model
from rest_framework.serializers import CharField, ModelSerializer

from .models import Dog, UserDog, UserPref


class UserSerializer(ModelSerializer):
    password = CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        UserPref(user=user).save()

        # UserPref(user=user).save()
        #
        dog_query = Dog.objects.all()
        for dog in dog_query:
            UserDog(
                user=user,
                dog=dog,
                status='u').save()
        return user

    class Meta:
        model = get_user_model()


class DogSerializer(ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'image_filename',
            'breed',
            'age',
            'gender',
            'size'
        )
        model = Dog


class UserDogSerializer(ModelSerializer):
    class Meta:
        fields = (
            'user',
            'dog',
            'status'
        )
        model = UserDog


class UserPrefSerializer(ModelSerializer):
    class Meta:
        fields = (
            'age',
            'gender',
            'size'
        )
        model = UserPref

