
from django.urls import path, include

from API import admin,frontend
app_name = 'API'
urlpatterns = [
    path('admin/',include(admin,namespace="admin")),
    path('frontend/',include(frontend,namespace="forntend"))
]
