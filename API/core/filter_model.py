import django_filters

from shop.models import goods
class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
     商品过滤器
    """
    title = django_filters.CharFilter(name='title', lookup_expr='icontains')
    desc = django_filters.CharFilter(name='desc', lookup_expr='icontains')

    class Meta:
        model = goods
        fields = ['title', 'desc' ]