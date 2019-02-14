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
from API.core import Authentications,permission
from utils.QiniuCore import token as qiniuToken,domian_url

class qiniuViews(APIView):
    # 认证类，通过token认证
    authentication_classes = (Authentications.ExpiringTokenAuthentication,)
    # 权限赋予类，赋予管理员权限
    permission_classes = (permission.AdminPermission,)
    def get(self, request):
        return Response({"token":qiniuToken,'domain_url':domian_url})

