
from rest_framework import  viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from API.frontend.blog.serializers import ArticleSerializer, CateGorySerializer, TagSerializer
from blog.models import Article, Tag, Category

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = LimitOffsetPagination
    def create(self, request, *args, **kwargs):
        '''
         创建订单时调用方法完成
        '''
        data = request.data
        data.update({
            'author': request.user.id,
        })
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = LimitOffsetPagination

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CateGorySerializer
    pagination_class = LimitOffsetPagination

