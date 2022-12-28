from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=user.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = user
        fields = ['username', 'password', 'password2', 'email', 'f_name', 'l_name']
        extra_kwargs = {
                'f_name': {'required':True}, 
                'l_name': {'required':True},
                }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password':"Password didn't match"})
        return attrs

    def create(self, validated_data):
        user2 = user.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            f_name = validated_data['f_name'],
            l_name = validated_data['l_name']
        )
        user2.set_password(validated_data['password'])
        user2.save()
        return user2
    
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=1000)

    class Meta:
        model = user
        fields = ['token']

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = user
        fields = ['username', 'password', 'tokens']

    def validate(self, attrs):
        username = attrs.get('username', )
        password = attrs.get('password', )

        request_user = auth.authenticate(username=username, password=password)
        if not request_user:
            raise AuthenticationFailed('Invalid credintials, try again')
        if not request_user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not request_user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        
        return {
            'username' : request_user.username,
            'tokens' : request_user.tokens
        }