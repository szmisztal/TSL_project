from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.contrib.auth.hashers import make_password
from django.dispatch import receiver
from rest_framework import serializers
from .models import CustomUser

@receiver(post_save, sender = CustomUser)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created:
        Token.objects.create(user = instance)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'email', 'role']
        extra_kwargs = {
            'password': {'required': True, 'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)
        custom_user = CustomUser.objects.create_user(**validated_data)
        return custom_user
