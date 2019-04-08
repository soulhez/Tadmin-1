import os
import sys
import time
from datetime import datetime,timedelta
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
from account.models import User
from django.contrib.auth.hashers import make_password
user=User.objects.get(email="58296672@qq.com")
user.password=make_password("abc123456")
user.save()
