from rest_framework import routers, serializers, viewsets,views
from rest_framework.pagination import LimitOffsetPagination

from django.http import JsonResponse
from django.shortcuts import HttpResponse
#
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.views import APIView
from rest_framework.decorators import action


# 认证类
class AuthToken(viewsets.ViewSet):
    '''
        用户登录注册注销修改密码
    '''
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    if coreapi is not None and coreschema is not None:
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="username",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Username",
                        description="Valid username for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    # def post(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data=request.data,
    #                                        context={'request': request})
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.validated_data['user']
    #     token, created = Token.objects.get_or_create(user=user)
    #     return Response({'token': token.key})
    # def get(self,request,*args,**kwargs):
    #     return Response({})
    @action(detail=False)
    def login(self):
        return Response({'s':"123"})


def list_router(methods=None,**kwargs):
    methods = ['get'] if (methods is None) else methods
    def decorator(func):
        func.bind_to_methods = methods
        func.detail = False
        func.kwargs = kwargs
        return func
    return decorator


'''
一个路由类 函数代表链接 examplt restframework gengrate moodelviewset
'''
class SimpleView(object):
    def __init__(self):
        self._registry = {}
        self.urlpatterns = []
        self.urlpatterns_fun_string=[]

    def has_permission(self, request):
        return request.user.is_active and request.user.is_staff

    def get_urls(self):
        from django.urls import path
        for method_str in dir(self):
            if "__" in method_str or method_str=='urls' or method_str=='get_urls':
                continue
            method = getattr(self,method_str)
            if hasattr(method,'bind_to_methods'):
                path_obj = path(method_str+"/",method,name=method_str)
                if method_str not in self.urlpatterns_fun_string:
                    self.urlpatterns.append(path_obj)
                    self.urlpatterns_fun_string.append(method_str)
        return self.urlpatterns
    @property
    def urls(self):
        return self.get_urls()

    @list_router(methods=['get'])
    def test(self,request):
        print(request.user)
        return HttpResponse('Ojbk')

SimpleView=SimpleView()