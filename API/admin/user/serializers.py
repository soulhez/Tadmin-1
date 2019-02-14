

from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers,validators
from rest_framework import viewsets
from rest_framework.utils import html, model_meta, representation

from account.models import UserProfile
User = UserProfile
from account.models import UserProfile,Role,UserRole,Menu


class AuthUserSerilizer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, allow_blank=False)
    email = serializers.EmailField(allow_blank=False,required=True)
    password = serializers.CharField(required=True,min_length=6,max_length=16)
    class Meta:
        model = User
        fields = ('username','email','password')

        class Meta:
            model = UserProfile
            fields = ('username', 'email', 'password')

class UserSerializer(serializers.ModelSerializer):
    roles_vo=serializers.SerializerMethodField()
    roles=serializers.ListField(write_only=True,required=False)
    password = serializers.CharField(write_only=True,required=False)
    class Meta:
        model = UserProfile
        fields = ( 'id','username', 'email','password', 'reg_time','avatar','birthday','gender','roles','roles_vo','last_login','is_admin','is_superuser')
    def get_roles_vo(self,obj):
        return Role.objects.filter(userrole__user=obj).values("id","name")

    def update(self, instance, validated_data):
        serializers.raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                if attr=="roles":
                    continue
                if attr == 'password':
                    value = make_password(value)
                setattr(instance, attr, value)
        #处理role
        roles=validated_data.get("roles")
        instance.save()
        instance.userrole_set.all().delete()
        for role in roles:
            UserRole.objects.create(
                role_id=role,
                user=instance
            )
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

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"