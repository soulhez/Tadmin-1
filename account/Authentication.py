<<<<<<< HEAD:account/Authentication.py

from rest_framework.authentication import BaseAuthentication,BasicAuthentication
from rest_framework import exceptions
from  account import models

class CustomAuthenticate(BasicAuthentication):
    def authenticate(self, request):
        username = request.META.get('X_USERNAME')
        if not username:
            return None
        try:
            user = models.UserProfile.objects.get(username=username)
        except models.UserProfile.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        return (user, None)

class SuperUserAuthenticate(BaseAuthentication):
    '''
        超级用户
    '''
    def authenticate(self, request):
        username = request.META.get('X_USERNAME')
        if not username:
            return None
        try:
            user = models.UserProfile.objects.get(username=username)
        except models.UserProfile.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

=======

from rest_framework.authentication import BaseAuthentication,BasicAuthentication
from rest_framework import exceptions
from  account import models

class CustomAuthenticate(BasicAuthentication):
    def authenticate(self, request):
        username = request.META.get('X_USERNAME')
        if not username:
            return None
        try:
            user = models.UserProfile.objects.get(username=username)
        except models.UserProfile.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        return (user, None)

class SuperUserAuthenticate(BaseAuthentication):
    '''
        超级用户
    '''
    def authenticate(self, request):
        username = request.META.get('X_USERNAME')
        if not username:
            return None
        try:
            user = models.UserProfile.objects.get(username=username)
        except models.UserProfile.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

>>>>>>> 93f4cb47c6f35636422bbda9c81e79a972b5ec84:account/Authentication.py
        return (user, None)