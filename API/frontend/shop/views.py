import logging
from datetime import datetime
from API.frontend.shop.serializers import ImoocLangSerializer, FunServerSerializer, qiaohuOrderSerializer, \
    qiaohuRecordSerializer, imoocSerilizer, WelfareSexxdSerializer, CourseSerializer, ResSerializer,WeiboASerializer
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from API.core.Paginations import LimitOffsetPagination,NormalPagination
from rest_framework.response import Response

from API.core.permission import SuperUserPermission
from shop.models import imooc,WeiboAPi
from shop.models import lang, funServer, qiaohuRecord, qiaohuOrder, welfaresexx, Course, resource

from utils.weibo.weibo import weibo_api
from core.nginx import get_ip
logger = logging.getLogger('accesslog')

from account.models import UserProfile
User=UserProfile
class ImoocViewSet(viewsets.ModelViewSet):
    queryset = imooc.objects.all()
    serializer_class = imoocSerilizer
    pagination_class = LimitOffsetPagination
    def get_queryset(self):
        lang_id = self.request.GET.get('lang')
        search = self.request.GET.get('search')
        con = Q()
        if search:
            q1 = Q()
            q1.connector = 'OR'
            q1.children.append(('title__icontains', search))
            q1.children.append(('desc__icontains', search))
            con.add(q1, 'AND')
        if lang_id:
            q2 = Q()
            q2.connector = 'AND'
            q2.children.append(('lang_id', lang_id))
            con.add(q2, 'AND')
        queryset = imooc.objects.filter(con)
        return queryset
class LangViewSet(viewsets.ModelViewSet):
    queryset = lang.objects.all()
    serializer_class = ImoocLangSerializer
#
class ResViewSet(viewsets.ModelViewSet):
    queryset = resource.objects.all()
    serializer_class = ResSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('title', )

class FunServerViewSet(viewsets.ModelViewSet):
    queryset = funServer.objects.all()
    serializer_class = FunServerSerializer

class qiaohuOrderViewSet(viewsets.ModelViewSet):
    queryset = qiaohuOrder.objects.all()
    serializer_class = qiaohuOrderSerializer
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    def create(self, request, *args, **kwargs):
        '''
         创建订单时调用方法完成
        '''
        data = request.data
        data.update({
            'user': request.user.id,
        })
        logger.info(data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class qiaohuRecordViewSet(viewsets.ModelViewSet):
    queryset = qiaohuRecord.objects.all()
    serializer_class = qiaohuRecordSerializer
    def get_queryset(self):
        con = Q()
        search = self.request.GET.get('search','')
        is_ok = self.request.GET.get('result','')
        if search:
            q1 = Q()
            q1.connector = 'OR'
            q1.children.append(('order__user__username',search))
            con.add(q1, 'AND')
        if is_ok:
            q2 = Q()
            q2.connector = 'AND'
            q2.children.append(('is_ok',is_ok))
            con.add(q2, 'AND')
        queryset = self.queryset.filter(con)
        return queryset



class WalfareSexxViewSet(viewsets.ModelViewSet):
    queryset = welfaresexx.objects.all()
    serializer_class = WelfareSexxdSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (SuperUserPermission,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    ordering_fields = ('upload_time','views_num','vote_num','praise_rate' )
    def get_queryset(self):
        start_date = self.request.GET.get('upload_time__gt')
        end_date = self.request.GET.get('upload_time__lt')
        search = self.request.GET.get('search')
        queryset = self.queryset
        if start_date:
            queryset = queryset.filter(upload_time__range=(start_date,end_date))
        if search:
            queryset=queryset.filter(Q(title__contains=search) | Q(summary__contains=search))
        return queryset

class CourseViewSet(viewsets.ModelViewSet):
    """"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = NormalPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('title', 'desc','tags','price','sales')

    @action(detail=False)
    def course_Statistics(self,request):
        '''
        :return: 课程统计
        '''
        values = Course.objects.values_list('res')
        success = 0
        unsuccess = 0
        for v in values:
            if v[0]:
                success +=1
            else:
                unsuccess +=1
        return Response({'success':success,'unsuccess': unsuccess} )


class WeiboAPIViewSet(viewsets.ModelViewSet):
    queryset = WeiboAPi.objects.all()
    serializer_class = WeiboASerializer
    pagination_class = NormalPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)

    def create(self, request, *args, **kwargs):
        phone=request.data.get('phone',None)
        password=request.data.get('password',None)
        if not phone or not password:
            return Response({"msg":"错误的请求"}, status=status.HTTP_400_BAD_REQUEST)
        for ret in range(3):
            try:
                result = weibo_api.login(phone, password)
            except Exception as e:
                logger.error("weibo api error:%s"%e)
                continue
            if result:
                data = {
                    "phone": phone,
                    "password": password,
                    "login_ip": result['login_ip'],
                    "create_ip": get_ip(request),
                    "login_datetime": datetime.now(),
                    "result_status": WeiboAPi.RESULT_SUCCESS
                }
                WeiboAPi.objects.create(**data)
                result.update(data)
                return Response(result)
        return Response({"msg":"登陆失败"})
