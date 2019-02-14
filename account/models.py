from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,Group,PermissionsMixin
)
from django.utils import timezone


class UserManager(BaseUserManager):

    def create_user(self, email, password):
        if not email:
            return
        user = self.model(email=self.normalize_email(email), last_login=timezone.now())
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user



class UserProfile(AbstractBaseUser,PermissionsMixin):
    gender_choise = (
        (0, "男"),
        (1, "女"),
        (2, "")
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=126,verbose_name="用户名",unique=True,null=True)
    mobile = models.CharField(u'手机', max_length=32, default=None, blank=True, null=True,unique=True)
    avatar = models.CharField(max_length=256, default="http://ozelrebbz.bkt.clouddn.com/defaultAvatar.jpg")
    birthday = models.DateField(auto_now=True,null=True)
    gender = models.SmallIntegerField(choices=gender_choise, default=0)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    reg_time = models.DateTimeField(auto_now_add=True)
    memo = models.TextField(u'备注', blank=True,null=True,default=None)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True
    def has_perms(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    def has_module_perms(self, app_label):
        return True

    # @property
    # def is_superuser(self):
    #     return self.is_superuser
    #     # return bool(self.userrole_set.filter(role__name='superuser'))
    @property
    def is_staff(self):
        return self.is_admin
    @property
    def roles(self):
        return [obj.role for obj in  self.userrole_set.all() ]
    def get_short_name(self):
        # The user is identified by their email address
        return self.email



    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = u"用户信息"


    objects = UserManager()


class Role(models.Model):
    '''
        用户与角色：多对多
    '''
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255,verbose_name='角色名称',unique=True)
    parent=models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE)

class UserRole(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(UserProfile,verbose_name='用户',on_delete=models.CASCADE)
    role=models.ForeignKey(Role,verbose_name='角色',on_delete=models.CASCADE)



class Menu(models.Model):
    '''菜单'''
    id=models.AutoField(primary_key=True)
    name=models.CharField("名称",max_length=64)
    key=models.CharField("键值",max_length=64,unique=True)
    is_active=models.BooleanField(default=True,verbose_name="是否启用")
    only_superuser=models.BooleanField(default=False,verbose_name="仅超管权限")
    parent=models.ForeignKey('self',"上级菜单",null=True,blank=True)

class MenuRole(models.Model):
    role=models.ForeignKey(Role,on_delete=models.CASCADE)
    menu=models.ForeignKey(Menu,on_delete=models.CASCADE)
    id=models.AutoField(primary_key=True)
    class Meta:
        unique_together=(("role","id"))
        
        
        
User=UserProfile