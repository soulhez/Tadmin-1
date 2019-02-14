from API.core.BaseViewSet import AdminViewSet,AuthUserViewSet
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import routers, viewsets,validators
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from API.admin.user.serializers import AuthUserSerilizer, UserRoleSerilizer, RoleSerilizer, UserSerializer
from account.models import UserProfile, Role, UserRole
from django.db.models import Q
from django.core.cache import cache
from django.contrib.auth.hashers import make_password, check_password
from API.core.BaseViewSet import AuthUserViewSet
# userprofile
User = UserProfile

class UserViewSet(AuthUserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('username', 'email')

    def get_queryset(self):
        '''
         普通管理员不能看到超级管理员
        '''

        if self.request.user.is_superuser:
            return User.objects.all()
        else:
            print('no cg')
            return User.objects.filter(is_superuser=False)

    @action(methods=['get'], detail=False)
    def info(self, request):
        current_user = request.user
        serializer = UserSerializer(current_user)
        return Response(serializer.data)

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerilizer

class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerilizer


class CustomAuthToken(ObtainAuthToken):
    serializer_class = AuthUserSerilizer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=False)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        user = UserProfile.objects.filter(Q(username=username)|Q(email=username)).first()
        if user and  user.check_password(password) and user.is_active:
            #删除原有的token
            try:
                token = Token.objects.get(user=user)
                token.delete()
                cache.delete("token_" + token)
            except:
                pass
            #创建token
            token, created = Token.objects.get_or_create(user=user)
            token_cache = 'token_' + token.key
            cache.set(token_cache,token,timeout=60*60*24*7)
            return Response({
                'token': token.key,
            })
        return  Response({'msg':"账户不存在或密码错误"},status=401)



class Register(ObtainAuthToken):
    serializer_class = AuthUserSerilizer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        #查看用户名是否存在
        if User.objects.filter(username=serializer.data.get('username')):
            raise ValidationError("用户名已存在")
        if User.objects.filter(email=serializer.data.get('enail')):
            raise ValidationError("邮箱已存在")
        instance=User.objects.create(**serializer.data)
        token, created = Token.objects.get_or_create(user=instance)
        token_cache = 'token_' + token.key
        cache.set(token_cache, token, timeout=60 * 60 * 24 * 7)
        return Response({
            'token': token.key,
        })




