
from rest_framework import (viewsets, status, serializers, validators)
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework import viewsets
from rest_framework.utils import html, model_meta, representation

from account.models import User
from account.models import UserProfile,Role,UserRole


class AuthUserSerilizer(serializers.ModelSerializer):
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False)
    email = serializers.EmailField( help_text="邮箱", label="邮箱", write_only=True,allow_blank=False,required=True)
    password = serializers.CharField(help_text="密码", label="密码", write_only=True,required=True)
    class Meta:
        model = UserProfile
        fields = ('username','email','password')
        validators = [
            validators.UniqueTogetherValidator(queryset=User.objects.all(),
                                               fields=('email',), message='该邮箱已被注册'),
            validators.UniqueTogetherValidator(queryset=User.objects.all(),
                                               fields=('username',), message='该用户名已被注册'),
        ]

class UserSerializer(serializers.ModelSerializer):
    roles=serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True,required=False)
    class Meta:
        model = User
        fields = ( 'id','username', 'email','password', 'reg_time','avatar','birthday','gender','roles','last_login','is_admin','is_superuser')
    def get_roles(self,obj):
        roles=[]
        if obj.is_admin:
            roles.append({'id':'admin','name':'admin'})
        if obj.is_superuser:
            roles.append({'id': 'superuser', 'name': 'superuser'})
        return [ {"id":role.id , "name":role.name} for role in obj.roles ] + roles

    def update(self, instance, validated_data):
        serializers.raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                if attr == 'password':
                    value = make_password(value)
                setattr(instance, attr, value)
        instance.save()

        return instance



class UserRoleSerilizer(serializers.ModelSerializer):
    """
        用户关联角色
    """
    class Meta:
        model = UserRole
        fields = "__all__"
class RoleSerilizer(serializers.ModelSerializer):
    """
        角色
    """
    class Meta:
        model = Role
        fields = "__all__"


