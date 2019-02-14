
'''
    一些基础的分页。。
'''
from collections import OrderedDict
from rest_framework import (pagination)
from rest_framework.response import Response
#分页

class LimitOffsetPagination(pagination.LimitOffsetPagination):
    #默认显示的个数
    default_limit = 10
    #当前的位置
    offset_query_param = "offset"
    #通过limit改变默认显示的个数
    limit_query_param = "limit"
    #一页最多显示的个数
    max_limit = 10




class NormalPagination(pagination.PageNumberPagination):
    # 每页显示多少个
    page_size = 10
    # 默认每页显示3个，可以通过传入pager1/?page=2&size=4,改变默认每页显示的个数
    page_size_query_param = "pagesize"
    # 最大页数不超过10
    max_page_size = 100
    # 获取页码数的
    page_query_param = "page"

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('num_pages', self.page.paginator.num_pages),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
