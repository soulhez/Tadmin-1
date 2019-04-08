import time
import requests
import logging
from API.admin.shop.serializers import ImoocLangSerializer, FunServerSerializer, qiaohuOrderSerializer, \
    qiaohuRecordSerializer, imoocSerilizer, WelfareSexxdSerializer, CourseSerializer, ResSerializer,CategorySerializer,\
    AttributeSerizalizer
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
# Create your views here.
from rest_framework import viewsets, status,validators
from rest_framework.decorators import action
from rest_framework.response import Response

from shop.models import imooc
from shop.models import lang, funServer, qiaohuRecord, qiaohuOrder, welfaresexx, Course, resource,Category,Attribute
from API.core.Paginations import NormalPagination,LimitOffsetPagination
from API.core.BaseViewSet import AdminViewSet,AdminDetailViewset
from rest_framework import urls

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

class qiaohuOrderViewSet(AdminViewSet):
    queryset = qiaohuOrder.objects.all()
    serializer_class = qiaohuOrderSerializer
    filter_fields=('is_pay','user','pay_type')
    search_fields=('remark','user__email','user__username')
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).order_by('-ctime')
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


class qiaohuRecordViewSet(AdminViewSet):
    queryset = qiaohuRecord.objects.all().order_by('-mtime')
    serializer_class = qiaohuRecordSerializer
    filter_fields=('order',)
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



class WalfareSexxViewSet(AdminViewSet):
    queryset = welfaresexx.objects.all()
    serializer_class = WelfareSexxdSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    ordering_fields = ('upload_time','views_num','vote_num','praise_rate', )
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
    @action(detail=True,methods=['get'])
    def get_location_url(self,request,pk,*args,**kwargs):
        import requests,re
        session=requests.session()
        instance=self.get_object()
        detail_res=session.get("http://www.caca050.com/videos/%s/1/"%instance.videoid)
        get_file_url=re.search(r"http://.+get_file.+?\.mp4",detail_res.text).group()
        return Response({"location":get_file_url})
    @action(detail=False,methods=['post'])
    def ansyc_domin(self,request):
        last_domin=request.data.get('last_domin')
        new_domin = request.data.get('new_domin')
        if not last_domin or not new_domin:
            return Response({})
        for i in self.queryset.filter(url__contains=last_domin,id__gt=1000):
            i.url=i.url.replace(last_domin,new_domin)
            i.video_url=i.video_url.replace(last_domin,new_domin)
            print(i.url)
            i.save()



class CourseViewSet(viewsets.ModelViewSet):
    """"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('title', 'desc','tags')

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

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


    @action(detail=False)
    def tree(self,request):
        data = self.filter_queryset(self.get_queryset()).order_by('id').values('id', 'label', 'pid_id')

        def get_children(item, childrens):
            results = []
            for i in childrens:
                if i['pid_id'] == item['id']:
                    results.append(get_children(i, childrens))
            item['children'] = results
            return item

        results = []
        for item in data:
            if not  item['pid_id']:
                results.append(get_children(item, data))
        return Response(results)


class AttributeViewSet(AdminViewSet):
    queryset = Attribute.objects.all()
    serializer_class=AttributeSerizalizer



class PandownloadViewset(AdminDetailViewset):
    search_fields=("key",)
    @action(detail=False)
    def search(self,request,*args,**kwargs):
        return Response({"detail":"接口开发ing....","code":"1001"},status=400)
        req_data=request.query_params
        params={
            "clienttype": 1,
            "highlight": 1,
            "key":req_data.get('key'),
            "page":req_data.get('page'),
            "timestamp":"1554707021",
            "sign": "828152926614276651646"
        }
        resp=requests.get(url='http://search.pandown.cn/api/query',params=params)
        if resp.status_code==200:
            try:
                data=resp.json()
                for item in data['data']:
                    item['list']=item.get('list').split("\n") if item.get('list') else []
                    item['surl']="https://pan.baidu.com/s/"+item['id']
                    item['needpassword']=True if item.get('password',False) else False
                    if not request.user.is_superuser and item['password']:
                        item.pop('password')
                        
                return Response(data)
            except Exception as e:
                data={"msg":"数据源解析失败(%s)"%str(e),"code":1001}
                return Response(data)
        else:
            raise validators.ValidationError(("1001","数据源失效"))