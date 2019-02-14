# -*- coding: utf-8 -*-
from rest_framework import (viewsets, status, serializers, validators)

from shop.models import lang,funServer,qiaohuOrder,qiaohuRecord,imooc,welfaresexx,Course,resource,Category,Attribute,Attribute_Value_Goods
from API.core.BaseSerializers import AdminSerilizer
from rest_framework.exceptions import ValidationError
class imoocSerilizer(serializers.ModelSerializer):
    """
    """
    lang_cn = serializers.CharField(source='lang.cn',read_only=True)
    class Meta:
        model = imooc
        fields = imooc.seralizer_field + ('lang_cn',)


class ImoocLangSerializer(serializers.ModelSerializer):
    status = serializers.CharField(required=False)
    class Meta:
        model = lang
        fields = '__all__'

class FunServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = funServer
        fields = '__all__'

class qiaohuOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = qiaohuOrder
        fields = ('email','user','user_id','id','source','order_num','order_price','url','completed','email','is_pay','ctime','remark')
class qiaohuRecordSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)
    def get_username(self,obj):
        return obj.order.user.username
    class Meta:
        model = qiaohuRecord
        fields = ('order','data','is_ok','msg','username','mtime','ctime')

class WelfareSexxdSerializer(serializers.ModelSerializer):
    index_img = serializers.SerializerMethodField()
    class Meta:
        model = welfaresexx
        fields = ("id","videoid","title","upload_time","index_img","vote_num","praise_rate","video_time","views_num")
    def get_index_img(self,obj):
        return obj.index_img.replace("preview.jpg","180x135/1.jpg")


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class ResSerializer(serializers.ModelSerializer):
    class Meta:
        model = resource
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs.get('pid')==self.instance:
            raise ValidationError("上级不能为自己","validate error")
        return attrs

    class Meta:
        model = Category
        fields='__all__'

class AttributeSerizalizer(AdminSerilizer):
    category_name=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Attribute
        fields='__all__'
    def get_category_name(self,obj):
        return obj.category.label