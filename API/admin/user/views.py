from datetime import datetime
from API.core.BaseViewSet import AdminViewSet
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from rest_framework import filters
from rest_framework import routers, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.core.cache import cache
from API.admin.user.serializers import AuthUserSerilizer, UserRoleSerilizer, RoleSerilizer, UserSerializer,MenuSerializer
from account.models import UserProfile, Role, UserRole,Menu,MenuRole
from rest_framework.views import APIView
import logging
logger = logging.getLogger("django") # 为loggers中定义的名称
# userprofile

class UserViewSet(AdminViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('username', 'email')
    def get_queryset(self):
        '''
         普通管理员不能看到超级管理员
        '''
        if self.request.user.is_superuser:
            return UserProfile.objects.all()
        else:
            return UserProfile.objects.filter(is_superuser=False)

    @action(methods=['get'], detail=False,url_name='account')
    def info(self, request):
        current_user = UserProfile.objects.get(id=request.user.id)
        serializer = UserSerializer(current_user)
        #获取菜单权限key name
        menus=Menu.objects.filter(is_active=True)
        if current_user.is_superuser:
            menu_data= menus.values("name","key")
            parent_data=[]
        else:
            menu_data = menus.filter(only_superuser=False).extra(
                where=("id in (select b.menu_id as id from account_role a,account_menurole b,account_userrole c where a.id=c.role_id and c.role_id =b.role_id)",))\
                .values("name","key","parent_id","id")
            pids=set(i['parent_id'] for i in menu_data)
            parent_data=menus.filter(id__in=pids).values("name","key","parent_id","id")
        result=serializer.data
        result['menu']=list(menu_data)+list(parent_data)
        return Response(result)

class RoleViewSet(AdminViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerilizer
    @action(detail=False,methods=['get'])
    def tree(self,request,*args,**kwargs):
        '''返回树形结构  数据结构目前未设置树形'''
        roles=Role.objects.values()
        menu=request.query_params.get('menu',None)
        if menu:
            ids=[i['role_id'] for i in MenuRole.objects.filter(menu_id=menu).values("role_id")]
        else:
            ids=[i.id for i in UserRole.objects.filter(user=request.user)]
        results={"data":roles,"has_role":ids}
        return Response(results)

    @action(detail=False,methods=['get'])
    def has_role(self,request,*args,**kwargs):
        '''用户或菜单拥有的角色'''
        menu=request.query_params.get('menu')
        if menu:
            ids=[i['role_id'] for i in MenuRole.objects.filter(menu_id=menu).values("role_id")]
        return Response({"has_roles":ids})
    @action(detail=True,methods=['post'])
    def setmenu(self,request,*args,**kwargs):
        checked_menu=request.data.get('data')
        role=self.get_object()
        MenuRole.objects.filter(role=role).delete()
        for item in checked_menu:
            MenuRole.objects.create(role=role,menu_id=item)
        return Response({})
    
    @action(detail=False,methods=['get'])
    def all(self,request,*args,**kwargs):
        '''返回列表结构  not page'''
        values=self.get_queryset().values()
        dict_values = {value['id']:value for value in values}
        results={}
        for k,v in dict_values.items():
            pass
            #todo
        results.setdefault('data',values)
        return Response(results)
class UserRoleViewSet(AdminViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerilizer


class AdminLogin(ObtainAuthToken):
    serializer_class = AuthUserSerilizer
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = UserProfile.objects.filter(Q(username=username)|Q(email=username)).first()
        if user and  user.check_password(password) and user.is_active:
            try:
                token = Token.objects.get(user=user)
                cache.delete("token_" + token.key)
                token.delete()
            except Token.DoesNotExist :
                pass
            #创建token
            user.last_login=timezone.now()
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            token_cache = 'token_' + token.key
            cache.set(token_cache,token,timeout=60*60*24*7)
            return Response({
                'token': token.key,
            })
        return  Response({'msg':"账户不存在或密码错误"},status=401)

class Logout(APIView):
    def get(self, request, *args, **kwargs):

        return Response({})


class Register(ObtainAuthToken):
    serializer_class = AuthUserSerilizer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=False)
        return Response({})


class MenuViewSet(AdminViewSet):
    queryset = Menu.objects.filter(is_active=True)
    serializer_class = MenuSerializer
    
    def list(self, request, *args, **kwargs):
        results=self.get_queryset().values()
        dict_data={i['id']:i for i in results}
        for k,v in dict_data.items():
            if 'nodes' not in v:
                v['nodes'] = []
            if v['parent_id']:
                v['nodes'] = dict_data[v['parent_id']]['nodes'] + [v['name']]
            else:
                v['nodes'] = [v['name']]
        list_data=[]
        for k,v in dict_data.items():
            v['nodes']="/".join(v['nodes'])
            list_data.append(v)
        results={
            "data":list_data
        }
        return Response(results)
    
    @action(detail=False,methods=['get'])
    def tree(self,request,*args,**kwargs):
        items=Menu.objects.filter().values()
        role=request.query_params.get('role',None)
        if not role:
            hasMenu=set([i['menu_id'] for i in MenuRole.objects.filter(role__userrole__user=request.user).values("menu_id")])
        else:
            hasMenu=set([i['menu_id'] for i in MenuRole.objects.filter(role=role).values("menu_id")])
        data={}
        for d in items:
            data.setdefault(d['id'],d)
        result=[]

        for k,v in data.items():
            if v['parent_id'] == None:
                result.append(v)
            else:
                data[v['parent_id']].setdefault('children', []).append(v)
        return Response({"results":result,"hasmenu":hasMenu})
    @action(detail=False,methods=['get'])
    def tree_list(self,request,*args,**kwargs):
        queryset=Menu.objects.filter()
        if not  request.user.is_superuser:
            queryset=queryset.filter(only_superuser=False)
        items=queryset.values()
        data={}
        for d in items:
            data.setdefault(d['id'],d)
        result=[]
        print(data)

        for k,v in data.items():
            if v['parent_id'] == None:
                result.append(v)
            else:
                data[v['parent_id']].setdefault('children', []).append(v)
        return Response(result)

    @action(detail=True, methods=['post'])
    def setrole(self, request, *args, **kwargs):
        checked_menu = request.data.get('data')
        menu= self.get_object()
        MenuRole.objects.filter(menu=menu).delete()
        for item in checked_menu:
            MenuRole.objects.create(menu=menu, role_id=item)
        return Response({})