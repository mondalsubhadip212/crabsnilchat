from .models import User, User_Friends
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class SignUp_User_Creation_Serializer(serializers.ModelSerializer):
    password1 = serializers.CharField(allow_null=False, allow_blank=False)
    password2 = serializers.CharField(allow_null=False, allow_blank=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def create(self, new_user_details):

        if new_user_details.validated_data['password1'] == new_user_details.validated_data['password2']:
            user = User.objects.create(username=new_user_details.validated_data['username'],
                                       email=new_user_details.validated_data['email'],
                                       password=make_password(new_user_details.validated_data['password1']))
            User_Friends.objects.create(user=user)
        else:
            raise serializers.ValidationError({'error': 'password must match'})
