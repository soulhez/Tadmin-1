# -*- coding: utf-8 -*-
from rest_framework import (viewsets, status, serializers, validators)

from blog.models import Article,Category,Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
class CateGorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
class ArticleSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = '__all__'
    def get_username(self,obj):
        return obj.author.username
