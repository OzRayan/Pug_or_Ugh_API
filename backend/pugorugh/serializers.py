from django.contrib.auth import get_user_model
from rest_framework.serializers import CharField, ModelSerializer

from .models import Dog, UserPref


class UserSerializer(ModelSerializer):
    """UserSerializer serializer
    :inherit: - ModelSerializer from rest_framework.serializers
    :field: - password
    :method: - create()
    """
    password = CharField(write_only=True)

    def create(self, validated_data):
        """create method - creates an user object
        :parameter: - validated_data
        :return: - user
        """
        user = get_user_model().objects.create(
            username=validated_data['username'],)
        user.set_password(validated_data['password'])
        user.save()

        # Prepares preferences for user
        UserPref(user=user).save()

        return user

    class Meta:
        model = get_user_model()


class DogSerializer(ModelSerializer):
    """DogSerializer serializer
    :inherit: - ModelSerializer from rest_framework.serializers
    """
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


class UserPrefSerializer(ModelSerializer):
    """DogSerializer serializer
    :inherit: - ModelSerializer from rest_framework.serializers
    """
    class Meta:
        fields = (
            'age',
            'gender',
            'size'
        )
        model = UserPref

