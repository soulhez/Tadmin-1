
from django.contrib import admin
from django.shortcuts import render, HttpResponse
from django.urls import path, include
from rest_framework.urls import *

from API.admin.user.views import AdminLogin


# logger = logging.getLogger('celery')

def test(request):
    print("this is start")
    add.delay()
    print('this is end')
    return HttpResponse('Ok')

def index(request):
    return render(request, "index.html")
urlpatterns = [
    path(r'test/',test),
    path(r'auth/',include('account.urls', namespace='account')),
    path(r'auth/token/',AdminLogin.as_view()),
    path(r'auth/logout/',logout),
    path('admin/', admin.site.urls),
    path(r'api/', include('API.urls',namespace='API')),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'wx/',include('wx.urls', namespace='wx')),
    # path(r'',index),
]