from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from .managers import CustomUserManager
from rest_framework_simplejwt.tokens import RefreshToken

class user(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    email = models.CharField(max_length=200, unique=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_picture/', blank=True)
    about = models.TextField(blank=True)
    admin_status = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    def __str__(self):
        return self.username + ' (' + self.designation() + ')'
    
    def designation(self):
        if self.is_staff == True:
            return 'staff'
        if self.is_superuser == True:
            return 'superuser'
        else:
            return 'user'

    def tokens(self):
        refresh_token = RefreshToken.for_user(self)
        access_token = RefreshToken.for_user(self).access_token
        return{
            'refresh token' : str(refresh_token),
            'access token' : str(access_token)
        }