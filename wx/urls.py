from django.contrib import admin
from django.urls import path,include
from wx import views as wx_views
app_name = 'wx'
urlpatterns = [
    path('server/', wx_views.server),
]
