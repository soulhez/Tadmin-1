import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
# os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')
import django

django.setup()

from rest_framework.test import APIRequestFactory,force_authenticate
from account.models import UserProfile
userModel=UserProfile
user=userModel.objects.filter().first()
print(user)

def weibo_login():
    from API.frontend.shop import views
    factory = APIRequestFactory()
    request = factory.get('/api/weiboapi/')
    request.user = user
    response=views.WeiboAPIViewSet.as_view({'get':'list'})(request)
    print(response.__dir__())


