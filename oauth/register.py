from accounts.models import user
import random
from django.contrib import auth
import os
from rest_framework.exceptions import AuthenticationFailed

def generate_username(name):
    username = ''.join(name.split(' ')).lower()
    if not user.objects.filter(username=username).exists():
        return username
    
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)
    
def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = user.objects.filter(email=email)

    if filtered_user_by_email.exists():
        raise AuthenticationFailed('Email already exists')
    else:
        User = {
            'username' : generate_username(name),
            'email' : email,
            'password' : os.environ.get('SOCIAL_PASS')
        }
        User = user.objects.create(**User)
        User.is_verified = True
        User.auth_provide = provider
        User.save()

        new_user = auth.authenticate(
            username = User['username'], password = os.environ.get('SOCIAL_PASS')
        )

        return {
            'username' : new_user.username,
            'email' : new_user.email,
            'tokens' : new_user.token(),
        }