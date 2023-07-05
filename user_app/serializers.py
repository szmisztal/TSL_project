from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from .models import CustomUser
from django.dispatch import receiver
from rest_framework import serializers

@receiver(post_save, sender = CustomUser)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created:
        Token.objects.create(user = instance)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 'email')
        extra_kwargs = {
            'password': {'required': True, 'write_only': True},
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
