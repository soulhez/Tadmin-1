# -*- coding: utf-8 -*-
from rest_framework import (serializers,)
from API.core.Paginations import NormalPagination


class AdminSerilizer(serializers.ModelSerializer):
    gination_class=NormalPagination
    page_size=5


