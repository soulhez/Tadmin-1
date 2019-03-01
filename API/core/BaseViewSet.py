'''
    基础视图  权限控制
'''
from rest_framework import viewsets
from API.core.Paginations import NormalPagination
from API.core.permission import SuperUserPermission, AdminPermission, AuthUserPermission
from API.core.Authentications import ExpiringTokenAuthentication
from rest_framework.authentication import BaseAuthentication,SessionAuthentication
from rest_framework import generics,filters,mixins, views

from API.core.filter_model import DjangoFilterBackend

class SuperUserViewSet(viewsets.ModelViewSet):
    permission_classes = (SuperUserPermission,)


class AdminViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication,ExpiringTokenAuthentication)
    pagination_class = NormalPagination
    filter_backends = (DjangoFilterBackend,filters.SearchFilter)
    



class AuthUserViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthUserPermission,)
    authentication_classes = (SessionAuthentication,ExpiringTokenAuthentication,)


class AdminDetailViewset(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    permission_classes = (AuthUserPermission,)
    authentication_classes = (SessionAuthentication,ExpiringTokenAuthentication,)
    