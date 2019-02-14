from rest_framework import permissions
class SuperUserPermission(permissions.BasePermission):
    '''
        超级用户权限  用户管理认证
    '''
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return False
class AdminPermission(permissions.BasePermission):
    '''
        管理员  后台登陆
    '''
    def has_permission(self, request, view):
        if request.user.is_authenticated and  request.user.is_admin:
            return True
        else:
            return False

class AuthUserPermission(permissions.BasePermission):
    '''
        普通用户  后台登陆
    '''
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        else:
            return False